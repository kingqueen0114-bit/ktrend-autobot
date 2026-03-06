#!/bin/bash
# ============================================
# K-TREND TIMES GCPインスタンス作成スクリプト
#
# 使用前に以下を実行:
#   1. Google Cloud SDK をインストール
#      brew install --cask google-cloud-sdk
#   2. 認証
#      gcloud auth login
#   3. プロジェクト設定
#      gcloud config set project YOUR_PROJECT_ID
# ============================================

set -e

# 設定
INSTANCE_NAME="ktrend-server"
ZONE="asia-northeast1-a"
MACHINE_TYPE="e2-medium"
IMAGE_FAMILY="ubuntu-2204-lts"
IMAGE_PROJECT="ubuntu-os-cloud"
BOOT_DISK_SIZE="30GB"

echo "============================================"
echo "K-TREND TIMES GCPインスタンス作成"
echo "============================================"

# プロジェクト確認
PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT" ]; then
    echo "エラー: GCPプロジェクトが設定されていません"
    echo "実行: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi
echo "プロジェクト: $PROJECT"

# インスタンス作成
echo ""
echo "インスタンスを作成中..."
gcloud compute instances create $INSTANCE_NAME \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --image-family=$IMAGE_FAMILY \
    --image-project=$IMAGE_PROJECT \
    --boot-disk-size=$BOOT_DISK_SIZE \
    --boot-disk-type=pd-ssd \
    --tags=http-server,https-server \
    --metadata=startup-script='#!/bin/bash
        apt-get update
        apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
        apt-get update
        apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
        usermod -aG docker $(whoami)
    '

# ファイアウォールルール作成（既存でなければ）
echo ""
echo "ファイアウォールルールを確認中..."
gcloud compute firewall-rules describe default-allow-http 2>/dev/null || \
    gcloud compute firewall-rules create default-allow-http \
        --allow tcp:80 \
        --target-tags http-server \
        --description "Allow HTTP"

gcloud compute firewall-rules describe default-allow-https 2>/dev/null || \
    gcloud compute firewall-rules create default-allow-https \
        --allow tcp:443 \
        --target-tags https-server \
        --description "Allow HTTPS"

# 外部IPを取得
echo ""
echo "インスタンス情報を取得中..."
EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME \
    --zone=$ZONE \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

# 静的IPに昇格
echo "静的IPに昇格中..."
gcloud compute addresses create ktrend-ip \
    --region=asia-northeast1 \
    --addresses=$EXTERNAL_IP 2>/dev/null || true

echo ""
echo "============================================"
echo "インスタンス作成完了!"
echo "============================================"
echo ""
echo "  インスタンス名: $INSTANCE_NAME"
echo "  外部IP: $EXTERNAL_IP"
echo "  ゾーン: $ZONE"
echo ""
echo "次のステップ:"
echo "  1. DNS設定: k-trendtimes.com → $EXTERNAL_IP"
echo "  2. SSH接続:"
echo "     gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
echo "  3. ファイル転送:"
echo "     gcloud compute scp --recurse ktrend_migration/* $INSTANCE_NAME:/opt/ktrend/ --zone=$ZONE"
echo ""
echo "============================================"
