from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

with open('openai_apikey.txt', 'r', encoding='utf-8') as file:
        api_key = file.read().strip()
client = OpenAI(api_key=api_key)  # Replace with your OpenAI API key

chat_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    chat_history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )

    ai_response = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": ai_response})

    return jsonify({'message': ai_response})

if __name__ == '__main__':
    app.run(debug=True)