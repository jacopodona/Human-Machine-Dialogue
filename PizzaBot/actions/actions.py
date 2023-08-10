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

import sys
#sys.path.append(os.path.join(sys.path[0],'bar','sub','dir'))
from actions.classes import Pizza,Drink,OrderedPizza,OrderedDrink,Order

order_id_counter=0

drink_menu=[
    Drink(name="water",price=1),
    Drink(name="tea",price=3),
    Drink(name="coke",price=3),
    Drink(name="sprite",price=3),
    Drink(name="beer",price=5)
]

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

toppings=["tomato sauce","mozzarella","garlic","pepperoni","ham","pineapple","bell peppers","eggplant","zucchini","spinach","onions",
          "olives","mushrooms","wurstel","grilled_chicken","sausage","potatoes","BBQ sauce"]

orders=[]

def getPizzasWithIngredient(ingredient):
    pizzas_with_ingredient = []
    for pizza in pizza_menu:
        if ingredient in pizza.ingredients:
            pizzas_with_ingredient.append(pizza)
    return pizzas_with_ingredient
def getPizzasWithoutIngredient(ingredient):
    pizzas_without_ingredient=[]
    for pizza in pizza_menu:
        if ingredient not in pizza.ingredients:
            pizzas_without_ingredient.append(pizza)
    return pizzas_without_ingredient

def updateOrderIDCounter():
    global order_id_counter
    order_id_counter+=1
def getOrderByUserID(user):
    print(f"Searching order for user {user}")
    for order in orders:
        if user==order.user_id:
            return order
    return None

def logOrderDB():
    message="DB orders:"+str(len(orders))
    for order in orders:
        message+=f"Order id: {order.id} \n {getOrderRecap(order)}\n Checkout method set to {order.delivery_method}"
        print(message)

def getPizzaFromMenuByName(pizza_name):
    for pizza in pizza_menu:
        if pizza_name==pizza.name:
            return pizza
    return None

def getDrinkFromMenuByName(drink_name):
    for drink in drink_menu:
        if drink_name == drink.name:
            return drink
    return None

def removeOrderByUserID(sender_id):
    for i in range(len(orders)):
        order=orders[i]
        if order.user_id==sender_id:
            return orders.pop(i)
    return None

def getOrderRecap(order):
    message="Your order currently contains "
    addDrinkComma=False
    for i in range(len(order.pizzas)):
        pizza_in_order=order.pizzas[i]
        if(i!=0):
            message+=", "
        if(pizza_in_order.amount==1):
            message += "a " + pizza_in_order.size + " " + pizza_in_order.pizza.name
        else:
            message += str(pizza_in_order.amount)+" " + pizza_in_order.size + " " + pizza_in_order.pizza.name
        if len(pizza_in_order.extras) != 0:
            message += " with " + pizza_in_order.extras
        addDrinkComma=True
    for j in range(len(order.drinks)):
        drink_in_order=order.drinks[j]
        if(addDrinkComma==True and j==0): #Put commas correctly after items if there are already pizzas in the order
            message += ", "
            addDrinkComma=False
        elif(j!=0):
            message += ", "
        if (drink_in_order.amount == 1):
            message += "a bottle of " + drink_in_order.drink.name
        else:
            message += str(drink_in_order.amount)+" bottles of " + drink_in_order.drink.name
    return message + ". "

def getDrinks():
    return [drink.name for drink in drink_menu]
def getPizzaSizes():
    return pizza_sizes

def getPizzaIngredient(pizza:Pizza):
    return pizza.ingredients

def getPizzaTypes():
    return [pizza.name for pizza in pizza_menu]

def computeOrderPrice(order):
    sum=0
    for pizza_in_order in order.pizzas:
        sum+=pizza_in_order.computePrice()
    for drink_in_order in order.drinks :
        sum += drink_in_order.computePrice()
    return sum


def updateExistingOrder(modified_order):
    global orders
    print(f"Order to insert: {modified_order.__dict__}")
    for i in range(len(orders)):
        order=orders[i]
        if order.id==modified_order.id:
            orders[i]=modified_order
            print(f"New order in the database: {orders[i].__dict__}")

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
            msg= "Here is our menu:\nfor pizzas we have "+result+"."
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
            drink=getDrinkFromMenuByName(key_to_find)
            if drink is None:
                msg = f"I'm afraid we do not have {key_to_find} in our menu. You can get a list of available drinks by asking 'What drinks do you have?'"
            else:
                drink_price=drink.price
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
                msg=f"In a {pizza.name} we put "
                if len(ingredients)==2:
                    msg+=ingredients[0]+" and "+ingredients[1]
                else:
                    last_two_ingredients = " and ".join(ingredients[-2:])
                    other_ingredients = " , ".join(ingredients[:-2])
                    msg += other_ingredients + ", " + last_two_ingredients
                msg+="."
            dispatcher.utter_message(text=msg)
            return []

