import os
import requests
from openai import OpenAI
from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from urllib.parse import urlencode
from va_logic import get_bot_response, get_prompt_list

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt_list = get_prompt_list()

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/chat')
def chat():
    return render_template('index.html')

@app.route('/play')
def play():
    return render_template('play.html')


@app.route('/message', methods=['POST'])
def message():
    user_input = request.json.get('message')
    response = get_bot_response(user_input, prompt_list)


    for prefix in ["Gaia:", "AI:", "AI", "Gaia", "?"]:
        if response.startswith(prefix):
            response = response[len(prefix):].strip()

    return jsonify({'reply': response})

if __name__ == '__main__':
    app.run(debug=True)




