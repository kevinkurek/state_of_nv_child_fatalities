# Load environment variables from .env file
source .env

# Deploy the image to Cloud Run
CURRENT_DATE=$(date "+%Y%m%d")
IMAGE_NAME="$GCP_PROJECT_ID-$CURRENT_DATE"
gcloud run deploy $SERVICE --image gcr.io/$GCP_PROJECT_ID/$IMAGE_NAME:$TAG --region $REGION --platform managed

# Get the URL of the Cloud Run service
URL=$(gcloud run services describe $SERVICE --region $REGION --format 'value(status.url)')

# Extract client_email from service key path
SERVICE_ACCOUNT_EMAIL=$(grep -o '"client_email": "[^"]*' $GCP_SERVICE_ACCOUNT_KEY_PATH | awk -F'"' '{print $4}')

# Create a Cloud Scheduler job that invokes the Cloud Run service
gcloud scheduler jobs create http $JOB --schedule="*/5 * * * *" --http-method=GET --uri=$URL --oidc-service-account-email=$SERVICE_ACCOUNT_EMAIL --location=$REGION
