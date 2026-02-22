#!/bin/bash
# K-Trend AutoBot Project Setup Script

# Configuration
CONFIG_NAME="ktrend-autobot"
PROJECT_ID="k-trend-autobot"
REGION="asia-northeast1"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Setting up Google Cloud configuration for K-Trend AutoBot...${NC}"

# Check if configuration exists
if gcloud config configurations list | grep -q "$CONFIG_NAME"; then
    echo "Configuration '$CONFIG_NAME' already exists."
else
    echo "Creating configuration '$CONFIG_NAME'..."
    gcloud config configurations create $CONFIG_NAME
fi

# Activate configuration
echo "Activating configuration '$CONFIG_NAME'..."
gcloud config configurations activate $CONFIG_NAME

# Set properties
echo "Setting project to '$PROJECT_ID'..."
gcloud config set project $PROJECT_ID

echo "Setting region to '$REGION'..."
gcloud config set functions/region $REGION
gcloud config set run/region $REGION

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo -e "Current configuration:"
gcloud config list
