import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# API Keys from dictionaryapi.com (stored securely in .env)
DICTIONARY_API_KEY = os.getenv("LEARNERS_KEY")
THESAURUS_API_KEY = os.getenv("THESAURUS_KEY")

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Dictionary API!"})

@app.route("/define")
def define_word():
    word = request.args.get("word")
    if not word:
        return jsonify({"error": "No word provided"}), 400

    # Fetch definition from dictionary API
    url = f"https://www.dictionaryapi.com/api/v3/references/learners/json/{word}?key={DICTIONARY_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch definition"}), 500

    data = response.json()

    if not data or isinstance(data, list) and not data[0].get("shortdef"):
        return jsonify({"error": "No definition found"}), 404

    return jsonify({
        "word": word,
        "definition": data[0]["shortdef"][0]  # Returning the first definition
    })

@app.route("/synonyms")
def get_synonyms():
    word = request.args.get("word")
    if not word:
        return jsonify({"error": "No word provided"}), 400

    # Fetch synonyms from thesaurus API
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={THESAURUS_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch synonyms"}), 500

    data = response.json()

    if not data or isinstance(data, list) and not data[0].get("meta"):
        return jsonify({"error": "No synonyms found"}), 404

    return jsonify({
        "word": word,
        "synonyms": data[0]["meta"]["syns"][0]  # Returning the first set of synonyms
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 if PORT is not set
    app.run(host="0.0.0.0", port=port)

