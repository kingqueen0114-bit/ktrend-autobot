#!/bin/bash
# Deploy updated server.js to GCP

set -e

GCP_PROJECT="k-trend-autobot"
GCP_ZONE="asia-northeast1-a"
GCP_INSTANCE="ktrend-server"
REMOTE_PATH="/home/yuiyane/ktrend-autobot/line-claude-bridge"

echo "📤 Deploying updated server.js to GCP..."
echo ""

# Upload server.js to GCP
echo "1. Uploading server.js..."
gcloud compute scp server.js ${GCP_INSTANCE}:${REMOTE_PATH}/server.js \
  --zone=${GCP_ZONE} \
  --project=${GCP_PROJECT}

echo ""
echo "2. Restarting Node.js server..."
gcloud compute ssh ${GCP_INSTANCE} \
  --zone=${GCP_ZONE} \
  --project=${GCP_PROJECT} \
  --command="cd ${REMOTE_PATH} && pm2 restart server || (pkill -f 'node.*server.js' && nohup node server.js > server.log 2>&1 &)"

echo ""
echo "✅ Deploy complete!"
echo ""
echo "🔗 Server URL: http://34.146.62.216:8080"
echo ""
echo "Test the editing screen:"
echo "  - Visit: http://34.146.62.216:8080/drafts"
echo "  - Edit a draft"
echo "  - You should see the new '画像クレジット' field below the image upload"
echo ""
