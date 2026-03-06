#!/bin/bash
# K-TREND TIMES Analytics Reporter - Cloud Functions デプロイスクリプト

set -e

# 色付き出力
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# プロジェクト設定
PROJECT_ID="k-trend-autobot"
REGION="asia-northeast1"
FUNCTIONS_DIR="functions/analytics-reporter"
SERVICE_ACCOUNT_KEY="k-trend-autobot-335cff2a54ef.json"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📊 K-TREND TIMES Analytics Reporter${NC}"
echo -e "${BLUE}   Cloud Functions デプロイ${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# gcloud コマンドのパス設定
GCLOUD="/Users/yuiyane/line-calendar-bot/google-cloud-sdk/bin/gcloud"

if [ ! -f "$GCLOUD" ]; then
    echo -e "${RED}❌ エラー: gcloud コマンドが見つかりません${NC}"
    echo "Google Cloud SDK をインストールしてください:"
    echo "https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# プロジェクト設定
echo -e "${GREEN}📋 プロジェクト設定中...${NC}"
$GCLOUD config set project $PROJECT_ID

# サービスアカウントキーをfunctionsディレクトリにコピー
echo -e "${GREEN}🔑 サービスアカウントキーをコピー中...${NC}"
cp "/Users/yuiyane/K-Trend-AutoBot/$SERVICE_ACCOUNT_KEY" "$FUNCTIONS_DIR/service-account-key.json"

# Cloud Functions API を有効化
echo -e "${GREEN}🔧 必要なAPIを有効化中...${NC}"
$GCLOUD services enable cloudfunctions.googleapis.com \
    cloudscheduler.googleapis.com \
    analyticsdata.googleapis.com \
    --project=$PROJECT_ID

# 日次レポート関数をデプロイ
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📅 日次レポート関数をデプロイ中...${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

$GCLOUD functions deploy ktrend-analytics-daily \
    --gen2 \
    --runtime=python312 \
    --region=$REGION \
    --source=$FUNCTIONS_DIR \
    --entry-point=daily_report \
    --trigger-http \
    --allow-unauthenticated \
    --env-vars-file=$FUNCTIONS_DIR/.env.yaml \
    --memory=512MB \
    --timeout=300s \
    --project=$PROJECT_ID

# 週次レポート関数をデプロイ
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📊 週次レポート関数をデプロイ中...${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

$GCLOUD functions deploy ktrend-analytics-weekly \
    --gen2 \
    --runtime=python312 \
    --region=$REGION \
    --source=$FUNCTIONS_DIR \
    --entry-point=weekly_report \
    --trigger-http \
    --allow-unauthenticated \
    --env-vars-file=$FUNCTIONS_DIR/.env.yaml \
    --memory=512MB \
    --timeout=300s \
    --project=$PROJECT_ID

# 月次レポート関数をデプロイ
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📈 月次レポート関数をデプロイ中...${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

$GCLOUD functions deploy ktrend-analytics-monthly \
    --gen2 \
    --runtime=python312 \
    --region=$REGION \
    --source=$FUNCTIONS_DIR \
    --entry-point=monthly_report \
    --trigger-http \
    --allow-unauthenticated \
    --env-vars-file=$FUNCTIONS_DIR/.env.yaml \
    --memory=512MB \
    --timeout=300s \
    --project=$PROJECT_ID

# Cloud Scheduler ジョブ作成
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}⏰ Cloud Scheduler ジョブを作成中...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 関数URLを取得
DAILY_URL=$($GCLOUD functions describe ktrend-analytics-daily --gen2 --region=$REGION --project=$PROJECT_ID --format="value(serviceConfig.uri)")
WEEKLY_URL=$($GCLOUD functions describe ktrend-analytics-weekly --gen2 --region=$REGION --project=$PROJECT_ID --format="value(serviceConfig.uri)")
MONTHLY_URL=$($GCLOUD functions describe ktrend-analytics-monthly --gen2 --region=$REGION --project=$PROJECT_ID --format="value(serviceConfig.uri)")

echo -e "${GREEN}✅ 関数URL取得完了${NC}"
echo "  日次: $DAILY_URL"
echo "  週次: $WEEKLY_URL"
echo "  月次: $MONTHLY_URL"
echo ""

# 日次レポート - 毎日午前9時
echo -e "${GREEN}📅 日次レポートスケジュール設定中...${NC}"
$GCLOUD scheduler jobs create http ktrend-analytics-daily-schedule \
    --location=$REGION \
    --schedule="0 9 * * *" \
    --uri="$DAILY_URL" \
    --http-method=POST \
    --time-zone="Asia/Tokyo" \
    --project=$PROJECT_ID \
    --description="K-TREND TIMES 日次アナリティクスレポート" \
    || echo "  (既に存在する場合はスキップ)"

# 週次レポート - 毎週月曜日午前10時
echo -e "${GREEN}📊 週次レポートスケジュール設定中...${NC}"
$GCLOUD scheduler jobs create http ktrend-analytics-weekly-schedule \
    --location=$REGION \
    --schedule="0 10 * * 1" \
    --uri="$WEEKLY_URL" \
    --http-method=POST \
    --time-zone="Asia/Tokyo" \
    --project=$PROJECT_ID \
    --description="K-TREND TIMES 週次アナリティクスレポート" \
    || echo "  (既に存在する場合はスキップ)"

# 月次レポート - 毎月1日午前11時
echo -e "${GREEN}📈 月次レポートスケジュール設定中...${NC}"
$GCLOUD scheduler jobs create http ktrend-analytics-monthly-schedule \
    --location=$REGION \
    --schedule="0 11 1 * *" \
    --uri="$MONTHLY_URL" \
    --http-method=POST \
    --time-zone="Asia/Tokyo" \
    --project=$PROJECT_ID \
    --description="K-TREND TIMES 月次アナリティクスレポート" \
    || echo "  (既に存在する場合はスキップ)"

# クリーンアップ（セキュリティのため）
echo ""
echo -e "${YELLOW}🧹 クリーンアップ中...${NC}"
rm -f "$FUNCTIONS_DIR/service-account-key.json"

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ デプロイ完了！${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "📋 設定されたスケジュール:"
echo "  📅 日次レポート: 毎日 09:00 (JST)"
echo "  📊 週次レポート: 毎週月曜 10:00 (JST)"
echo "  📈 月次レポート: 毎月1日 11:00 (JST)"
echo ""
echo "🔍 Cloud Scheduler ジョブを確認:"
echo "  https://console.cloud.google.com/cloudscheduler?project=$PROJECT_ID"
echo ""
echo "💡 手動でテスト実行する場合:"
echo "  gcloud scheduler jobs run ktrend-analytics-daily-schedule --location=$REGION"
echo ""