class ActionTellPizzaWithoutIngredient(Action):

    def name(self) -> Text:
        return "action_tell_pizza_without_ingredient"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ingredient=tracker.get_slot("ingredient")

        if ingredient is None:
            dispatcher.utter_message("I didn't not understand, could you repeat please?")
            return [SlotSet("ingredient",None)]
        else:
            ingredient=ingredient.lower() #Send to lowercase
            if ingredient in toppings:
                pizzas=getPizzasWithoutIngredient(ingredient)
                response =""
                if len(pizzas) == 0:
                    response += pizzas[0].name
                    dispatcher.utter_message(f"We don't put {ingredient} in any pizza.")
                    return [SlotSet("ingredient", None)]
                else:
                    if len(pizzas) == 1:
                        response += pizzas[0].name
                    elif len(pizzas)== 2:
                        response += pizzas[0].name+ " and "+pizzas[1].name
                    else:
                        pizza_names=[pizza.name for pizza in pizzas]
                        last_two_pizzas = " and ".join(pizza_names[-2:])
                        other_pizzas = ", ".join(pizza_names[:-2])
                        # Concatenate the two parts
                        response = other_pizzas + ", " + last_two_pizzas
                    dispatcher.utter_message(f"Our pizzas without {ingredient} are {response}.")
                    return [SlotSet("ingredient",None)]
            else:
                dispatcher.utter_message(f"We don't put {ingredient} in any pizza.")
                return [SlotSet("ingredient", None)]

class ActionTellPizzaWithoutIngredient(Action):

    def name(self) -> Text:
        return "action_tell_pizza_with_ingredient"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ingredient=tracker.get_slot("ingredient")

        if ingredient is None:
            dispatcher.utter_message("I didn't not understand, could you repeat please?")
            return [SlotSet("ingredient",None)]
        else:
            ingredient=ingredient.lower() #Send to lowercase
            if ingredient in toppings:
                pizzas=getPizzasWithIngredient(ingredient)
                response =""
                if len(pizzas) == 0:
                    dispatcher.utter_message(f"We don't put {ingredient} in any pizza.")
                    return [SlotSet("ingredient", None)]
                else:
                    if len(pizzas) == 1:
                        response += pizzas[0].name
                    elif len(pizzas)== 2:
                        response += pizzas[0].name+ " and "+pizzas[1].name
                    else:
                        pizza_names=[pizza.name for pizza in pizzas]
                        last_two_pizzas = " and ".join(pizza_names[-2:])
                        other_pizzas = ", ".join(pizza_names[:-2])
                        # Concatenate the two parts
                        response = other_pizzas + ", " + last_two_pizzas
                    dispatcher.utter_message(f"Our pizzas with {ingredient} are {response}.")
                    return [SlotSet("ingredient",None)]
            else:
                dispatcher.utter_message(f"We don't put {ingredient} in any pizza.")
                return [SlotSet("ingredient", None)]

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

class ValidateDrinkOrderForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_drink_order_form"

    def validate_drink_name(self,slot_value:Any,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: DomainDict)-> Dict[Text, Any]:
        """ Validate 'drink_name' value"""
        if slot_value is not None:
            if slot_value.lower() not in getDrinks():
                dispatcher.utter_message(text=f"We don't have {slot_value} in our available drinks, for more indications on the available ones, ask 'What drinks do you have?'")
                return {"drink_name":None}
            dispatcher.utter_message(text=f"Ok! You want to have {slot_value}.")
            return {"drink_name":slot_value}

    def validate_drink_amount(self,slot_value:Any,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: DomainDict)-> Dict[Text, Any]:

        if slot_value is not None:
            if str(slot_value).isnumeric():
                dispatcher.utter_message(text=f"Ok! You want to have {slot_value} bottles.")
                return {"drink_amount":slot_value}
            else:
                dispatcher.utter_message(text="Sorry, I don't recognize that amount, please provide me a valid number.")

class ValidatePickupOrderForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_pickup_order_form"

    def validate_order_time(self, slot_value: Any,
                             dispatcher: CollectingDispatcher,
                             tracker: Tracker,
                             domain: DomainDict) -> Dict[Text, Any]:
        dispatcher.utter_message(text=f"Ok! Registering the order for {slot_value}.")
        return {"order_time": slot_value}

    def validate_client_name(self,slot_value:Any,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: DomainDict)-> Dict[Text, Any]:
        if len(slot_value.split())!=2:
            dispatcher.utter_message(text="Please, give me your first and last name.")
            return {"client_name":None}
        dispatcher.utter_message(text=f"Ok! Registering the order for {slot_value}.")
        return {"client_name":slot_value}


class ValidateDeliveryOrderForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_delivery_order_form"

    def validate_address_street(self, slot_value: Any,
                             dispatcher: CollectingDispatcher,
                             tracker: Tracker,
                             domain: DomainDict) -> Dict[Text, Any]:
        dispatcher.utter_message(text=f"Ok! Registering the address at {slot_value}.")
        return {"address_street": slot_value}

    def validate_order_time(self, slot_value: Any,
                             dispatcher: CollectingDispatcher,
                             tracker: Tracker,
                             domain: DomainDict) -> Dict[Text, Any]:
        dispatcher.utter_message(text=f"Ok! Registering the order for {slot_value}.")
        return {"order_time": slot_value}

    def validate_client_name(self,slot_value:Any,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: DomainDict)-> Dict[Text, Any]:
        if len(slot_value.split())!=2:
            dispatcher.utter_message(text="Please, give me your first and last name.")
            return {"client_name":None}
        dispatcher.utter_message(text=f"Ok! Registering the order for {slot_value}.")
        return {"client_name":slot_value}

class ActionCheckOrderReady(Action):

    def name(self) -> Text:
        return "action_check_order_ready"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        #print("Running order check, previous value:",tracker.get_slot("order_ready"))
        userOrder = getOrderByUserID(tracker.sender_id)
        if userOrder is None:
            #print(f"User {tracker.sender_id} does not have an order")
            return [SlotSet("order_ready", False)]
        else:
            #print(f"User {tracker.sender_id} has an order")
            return [SlotSet("order_ready", True)]


