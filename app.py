from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import json
import random

app = Flask(__name__)

with open('openai_apikey.txt', 'r', encoding='utf-8') as file:
    api_key = file.read().strip()
client = OpenAI(api_key=api_key)

chat_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

# Load the JSON file during initialization
with open('chatbot_data.json') as file:
    chatbot_data = json.load(file)

@app.route('/')
def home():
    # Generate or retrieve an initial message from the chatbot
    initial_message = generate_initial_message()
    return render_template('index.html', initial_message=initial_message)

def generate_initial_message():
    # Find the appropriate intent for the initial message
    initial_intent = None
    for intent in chatbot_data['intents']:
        if intent['name'] == 'intro':
            initial_intent = intent
            break

    if initial_intent:
        # Select a random response from the intent's responses
        initial_message = random.choice(initial_intent['responses'])
    else:
        # If no matching intent found, use a default initial message
        initial_message = "Hello! How can I assist you today?"

    return initial_message

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    chat_history.append({"role": "user", "content": user_message})

    # Match user input against intents
    matched_intent = None
    for intent in chatbot_data['intents']:
        if user_message.lower() in intent['patterns']:
            matched_intent = intent
            break

    if matched_intent:
        # Get response and action for the matched intent
        response_text = random.choice(matched_intent['responses'])
        action = matched_intent.get('actions', [])
        
        # Perform action if specified
        if action:
            if "list_products" in action:
                # Logic to list available products
                products = ["Smartphone X", "Laptop Y", "Tablet Z"]
                response_text += "\n\nHere are our available products:\n" + "\n".join(products)
            elif "show_product_details" in action:
                # Logic to show details of a specific product
                product_details = "Smartphone X features:\n- 6.5-inch OLED display\n- Quad-core processor\n- 128GB storage\n- Dual rear cameras"
                response_text += "\n\n" + product_details
            elif "start_purchase_process" in action:
                # Logic to initiate the purchase process
                response_text += "\n\nTo start the purchase process, please visit our website at www.example.com and add the desired product to your cart. Proceed to checkout and follow the steps to complete your order."
    else:
        # If no intent matched, use GPT to generate a response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history
        )
        response_text = response.choices[0].message.content

    chat_history.append({"role": "assistant", "content": response_text})
    return jsonify({'message': response_text})

if __name__ == '__main__':
    app.run(debug=True)