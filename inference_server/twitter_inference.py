""" File governing the rumour detection pipleine for the browser extension.
"""
import sys,os
sys.path.append(os.getcwd())
import torch
from torch_geometric.data import DataLoader
from rumour_detection_module.model.Twitter.BiGCN_Twitter import Net
import torch.nn.functional as F
import logging
from api_modules.twitter_fetcher import TwitterFetcher
from api_modules.news_fetcher import NewsFetcher
from rumour_detection_module.Process.rand5fold import *
from rumour_detection_module.Process.process import *
from rumour_detection_module.Process.getTwittergraph import create_inference_data_representation
from rumour_detection_module.preprocessing.node import Node
from dotenv import load_dotenv
from tqdm import tqdm
from pathlib import Path
from datetime import datetime
from nltk import TweetTokenizer
import json

# Specifies the pretrained model file path
MODEL_CHECKPOINT_PATH = os.path.join(Path(
    os.path.abspath(__file__)).parent.parent,"rumour_detection_module","model","Twitter","model_weights", "Twitter16_0")

# Specifies data storage location so that data may be cached for later use.
DATA_PATH = os.path.join(
    Path(os.path.abspath(__file__)).parent.parent,"rumour_detection_module","data")

DATA_FOLDER_NAME = "inference_data"

LABELS = {
    0: "Non-rumour",
    1: "False",
    2: "True",
    3: "Unverified",
}

logging.basicConfig(level=logging.DEBUG,
                    format='[%(filename)s:%(lineno)d] - %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv(dotenv_path=os.path.join(
    (Path(os.path.dirname(__file__)).parent.parent), ".env"))

tweet_fetcher = TwitterFetcher(os.getenv("BEARER_TOKEN"))
news_fetcher = NewsFetcher(os.getenv("NEWS_API_KEY"))

def perform_inference(tweet_id):
    """Perform rumour detection for a given Tweet ID

    Args:
        tweet_id (str): The Tweet ID for which we wish to perform rumour detection.
    Returns:
        The rumour classification instance and the related news articles 
    """
    logger.info("Checking cache for Tweet.")
    logger.info("Fetching source Tweet text.")
    tweet = tweet_fetcher.fetch_tweet_by_id(tweet_id)
    if not isinstance(tweet, Node):
        return -1, []
    if os.path.exists(os.path.join(DATA_PATH, DATA_FOLDER_NAME,tweet_id+".txt")):
        logger.info("Tweet has been processed before. Do not fetch.")
    else:
        if not tweet:
            logger.info("Source tweet not found.")
            return -1, []
        logger.info("Source tweet found.")
        logger.info("Fetching replies")
        tweet_cascade = fetch_tweets_for_cascade(tweet)
        if not tweet_cascade:
            logger.info("Could not retrieve the relevant data")
            return -1, []
        create_tweet_cascade(tweet, tweet_cascade)
        create_inference_data_representation(tweet.tweet_id)

    logger.info("Loading latest model weights")
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = Net(5000, 64, 64).to(device)
    model.load_state_dict(torch.load(MODEL_CHECKPOINT_PATH))
    model.eval()
    logger.info("Loaded ")
    logger.info("Attempting to preform inference.")
    logger.info("Checking if file exists")
    if not(os.path.exists(os.path.join(DATA_PATH,DATA_FOLDER_NAME+"_graph",tweet_id + ".npz"))):
        return -1, []
    logger.info("Loaded npz file")
    inference_data = load_inference_example(tweet_id)
    logger.info("File found")
    data_loader = DataLoader(
        inference_data, shuffle=True, num_workers=0)
    tqdm_test_loader = tqdm(data_loader)
    temp_val_losses = []

    for Batch_data in tqdm_test_loader:
        logger.info(f"Correct label is: {LABELS[Batch_data.y.item()]}")
        Batch_data.to(device)
        val_out = model(Batch_data)
        val_loss = F.nll_loss(val_out, Batch_data.y)
        temp_val_losses.append(val_loss.item())
        _, val_pred = val_out.max(dim=1)
        logger.info(f"The predicted label is: {LABELS[val_pred.item()]}")

    prediction = val_pred.item()
    logger.info("Classified tweet")
    logger.info("Fetching news articles.")
    news_articles = news_fetcher.fetch_relalted_news(tweet.text)
    return prediction, news_articles

