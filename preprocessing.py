import re
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS as sw
from nltk.stem import PorterStemmer


def preprocess_text(text, whitespace=True, specialchars=True, stopwords=True, stem=True):
    '''
    The preprocess_text function pre-processes the information crawled by
    the spiders in this project. whitespace=True removes all trailing whitespaces
    in the text. specialchars=True removes all special characters and converts
    text to lowercase. stopwords=True removes stopwords, and stem=True uses a
    porterstemmer to turn each word to its stem. At default, all options are enabled.
    '''
    # remove trailing whitespaces
    if whitespace:
        text = " ".join(text.split())
    # remove special characters and convert to lowercase
    if specialchars:
        text = re.sub(r'[^a-zA-Z0-9\s]', "", str(text)).lower()
    # remove stopwords
    if stopwords:
        text = [word for word in text.split() if word not in (sw)]
    # convert words to stem
    if stem:
        ps = PorterStemmer()
        text = ' '.join([ps.stem(word) for word in text])

    return text
