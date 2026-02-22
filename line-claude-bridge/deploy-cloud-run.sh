#!/bin/bash
# Deploy line-claude-bridge to Cloud Run

set -e

PROJECT_ID="k-trend-autobot"
SERVICE_NAME="line-claude-bridge"
REGION="asia-northeast1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "📦 Cloud Runへのデプロイを開始します..."
echo ""

# gcloudのパス設定
export PATH="/Users/yuiyane/line-calendar-bot/google-cloud-sdk/bin:$PATH"

# 1. Dockerイメージをビルド
echo "1️⃣ Dockerイメージをビルド中..."
gcloud builds submit --tag ${IMAGE_NAME} --project=${PROJECT_ID}

echo ""
echo "2️⃣ Cloud Runにデプロイ中..."

# 2. Cloud Runにデプロイ
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --project ${PROJECT_ID}

echo ""
echo "✅ デプロイ完了！"
echo ""

# サービスURLを取得
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
  --platform managed \
  --region ${REGION} \
  --project ${PROJECT_ID} \
  --format 'value(status.url)')

echo "🔗 サービスURL: ${SERVICE_URL}"
echo ""
echo "📋 エンドポイント:"
echo "  - 未公開記事一覧: ${SERVICE_URL}/drafts"
echo "  - 記事編集: ${SERVICE_URL}/edit/{draft_id}"
echo "  - プレビュー: ${SERVICE_URL}/draft/{draft_id}"
echo "  - Webhook: ${SERVICE_URL}/webhook"
echo ""
echo "💡 次のステップ:"
echo "  1. LINE Messaging APIのWebhook URLを更新してください"
echo "  2. ${SERVICE_URL}/drafts にアクセスして動作確認"
echo ""