def get_all_replies(tweet_id):
    """Retrieve all the replies related to a given Tweet ID.

    Args:
        tweet_id (str): Tweet ID

    Returns:
        list: A list representing all the replies as JSON objects.
    """
    all_replies = []
    replies_content = tweet_fetcher.fetch_replies_for_tweet(tweet_id, until_id=[])
    if replies_content == "Error" or not replies_content:
        return []
    # First set of replies:
    replies_content = sorted(replies_content, key=lambda x: datetime.strptime(x["created_at"] ,"%Y-%m-%dT%H:%M:%S.%fZ"))
    all_replies.extend(replies_content)
    oldest_id = replies_content[0]["id"]
    while replies_content:
        replies_content = tweet_fetcher.fetch_replies_for_tweet(tweet_id, oldest_id)
        if replies_content and replies_content != "Error":
            replies_content = sorted(replies_content, key=lambda x: datetime.strptime(x["created_at"] ,"%Y-%m-%dT%H:%M:%S.%fZ"))
            all_replies.extend(replies_content)
            oldest_id = replies_content[0]["id"]
        elif replies_content == "Error":
            logger.info("Preforming under-represented inference.")
            replies_content = []
    return all_replies

def get_all_quote_tweets(tweet_id):
    """Retrieve all the quotes and retweets related to a given Tweet ID.

    Args:
        tweet_id (str): Tweet ID

    Returns:
        list: A list representing all the retweets and quote tweets as JSON objects.
    """
    all_quote_tweets = []
    quote_content, next_token = tweet_fetcher.fetch_quote_tweets_for_tweet(tweet_id, next_token = [])
    if quote_content == "Error":
        return []
    quote_content = sorted(quote_content, key=lambda x: datetime.strptime(x["created_at"] ,"%Y-%m-%dT%H:%M:%S.%fZ"))
    all_quote_tweets.extend(quote_content)
    while next_token:
        quote_content, next_token = tweet_fetcher.fetch_quote_tweets_for_tweet(tweet_id, next_token = next_token)
        if quote_content and next_token:
            quote_content = sorted(quote_content, key=lambda x: datetime.strptime(x["created_at"] ,"%Y-%m-%dT%H:%M:%S.%fZ"))
            all_quote_tweets.extend(quote_content)
        elif quote_content == "Error":
            logger.info("Preforming under-represented inference.")
    return all_quote_tweets

def fetch_tweets_for_cascade(root_tweet):
    """Generate the tweet cascade for a tweet.

    Args:
        root_tweet (Node): Node object representing the root tweet in the cascade.

    Returns:
        list: List containing all the tweets, represented as JSON objects, in a cascade
    """
    logger.info(f"The root tweet id is: {root_tweet.tweet_id}")
    # Retrieve the replies in the cascade. Twitter API is able to fetch all information.
    all_replies = get_all_replies(root_tweet.tweet_id)
    if not all_replies:
        logger.info("Unable to fetch replies")
        return []
    logger.info(f"There are {len(all_replies)} replies in the cascade.")
    logger.info("Begin finding quote tweets.")
    all_quote_tweets = get_all_quote_tweets(root_tweet.tweet_id)
    if not all_replies:
        logger.info("Unable to fetch quote tweets")
        return []
    logger.info(f"There are {len(all_quote_tweets)} quote tweets in the cascade.")
    return all_replies + all_quote_tweets


def load_inference_example(tweet_id):
    """Load the precomputed graph for the given tweet_id

    Args:
        tweet_id (str): Tweet ID

    Returns:
        BiGraphDataset: BiGraph representing the tweet.
    """
    treeDic = load_single_tree(tweet_id)
    fold_x = [tweet_id]
    testdata_list = BiGraphDataset(
        fold_x, treeDic, data_path=os.path.join(DATA_PATH, DATA_FOLDER_NAME+"_graph"))
    return testdata_list


def load_single_tree(tweet_id):
    """Load in the tree structure for the given tweet ID.

    Args:
        tweet_id (str): Tweet ID.
    Returns:
        dict: The tree representing the given tweet ID.
    """
    treePath = os.path.join(DATA_PATH, DATA_FOLDER_NAME,tweet_id+".txt")
    print("reading twitter tree")
    treeDic = {}
    for line in open(treePath):
        line = line.rstrip()
        eid, indexP, indexC = line.split('\t')[0], line.split('\t')[
            1], int(line.split('\t')[2])
        if tweet_id == eid: 
            max_degree, maxL, Vec = int(line.split('\t')[3]), int(
                line.split('\t')[4]), line.split('\t')[5]
            if not treeDic.__contains__(eid):
                treeDic[eid] = {}
            treeDic[eid][indexC] = {
                'parent': indexP, 'max_degree': max_degree, 'maxL': maxL, 'vec': Vec}
    print('tree no:', len(treeDic))
    return treeDic