class ActionSeeOrderInfo(Action):

    def name(self) -> Text:
        return "action_see_order_information"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        logOrderDB()
        userOrder = getOrderByUserID(tracker.sender_id)
        if userOrder is None:
            print(f"User {tracker.sender_id} does not have an order")
            dispatcher.utter_message(response="utter_no_user_order")
            return []
        else:
            print(f"User {tracker.sender_id} has an order")
            orderRecap=getOrderRecap(userOrder)
            method=userOrder.delivery_method
            id=userOrder.id
            delivery_info =""
            if method is None:
                delivery_info="You didn't tell me how you wish to receive your order."
            elif method=="delivery":
                name=userOrder.client_name
                address=userOrder.address
                order_time=userOrder.order_time
                delivery_info=f"Your order will be delivered at {address} around {order_time}, the saved name is {name}."
            elif method=="pickup":
                order_time=userOrder.order_time
                name=userOrder.client_name
                delivery_info=f"You will come to pickup your order at {order_time}, the saved name is {name}."
            order_id_information=f"Your order ID is {str(id)}."
            message=orderRecap+"\n"+delivery_info+"\n"+order_id_information
            dispatcher.utter_message(message)
            print(f"Order info to send user: {userOrder.__dict__}")
            return []


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
                pizza_to_add = OrderedPizza(pizza=getPizzaFromMenuByName(pizza_type), size=pizza_size, toppings=[],amount=1)
                order=getOrderByUserID(tracker.sender_id)
                if order is None: #User does not have an order yet, create it and add pizza
                    order=Order(id=order_id_counter,user_id=tracker.sender_id)
                    order.addPizza(pizza_to_add)
                    orders.append(order)
                    updateOrderIDCounter()
                else: #User has already an order, modify it with new pizza
                    order.addPizza(pizza_to_add)
                    updateExistingOrder(order)
                message=getOrderRecap(order)
                dispatcher.utter_message(text=message)
                #dispatcher.utter_message(response="utter_anything_else_order")
                return[FollowupAction("utter_anything_else_order"),SlotSet("pizza_type",None),SlotSet("pizza_size",None)]
            elif (bot_event['metadata']['utter_action'] == 'utter_submit_drink'):
                drink_name = tracker.slots['drink_name']
                drink_amount = tracker.slots['drink_amount']
                message="Perfect! It was added to your order.\n"
                drink=getDrinkFromMenuByName(drink_name)
                drink_to_add=OrderedDrink(drink=drink,amount=int(drink_amount))
                order = getOrderByUserID(tracker.sender_id)
                if order is None: #User does not have an order yet, create it and add pizza
                    order=Order(id=order_id_counter,user_id=tracker.sender_id)
                    order.addDrink(drink_to_add)
                    orders.append(order)
                    updateOrderIDCounter()
                else: #User has already an order, modify it with new pizza
                    order.addDrink(drink_to_add)
                    updateExistingOrder(order)
                message+=getOrderRecap(order)
                dispatcher.utter_message(text=message)
                return [FollowupAction("utter_anything_else_order"),SlotSet("drink_name", None), SlotSet("drink_amount", None)]
            elif (bot_event['metadata']['utter_action'] == "utter_submit_pickup"):
                order=getOrderByUserID(tracker.sender_id)
                client_name = tracker.slots['client_name']
                order_time = tracker.slots['order_time']
                order.setPickupInformation(pickup_time=order_time, pickup_client=client_name)
                updateExistingOrder(order)
                dispatcher.utter_message(response="utter_order_saved_pickup")
                return[SlotSet("client_name",None),SlotSet("order_time",None)]
            elif (bot_event['metadata']['utter_action'] == "utter_submit_delivery"):
                order = getOrderByUserID(tracker.sender_id)
                client_name = tracker.slots['client_name']
                order_time = tracker.slots['order_time']
                address= tracker.slots['address_street']
                order.setDeliveryInformation(delivery_time=order_time, delivery_address=address, delivery_client=client_name)
                print(f"Order {order.id} will be delivered at {address} at {order_time} for the client {client_name}")
                updateExistingOrder(order)
                dispatcher.utter_message(response="utter_order_saved_delivery")
                return [SlotSet("address_street", None),SlotSet("client_name", None), SlotSet("order_time", None)]
            elif (bot_event['metadata']['utter_action'] == "utter_ask_delete_order_confirmation"):
                removed=removeOrderByUserID(tracker.sender_id)
                if removed is None:
                    dispatcher.utter_message(response="utter_delete_order_error")
                else:
                    dispatcher.utter_message(response="utter_order_deleted")
                return []
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
            previous_action=bot_event['metadata']['utter_action']
            if(previous_action == "utter_anything_else_order"):
                message="Ok, checking out your order...\n"
                order=getOrderByUserID(tracker.sender_id)
                print("Checking out the order "+getOrderRecap(order))
                message+=getOrderRecap(order)
                price=computeOrderPrice(order)
                message+="The total price is: "+str(price)+" €"
                dispatcher.utter_message(text=message)
                dispatcher.utter_message(response="utter_ask_delivery_method")
            elif (bot_event['metadata']['utter_action'] == 'utter_submit_pizza'):
                dispatcher.utter_message(text="Ok, removing this last item.")
                return[SlotSet("pizza_type",None),SlotSet("pizza_size",None),FollowupAction("pizza_order_form")]
            elif (bot_event['metadata']['utter_action'] == 'utter_submit_drink'):
                dispatcher.utter_message(text="Ok, removing this last item.")
                return [SlotSet("drink_name", None), SlotSet("drink_amount", None),FollowupAction("drink_order_form")]
            elif (bot_event['metadata']['utter_action'] == 'utter_submit_delivery'):
                dispatcher.utter_message(text="Ok, removing these details.")
                return [SlotSet("address_street", None), SlotSet("order_time", None),SlotSet("client_name", None),FollowupAction("delivery_order_form")]
            elif (bot_event['metadata']['utter_action'] == 'utter_submit_pickup'):
                dispatcher.utter_message(text="Ok, removing these details.")
                return [SlotSet("order_time", None), SlotSet("client_name", None),FollowupAction("pickup_order_form")]
            elif (bot_event['metadata']['utter_action'] == 'utter_ask_delete_order_confirmation'):
                dispatcher.utter_message(text="Ok, your order has not been deleted.")
                return []
            else:
                dispatcher.utter_message("I don't understand what are you referring to, could you please be more specific?")
        except:
            dispatcher.utter_message("Sorry, can you repeat that?")
        return []


