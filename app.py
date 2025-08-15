from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get('GEMINI_API_KEY')

@app.route('/')
def home():
    return jsonify({
        "status": "active",
        "service": "Promptica Backend",
        "endpoint": "POST /generate"
    })

@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({"error": "يجب تقديم 'prompt' في جسم الطلب"}), 400
            
        if not API_KEY:
            return jsonify({"error": "لم يتم تكوين مفتاح API"}), 500
        
        # استدعاء Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        gemini_response = response.json()
        
        return jsonify(gemini_response)
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"خطأ في الاتصال بـ Gemini API: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"خطأ غير متوقع: {str(e)}"}), 500

# هذا الكود ضروري لتشغيل الخادم محلياً
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))