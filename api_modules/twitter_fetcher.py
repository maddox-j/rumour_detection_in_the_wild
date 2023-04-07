"""Class that encapsulates interaction with the Twitter API.
"""
import sys,os
sys.path.append(os.getcwd())
import requests
import logging
from rumour_detection_module.preprocessing.node import Node

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(filename)s:%(lineno)d] - %(asctime)s - %(levelname)s - %(message)s')


class TwitterFetcher():
    """Object that facilitates interaction with the Twitter API.
    """
    def __init__(self, bearer_token):
        """Instantiates a TwitterFetcher object

        Args:
            bearer_token (str): TwitterAPI key.
        """
        self.bearer_token = bearer_token

    def fetch_tweet_by_id(self, tweet_id):
        """Fetch a given tweet from the Twitter API according to its Tweet ID.

        Args:
            tweet_id (str): The ID of tthe tweet that we wish to retrieve.
        Returns:
            Node: A Node object representing the tweet.
        """
        url = self.__create_url([tweet_id])
        json_response = self.__connect_to_endpoint(url)
        if json_response == -1:
            return "Error"
        if "data" in json_response:
            tweet = json_response["data"][0]
            root_tweet = Node(uid = "ROOT", tweet_id = "ROOT", parent = None)
            tweet = Node(uid = tweet["author_id"], tweet_id = tweet["id"], text = tweet["text"],
                        time_delay = 0.0, root = True, created_at = tweet["created_at"], parent = root_tweet)
            return tweet
        else:
            return None
    
    def fetch_replies_for_tweet(self,tweet_id, until_id):
        """Fetches the replies related to a particular tweet ID older that a specified tweet ID.

        Args:
            tweet_id (str): The tweet ID of the tweet for which we wish to find replies.
            until_id (str): A tweet ID that specifies the "newest" tweet chronologically. These
            provides a limit for the API to return tweets that are older than the until_id.

        Returns:
            list: A list of replies represented in JSON format.
        """
        url = self.__create_replies_tweet_url(tweet_id, until_id)
        json_response = self.__connect_to_endpoint(url)
        if json_response == -1:
            return "Error"
        if json_response["meta"]["result_count"] > 0:
            return json_response["data"]
        else:
            return []
    
    def fetch_quote_tweets_for_tweet(self, tweet_id, next_token):
        """Fetches the quote tweets and retweets related to a particular tweet ID older that a specified tweet ID.

        Args:
            tweet_id (str): The tweet ID of the tweet for which we wish to find quote tweets and retweets.
            next_token (str): A token that specifies the next "page" of results. This allows our TwitterFetcher
            to cycle through results returned from the Twitter API.

        Returns:
            list: A list of tweets represented in JSON format.
        """
        url = self.__create_quote_tweet_url(tweet_id, next_token)
        json_response = self.__connect_to_endpoint(url)
        if json_response == -1:
            return "Error", []
        if json_response["meta"]["result_count"] > 0:
            # We want to map that the quote tweets are related to the original Tweet they quoted.
            for response in json_response["data"]:
                if response["conversation_id"] != tweet_id:
                    response["conversation_id"] = tweet_id
            if "next_token" in json_response["meta"]:
                next_token = json_response["meta"]["next_token"]
            else:
                next_token = []
            return json_response["data"], next_token
        else:
            return [], []

    def __create_url(self, tweet_ids):
        """Generate the Tweet search URL.

        Args:
            tweet_ids (str): Tweet IDs to be searched
        Returns:
            str: String representing the tweet search url.
        """
        tweet_id_string = ",".join(tweet_ids)  
        ids = f"ids={tweet_id_string}"
        url = "https://api.twitter.com/2/tweets?{}".format(
            ids)
        return url

    def __create_replies_tweet_url(self, conversation_id, until_id):
        """Generate the Tweet reply search URL.

        Args:
            tweet_ids (str): Tweet ID to be searched
            until_id (str): Tweet ID of the newest tweet chronologically.
        Returns:
            str: String representing the tweet reply search url.
        """
        if until_id:
            conversation_id = f"conversation_id:{conversation_id}&until_id={until_id}"
        else:
            conversation_id = f"conversation_id:{conversation_id}"
        url = f"https://api.twitter.com/2/tweets/search/recent?query={conversation_id}&max_results=100"
        return url

    def __create_quote_tweet_url(self, tweet_id, next_token):
        """Generate the Tweet quote search URL.

        Args:
            tweet_ids (str): Tweet ID to be searched
            next_token (str): Unique token corresponding to the text page of results.
        Returns:
            str: String representing the tweet reply search url.
        """
        if next_token:
            url = f"https://api.twitter.com/2/tweets/{tweet_id}/quote_tweets?max_results=100&pagination_token={next_token}"
        else: 
            url = f"https://api.twitter.com/2/tweets/{tweet_id}/quote_tweets?max_results=100"
        return url

    
    def __bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """
        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2TweetLookupPython"
        return r

    def __connect_to_endpoint(self, url):
        """Connect the client to the specified Twitter API endpoint

        Args:
            url (str): A URL representing the request to the TwitterAPI server.

        Returns:
            json: Response from the server
        """
        tweet_fields = "tweet.fields=in_reply_to_user_id,author_id,created_at,conversation_id" 
        response = requests.request("GET", url, auth=self.__bearer_oauth, params=tweet_fields)
        logger.info(f"The response status code is {response.status_code}")
        if response.status_code != 200:
            logger.error("Request returned an error: {} {}".format(response.status_code, response.text))
            return -1
        else:
            return response.json()
