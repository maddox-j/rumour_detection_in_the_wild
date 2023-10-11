# Rumour Detection in the Wild: A Browser Extension for Twitter
This is a repoistory containing all the materials related to the paper Rumour Detection in the Wild: A Browser Extension for Twitter accepted at NLP-OSS@EMNLP 2023. 
```
@inproceedings{
jovanovic2023rumour,
title={Rumour Detection in the Wild: A Browser Extension for Twitter},
author={Andrej Jovanovic and Bj{\"o}rn Ross},
booktitle={3rd Workshop for Natural Language Processing Open Source Software},
year={2023},
url={https://openreview.net/forum?id=9akS9IBfKs}
}
```

The project structure is the following: 
```
📦rumour_detection_in_the_wild
 ┣ 📂api_modules
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜news_fetcher.py
 ┃ ┗ 📜twitter_fetcher.py
 ┣ 📂browser_extension
 ┃ ┣ 📜128.png
 ┃ ┣ 📜background.js
 ┃ ┣ 📜bootstrap.min.js
 ┃ ┣ 📜bootstrap.min.js.map
 ┃ ┣ 📜index.html
 ┃ ┣ 📜jquery.min.js
 ┃ ┣ 📜manifest.json
 ┃ ┗ 📜script.js
 ┣ 📂inference_server
 ┃ ┣ 📂templates
 ┃ ┃ ┗ 📜index.html
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜server.py
 ┃ ┣ 📜user_study_sever.py
 ┃ ┗ 📜twitter_inference.py
 ┣ 📂rumour_detection_module
 ┃ ┣ 📂Process
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜dataset.py
 ┃ ┃ ┣ 📜getTwittergraph.py
 ┃ ┃ ┣ 📜getWeibograph.py
 ┃ ┃ ┣ 📜process.py
 ┃ ┃ ┗ 📜rand5fold.py
 ┃ ┣ 📂data
 ┃ ┣ 📂model
 ┃ ┃ ┣ 📂Twitter
 ┃ ┃ ┃ ┣ 📂model_weights
 ┃ ┃ ┃ ┣ 📜BiGCN_Twitter.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📂Weibo
 ┃ ┃ ┃ ┣ 📜BiGCN_Weibo.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂preprocessing
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜node.py
 ┃ ┃ ┗ 📜preprocess.py
 ┃ ┣ 📂scripts
 ┃ ┃ ┣ 📜data_generation_scripts.py
 ┃ ┃ ┣ 📜dataset_mixing.py
 ┃ ┃ ┗ 📜node_ablation_test.py
 ┃ ┣ 📂tools
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜earlystopping.py
 ┃ ┃ ┣ 📜earlystopping2class.py
 ┃ ┃ ┗ 📜evaluate.py
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜main.sh
 ┃ ┣ 📜readme.md
 ┃ ┗ 📜requirements.txt
 ┣ 📂testing_results
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜concept_drift_test.py
 ┣ 📜.gitignore
 ┣ 📜Dockerfile
 ┣ 📜README.md
 ┣ 📜requirements_docker.txt
 ┗ 📜requirements.txt
```

## Development
### Data
The data used throughout this project can be found at the following locations:
- https://www.dropbox.com/s/46r50ctrfa0ur1o/rumdect.zip?dl=0.
- https://www.dropbox.com/s/7ewzdrbelpmrnxu/rumdetect2017.zip?dl=0.
- https://drive.google.com/drive/u/0/folders/1pi71FGwfHvkuzSPtLCWL6iky1MCzexZx

The data should be downloaded in the `rumour_detection_module/data` subdirectory.

### Setting up
This project is set up to run effectively with the use of miniconda.

To create your conda environment, preform the following:
```
conda create --name project-thola python=3.8
```
_project-thola_ is the code name for this work.

Then, install all the the required packages:
```
pip3 install torch # We had issues installing inside of the requirements.txt.
pip3 install -r requirements.txt / make setup_project
```

In order to use all of the services, we need two API keys: one for the Twitter API and one for the NewsAPI. We specify both of these in a `.env` file in the root directory of the project as follows
```
BEARER_TOKEN = xxxxxxxxxx # This is the Twitter API key
NEWS_API_KEY = xxxxxxxxxx
```
### Rumour Detection Model
The rumour detection algorithm has been added as a submodule, which originates from the following GitHub repository: https://github.com/TianBian95/BiGCN. We created a private fork of the repository so that we could mofidy a few of the files, but all the credit goes to the original repository.

The BiGCN has its own requirements; these have been incorporated into the the requirements for our environment. Regarding the setup of the BiGCN model, the authors of the paper outline the steps necessary in `rumour_detection_module/main.sh`.

These are simplified below:

In order to train the rumour detection model:
- We have to build the graphical structure of the graph using:
```
python rumour_detection_module/Process/getTwittergraph.py <name_of_dataset>

e.g. 

python rumour_detection_module/Process/getTwittergraph.py Twitter16
```
This command assumes that you have the `<name_of_datset>` and `<name_of_datset>graph` folders in `rumour_detection_module/data`.

In order to train the model, we run the following command
```
python rumour_detection_module/model/Twitter/BiGCN_Twitter.py <name_of_dataset> <number_of_iterations> <model_weights_save>   

e.g. 

python rumour_detection_module/model/Twitter/BiGCN_Twitter.py Twitter16 1 True
```
where: 
- `name_of_dataset` - A string giving the name of the dataset that you wish to train the data on.
- `number_of_iterations` - An integer specifying the number of iterations you wish the experiments to be run for.
- `model_weights_save` - A String (True or False) indicating whether you want the model weights to be saved after training.

