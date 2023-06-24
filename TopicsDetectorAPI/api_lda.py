from nltk.corpus import stopwords
import spacy
from gensim.models import CoherenceModel
from gensim.utils import simple_preprocess
import gensim.corpora as corpora
import gensim
import re
import numpy as np
from langdetect import detect as detect_language
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline, AutoModelForSeq2SeqLM, MarianMTModel, AutoModelForTokenClassification

import nltk
nltk.download('stopwords')


def translate(text, source_language="bg", target_language="en"):
    model_name = f"Helsinki-NLP/opus-mt-{source_language}-{target_language}"
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    batch = tokenizer([text], return_tensors="pt")
    generated_ids = model.generate(**batch)
    translated_text = tokenizer.batch_decode(
        generated_ids, skip_special_tokens=True)[0]
    return translated_text


def sent_to_words(sentences):
    for sentence in sentences:
        # deacc=True removes punctuations
        yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))


def remove_stopwords(texts, stop_words):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]


def make_bigrams(texts, bigram_mod):
    return [bigram_mod[doc] for doc in texts]


def make_trigrams(texts, bigram_mod, trigram_mod):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]


def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'], nlp=lambda x: x):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append(
            [token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


def predict_topic_keywords(text, stopwords):
    # load corpus
    data = [text]
    # prepare stopwords
    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu'])
    # Remove Emails
    data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]
    # Remove new line characters
    data = [re.sub('\s+', ' ', sent) for sent in data]
    # Remove distracting single quotes
    data = [re.sub("\'", "", sent) for sent in data]
    # Tokenize words and Clean-up text
    data_words = list(sent_to_words(data))

    # Build the bigram and trigram models
    # higher threshold fewer phrases.
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    # Remove Stop Words
    data_words_nostops = remove_stopwords(data_words, stop_words)

    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops, bigram_mod)

    # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
    # python3 -m spacy download en_core_web_sm # or python3 -m spacy download en
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=[
                                    'NOUN', 'ADJ', 'VERB', 'ADV'], nlp=nlp)

    # Create Dictionary
    id2word = corpora.Dictionary(data_lemmatized)

    # Create Corpus
    texts = data_lemmatized

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # Human readable format of corpus (term-frequency)
    readable_corpus = [[(id2word[id], freq) for id, freq in cp]
                       for cp in corpus[:1]]

    # Build LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=1,  # 20,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)

    lda_topic = lda_model.print_topics()[0][1]
    lda_topic_keywords = [keyword.split(
        "*")[1].replace("\"", "").strip() for keyword in lda_topic.split("+")]

    return lda_topic_keywords


# def predict_topic(topic_keywords):
#     # predict topic of text from topic keywords
#     # topic_keywords = ["travel","new","blog","quit","post","decide","job","world"]
#     # topics_pred should be one topic definition prediction based on topic_keywords
#     return topics_pred


app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    text = request.json["text"]
    source_language = detect_language(text)
    target_language = "en"
    translated_text = text
    if source_language != target_language:
        translated_text = translate(text, source_language, target_language)

    topic_keywords = predict_topic_keywords(translated_text, stopwords)

    # predicted_topics = predict_topic(topic_keywords)

    prediction_object = {
        "text_language": source_language,
        "translated_language": target_language,
        "translated_text": translated_text,
        "topic_keywords": topic_keywords,
        # "predicted_topics": predicted_topics
    }

    return jsonify({"prediction": prediction_object})


if __name__ == '__main__':
    app.run(debug=True)
