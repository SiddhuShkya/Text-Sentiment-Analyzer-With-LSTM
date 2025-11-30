import re
import numpy as np
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
# from spellchecker import SpellChecker
from nltk.stem import WordNetLemmatizer

lem = WordNetLemmatizer()
# spell = SpellChecker()
STOPWORDS = set(stopwords.words('english'))
CLEANED_STOPWORDS = [word.replace("'", "") for word in list(STOPWORDS)]


def remove_stopwords(text):
    text = " ".join([word for word in text.split() if word not in CLEANED_STOPWORDS])
    return text

def remove_symbols_and_numbers(text):
    pattern = r'[^a-zA-Z\s]'
    cleaned_text = re.sub(pattern, ' ', text)
    return cleaned_text

def lowercasing(text):
    return text.lower()

def lemmatize_words(text):
    lemmatized_text = " ".join([lem.lemmatize(w, pos="v") for w in text.split()])
    return lemmatized_text

def remove_html_tags(text):
    pattern = re.compile(r'<.*?>')
    cleaned_text = re.sub(pattern, ' ', text)
    return cleaned_text

# def correct_text(text):
#     text_array = np.array(text.split())
#     corrected_array = np.array([spell.correction(w) if spell.correction(w) is not None else w for w in text_array])
#     corrected_text = corrected_array.tolist()
#     return " ".join(corrected_text)

def remove_urls(text):
    url_pattern = r'https?://(?:www\.)?\S+'
    tag_pattern = r'@\w+'
    combined_pattern = f'({url_pattern})|({tag_pattern})'
    cleaned_text = re.sub(combined_pattern, ' ', text)
    return cleaned_text

def remove_emojis(text):
    emoji_pattern = re.compile("["
                    u"\U0001F600-\U0001F64F"
                    u"\U0001F300-\U0001F5FF"
                    u"\U0001F680-\U0001F6FF"
                    u"\U0001F1E0-\U0001F1FF"
                    u"\U00002702-\U000027B0"
                    u"\U000024C2-\U0001F251"
                    "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r' ', text)

def preprocess_text(text):
    text = text.lower()
    text = remove_urls(text)
    text = remove_emojis(text)
    text = remove_symbols_and_numbers(text)
    # text = correct_text(text)
    text = " ".join([lem.lemmatize(w, pos="v") for w in text.split()])
    text = remove_stopwords(text)
    return text