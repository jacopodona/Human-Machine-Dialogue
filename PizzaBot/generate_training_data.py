pizza_types = ["margherita", "marinara", "diavola", "capricciosa","hawaiian", "vegetarian", "pub", "rustic","kebab", "cheesey", "light", "pesto"]
pizza_sizes = ["small","medium","large"]
ingredients = ["tomato sauce","mozzarella","garlic","pepperoni","ham","pineapple","bell peppers","eggplant","zucchini","spinach","onions",
          "olives","mushrooms","wurstel","chicken","sausage","potatoes","BBQ sauce"]
drink_amounts=[1,2,3,4,5,6,7,8]
drink_names=["water","tea","coke","beer","sprite"]
order_times=["7.30pm","19.30","7.30","19:30","7:30","8pm","20","20.00","8","8.00","8:00","20:00","8.30pm","20.30","8.30","20:30","8:30",
            "9pm","21","21.00","9","9:00","21:00"]

def generateFullPizzaRequests():
    training_data = []
    variations = ["I want to order a [{pizza_size}](pizza_size) [{pizza_name}](pizza_type) with [{ingredient}](ingredient)",
                  "I would like to order a [{pizza_size}](pizza_size) [{pizza_name}](pizza_type) with {ingredient}(ingredient)",
                  "I want a [{pizza_size}](pizza_size) [{pizza_name}](pizza_type) with {ingredient}(ingredient)",
                  "I want to add a [{pizza_size}](pizza_size) [{pizza_name}](pizza_type) with {ingredient}(ingredient)"]
    for sentence in variations:
        for pizza_name in pizza_types:
            for ingredient in ingredients:
                for pizza_size in pizza_sizes:
                    user_message=sentence.format(pizza_name=pizza_name, ingredient=ingredient,pizza_size=pizza_size)
                    training_data.append(user_message)
    return training_data

def generatePizzaWithIngredientRequests():
    training_data = []
    variations = ["I want to order a  [{pizza_name}](pizza_type) with [{ingredient}](ingredient)",
                  "I would like to order a [{pizza_name}](pizza_type) with {ingredient}(ingredient)",
                  "I want a [{pizza_name}](pizza_type) with {ingredient}(ingredient)",
                  "I want to add a [{pizza_name}](pizza_type) with {ingredient}(ingredient)"]
    for sentence in variations:
        for pizza_name in pizza_types:
            for ingredient in ingredients:
                user_message=sentence.format(pizza_name=pizza_name, ingredient=ingredient)
                training_data.append(user_message)
    return training_data

def generateSimplePizzaRequests():
    training_data = []
    variations = ["I want to order a [{pizza_name}](pizza_type)",
                  "I would like to order a [{pizza_name}](pizza_type)",
                  "I want a [{pizza_name}](pizza_type)",
                  "I want to add a [{pizza_name}](pizza_type)",
                  "I want another [{pizza_name}](pizza_type)",
                  "Give me a [{pizza_name}](pizza_type)",
                  "Add a [{pizza_name}](pizza_type)",
                  "Get me a [{pizza_name}](pizza_type)"]
    for sentence in variations:
        for pizza_name in pizza_types:
            user_message=sentence.format(pizza_name=pizza_name)
            training_data.append(user_message)
    return training_data

def generateFullDrinkRequests():
    training_data = []
    variations = ["I want [{drink_amount}](drink_amount) [{drink_name}s](drink_name)",
                  "I want [{drink_amount}](drink_amount) bottles of [{drink_name}](drink_name)",
                  "Add [{drink_amount}](drink_amount) bottles of [{drink_name}](drink_name)",
                  "I would like [{drink_amount}](drink_amount) bottles of [{drink_name}](drink_name)"
                  ]
    for sentence in variations:
        for drink_amount in drink_amounts:
            for drink_name in drink_names:
                user_message=sentence.format(drink_amount=drink_amount,drink_name=drink_name)
                training_data.append(user_message)
    return training_data

def generateSimpleDrinkRequests():
    training_data = []
    variations = ["I want some [{drink_name}](drink_name)",
                  "I want a bottle of [{drink_name}](drink_name)",
                  "I would like a [{drink_name}](drink_name)",
                  "I want to drink [{drink_name}](drink_name)",
                  "Can I have some [{drink_name}](drink_name)",
                  "I would like to add some [{drink_name}](drink_name)",
                  "I want to order [{drink_name}](drink_name)",
                  ]
    for sentence in variations:
        for drink_name in drink_names:
                    user_message=sentence.format(drink_name=drink_name)
                    training_data.append(user_message)
    return training_data

def generateSayPizzaName():
    training_data = []
    variations = ["[{pizza_type}](pizza_type)",
                  "a [{pizza_type}](pizza_type)",
                  "the [{pizza_type}](pizza_type)",
                  "one [{pizza_type}](pizza_type)",
                  "a [{pizza_type}](pizza_type) with [{ingredient}](ingredient)"
                  ]
    for sentence in variations:
        for pizza_type in pizza_types:
            for ingredient in ingredients:
                user_message=sentence.format(pizza_type=pizza_type,ingredient=ingredient)
                training_data.append(user_message)
    return training_data

def generateSayOrderTime():
    training_data = []
    variations = ["at [{order_time}](order_time)",
                  "[{order_time}](order_time)",
                  ]
    for sentence in variations:
        for order_time in order_times:
            user_message = sentence.format(order_time=order_time)
            training_data.append(user_message)
    return training_data

def getRasaSentences(training_data):
    for sentence in training_data:
        print("- "+sentence)
    print("="*30)
    print(f"Generated {len(training_data)} training samples")


if __name__ == '__main__':
    training_data = generateSayOrderTime()
    getRasaSentences(training_data)