from modules.translation import translate
from modules.lda import predict_topic_keywords
from langdetect import detect as detect_language

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    text = request.json["text"]
    topic_keywords = predict_topic_keywords(text)
    prediction_object = {
        "topic_keywords": topic_keywords,
    }

    return jsonify({"prediction": prediction_object})


@app.route("/translate", methods=["POST"])
def translate_text():
    text = request.json["text"]

    # optional source and target languages
    source_language = request.json.get("source_language")
    target_language = request.json.get("target_language") or "en"

    detected_language = detect_language(text)

    if detected_language != target_language:
        if source_language:
            translated_text = translate(text, source_language, target_language)
        else:
            translated_text = translate(text, detected_language, target_language)
        print("Translating text...")
    else:
        print("Skipping translation.")
        translated_text = text

    translation_object = {
        "source_language": source_language,
        "target_language": target_language,
        "detected_language": detected_language,
        "translated_text": translated_text,
    }

    return jsonify({"translation": translation_object})


if __name__ == '__main__':
    app.run(debug=True)
