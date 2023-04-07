import sys
import os
sys.path.append(os.getcwd())
from inference_server.twitter_inference import perform_inference
from flask import Flask, request, jsonify, render_template
import logging
import time

app = Flask(__name__)

LABELS = {
    0: "Non-rumour",
    1: "False",
    2: "True",
    3: "Unverified",
    -1: "Error",
}

logging.basicConfig(level=logging.DEBUG,
                    format='[%(filename)s:%(lineno)d] - %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

INFERENCE_TIME_FILE = os.path.join(os.path.abspath(""),"testing_results", "extension_latency.txt")

@app.route("/")
def welcome_to_server():
    """Generate the welcome page, and the privacy policy of the browser extension
    """
    return render_template("index.html")

@app.route('/inference', methods=['POST'])
def predict():
    """Perform rumour detection

    Returns:
        json: The rumour classification label, and the semantically-related news articles
        as a JSON object.
    """
    # Get the data from the POST request.
    # Make prediction using model loaded from disk as per the data.
    start_time = time.time()
    logger.info("Preforming inference")
    data = request.get_json(force=True)
    tweet_id = data["tweet_id"]
    response, news = perform_inference(tweet_id)
    total_time = time.time() - start_time
    with open(INFERENCE_TIME_FILE, mode = "a") as f:
        f.write(str(total_time) + ",\n")
    logger.info(f"Total time takenL {total_time}")
    return jsonify({'classification': LABELS[response], 'news': news})

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)), debug=True, threaded=True)
