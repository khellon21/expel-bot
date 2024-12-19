from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_ngrok import run_with_ngrok
import requests
import os

app = Flask(__name__, static_folder='.')
CORS(app)
run_with_ngrok(app)

# NVIDIA API configuration
API_KEY = "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"
BASE_URL = "https://integrate.api.nvidia.com/v1"

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        history = data.get('history', [])
        
        messages = [{"role": "system", "content": "You are a friendly Chatbot."}]
        messages.extend(history)
        messages.append({"role": "user", "content": message})
        
        # Make request to NVIDIA API
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "nvidia/llama-3.1-nemotron-70b-instruct",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1024
            }
        )
        
        response_data = response.json()
        bot_response = response_data['choices'][0]['message']['content']
        
        return jsonify({
            "response": bot_response
        })
        
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run() 