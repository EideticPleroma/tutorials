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

## 7. IDE Setup

This tutorial works with any AI-capable IDE or text editor. Choose the option that best fits your workflow:

### Option 1: Cursor (Recommended)

**Best for:** Complete AI-first development experience with built-in chat and code generation.

1.  **Install**: Download from [cursor.sh](https://cursor.sh/)
2.  **Configuration**: Create `.cursorrules` file (already included in this repo)
3.  **Usage**:
    - Press `Cmd/Ctrl+K` for inline code generation
    - Press `Cmd/Ctrl+L` to open AI chat
    - Reference files with `@filename`
    - Tag codebase with `@Codebase` for broad questions

**Pro Tips:**
- Use `@src/agent/simple_agent.py` to reference specific files
- Start new chats when switching tasks to clear context
- The `.cursorrules` file guides AI behavior for this project

### Option 2: VS Code with Continue

**Best for:** VS Code users who want powerful AI assistance with local model support.

1.  **Install VS Code**: Download from [code.visualstudio.com](https://code.visualstudio.com/)
2.  **Install Continue Extension**:
    - Open VS Code Extensions (Cmd/Ctrl+Shift+X)
    - Search for "Continue"
    - Install the extension
3.  **Configure Continue**:
    ```bash
    # Continue will auto-detect Ollama
    # Access Continue with Cmd/Ctrl+L
    ```
4.  **Configuration**: Continue reads `.cursorrules` automatically

**Pro Tips:**
- Use `Cmd/Ctrl+L` to open Continue sidebar
- Reference files with `@filename`
- Continue supports both local (Ollama) and cloud models

### Option 2b: VS Code with Cline (Claude Code)

**Best for:** Developers who prefer Claude's reasoning capabilities with agentic workflows.

1.  **Install VS Code**: Download from [code.visualstudio.com](https://code.visualstudio.com/)
2.  **Install Cline Extension**:
    - Open VS Code Extensions (Cmd/Ctrl+Shift+X)
    - Search for "Cline" (formerly Claude Dev)
    - Install the extension
3.  **Configure Cline**:
    - Add your Anthropic API key (requires paid Claude API access)
    - OR configure to use local Ollama for free alternative
    - Cline reads `.cursorrules` automatically
4.  **Usage**:
    - Cline appears in sidebar
    - Can autonomously execute multi-step tasks
    - Reviews and approves changes before applying

**Pro Tips:**
- Cline is more autonomous than Continue (can run commands, edit multiple files)
- Best for complex refactoring and multi-file changes
- Use "Agentic Mode" for hands-off implementation
- Reads `.cursorrules` for project guidelines

### Option 3: VS Code with GitHub Copilot

**Best for:** Developers with GitHub Copilot subscription who want inline suggestions.

1.  **Install VS Code**: Download from [code.visualstudio.com](https://code.visualstudio.com/)
2.  **Install Copilot**:
    - Sign up at [github.com/features/copilot](https://github.com/features/copilot)
    - Install "GitHub Copilot" extension in VS Code
    - Sign in with your GitHub account
3.  **Usage**:
    - Copilot provides inline suggestions as you type
    - Use `Cmd/Ctrl+I` for Copilot chat
    - Ask questions in natural language

**Note:** Copilot uses cloud models (not local Ollama). Your code is sent to GitHub's servers.

### Option 4: Any Text Editor + Manual AI Consultation

**Best for:** Users who prefer their existing editor or want maximum control.

1.  **Use your favorite editor**: vim, Emacs, Sublime, etc.
2.  **Consult AI manually**:
    - Use ChatGPT/Claude in browser for questions
    - Run Ollama directly: `ollama run llama3.1`
    - Copy/paste code and questions as needed

**Pro Tips:**
- Keep the [documentation](../tutorial-1/READING_GUIDE.md) open for reference
- Use the prompts from [Exercise 3](./exercises/03-prompt-engineering.md) to ask effective questions
- This approach takes longer but gives you complete control

### IDE Feature Comparison

| Feature | Cursor | Continue | Cline | Copilot | Manual |
|---------|--------|----------|-------|---------|--------|
| **Local Models** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes |
| **Inline Suggestions** | ✅ Yes | ✅ Yes | ⚠️ Limited | ✅ Yes | ❌ No |
| **AI Chat** | ✅ Built-in | ✅ Sidebar | ✅ Sidebar | ✅ Panel | ⚠️ External |
| **File References** | ✅ @file | ✅ @file | ✅ Auto | ⚠️ Limited | ❌ Manual |
| **Codebase Search** | ✅ @Codebase | ✅ @Codebase | ✅ Auto | ⚠️ Limited | ❌ Manual |
| **Agentic Mode** | ⚠️ Limited | ❌ No | ✅ Yes | ❌ No | ❌ No |
| **Auto-Execute** | ❌ No | ❌ No | ✅ Yes | ❌ No | ❌ No |
| **Cost** | Free | Free | $20/month* | $10/month | Free |
| **Privacy** | Full | Full | API/Local | Cloud | Full |

*Can use free local Ollama, but less capable than Claude API

**Our Recommendation:** 
- **Best for learning**: **Cursor** - Most balanced feature set
- **Best for VS Code users**: **Continue** - Free, powerful, supports local models
- **Best for autonomous coding**: **Cline** - Can implement entire features, requires API key or uses Ollama
- **Best for quick suggestions**: **Copilot** - Great inline completion, requires subscription

### IDE Configuration Files

This project includes configuration files for each IDE:

- **`.cursorrules`**: Auto-loaded by Cursor and Continue
- **`.vscode/settings.json`**: VS Code configuration (Continue, Copilot, Python)
- **`.vscode/extensions.json`**: Recommended VS Code extensions

**📖 [Complete IDE Configuration Guide](./IDE_CONFIGURATION.md)** - Detailed setup and troubleshooting for each IDE

## 8. Pro Tip: Always Include .cursorrules in AI Context

> **💡 This is the #1 skill that will accelerate your learning!**

The `.cursorrules` file at the project root contains all the guidelines, coding standards, and debugging approaches for this tutorial. When asking your AI assistant for help, **always include it in context**.

### Why This Matters

Your AI will give answers that:
- ✅ Follow the tutorial's methodology
- ✅ Use the correct patterns (decorators, imports, testing)
- ✅ Match the project's coding standards
- ✅ Are more educational (not just quick fixes)

**Without context:** "Try adding this code..." (might not match project style)
**With context:** "According to the project's tool registration pattern, you need to..." (matches tutorial approach)

### How to Include .cursorrules in Context

#### In Cursor

Type `@.cursorrules` at the start of your chat:

```
@.cursorrules

I'm working on Exercise 2 and getting KeyError: 'search_files'.
What am I missing according to the project guidelines?
```

**Keyboard shortcut:** Just type `@` and select `.cursorrules` from the menu.

#### In Continue (VS Code)

Continue automatically reads `.cursorrules` - just ask your question:

```
I'm getting KeyError: 'search_files' in Exercise 2.
What should I check based on the project setup?
```

**No need to explicitly reference it** - Continue loads it automatically!

#### In Cline (VS Code)

Cline also automatically reads `.cursorrules`:

```
Debug this error according to the project's guidelines:
KeyError: 'search_files'
```

#### In GitHub Copilot

Copilot **doesn't auto-read** `.cursorrules`. You need to manually include it:

**Option 1: Reference in every chat**
```
I'm following the lesson-1-fundamentals tutorial which uses:
- Python decorators for tool registration
- Side-effect imports (# noqa: F401)
- O.V.E. testing methodology

My problem: [describe issue]
```

**Option 2: Open .cursorrules file**
- Keep `.cursorrules` open in a tab
- Copilot can see open files
- Reference it: "Based on the open .cursorrules file..."

#### For Manual AI Consultation (ChatGPT, Claude, etc.)

1. Open `.cursorrules` in your editor
2. Copy relevant sections:
   - Coding Standards
   - Agentic Development Rules
   - Testing Methodology
3. Paste into your chat along with your question

**Example prompt:**
```
I'm working on an Agentic AI tutorial. Here are the project guidelines:

[PASTE RELEVANT .cursorrules SECTIONS]

My problem:
- Exercise: 2 (Adding Tools)
- Error: KeyError: 'search_files'
- What I tried: [your attempts]

Please help me debug following these guidelines.
```

### Example: Good vs Bad AI Questions

**❌ Bad (No Context):**
```
How do I add a tool to my agent?
```

**Why bad:** AI doesn't know your project structure, patterns, or requirements.

**✅ Good (With Context - Cursor/Continue):**
```
@.cursorrules

How do I add a file_search tool following the project's 
tool registration pattern? I'm on Exercise 2.
```

**Why good:** AI knows to use `@registry.register`, proper imports, docstrings, etc.

**✅ Also Good (With Context - Detailed):**
```
@.cursorrules

I'm implementing file_search tool in Exercise 2.

Current error: KeyError: 'search_files'

My code:
- Created src/agent/tools/file_search.py
- Added @registry.register decorator
- Function signature: def search_files(directory: str, pattern: str) -> str

What am I missing per the project's tool registration workflow?
```

**Why best:** Specific exercise, error, what you tried, asks for project-specific solution.

### Make It a Habit

**Every time you ask your AI assistant for help:**

1. **Include context:** `@.cursorrules` (Cursor) or open the file (Copilot)
2. **Specify exercise:** "I'm on Exercise 2..."
3. **Show what you tried:** "I created the file, added the decorator..."
4. **Ask project-specific:** "According to the project guidelines..."

**Result:** Better answers, faster learning, fewer dead-ends.

### Quick Reference Card

Save this for easy copy-paste:

```
@.cursorrules

Exercise: [1/2/3/4/Challenge]
Error: [exact error message or "no error, just stuck"]

What I'm trying to do: [goal]
What I tried: [attempts]
Expected: [what should happen]
Actual: [what's happening]

According to the project guidelines, what should I check?
```

---

## 9. Understanding the Test Data

The repository includes sample data files in `data/` for testing your tools:

### data/todos.txt
A sample TODO list file used to test file reading capabilities. Contains project tasks in a realistic format.

### data/notes.txt
A simple notes file with project information. Used for testing file search and read operations.

### data/sample.py
A basic Python file for testing code file operations. Demonstrates how tools interact with different file types.

**Why these files exist**: When building agentic tools, you need realistic test data to verify your agent can find and read files correctly. These files provide consistent test cases for the O.V.E. methodology.