Saving the model weights are needed for the browser extension to function, but also to run the relevant experiments below. These are saved in the `rumour_detection_module/model/Twitter/model_weights` directory.
### Running the server
For the browser extension, we have developed a web server to house all of the functionality. In the root folder, run the following command:

```
python project_thola/inference_server/server.py
```
To test that the server works, perform the following:

```
curl -X POST http://127.0.0.1:8080/inference -d '{"tweet_id":"12323434435"}'
```
Or you can do so via the browser extension directly.

NB: The inference server in this repository can be used for any tweet. The version that was used in the user_study can be seen in the `inference_sever/user_study_server.py`
### Browser Extension
All of the files for the browser extension lie in `browser_extension`. There are two ways you can use the browser extension. You can either load the unpacked version onto Google Chrome, which is useful for development (https://developer.chrome.com/docs/extensions/mv3/getstarted/development-basics/). In order to specify which web server you wish the browser extension to communicate with, you need to specify the URL in:
- `browser_extension/manifest.json`
- `browser_extension/script.js`
- `browser_extension/background.js`

By default, this is the local host server.


Or you can use the browser extension released on the Google store: https://chrome.google.com/webstore/detail/twitter-rumour-detection/kohomgmgkeknmigmjiidanahahhlkdla?hl=en-GB&authuser=3

However, this commiucates with the web server that we had created for the rumour detection study, which limits POST requests to specific tweet IDs. The remote server may be shut down to avoid incurring costs on GCP. The link to the remote server is: https://thola-server-2abtt3ds6q-ue.a.run.app/

### Deploying the server to GCP
We use the server locally for testing, but we deploy the server to GCP to use for the user study. However, this can be useful more generally.

For this, we need to create a Docker image of the server and the rumour detection algorithm. We have prespecified the `Dockerfile` that we need for this.

NB: The cache of the sentence-transformers has not been included in the repository due to size constraints. You would need to copy this from your own HuggingFace cache.

NB: This asssumes that you have knowledge of how Docker works, and that you have the necessary prerequisites installed. If you are uncomfortable with this, visit the Docker docs for assistance: https://docs.docker.com/. Furthermore, you need to have a GCP account with a project created. Follow this tutorial as an example: https://medium.com/fullstackai/how-to-deploy-a-simple-flask-app-on-cloud-run-with-cloud-endpoint-e10088170eb7

The Docker file has been configured to work with a subset of the dependencies in the project (`requirements_docker.txt`)

To create the Docker image (This is done because there are issues with M1 Macs creating Docker images that are incompatible with cloud run. ):
```
docker buildx build --platform linux/amd64 -t gcr.io/project-thola/tholaserver:v1 .
```

The same tutorial mentioned above shows how one would upload the Docker image to cloud run: https://medium.com/fullstackai/how-to-deploy-a-simple-flask-app-on-cloud-run-with-cloud-endpoint-e10088170eb7

### Running Experiments
During the project, we ran a number of experiments. The relevant data generation scripts are included in `rumour_detection_module/scripts`. Additional experiment scripts are in `testing_results`.

#### Out-of-Distribution Data Experiments
To run the mixing experiments, we make use of the script in `testing_results/concept_drift_test.py`

An example experiment can be ran using the following command:
```
python testing_results/concept_drift_test.py --weights_name <name_of_weights> --dataset_name <name_of_dataset>
e.g 
python testing_results/concept_drift_test.py --weights_name Twitter15 --dataset_name Twitter16
```
where:
- `<name_of_weights>` is the name of the pretrained model.
- `<name_of_dataset>` is the name of dataset on which we wish to evaluate the pretrained model.

In order to generate the TwitterMix dataset, we make use of the `rumour_detection_module/scripts/dataset_mixing.py`. To generate a TwitterMix dataset, the following command is to be used:
```
python rumour_detection_module/scripts/dataset_mixing.py --mix_amount_15 <mix_amount_15> --mix_amount_16 <mix_amount_16>

e.g. 

python rumour_detection_module/scripts/dataset_mixing.py --mix_amount_15 0.5 --mix_amount_16 0.5
```
#### Text Ablation Experiment
For this experiment, we need to create the text ablation datasets. To do so, we make use of the `rumour_detection_module/scripts/data_generation_scripts.py`.

To generate a dataset, we make use of the following command:
```
python rumour_detection_module/scripts/data_generation_scripts.py --dataset_name <name_of_dataset> --drop_amount <drop_amount> --type text

e.g.

python rumour_detection_module/scripts/data_generation_scripts.py --dataset_name Twitter16 --drop_amount 0.5 --type text
```

where:
- `<name_of_dataset>` is the name of dataset on which we wish to ablate.
- `<drop_amount>` is the amount of ablation to be used.

We then use the training command for this newly created dataset as above.
#### Node Ablation Experiment
For this experiment, we need to create the node ablation datasets. To do so, we make use of the `rumour_detection_module/scripts/data_generation_scripts.py`.

To generate a dataset, we make use of the following command:
```
python rumour_detection_module/scripts/data_generation_scripts.py --dataset_name <name_of_dataset> --drop_amount <drop_amount> --type node

e.g.

python rumour_detection_module/scripts/data_generation_scripts.py --dataset_name Twitter16 --drop_amount 0.5 --type node
```

where:
- `<name_of_dataset>` is the name of dataset on which we wish to ablate.
- `<drop_amount>` is the amount of ablation to be used.

We then use the training command for this newly created dataset as above.