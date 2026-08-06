from flask import Flask, request, jsonify, render_template
from chatbot import get_bot_reply

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    result = get_bot_reply(user_input)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
