#!/bin/bash
# ============================================
# K-TREND 画像移行実行スクリプト
# ローカルから実行: ./run-migration.sh
# ============================================

set -e

# Google Cloud SDK パス設定
export PATH="$HOME/google-cloud-sdk/bin:$PATH"

ZONE="asia-northeast1-a"
INSTANCE="ktrend-server"

echo "=== K-TREND 画像移行スクリプト ==="
echo ""

# 1. migrate-images.php をサーバーにコピー
echo "[1/3] スクリプトをサーバーにコピー中..."
gcloud compute scp output/migrate-images.php ${INSTANCE}:/tmp/ --zone=${ZONE}

# 2. サーバー上でスクリプトを実行
echo "[2/3] サーバーで移行スクリプトを実行中..."
gcloud compute ssh ${INSTANCE} --zone=${ZONE} --command="
cd /opt/ktrend

# WordPressコンテナにスクリプトをコピー
docker cp /tmp/migrate-images.php ktrend-wordpress:/var/www/html/

# WP-CLIが無ければインストール
docker exec ktrend-wordpress sh -c '
if ! command -v wp &> /dev/null; then
    echo \"WP-CLIをインストール中...\"
    curl -sO https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
    chmod +x wp-cli.phar
    mv wp-cli.phar /usr/local/bin/wp
fi
'

# 画像移行を実行
echo \"\"
echo \"=== 画像移行を開始 ===\"
docker exec ktrend-wordpress wp eval-file /var/www/html/migrate-images.php --allow-root

# 後片付け
docker exec ktrend-wordpress rm /var/www/html/migrate-images.php
"

echo ""
echo "[3/3] 完了!"
echo ""
echo "サイトを確認してください: http://34.84.132.199"
