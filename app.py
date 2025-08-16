from flask import Flask
from pyngrok import ngrok

app = Flask(__name__)

@app.route("/")
def home():
    return "Server via GitHub Actions + ngrok"

if __name__ == "__main__":
    public_url = ngrok.connect(8000)
    print("Public URL:", public_url)
    app.run(host="0.0.0.0", port=8000)