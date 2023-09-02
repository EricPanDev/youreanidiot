import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
def find(string: str):
    url = re.findall(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", string)
    data = [x[0] for x in url]
    new = []
    for i in data:
        new.append(i)
        new.append(f"http://webcache.googleusercontent.com/search?q=cache:{i}")
    return new

from newspaper import Article
from newspaper.article import ArticleException, ArticleDownloadState

from time import sleep

def article(url, timeout=4):
    try:
        print(url)
        article2 = Article(url)
        article2.download()
        slept = 0
        while article2.download_state == ArticleDownloadState.NOT_STARTED:
            if slept > timeout:
                return ""
            sleep(1)
            slept += 1
        article2.parse()
        return article2.text
    except:
        return ""

def summarize(text, per):
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary.strip()

def fetch_info(message):
    data = []
    for link in find(message):
        Data = article(link)
        try:
            data.append({"role": "system", "content": f"Talk about what is in this link. The link {link} is about: {summarize(Data, 0.05)}".replace("\n", "")})
        except ValueError:
            data.append({"role": "system", "content": f"The link {link} has no text on it."})
    return data