# أضف هذه الدوال قبل تعريف المسارات
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = jsonify({})
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        res.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return res

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
# حل مشكلة المسارات في Vercel
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, request, jsonify
import requests
import os
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# إعداد سجلات التصحيح
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        # تسجيل الطلب الوارد
        logger.info("Received request: %s", request.json)
        
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            logger.error("Missing 'prompt' in request")
            return jsonify({"error": "يجب تقديم 'prompt' في جسم الطلب"}), 400
            
        if not API_KEY:
            logger.error("API_KEY is not set")
            return jsonify({"error": "لم يتم تكوين مفتاح API"}), 500
        
        # استدعاء Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        logger.info("Sending request to Gemini API: %s", payload)
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        gemini_response = response.json()
        logger.info("Received response from Gemini: %s", gemini_response)
        
        return jsonify(gemini_response)
        
    except requests.exceptions.RequestException as e:
        logger.error("Request to Gemini failed: %s", str(e))
        return jsonify({"error": f"خطأ في الاتصال بـ Gemini API: {str(e)}"}), 500
    except Exception as e:
        logger.exception("Unexpected error occurred")
        return jsonify({"error": f"خطأ غير متوقع: {str(e)}"}), 500

# هذا الكود ضروري لتشغيل الخادم محلياً
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))