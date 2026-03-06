#!/bin/bash
# ============================================
# K-TREND TIMES GCPサーバーセットアップスクリプト
# Ubuntu 22.04 LTS 用
# ============================================

set -e

echo "============================================"
echo "K-TREND TIMES サーバーセットアップ開始"
echo "============================================"

# カラー出力
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[注意]${NC} $1"
}

# ============================================
# 1. システム更新
# ============================================
echo ""
echo "1. システムを更新中..."
sudo apt update && sudo apt upgrade -y
print_status "システム更新完了"

# ============================================
# 2. 必要なパッケージをインストール
# ============================================
echo ""
echo "2. 必要なパッケージをインストール中..."
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    ufw
print_status "パッケージインストール完了"

# ============================================
# 3. Docker インストール
# ============================================
echo ""
echo "3. Dockerをインストール中..."

# Docker公式GPGキーを追加
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Dockerリポジトリを追加
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Docker インストール
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 現在のユーザーをdockerグループに追加
sudo usermod -aG docker $USER

print_status "Docker インストール完了"

# ============================================
# 4. ファイアウォール設定
# ============================================
echo ""
echo "4. ファイアウォールを設定中..."
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw --force enable
print_status "ファイアウォール設定完了"

# ============================================
# 5. プロジェクトディレクトリ作成
# ============================================
echo ""
echo "5. プロジェクトディレクトリを作成中..."
PROJECT_DIR="/opt/ktrend"
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR
print_status "ディレクトリ作成完了: $PROJECT_DIR"

# ============================================
# 6. 完了メッセージ
# ============================================
echo ""
echo "============================================"
echo -e "${GREEN}セットアップ完了!${NC}"
echo "============================================"
echo ""
echo "次のステップ:"
echo "  1. 一度ログアウトして再ログイン (dockerグループ反映)"
echo "     $ exit"
echo ""
echo "  2. プロジェクトファイルをサーバーにアップロード"
echo "     $ scp -r ktrend_migration/* user@SERVER_IP:/opt/ktrend/"
echo ""
echo "  3. 環境変数を設定"
echo "     $ cd /opt/ktrend"
echo "     $ cp .env.example .env"
echo "     $ nano .env  # パスワードを変更"
echo ""
echo "  4. SSL証明書を取得 (初回のみ)"
echo "     $ ./init-ssl.sh"
echo ""
echo "  5. Docker Compose で起動"
echo "     $ docker compose up -d"
echo ""
echo "============================================"
