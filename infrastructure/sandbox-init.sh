#!/bin/bash
# Initialize K-Trend project inside the sandbox VM
# Run this after SSHing into the VM

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

WORKSPACE="/home/workspace"
PROJECT_DIR="$WORKSPACE/ktrend-autobot"

echo -e "${BLUE}=== K-Trend Sandbox Initialization ===${NC}"
echo ""

# Wait for startup script to complete
echo -e "${YELLOW}Waiting for system setup to complete...${NC}"
while [ ! -f /var/log/sandbox-setup.log ]; do
    echo "  Waiting..."
    sleep 10
done
echo -e "${GREEN}System setup complete!${NC}"
echo ""

# Clone or sync project
echo -e "${YELLOW}Setting up project...${NC}"
cd $WORKSPACE

if [ -d "$PROJECT_DIR" ]; then
    echo "Project exists, pulling latest..."
    cd $PROJECT_DIR
    git pull
else
    echo "Cloning project..."
    # You'll need to set up Git credentials or use a deploy key
    git clone https://github.com/YOUR_USERNAME/ktrend-autobot.git || {
        echo "Git clone failed. Creating empty project directory..."
        mkdir -p $PROJECT_DIR
    }
fi

cd $PROJECT_DIR

# Setup Python virtual environment
echo -e "${YELLOW}Setting up Python environment...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Setup environment variables
echo -e "${YELLOW}Setting up environment...${NC}"
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo "Created .env from .env.example - please edit with your credentials"
fi

# Create tmux session for Claude Code
echo -e "${YELLOW}Setting up tmux session...${NC}"
tmux new-session -d -s claude-code -n main 2>/dev/null || true

echo ""
echo -e "${GREEN}=== Sandbox Ready ===${NC}"
echo ""
echo -e "${BLUE}Start Claude Code:${NC}"
echo "  claude"
echo ""
echo -e "${BLUE}Or attach to tmux session:${NC}"
echo "  tmux attach -t claude-code"
echo ""
echo -e "${BLUE}Project directory:${NC}"
echo "  $PROJECT_DIR"
echo ""
echo -e "${YELLOW}Note: Set your ANTHROPIC_API_KEY before running Claude Code:${NC}"
echo "  export ANTHROPIC_API_KEY='your-api-key'"
