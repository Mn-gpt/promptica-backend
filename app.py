from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY")

# إضافة هذا لمعالجة طلبات GET (اختياري)
@app.route('/')
def health_check():
    return jsonify({"status": "active", "service": "Promptica Backend"})

# إضافة هذا لمعالجة طلبات GET لـ /generate (اختياري)
@app.route('/generate', methods=['GET'])
def generate_get():
    return jsonify({"error": "Use POST method with 'prompt' in JSON body"}), 405

# النقطة الرئيسية
@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        data = request.json
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({"error": "Missing 'prompt' in request body"}), 400
            
        if not API_KEY:
            return jsonify({"error": "API key not configured"}), 500
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return jsonify(response.json())
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))