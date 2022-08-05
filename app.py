# backend -> frontend, frontend -> backend (jinja from Flask)
from googletrans import Translator
from flask import Flask, render_template
import requests
from flask import request as req


app = Flask(__name__)

translator = Translator()


@app.route("/", methods=["GET", "POST"])
def Index():
    return render_template("index.html")


@app.route("/Summarise", methods=["GET", "POST"])
def Summarise():
    if req.method == "POST":
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": f"Bearer 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"}

        data = req.form["data"]

        # translating hindi input from user into english
        translated_input = translator.translate(data, dest="en")

        maxL = int(req.form["maxL"])
        minL = maxL // 4

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        output = query(
            {
                "inputs": translated_input.text,
                "parameters": {
                    "min_length": minL,
                    "max_length": maxL,
                },
            }
        )[0]

        # translating english output from backend to hindi output for user
        translated_output = translator.translate(output["summary_text"], dest="hi")

        return render_template("index.html", result=translated_output.text)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
