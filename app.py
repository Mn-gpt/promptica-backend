from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
API_KEY = os.environ.get("GEMINI_API_KEY")  # سيأخذ المفتاح من البيئة الآمنة

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.json
    prompt = data.get('prompt')
    
    # استدعاء Gemini API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={AIzaSyBzuARR_b09uXJIlfe7SB5U1ojKIsr2fy4}"
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
