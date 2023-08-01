# HMD Project

### Domain
Pizza ordering bot

### Available Actions
- Order pizza(s)
  - make the intent contain the pizza slot (to finetune)
    - try merge say_pizza_type e size
    - try adding complete requests in init_request
  - make the form flexible to unhappy user paths (TODO)
- Order drink(s) 
  - make the intent contain the pizza slot (to finetune)
- Customize pizza (TODO)
- Ask for price of pizza/drink
- Ask for ingredients in pizza
- Ask for menu
- Ask for pizza recommendation (TODO)
  - Suggest me a pizza with/without (topping)
  - Ask for pizza of the day?
- Place order (TODO)
  - Order recap
  - Specify delivery or takeaway
- Modify order (TODO)

### Training the model

```
Look! You can see my backticks.
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