# Declare the knowledge base
from scipy.spatial._ckdtree import ordered_pairs


class Pizza:
    def __init__(self, name, price, ingredients):
        self.name = name
        self.price = price
        self.ingredients=ingredients

class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class OrderedPizza:
    def __init__(self, pizza, size, toppings,amount):
        self.pizza=pizza
        self.size=size
        self.amount=amount
        self.extras=toppings

    def computePrice(self):
        base_price = self.pizza.price
        if (self.size == "small"):
            base_price -= 1
        elif (self.size == "large"):
            base_price += 2
        return (base_price+len(self.extras))*int(self.amount)

    def printExtras(self):
        message=""
        if len(self.extras)==0:
             message+="no addition"
        elif len(self.extras)==1:
             message+=self.extras[0]
        elif len(self.extras)==2:
            message+= self.extras[0]+" and "+self.extras[1]
        else:
            last_two_extras = " and ".join(self.extras[-2:])
            other_extras = ", ".join(self.extras[:-2])

            # Concatenate the two parts
            message += other_extras + ", " + last_two_extras
        return message

    def __eq__(self, other):
        isEqual=(self.pizza.name==other.pizza.name) and (self.extras==other.extras) and (self.size == other.size) #Check all parameters are identical
        return isEqual

class OrderedDrink:
    def __init__(self, drink: Drink, amount):
        self.drink=drink
        self.amount=amount

    def computePrice(self):
        return int(self.amount)*self.drink.price

    def __eq__(self, other):
        isEqual = (self.drink.name == other.drink.name)# Check all parameters are identical
        return isEqual

class Order:
    def __init__(self, id, user_id):
        self.id = id
        self.user_id = user_id
        self.pizzas = []
        self.drinks = []
        self.delivery_method = None  # Can be "delivery" or "pickup"
        self.client_name = None
        self.address = None
        self.order_time = None
        self.phone = None


    def addPizza(self, pizza_to_add: OrderedPizza):
        for i in range(len(self.pizzas)):
            ordered_pizza=self.pizzas[i]
            if ordered_pizza == pizza_to_add: #If pizza is already in order, add to its amount
                ordered_pizza.amount+=pizza_to_add.amount
                self.pizzas[i]=ordered_pizza
                return
        self.pizzas.append(pizza_to_add)

    def addDrink(self, drink_to_add: OrderedDrink):
        for i in range(len(self.drinks)):
            ordered_drink=self.drinks[i]
            if ordered_drink == drink_to_add: #If drink is already in order, add to its amount
                ordered_drink.amount+=drink_to_add.amount
                self.drinks[i]=ordered_drink
                return
        self.drinks.append(drink_to_add) #else, just add a new drink

    def setPickupInformation(self, pickup_time, pickup_client):
        self.delivery_method = "pickup"
        self.order_time = pickup_time
        self.client_name = pickup_client

    def setDeliveryInformation(self, delivery_time, delivery_address, delivery_client):
        self.delivery_method = "delivery"
        self.order_time = delivery_time
        self.client_name = delivery_client
        self.address = delivery_address