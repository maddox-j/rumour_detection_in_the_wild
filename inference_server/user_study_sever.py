import sys
import os
sys.path.append(os.getcwd())
from inference_server.twitter_inference import perform_inference
from flask import Flask, request, jsonify, render_template
import logging


app = Flask(__name__)

LABELS = {
    0: "Non-rumour",
    1: "False",
    2: "True",
    3: "Unverified",
    -1: "Error",
}

ACCEPTED_TWEET_IDS = [
    "1627718879525863437",
    "1627875644989181952",
    "1625809122326196225",
    "1624445694646923271",
    "1624446398904127491",
    "1621161107321675777",
]

logging.basicConfig(level=logging.DEBUG,
                    format='[%(filename)s:%(lineno)d] - %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.route("/")
def welcome_to_server():
    return render_template("index.html")

@app.route('/inference', methods=['POST'])
def predict():
    # Get the data from the POST request.
    # Make prediction using model loaded from disk as per the data.
    logger.info("Preforming inference")
    data = request.get_json(force=True)
    # Ensure that a certain subset of tweets are allowed.``
    if data["tweet_id"] not in ACCEPTED_TWEET_IDS:
        return jsonify({'classification': LABELS[-1], 'news': []})
    else: 
        tweet_id = data["tweet_id"]
        # tweet_id = "1616011667116023808"
        response, news = perform_inference(tweet_id)
        return jsonify({'classification': LABELS[response], 'news': news})

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)), debug=True, threaded=True)