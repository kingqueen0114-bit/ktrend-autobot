#!/bin/bash
# K-Trend AutoBot Cloud Sandbox Setup
# GCP Compute Engine で Claude Code を動かすサンドボックス環境を構築

set -e

# Configuration
PROJECT_ID="line-calendar-bot-20260203"
ZONE="asia-northeast1-b"
INSTANCE_NAME="ktrend-sandbox"
MACHINE_TYPE="e2-medium"  # 2 vCPU, 4GB RAM
DISK_SIZE="50GB"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== K-Trend Cloud Sandbox Setup ===${NC}"
echo ""

# Check if gcloud is available
GCLOUD_CMD="${GCLOUD_CMD:-gcloud}"
if ! command -v $GCLOUD_CMD &> /dev/null; then
    GCLOUD_CMD="$HOME/line-calendar-bot/google-cloud-sdk/bin/gcloud"
fi

echo -e "${YELLOW}1. Creating Compute Engine instance...${NC}"

# Create VM with startup script
$GCLOUD_CMD compute instances create $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --boot-disk-size=$DISK_SIZE \
    --boot-disk-type=pd-balanced \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server,https-server \
    --metadata=startup-script='#!/bin/bash
# Startup script for K-Trend Sandbox

# Update system
apt-get update
apt-get upgrade -y

# Install essential tools
apt-get install -y \
    git \
    curl \
    wget \
    vim \
    htop \
    tmux \
    build-essential \
    python3 \
    python3-pip \
    python3-venv

# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Create workspace directory
mkdir -p /home/workspace
chmod 777 /home/workspace

# Log completion
echo "Sandbox setup complete!" > /var/log/sandbox-setup.log
'

echo -e "${GREEN}VM created successfully!${NC}"
echo ""

echo -e "${YELLOW}2. Waiting for VM to be ready...${NC}"
sleep 30

echo -e "${YELLOW}3. Getting VM external IP...${NC}"
EXTERNAL_IP=$($GCLOUD_CMD compute instances describe $INSTANCE_NAME \
    --zone=$ZONE \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo -e "${GREEN}External IP: $EXTERNAL_IP${NC}"
echo ""

echo -e "${YELLOW}4. Creating firewall rule for SSH...${NC}"
$GCLOUD_CMD compute firewall-rules create allow-ssh-sandbox \
    --project=$PROJECT_ID \
    --allow=tcp:22 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=http-server \
    2>/dev/null || echo "Firewall rule already exists"

echo ""
echo -e "${GREEN}=== Setup Complete ===${NC}"
echo ""
echo -e "${BLUE}Connect to sandbox:${NC}"
echo "  gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
echo ""
echo -e "${BLUE}Or use SSH directly:${NC}"
echo "  ssh $EXTERNAL_IP"
echo ""
echo -e "${BLUE}Instance details:${NC}"
echo "  Name: $INSTANCE_NAME"
echo "  Zone: $ZONE"
echo "  IP: $EXTERNAL_IP"
echo ""
echo -e "${YELLOW}Note: Wait 2-3 minutes for startup script to complete.${NC}"
echo "Check setup status with:"
echo "  gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='cat /var/log/sandbox-setup.log'"
