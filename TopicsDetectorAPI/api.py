from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline, AutoModelForSeq2SeqLM, MarianMTModel, AutoModelForTokenClassification

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download('stopwords')


def detect_language(text):
    model = AutoModelForSequenceClassification.from_pretrained(
        "papluca/xlm-roberta-base-language-detection")
    tokenizer = AutoTokenizer.from_pretrained(
        "papluca/xlm-roberta-base-language-detection")
    classifier = pipeline("sentiment-analysis",
                          model=model, tokenizer=tokenizer)
    result = classifier(text)[0]
    return result['label']


def translate(text, source_language="bg", target_language="en"):
    model_name = f"Helsinki-NLP/opus-mt-{source_language}-{target_language}"
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    batch = tokenizer([text], return_tensors="pt")
    generated_ids = model.generate(**batch)
    translated_text = tokenizer.batch_decode(
        generated_ids, skip_special_tokens=True)[0]
    return translated_text


def summarize(text):
    classifier = pipeline("summarization")
    summary = classifier(text)[0]["summary_text"]
    return summary


def extract_keywords(text):
    tokenizer = AutoTokenizer.from_pretrained(
        "yanekyuk/bert-uncased-keyword-extractor")
    model = AutoModelForTokenClassification.from_pretrained(
        "yanekyuk/bert-uncased-keyword-extractor")
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    keywords = []
    for i in range(len(logits[0])):
        if logits[0][i][0] > 0:
            keywords.append(tokenizer.convert_ids_to_tokens(
                inputs["input_ids"][0][i].item()))
    return keywords


def generate_suggested_topics_keywords(text, general_topics):
    stopwords = nltk.corpus.stopwords.words('english')
    text = ' '.join([word for word in text.split() if word not in stopwords])
    text = ''.join([i for i in text if not i.isdigit()])
    text = ''.join([i for i in text if i.isalpha() or i.isspace()])
    text = ' '.join([w for w in text.split() if len(w) > 2 and len(w) < 15])
    keywords = extract_keywords(text)
    lemmatizer = WordNetLemmatizer()
    lemma_keywords = [lemmatizer.lemmatize(keyword) for keyword in keywords]
    keywords = list(set(keywords + general_topics + lemma_keywords))
    return keywords


def predict_topic(text, topics):
    classifier = pipeline("zero-shot-classification",
                          model="facebook/bart-large-mnli")
    prediction = classifier(text, topics)
    topics_pred = prediction["labels"]
    return topics_pred


app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    general_topics = [
        "art",
        "business",
        "celebrities",
        "diaries",
        "entertainment",
        "lifestyle",
        "family",
        "fashion",
        "style",
        "movies",
        "fitness",
        "health",
        "food",
        "gaming",
        "learning",
        "educational",
        "music",
        "news",
        "hobbies",
        "relationships",
        "science",
        "technology",
        "sports",
        "travel",
        "adventure",
        "politics",
        "history",
        "culture",
        "philosophy",
        "religion",
        "environment",
        "finance",
        "economy",
        "architecture",
        "design",
        "blog",
        "programming",
        "tutorial",
        "documentation",
        "tools",
        "investment",
        "diets",
        "motivation",
        "ideas",
    ]

    text = request.json["text"]
    language = detect_language(text)
    if language == "en":
        text_en = text
    else:
        text_en = translate(text, language, "en")

    if len(text_en) > 512:
        text_summary = summarize(text_en)
    else:
        text_summary = text_en

    suggested_topics_keywords = generate_suggested_topics_keywords(
        text_summary, general_topics)

    topics_pred = predict_topic(text_summary, suggested_topics_keywords)

    topics_pred = topics_pred[:5]

    return jsonify({"prediction": topics_pred})


if __name__ == '__main__':
    app.run(debug=True)
