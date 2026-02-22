#!/bin/bash
# K-TREND TIMES 画像クレジットCSS デプロイスクリプト

set -e

# 色付き出力
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}K-TREND TIMES 画像クレジットCSS デプロイ${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# プラグインファイルのパス
PLUGIN_FILE="ktrend-image-credit.php"
TARGET_PATH="/var/www/html/wp-content/mu-plugins/${PLUGIN_FILE}"

if [ ! -f "$PLUGIN_FILE" ]; then
    echo -e "${RED}❌ エラー: ${PLUGIN_FILE} が見つかりません${NC}"
    exit 1
fi

echo -e "${GREEN}📋 デプロイ手順:${NC}"
echo ""
echo "以下のコマンドを実行してください:"
echo ""
echo -e "${YELLOW}1. GCPにSSH接続:${NC}"
echo "   gcloud compute ssh ktrend-server --zone=asia-northeast1-a --project=k-trend-autobot"
echo ""
echo -e "${YELLOW}2. Dockerコンテナに入る:${NC}"
echo "   docker exec -it ktrend-wordpress bash"
echo ""
echo -e "${YELLOW}3. mu-pluginsディレクトリに移動:${NC}"
echo "   cd /var/www/html/wp-content/mu-plugins"
echo ""
echo -e "${YELLOW}4. プラグインファイルを作成:${NC}"
echo "   cat > ${PLUGIN_FILE} << 'EOFPHP'"
cat "$PLUGIN_FILE"
echo "EOFPHP"
echo ""
echo -e "${YELLOW}5. パーミッション設定:${NC}"
echo "   chown www-data:www-data ${PLUGIN_FILE}"
echo "   chmod 644 ${PLUGIN_FILE}"
echo ""
echo -e "${YELLOW}6. 確認:${NC}"
echo "   ls -la ${PLUGIN_FILE}"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}または、ローカルからアップロード:${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "1. GCPにファイルをアップロード:"
echo "   gcloud compute scp ${PLUGIN_FILE} ktrend-server:/tmp/ --zone=asia-northeast1-a --project=k-trend-autobot"
echo ""
echo "2. SSH接続:"
echo "   gcloud compute ssh ktrend-server --zone=asia-northeast1-a --project=k-trend-autobot"
echo ""
echo "3. Dockerコンテナにコピー:"
echo "   docker cp /tmp/${PLUGIN_FILE} ktrend-wordpress:${TARGET_PATH}"
echo "   docker exec ktrend-wordpress chown www-data:www-data ${TARGET_PATH}"
echo "   docker exec ktrend-wordpress chmod 644 ${TARGET_PATH}"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
