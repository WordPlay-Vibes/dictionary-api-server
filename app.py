import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Dictionary API!"})

@app.route("/define")
def define_word():
    word = request.args.get("word")
    if not word:
        return jsonify({"error": "No word provided"}), 400

    return jsonify({"word": word, "definition": "This is a sample definition."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 if PORT is not set
    app.run(host="0.0.0.0", port=port)

