# HMD Project

### Domain
Pizza ordering bot

### Available Actions
- Order pizza(s)
  - make the intent contain the pizza slot (to finetune)
    - try merge say_pizza_type e size
    - try adding complete requests in init_request
  - make the form flexible to unhappy user paths
- Order drink(s) 
  - support for text instead of numbers (two vs 2) (TODO)
  - make the form flexible to unhappy user paths
- Customize pizza (to finetune)(only 1 topping)
- Ask for price of pizza/drink
- Ask for ingredients in pizza
- Ask for menu
- Ask for pizza recommendation
  - Suggest me pizzas with/without (topping)
- Place order
  - Order recap
  - Specify delivery or takeaway
  - Add error handling
  - make the form flexible to unhappy user paths (TODO)
- Modify order (TODO)
  - Add pizza (TODO?)
  - Remove pizza (TODO)
  - Change pizza (TODO)
  - Add drink (TODO?)
  - Remove drink (TODO)
  - Change drink (TODO)
  - Change address (TODO)
  - Change time (TODO)
  - Change delivery method (TODO)
- Deploy on Alexa (TODO)

### Training the model

```
rasa train
```

A pretrained model is also available in /models

### Running the code

Open two terminals, on one type:

```
rasa run actions
```
to start the action server. In the other type:
```
rasa shell
```
to start the conversational agent.