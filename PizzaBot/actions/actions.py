# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker,FormValidationAction
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

drink_menu={
    "water": 1,
    "tea": 2,
    "coke": 3,
    "beer": 5,
    "sprite": 3,
}

def getDrinks():
    return list(drink_menu.keys())
def getPizzaSizes():
    return ["small","medium","large"]

def getPizzaTypes():
    return ["margherita","marinara","pepperoni"]


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

class ActionTellDrinkList(Action):

    def name(self) -> Text:
        return "action_tell_drink_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        key_to_find = next(tracker.get_latest_entity_values("drink_name"), None)

        if key_to_find is None:
            dispatcher.utter_message(response="I did not understand, could you ask me again please?")
        else:
            drink_price = value = drink_menu.get(key_to_find, None)
            if drink_price is None:
                msg = f"I'm afraid we do not have {key_to_find} in our menu. You can get a list of available drinks by asking 'What drinks do you have?'"
            else:
                msg = f"A {key_to_find} costs {str(drink_price)} €"
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

