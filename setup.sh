#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Tutorial 1 Environment Setup...${NC}"

# Function to check if a command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed.${NC}"
        return 1
    fi
    return 0
}

# 1. Check Prerequisites
echo -e "\n${YELLOW}[1/5] Checking prerequisites...${NC}"
check_command python3 || exit 1
check_command node || exit 1
check_command npm || exit 1
check_command ollama || { echo -e "${YELLOW}Warning: Ollama not found. Please install it or run via Docker.${NC}"; }

# 2. Python Setup
echo -e "\n${YELLOW}[2/5] Setting up Python environment...${NC}"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
echo "Installing Python dependencies..."
pip install -r src/agent/requirements.txt
echo "Python setup complete."

# 3. Node.js Setup
echo -e "\n${YELLOW}[3/5] Setting up Node.js environment...${NC}"
cd src/tools
if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install
fi
echo "Building TypeScript tools..."
npm run build
cd ../..
echo "Node.js setup complete."

# 4. Ollama Model Setup
echo -e "\n${YELLOW}[4/5] Checking/Pulling Llama models...${NC}"
if command -v ollama &> /dev/null; then
    # Check if ollama server is running
    if ! pgrep -x "ollama" > /dev/null; then
        echo "Ollama server not running. Starting it in background..."
        ollama serve &
        OLLAMA_PID=$!
        sleep 5
    fi

    echo "Pulling llama3.1:8b..."
    ollama pull llama3.1:8b
    
    # Optional: Pull smaller model
    # echo "Pulling llama3.1:2b..."
    # ollama pull llama3.1:2b
else
    echo "Skipping model pull (Ollama not installed locally)."
fi

# 5. Environment & Aliases
echo -e "\n${YELLOW}[5/5] Creating helper aliases...${NC}"
cat << EOF > .env_setup
# Source this file to activate the environment: source .env_setup

export PYTHONPATH=\$PWD/src
export PATH=\$PWD/src/tools/node_modules/.bin:\$PATH

# Aliases
alias run-agent="python3 -m src.agent.simple_agent"
alias run-tests="pytest tests/"
alias dev-env="source venv/bin/activate && source .env_setup"

echo "Environment configured!"
EOF

echo -e "\n${GREEN}Setup Complete!${NC}"
echo -e "To activate the environment, run:"
echo -e "  ${YELLOW}source venv/bin/activate${NC}"
echo -e "  ${YELLOW}source .env_setup${NC}"
