"""Class file that is reponsibnle for interacting with the NewsAPI service.
Returns:
"""
from keybert import KeyBERT
from newsapi import NewsApiClient
from nltk import TweetTokenizer
from nltk.corpus import stopwords
import string
import re

class NewsFetcher:
    """NewsFetcher object. Allows the user to interact with the NewsAPI direcly by only providing
    an API key.
    """
    def __init__(self, api_key):
        """Instantiates a NewsFetcher object. 

        Args:
            api_key (str): NewsAPI API key.
        """
        self.tokenizer = TweetTokenizer(preserve_case=False,
            strip_handles=False,
            reduce_len=True)
        self.keyword_model = KeyBERT()
        self.news_api = NewsApiClient(api_key=api_key)

    def fetch_relalted_news(self, source_tweet_text):
        """Fetches news articles from NewsAPI that are semantically related to
        the source Tweet.

        Args:
            source_tweet_text (str): The raw text of the source tweet

        Returns:
            list(dict): Returns a list of JSON objects corresponding to the rleated news articles.
        """
        cleaned_string = self.tokenizer.tokenize(source_tweet_text)
        cleaned_string = [word for word in cleaned_string if (word not in stopwords.words("english") and
                                       word not in string.punctuation)]
        cleaned_string = " ".join(cleaned_string)
        # Remove links
        cleaned_string = re.sub(r"http\S+", "", cleaned_string)
        print(cleaned_string)
        keywords = self.keyword_model.extract_keywords(cleaned_string, keyphrase_ngram_range=(1, 3), stop_words='english',
                                use_mmr=True, diversity=0.7)
        
        search_query = ' AND '.join([q[0] for q in keywords])

        news_articles = (self.news_api.get_everything(q = search_query))['articles']
        if len(news_articles) > 5:
            news_articles = news_articles[:5]
        elif len(news_articles) == 0:
            search_query = ' OR '.join([q[0] for q in keywords])
            news_articles = (self.news_api.get_everything(q = search_query))['articles']
            if len(news_articles) > 5:
                news_articles = news_articles[:5]
        return news_articles