# Use Python38
FROM python:3.8

USER 0

# Copy requirements.txt to the docker image and install packages
COPY requirements_docker.txt /

# Load resources
COPY .env .env
COPY api_modules/ api_modules/
COPY inference_server/ inference_server/
COPY rumour_detection_module/ rumour_detection_module/
RUN mkdir -p /root/.cache/torch/sentence_transformers/sentence-transformers_all-MiniLM-L6-v2/
# Load model cache to speed up server boot.
COPY sentence-transformers_all-MiniLM-L6-v2 /root/.cache/torch/sentence_transformers/sentence-transformers_all-MiniLM-L6-v2/
# Install torch seperately due to issues in requirements.txt install.
RUN pip install torch
RUN pip install -r requirements_docker.txt

EXPOSE 8080
ENV PORT 8080
# Use gunicorn as the entrypoint 
CMD exec gunicorn --bind :$PORT inference_server.server:app --workers 1 --threads 1 --timeout 60