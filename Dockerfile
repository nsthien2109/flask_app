# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

FROM nvidia/cuda:11.1-base

# Install additional CUDA Toolkit components
RUN apt-get update && apt-get install -y \
    cuda-libraries-11-1 \
    cuda-nvtx-11-1 \
    cuda-command-line-tools-11-1

# Set LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app