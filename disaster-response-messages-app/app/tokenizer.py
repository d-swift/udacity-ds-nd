import re

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')


def tokenizer(text: str):
    """Normalize, tokenize and lemmatize text.

    Args:
        text: str. A body of text.

    Returns:
        tokens: list(str). A list of normalised and lemmatized words.
    """
    # Replace url with 'website'.
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    found_urls = re.findall(url_regex, text)
    for url in found_urls:
        text = text.replace(url, "website")

    # Convert to lower case and remove punctuation
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())

    # Lemmatize and remove stop words.
    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words('english')

    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
    return tokens