#!/usr/bin/env bash
set -e

PROJECT_ID=$(gcloud config get-value project)
SERVICE_NAME="aether-ops-agent"
REGION="us-central1"

echo "Building and deploying ${SERVICE_NAME} to Google Cloud Run in ${REGION}..."

gcloud run deploy ${SERVICE_NAME} \
  --source . \
  --region ${REGION} \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=production,ENFORCE_SPIFFE_AUTH=true \
  --min-instances 0 \
  --max-instances 5 \
  --memory 512Mi \
  --cpu 1

echo "Deployment complete! Fetching service URL..."
gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format 'value(status.url)'

