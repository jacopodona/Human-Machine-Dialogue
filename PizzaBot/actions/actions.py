# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from asyncore import dispatcher
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa.shared.core.events import AllSlotsReset
from rasa_sdk import Action, Tracker,FormValidationAction

from rasa_sdk.events import EventType, SlotSet,AllSlotsReset,ActionExecuted,FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

# Declare the knowledge base
class Pizza:
    def __init__(self, name, price, ingredients):
        self.name = name
        self.price = price
        self.ingredients=ingredients

class OrderedPizza():
    def __init__(self, pizza, size, toppings):
        self.pizza=pizza
        self.size=size
        price=pizza.price
        if(size=="small"):
            price-=2
        elif(size=="large"):
            price+=2
        self.price=price+len(toppings)
        self.extras=toppings

drink_menu={
    "water": 1,
    "tea": 2,
    "coke": 3,
    "beer": 5,
    "sprite": 3,
}

pizza_menu=[
    Pizza(name="margherita",price=6,ingredients=["tomato sauce","mozzarella"]),
    Pizza(name="marinara",price=6,ingredients=["tomato sauce","garlic"]),
    Pizza(name="pepperoni", price=7, ingredients=["tomato sauce", "mozzarella", "pepperoni"]),
    Pizza(name="capricciosa", price=8, ingredients=["tomato sauce", "mozzarella","ham", "mushrooms"]),
    Pizza(name="hawaiian", price=9, ingredients=["tomato sauce", "mozzarella", "ham", "pineapple"]),
    Pizza(name="vegetarian", price=8, ingredients=["tomato sauce", "mozzarella", "zucchini", "bell peppers", "eggplant"]),
    Pizza(name="pub", price=8, ingredients=["tomato sauce", "mozzarella", "wurstel", "potatoes"]),
    Pizza(name="rustic", price=8, ingredients=["tomato sauce", "mozzarella", "sausage", "potatoes"]),
    Pizza(name="chicken", price=9, ingredients=["BBQ sauce", "mozzarella", "grilled chicken"]),
    Pizza(name="cheesey", price=8, ingredients=["tomato sauce", "mozzarella", "cheddar", "parmesan", "gorgonzola"]),
    Pizza(name="light", price=8, ingredients=["mozzarella", "spinach", "feta"]),
    Pizza(name="pesto", price=7, ingredients=["mozzarella", "pesto", "tomatoes"])
]

pizza_sizes=["small","medium","large"]

toppings=["tomato sauce","mozzarella","pepperoni","ham","spinach","onions","olives","mushrooms","wurstel", "hot dog",
          "grilled_chicken","sausage"]

order=[]

def getPizzaFromMenuByName(pizza_name):
    for pizza in pizza_menu:
        if pizza_name==pizza.name:
            return pizza
    return None

def resetOrder():
    global order
    order=[]

def getOrderRecap():
    message="Your order currently contains "
    print(order)
    for i in range(len(order)):
        pizza_in_order=order[i]
        message+="a "+pizza_in_order.size+" "+pizza_in_order.pizza.name
        if len(pizza_in_order.extras)!=0:
            message+=" with "+pizza_in_order.extras
        if(i!=len(order)-1):
            message+=", "
    return message+". "

def getDrinks():
    return list(drink_menu.keys())
def getPizzaSizes():
    return pizza_sizes

def getPizzaIngredient(pizza:Pizza):
    return pizza.ingredients

def getPizzaTypes():
    return [pizza.name for pizza in pizza_menu]

def computeOrderPrice(order):
    sum=0
    print("Order:", order)
    for pizza in order:
        print("Pizza price:",pizza.price)
        sum+=pizza.price
    return sum

# Declare Actions

class ActionTellDrinkList(Action):

    def name(self) -> Text:
        return "action_tell_drink_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        drinks = getDrinks()

        if len(drinks)==0:
            msg = "Looks like we are out of beverages, we have none available at the moment"
        else:
            last_two_drinks = " and ".join(drinks[-2:])
            other_drinks = ", ".join(drinks[:-2])

            # Concatenate the two parts
            result = other_drinks + ", " + last_two_drinks
            msg= "We currently offer "+result
        dispatcher.utter_message(text=msg)

        return []

class ActionTellPizzaMenu(Action):

    def name(self) -> Text:
        return "action_tell_pizza_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pizzas = getPizzaTypes()

        if len(pizzas)==0:
            msg = "Looks like we are out of pizzas, we have none available at the moment"
        else:
            #Format the message such as a list of pizzas separated by commas is printed, except for the last two which are separated by and
            #Example "margherita, marinara, pepperoni and capricciosa
            last_two_pizzas = " and ".join(pizzas[-2:])
            other_pizzas = ", ".join(pizzas[:-2])

            # Concatenate the two parts
            result = other_pizzas + ", " + last_two_pizzas
            msg= "Our pizzas are "+result
        dispatcher.utter_message(text=msg)

        return []

class ActionTellDrinkPrice(Action):

    def name(self) -> Text:
        return "action_tell_drink_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        key_to_find = next(tracker.get_latest_entity_values("drink_name"), None)

        if key_to_find is None:
            dispatcher.utter_message(text="I did not understand, could you ask me again please?")
        else:
            drink_price = drink_menu.get(key_to_find, None)
            if drink_price is None:
                msg = f"I'm afraid we do not have {key_to_find} in our menu. You can get a list of available drinks by asking 'What drinks do you have?'"
            else:
                msg = f"A {key_to_find} costs {str(drink_price)} €"
            dispatcher.utter_message(text=msg)
        return []

