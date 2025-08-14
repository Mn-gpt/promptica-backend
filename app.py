from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get('GEMINI_API_KEY')

@app.route('/')
def home():
    return "الخادم يعمل بنجاح!"

@app.route('/generate', methods=['POST'])
def generate_content():
    return jsonify({"message": "وظيفة توليد المحتوى تعمل!"})