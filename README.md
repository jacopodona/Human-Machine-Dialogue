# HMD Project

### Domain
Pizza ordering bot

### Available Actions
- Order pizza(s)
  - make the intent contain the pizza slot
    - try adding complete requests in init_request (TODO with topping)
    - If user asks "What is in a diavola" inside the form, the form will automatically load the slot and continue (TODO)
    - make the form flexible to unhappy user paths
- Order drink(s) 
  - support for text instead of numbers (two vs 2) (TODO)
  - make the form flexible to unhappy user paths
  - ignore some intents within the form (TODO)
- Customize pizza (only 1 topping)
- Ask for price of pizza/drink
- Ask for ingredients in pizza
- Ask for menu
- Ask for pizza recommendation
  - Suggest me pizzas with/without topping
- Place order
  - Order recap
  - Specify delivery or takeaway
    - add street number to delivery (TODO)
  - make the form flexible to unhappy user paths
- Modify order (TODO)
  - Add pizza
  - Remove pizza
    - add topping to request (TODO)
  - Add drink 
  - Remove drink
  - Change address (TODO)
  - Change time
  - Change name
  - Change delivery method
  - Delete order
- Try removing the global action to speed up time (TODO)
  - make order complete and order_ready start at false by default at conversation start
- Add stories and test stories (TODO)
- Make 2nd Configuration file (TODO)
- Deploy on Alexa (TODO)

### Training the model

```
rasa train
```

A pretrained model is also available in /models folder.

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