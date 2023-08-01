# Declare the knowledge base

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

class OrderedDrink:
    def __init__(self, drink: Drink, amount):
        self.drink=drink
        self.amount=amount
        self.price=int(amount)*self.drink.price