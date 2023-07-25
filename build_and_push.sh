#!/bin/bash

# Load environment variables from .env file
source .env

# Use the environment variables in your script
gcloud config set project $GCP_PROJECT_ID
gcloud auth activate-service-account --key-file=$GCP_SERVICE_ACCOUNT_KEY_PATH

# Get the current date in the format "YYYYMMDD"
CURRENT_DATE=$(date "+%Y%m%d")

# Concatenate GCP_PROJECT_ID and DATE to form IMAGE_NAME
IMAGE_NAME="$GCP_PROJECT_ID-$CURRENT_DATE"

# Build the Docker image
docker build -t gcr.io/$GCP_PROJECT_ID/$IMAGE_NAME:$TAG .

# Authenticate Docker to GCR
gcloud auth configure-docker

# Push the Docker image to Google Container Registry
docker push gcr.io/$GCP_PROJECT_ID/$IMAGE_NAME:$TAG
