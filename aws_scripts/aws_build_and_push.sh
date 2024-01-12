#!/bin/bash

# Define variables
DOCKER_IMAGE_NAME="your-docker-image-name"
DOCKER_IMAGE_TAG="your-tag"
AWS_REGION="your-aws-region"
AWS_ACCOUNT_ID="your-aws-account-id"
ECR_REPOSITORY_NAME="your-ecr-repository-name"

# Step 1: Build the Docker image
docker build -t $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG .

# Step 2: Authenticate with ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Step 3: Tag the Docker image for ECR
docker tag $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:$DOCKER_IMAGE_TAG

# Step 4: Push the Docker image to ECR
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:$DOCKER_IMAGE_TAG

# Done
echo "Docker image pushed to ECR successfully."
