import os
os.system("pip install unidecode")
os.system("pip install enelvo")
os.system("pip install emoji")
os.system("python -m spacy download pt_core_news_lg")

import re
import spacy
import emoji
from unidecode import unidecode
from enelvo import normaliser

class TweetPreprocessor:
    def __init__(self):
        self.norm = normaliser.Normaliser()
        self.nlp = spacy.load("pt_core_news_lg")

    def normalize_emoji(self, tweet):
        return emoji.demojize(tweet, language="pt")

    def normalize_accentuation(self, tweet):
        return unidecode(tweet)

    def remove_noises(self, tweet):
        tweet = re.sub(r"\brt\b|\bretweet\b", '', tweet, flags=re.IGNORECASE)
        tweet = re.sub(r"@[A-Za-z0-9_]+", ' ', tweet)
        tweet = re.sub(r'#\w+', '', tweet)
        tweet = re.sub(r'https?://\S+', '', tweet)
        tweet = re.sub(r"[^a-zA-Z.!?]", ' ', tweet)
        tweet = re.sub(r'([!?.])\1+', r'\1', tweet)
        tweet = re.sub(r" +", ' ', tweet)
        tweet = tweet.strip()
        return tweet

    def normalize_tweet(self, tweet):
        return self.norm.normalise(tweet)

    def relevant_text(self, tweet):
        doc = self.nlp(tweet)
        relevant_tokens = [token for token in doc if token.pos_ in {"NOUN", "ADJ", "INTJ", "VERB"}]
        if len(relevant_tokens) >= 5:
            return tweet
        return None
    
    def process_tweet(self, tweet):
        tweet = self.normalize_emoji(tweet)
        tweet = self.normalize_accentuation(tweet)
        tweet = self.remove_noises(tweet)
        tweet = self.normalize_tweet(tweet)
        tweet = self.relevant_text(tweet)
        return tweet