class ActionTellPizzaPrice(Action):

    def name(self) -> Text:
        return "action_tell_pizza_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        key_to_find = next(tracker.get_latest_entity_values("pizza_type"), None)

        if key_to_find is None:
            dispatcher.utter_message(text="I did not understand, could you ask me again please?")
            return []
        else:
            pizza = getPizzaFromMenuByName(key_to_find)
            if pizza is None:
                msg = f"I'm afraid we do not have {key_to_find} in our menu. You can get a list of available drinks by asking 'What drinks do you have?'"
                dispatcher.utter_message(text=msg)
                return []
            else:
                msg = f"A {pizza.name} costs {str(pizza.price)} €\n"
                dispatcher.utter_message(text=msg)
                return [FollowupAction("utter_topping_and_size_price")]

class ActionTellPizzaIngredients(Action):

    def name(self) -> Text:
        return "action_tell_pizza_ingredients"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        key_to_find = next(tracker.get_latest_entity_values("pizza_type"), None)

        if key_to_find is None:
            dispatcher.utter_message(text="I did not understand, could you ask me again please?")
            return []
        else:
            pizza = getPizzaFromMenuByName(key_to_find)
            if pizza is None:
                msg = f"I'm afraid we do not have {key_to_find} in our menu. You can get a list of available drinks by asking 'What drinks do you have?'"
            else:
                ingredients=pizza.ingredients
                last_two_ingredients = " and ".join(ingredients[-2:])
                other_ingredients = " , ".join(ingredients[:-2])
                ingredient_list=other_ingredients+", "+last_two_ingredients
                print(ingredients)
                msg=f"In a {pizza.name} we put "
                for i in range(len(ingredients)):
                    ingredient = ingredients[i]
                    msg += ingredient
                    print(msg)
                    if (i < len(ingredients) - 1):
                        msg += ", "
                msg+="."
            dispatcher.utter_message(text=msg)
            return []

class ValidatePizzaOrderForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_pizza_order_form"

    def validate_pizza_size(self,slot_value:Any,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: DomainDict)-> Dict[Text, Any]:
        """ Validate 'pizza_size' value"""
        if slot_value.lower() not in getPizzaSizes():
            dispatcher.utter_message(text=f"We only accept pizza sizes : small/medium/large")
            return {"pizza_size":None}
        dispatcher.utter_message(text=f"Ok! You want to have a {slot_value} pizza.")
        return {"pizza_size":slot_value}

    def validate_pizza_type(self,slot_value:Any,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: DomainDict)-> Dict[Text, Any]:
        if slot_value.lower() not in getPizzaTypes():
            dispatcher.utter_message(text=f"I don't recognize that pizza, for more indications on the available pizzas, ask 'What pizzas do you have in the menu?'")
            return {"pizza_type":None}
        dispatcher.utter_message(text=f"Ok! You want to have a {slot_value} pizza.")
        return {"pizza_type":slot_value}

class ActionResponsePositive(Action):
    def name(self):
        return 'action_response_positive'

    def run(self, dispatcher, tracker, domain):
        try:
            bot_event = next(e for e in reversed(tracker.events) if e["event"] == "bot")
            if (bot_event['metadata']['utter_action'] == 'utter_submit_pizza'):
                dispatcher.utter_message("Perfect! It was added to your order.")
                pizza_type = tracker.slots['pizza_type']
                pizza_size = tracker.slots['pizza_size']
                #TODO extras
                pizza_to_add=OrderedPizza(pizza=getPizzaFromMenuByName(pizza_type),size=pizza_size,toppings=[])
                order.append(pizza_to_add)
                message=getOrderRecap()
                dispatcher.utter_message(text=message)
                return[FollowupAction("utter_anything_else_order"),SlotSet("pizza_type",None),SlotSet("pizza_size",None)]
            elif(bot_event['metadata']['utter_action'] == "utter_anything_else_order"):
                #The user wants something else"
                dispatcher.utter_message("What would you like to add to your order?")
                return []
            else:
                dispatcher.utter_message("I don't understand what are you referring to, could you please be more specific?")
        except:
            dispatcher.utter_message("Sorry, can you repeat that?")
        return []

class ActionResponseNegative(Action):
    def name(self):
        return 'action_response_negative'

    def run(self, dispatcher, tracker, domain):
        try:
            bot_event = next(e for e in reversed(tracker.events) if e["event"] == "bot")
            print(bot_event)
            previous_action=bot_event['metadata']['utter_action']
            print(previous_action)
            print(previous_action=="utter_anything_else_order")
            if(previous_action == "utter_anything_else_order"):
                print("User does not want anything more --> checkout")
                message="Ok, checking out your order...\n"
                print("Building message...")
                message+=getOrderRecap()
                print("Computing price...")
                price=computeOrderPrice(order)
                print("Prepare message for user")
                message+="The total price is: "+str(price)+" €"
                dispatcher.utter_message(text=message)
                print("Printed message")
                resetOrder()
                print("Resetted order")
                return [FollowupAction("utter_ask_delivery_method")]
            else:
                dispatcher.utter_message("I don't understand what are you referring to, could you please be more specific?")
        except:
            dispatcher.utter_message("Sorry, can you repeat that?")
        return []


