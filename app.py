from flask import Flask, request, jsonify
import requests
import os
import logging
from flask_cors import CORS

# تهيئة التطبيق
app = Flask(__name__)
CORS(app)  # تفعيل CORS

# إعداد سجلات التصحيح
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# الحصول على مفتاح API من متغيرات البيئة
API_KEY = os.environ.get('GEMINI_API_KEY')

# نقطة النهاية للصفحة الرئيسية
@app.route('/')
def home():
    return jsonify({
        "status": "active",
        "service": "Promptica Backend",
        "endpoint": "POST /generate"
    })

# معالجة طلبات OPTIONS لـ CORS
@app.route('/generate', methods=['OPTIONS'])
def handle_preflight():
    response = jsonify({})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# نقطة النهاية لتوليد المحتوى مع التعديلات الكاملة
@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        # تسجيل وصول الطلب
        logger.info("تم استلام طلب جديد")
        
        # التحقق من وجود البيانات
        if not request.is_json:
            logger.error("الطلب ليس بصيغة JSON")
            return jsonify({"error": "يجب أن يكون الطلب بصيغة JSON"}), 400
            
        data = request.get_json()
        prompt = data.get('prompt')
        
        # التحقق من وجود الـ prompt
        if not prompt:
            logger.error("لم يتم تقديم 'prompt' في الطلب")
            return jsonify({"error": "يجب تقديم 'prompt' في جسم الطلب"}), 400
            
        # التحقق من وجود مفتاح API
        if not API_KEY:
            logger.error("مفتاح API غير موجود")
            return jsonify({"error": "لم يتم تكوين مفتاح API"}), 500
        
        # إعداد طلب Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        logger.info(f"إرسال الطلب إلى Gemini API: {payload}")
        
        # إرسال الطلب إلى Gemini
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        # التحقق من نجاح الطلب
        response.raise_for_status()
        
        # الحصول على الرد ومعالجته
        gemini_response = response.json()
        logger.info(f"تم استلام الرد من Gemini: {gemini_response}")
        
        # إرجاع الرد مع رؤوس CORS
        response = jsonify(gemini_response)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
        
    except requests.exceptions.RequestException as e:
        # معالجة أخطاء الشبكة وAPI
        logger.error(f"فشل الاتصال بـ Gemini API: {str(e)}")
        error_msg = f"خطأ في الاتصال بـ Gemini API: {str(e)}"
        response = jsonify({"error": error_msg})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 500
        
    except Exception as e:
        # معالجة الأخطاء العامة
        logger.exception("حدث خطأ غير متوقع")
        error_msg = f"خطأ غير متوقع: {str(e)}"
        response = jsonify({"error": error_msg})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 500

# تشغيل الخادم عند التنفيذ المباشر (للتجارب المحلية)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)