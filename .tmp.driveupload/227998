#!/bin/bash
export PATH="/Users/yuiyane/google-cloud-sdk/bin:$PATH"
set -e

echo "Deploying ktrend-line-webhook..."

gcloud functions deploy ktrend-line-webhook \
  --gen2 \
  --runtime=python311 \
  --region=asia-northeast1 \
  --source=. \
  --entry-point=handle_line_webhook \
  --trigger-http \
  --allow-unauthenticated \
  --env-vars-file=.env.deploy.yaml \
  --set-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest,LINE_CHANNEL_ACCESS_TOKEN=LINE_CHANNEL_ACCESS_TOKEN:latest,LINE_CHANNEL_SECRET=LINE_CHANNEL_SECRET:latest,WORDPRESS_APP_PASSWORD=WORDPRESS_APP_PASSWORD:latest" \
  --timeout=540s \
  --memory=512MB

echo "ktrend-line-webhook deployed successfully!"
