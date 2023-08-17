#!/bin/bash

# Navigate to the directory containing main.py & .env
cd ..

# Check if .env exists
if [ ! -f .env ]; then
    echo ".env file not found!"
    exit 1
fi

# Load environment variables from .env file
source .env

# Use the environment variables in your script
gcloud config set project $GCP_PROJECT_ID
gcloud auth activate-service-account --key-file=$GCP_SERVICE_ACCOUNT_KEY_PATH

# Deploy the function using gcloud
gcloud functions deploy $FUNCTION_NAME \
--runtime python310 \
--trigger-http \
--entry-point main \
--allow-unauthenticated

# Check deployment status
if [ $? -eq 0 ]; then
    echo "Function deployed successfully!"
else
    echo "Function deployment failed!"
    exit 1
fi
