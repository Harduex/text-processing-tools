import spacy
from gensim.utils import simple_preprocess
import gensim.corpora as corpora
import gensim
import re

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')


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


def predict_topic_keywords(text):
    # load corpus
    data = [text]
    # prepare stopwords
    stop_words = stopwords.words('english')
    additional_stop_words = ['do', 'm', 'un', 's', 'go', 're']
    stop_words.extend(additional_stop_words)
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
    # trigram = gensim.models.Phrases(bigram[data_words], threshold=100)

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    # trigram_mod = gensim.models.phrases.Phraser(trigram)

    # Remove Stop Words
    data_words_nostops = remove_stopwords(data_words, stop_words)

    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops, bigram_mod)

    # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
    # python3 -m spacy download en_core_web_sm # or python3 -m spacy download en
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

    # Do lemmatization keeping only noun, adj, vb, adv
    # data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=[
    #                                 'NOUN', 'ADJ', 'VERB', 'ADV'], nlp=nlp)
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=[
                                    'NOUN', 'VERB'], nlp=nlp)

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
