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

# Version checking functions (November 2025 requirements)
check_python_version() {
    local version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
    local major=$(echo $version | cut -d. -f1)
    local minor=$(echo $version | cut -d. -f2)
    
    if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 10 ]); then
        echo -e "${RED}Error: Python 3.10+ required. Found: $version${NC}"
        echo -e "${YELLOW}Install Python 3.10+ from https://www.python.org${NC}"
        echo -e "${YELLOW}Recommended: Python 3.11, 3.12, or 3.13${NC}"
        return 1
    fi
    echo -e "  ✓ Python $version (3.10+ required, 3.11-3.13 recommended)"
    return 0
}

check_node_version() {
    local version=$(node --version 2>&1 | grep -oP '\d+' | head -1)
    
    if [ "$version" -lt 18 ]; then
        echo -e "${YELLOW}Warning: Node 18+ LTS recommended. Found: v$version${NC}"
        echo -e "${YELLOW}Consider upgrading: https://nodejs.org${NC}"
    else
        echo -e "  ✓ Node v$version (18.x, 20.x, 22.x LTS supported)"
    fi
    return 0
}

check_ollama_version() {
    if command -v ollama &> /dev/null; then
        local version=$(ollama --version 2>&1 | grep -oP 'ollama version is \K[\d.]+' || echo "unknown")
        
        if [[ "$version" =~ ^0\.([0-2])\. ]]; then
            echo -e "${RED}Error: Ollama 0.3.0+ required for tool calling. Found: $version${NC}"
            echo -e "${YELLOW}Update: curl -fsSL https://ollama.com/install.sh | sh${NC}"
            return 1
        elif [[ "$version" =~ ^0\.([3-4])\. ]]; then
            echo -e "${YELLOW}Warning: Ollama 0.5.0+ recommended. Found: $version${NC}"
            echo -e "  (Version $version works, but 0.5.0+ has performance improvements)"
        elif [ "$version" != "unknown" ]; then
            echo -e "  ✓ Ollama $version (0.5.0+ recommended, 0.3.0+ minimum)"
        else
            echo -e "  ✓ Ollama installed (version unknown)"
        fi
    fi
    return 0
}

# 1. Check Prerequisites
echo -e "\n${YELLOW}[1/5] Checking prerequisites and versions...${NC}"
check_command python3 || exit 1
check_python_version || exit 1

check_command node || exit 1
check_node_version

check_command npm || exit 1

check_command ollama || { echo -e "${YELLOW}Warning: Ollama not found. Please install it from https://ollama.com${NC}"; }
check_ollama_version

# 2. Python Setup
echo -e "\n${YELLOW}[2/5] Setting up Python environment...${NC}"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
echo "Installing Python dependencies..."
# Use root requirements.txt if available, otherwise use tutorial-specific
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install -r src/agent/requirements.txt
fi
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
    # echo "Pulling llama3.1:8b (alternative)..."
    # ollama pull llama3.1:8b
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
