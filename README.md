# HMD Project

### Domain
Pizza ordering bot

### Available Actions
- Order pizza(s)
  - make the intent contain the pizza slot
    - If user asks "What is in a diavola" inside the form, the form will automatically load the slot and continue (TODO)
    - make the form flexible to unhappy user paths
- Order drink(s) 
  - support for text instead of numbers (two vs 2)
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
    - add street number to delivery
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
- Try removing the global action to speed up time
  - make order complete and order_ready start at false by default at conversation start
- Add test stories (TODO)
- Make 2nd Configuration file
- Deploy on Alexa

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

### Deploy on alexa

Open two terminals, on one type:

```
rasa run actions
```
to start the action server. In the other type:
```
rasa run -m models --endpoints endpoints.yml -p 5005 --credentials credentials.yml
```
to start the conversational agent.

Open ngrok and run 
```
ngrok http 5005
```
It should give an https url, go to the alexa skill endpoint and copy the URL, appending the suffix "/webhooks/alexa_assistant/webhook"

To Alexa, say "Start Pizza Bot"
### Testing the model

#### NLU

This command test the 2 configurations on performing Intent Classification and Entity Extraction on the nlu.yml file by performing cross validation using 5 folds.
```
rasa test nlu --nlu data/nlu.yml --config config_1.yml config_2.yml --cross-validation --folds 5
```