def tokenizer_tweet_dataset():
    """Method used to preload dict of 5000 most common tokens for preprocessing pipeline.
    """
    with open(os.path.join(os.path.join(DATA_PATH, "twitter16_helper", "dict.json")), mode="r", encoding="utf-8") as f:
        test_dict = json.load(f)
    return test_dict

def generate_local_dict_repr(tokenized_text, word_dict):
    """Generate the index:count representation for a tweet.

    Args:
        tokenized_text (list): A list of tokens in the tokenized text of a tweet
        word_dict (dict): Precomputed word dictionary.
    Returns:
        str: String representation of the index:count textual encoding.
    """
    local_dict = {}
    for token in tokenized_text:
        if token in word_dict:
            if word_dict[token] not in local_dict:
                local_dict[word_dict[token]] = 1 
            else:
                local_dict[word_dict[token]] += 1 
    dict_repr = str(local_dict).replace(" ","").replace("{","").replace("}","").replace(","," ")
    return dict_repr

def create_tweet_cascade(root_tweet, tweets_in_cascade):
    """Generate the full tweet cascade for a given root tweet, and write to an external file.

    Args:
        root_tweet (Node): Node object representing the root tweet in the cascade.
        tweets_in_cascade (list): List containing all the tweets, represented as JSON objects, in a cascade
    """
    word_dict = tokenizer_tweet_dataset()
    tokenizer = TweetTokenizer(
        preserve_case=False,
        strip_handles=False,
        reduce_len=True)
    node_list = [root_tweet]
    root_tweet.dict_repr = generate_local_dict_repr(tokenizer.tokenize(root_tweet.text + " <end>"), word_dict)
    # Order the tweets chronologically.
    tweets_in_cascade = sorted(tweets_in_cascade, key=lambda x: datetime.strptime(x["created_at"] ,"%Y-%m-%dT%H:%M:%S.%fZ"))
    parents_set = set()
    
    max_length = 0
    for reply in tweets_in_cascade:
        new_datetime = datetime.strptime(reply["created_at"] ,"%Y-%m-%dT%H:%M:%S.%fZ")
        # Assume that parent is already in list -> This would necessarily happen chronologically.
        if "in_reply_to_user_id" in reply:
            key = "in_reply_to_user_id"
        else:
            key = "conversation_id"
        potential_parent = [tweet for tweet in node_list if tweet.uid == reply[key]]
        if potential_parent:
            parent = potential_parent[0]
        else:
            parent = None
        parents_set.add(parent.tweet_id if parent is not None else root_tweet.tweet_id)
        delta = (new_datetime - root_tweet.created_at).total_seconds()/60.0
        tokenized_text = tokenizer.tokenize(reply["text"] + " <end>")
        if (len(tokenized_text)) > max_length:
            max_length = len(tokenized_text)
        dict_repr = generate_local_dict_repr(tokenized_text, word_dict)
        node = Node(tweet_id = reply["id"], text=reply["text"],uid=reply["author_id"], created_at = reply["created_at"], 
                    time_delay = delta, parent = parent, tokenized_text = tokenized_text, dict_repr = dict_repr)
        node_list.append(node)

    # If we are able to preserve the root tweet.
    if node_list[0].root: 
        indexed_nodes = dict(enumerate(node_list))
        indexed_nodes = {v: k for k, v in indexed_nodes.items()}
        local_tweet_id = node_list[0].tweet_id
        total_parents =  len(parents_set)
        for tweet in node_list:
            parent = None
            if tweet.parent in indexed_nodes:
                parent = indexed_nodes[tweet.parent] + 1
            idx = indexed_nodes[tweet] + 1            
            node_string = local_tweet_id + "\t" + str(parent) + "\t" + str(idx)  + "\t" + \
                str(total_parents) + "\t" + str(max_length) + "\t" + str(tweet.dict_repr) + "\n"
            f = open(os.path.join(DATA_PATH, "inference_data", local_tweet_id+ ".txt"), "a", encoding="utf-8")
            f.write(node_string)
            f.close()
            
if __name__ == "__main__":
    datasetname = sys.argv[1]  # "Twitter15"、"Twitter16"
    tweet_id = input("Please provide the Tweet ID that you wish you classify:")
    perform_inference(datasetname, tweet_id)
