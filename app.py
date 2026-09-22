import os

import requests
from flask import Flask, render_template, request
from googletrans import Translator

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/Summarise", methods=["GET", "POST"])
async def summarise():
    if request.method != "POST":
        return render_template("index.html")

    token = os.environ.get("HF_API_TOKEN")
    if not token:
        return "HF_API_TOKEN is not configured", 503

    data = request.form["data"]
    max_length = int(request.form["maxL"])

    async with Translator() as translator:
        translated_input = await translator.translate(data, dest="en")
        response = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {token}"},
            json={
                "inputs": translated_input.text,
                "parameters": {
                    "min_length": max_length // 4,
                    "max_length": max_length,
                },
            },
            timeout=60,
        )
        response.raise_for_status()
        summary = response.json()[0]["summary_text"]
        translated_output = await translator.translate(summary, dest="hi")

    return render_template("index.html", result=translated_output.text)


if __name__ == "__main__":
    app.run()
