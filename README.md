# HMD Project

### Domain
Pizza ordering bot

### Available Actions
- Order pizza(s)
  - If user asks "What is in a diavola" inside the form, the form will automatically load the slot and continue (TODO)
  - Customize pizza by adding a topping
- Order drink(s) 
  - support for text instead of numbers (two vs 2)
  - make the form flexible to unhappy user paths
  - ignore some intents within the form (TODO)
- Place order
  - Order recap
  - Specify delivery or takeaway
- Ask for price of pizza/drink
- Ask for ingredients in pizza
- Ask for menu
- Ask for pizza recommendation
- Ask for pizzeria location
- Ask for timings of pizzeria (TODO)
  - Suggest pizzas with/without topping
- Modify order
  - Add pizza
  - Remove pizza
  - Add drink 
  - Remove drink
  - Change time
  - Change name
  - Change delivery method
  - Delete order
- Add test stories (TODO)
- Make 2nd Configuration file
- Deploy on Alexa

### Training the model

```
rasa train
```

A pretrained model is also available in /models folder.

### Running the bot locally

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
