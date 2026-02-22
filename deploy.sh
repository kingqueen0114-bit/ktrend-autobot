#!/bin/bash
export PATH="/Users/yuiyane/google-cloud-sdk/bin:$PATH"
# K-Trend AutoBot Cloud Functions Deploy Script

set -e

# Configuration
FUNCTION_NAME="ktrend-autobot"
REGION="asia-northeast1"
RUNTIME="python311"
ENTRY_POINT="main"
MEMORY="256MB"
TIMEOUT="540s"


# Validations
REQUIRED_PROJECT="k-trend-autobot"
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)

if [ "$CURRENT_PROJECT" != "$REQUIRED_PROJECT" ]; then
    echo -e "${YELLOW}⚠️  Current project is '$CURRENT_PROJECT', but '$REQUIRED_PROJECT' is required.${NC}"
    echo -e "${YELLOW}🔄 Switching project to '$REQUIRED_PROJECT'...${NC}"
    gcloud config set project $REQUIRED_PROJECT
else
    echo -e "${GREEN}✅ Project check passed: $CURRENT_PROJECT${NC}"
fi

echo -e "${YELLOW}Deploying K-Trend AutoBot to Cloud Functions...${NC}"

# Deploy
gcloud functions deploy ${FUNCTION_NAME} \
  --gen2 \
  --region=${REGION} \
  --runtime=${RUNTIME} \
  --entry-point=${ENTRY_POINT} \
  --trigger-http \
  --allow-unauthenticated \
  --memory=512MB \
  --timeout=${TIMEOUT} \
  --env-vars-file=.env.deploy.yaml \
  --set-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest,LINE_CHANNEL_ACCESS_TOKEN=LINE_CHANNEL_ACCESS_TOKEN:latest,LINE_CHANNEL_SECRET=LINE_CHANNEL_SECRET:latest,WORDPRESS_APP_PASSWORD=WORDPRESS_APP_PASSWORD:latest" \
  --source=.

echo -e "${GREEN}Deploy complete!${NC}"
echo ""

# Get URL
FUNCTION_URL=$(gcloud functions describe ${FUNCTION_NAME} --region=${REGION} --gen2 --format='value(serviceConfig.uri)')
echo -e "${GREEN}Function URL: ${FUNCTION_URL}${NC}"
echo ""
echo "Endpoints:"
echo "  - Webhook: ${FUNCTION_URL}/webhook"
echo "  - Approve: ${FUNCTION_URL}/approve"
echo "  - Reject:  ${FUNCTION_URL}/reject"
echo "  - Draft:   ${FUNCTION_URL}/draft/{id}"
