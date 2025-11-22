# Lab 1 Setup Guide

This guide covers how to prepare your environment for the lab, specifically focused on **Windows Subsystem for Linux (WSL)**.

If you are on macOS or standard Linux, most steps are similar, but you can skip the WSL specific parts.

## 1. Open WSL

We recommend running this tutorial inside a Linux environment on Windows (WSL2).

1.  Open **PowerShell** or your terminal of choice.
2.  Enter your WSL distribution:
    ```bash
    wsl
    ```
    *(If this command fails, you may need to install WSL by running `wsl --install` in an Administrator PowerShell and restarting).*

3.  Navigate to your project folder. Note that your Windows drives are mounted at `/mnt/`.
    ```bash
    # Example: If project is in D:\Projects\tutorials
    cd /mnt/d/Projects/tutorials
    ```

## 2. Install System Dependencies

In a fresh WSL installation, you might be missing Python or other basics.

1.  **Update Package Lists**:
    ```bash
    sudo apt update
    ```

2.  **Install Python & Pip**:
    ```bash
    sudo apt install -y python3 python3-venv python3-pip
    ```

3.  **Install Unzip & Build Tools** (often needed for extensions):
    ```bash
    sudo apt install -y unzip build-essential
    ```

## 3. Install Node.js

The tutorial uses TypeScript tools, so we need Node.js. We recommend using `nvm` (Node Version Manager).

1.  **Install nvm**:
    ```bash
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    ```

2.  **Activate nvm** (or close and reopen terminal):
    ```bash
    source ~/.bashrc
    ```

3.  **Install Node**:
    ```bash
    nvm install --lts
    ```

4.  **Verify**:
    ```bash
    node --version
    npm --version
    ```

## 4. Install Ollama

The Agent needs a brain. We use Ollama to run Llama 3.1 locally.

1.  **Install**:
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ```

2.  **Start Server**:
    ```bash
    ollama serve &
    ```
    *(If it says "address already in use", it's likely already running in the background or on Windows. That's fine!)*

3.  **Pull the Model**:
    ```bash
    ollama pull llama3.1:8b
    ```

## 5. Project Setup

Now that the system is ready, configure the project dependencies.

1.  **Run the Setup Script**:
    ```bash
    ./setup.sh
    ```

2.  **Activate Environment**:
    ```bash
    source venv/bin/activate
    source .env_setup
    ```

## 6. Verification

Run these commands to ensure you are ready:

```bash
# Should return python 3.x
python3 --version
# Output: Python 3.12.x (or similar)

# Should return a list of pip packages
pip list
# Output: 
# Package    Version
# ---------- -------
# ollama     0.1.x
# pytest     ...

# Should show the llama3.1 model
ollama list
# Output:
# NAME          ID           SIZE   MODIFIED
# llama3.1:8b   ...          4.7GB  ...

# Should run the agent module (type 'exit' to quit)
python -m src.agent.simple_agent
# Output:
# Initializing Agent...
# Agent Ready. Type 'exit' to quit.
#
# You:
```

If all of these work, you are ready to start the [Lab Checklist](./lab-checklist.md).

## 7. Understanding the Test Data

The repository includes sample data files in `data/` for testing your tools:

### data/todos.txt
A sample TODO list file used to test file reading capabilities. Contains project tasks in a realistic format.

### data/notes.txt
A simple notes file with project information. Used for testing file search and read operations.

### data/sample.py
A basic Python file for testing code file operations. Demonstrates how tools interact with different file types.

**Why these files exist**: When building agentic tools, you need realistic test data to verify your agent can find and read files correctly. These files provide consistent test cases for the O.V.E. methodology.

