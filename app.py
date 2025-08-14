from flask import Flask, request, jsonify
import requests
import os

# استخدم نفس اسم المتغير المستخدم في Render
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.json
    prompt = data.get('prompt')
    
    if not API_KEY:
        return jsonify({"error": "API key not configured"}), 500
    
    # استدعاء Gemini API - استخدم المتغير API_KEY
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
