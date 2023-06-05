import os
import json
from flask import Flask, render_template, request, jsonify
import openai
from openai.error import RateLimitError

openai.api_key = os.environ.get('OPENAI_API_KEY')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gpt', methods = ['GET', 'POST'])
def gpt():
    input_prompt = request.args.get('prompt') if request.method == 'GET' else request.form['prompt']
    message = [{'role': 'user', 'content': input_prompt}]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message
        )
        content = response.choices[0].message['content']
        # content = response
    except RateLimitError:
        content = 'the server is experiencing a high valume of requests'
    
    return jsonify(content=content)

if __name__ == '__main__':
    app.run(port="8080",debug=True)