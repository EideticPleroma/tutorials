# Troubleshooting Lab 1

> **💡 First Time Here?** Start with the [Getting Unstuck Guide](./getting-unstuck.md) for a systematic debugging approach.

This guide covers common errors, what they mean, and how to fix them. Each error includes an **"Ask Your AI"** prompt to help you learn debugging with AI assistance.

---

## Table of Contents

- [Debug Mode & Logging](#debug-mode--logging)
- [Setup & Environment Errors](#setup--environment-errors)
- [Tool Registration Errors](#tool-registration-errors)
- [Import & Module Errors](#import--module-errors)
- [Agent Behavior Issues](#agent-behavior-issues)
- [Testing Issues](#testing-issues)
- [Ollama & Model Errors](#ollama--model-errors)
- [WSL-Specific Issues](#wsl-specific-issues)
- [Performance Issues](#performance-issues)
- [Rollback Strategies](#rollback-strategies)

---

## Debug Mode & Logging

### Enable Verbose Logging

Add this to the top of `src/agent/simple_agent.py`:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

Then add debug statements throughout your code:

```python
def chat(self, user_input: str) -> str:
    logger.debug(f"User input: {user_input}")
    logger.debug(f"Tool schemas: {registry.get_schemas()}")
    # ... rest of code
```

### Quick Debug Checklist

Run these commands to verify your setup:

```bash
# 1. Check Ollama is running
curl localhost:11434

# 2. Check model is available
ollama list | grep llama3.1

# 3. Check Python environment
python --version
pip list | grep ollama

# 4. Test tool registry
python -c "from src.agent.tool_registry import registry; from src.agent import simple_agent; print([s['function']['name'] for s in registry.get_schemas()])"

# 5. Check file structure
ls -la src/agent/tools/
```

---

## Setup & Environment Errors

### Error 1: `bash: ./setup.sh: Permission denied`

**What It Means:** The setup script doesn't have execute permissions.

**Why It Happens:** File permissions weren't set when cloning the repository.

**How To Fix:**
```bash
chmod +x setup.sh
./setup.sh
```

**Ask Your AI:**
```
@.cursorrules
I'm getting "Permission denied" when running ./setup.sh
What's the correct way to run setup scripts in this project?
```

---

### Error 2: `ModuleNotFoundError: No module named 'ollama'`

**What It Means:** The Python `ollama` package is not installed in your environment.

**Why It Happens:**
- Virtual environment not activated
- Dependencies not installed
- Wrong Python interpreter being used

**How To Fix:**
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Verify
pip list | grep ollama
```

**Ask Your AI:**
```
@.cursorrules
I'm getting "ModuleNotFoundError: No module named 'ollama'"

What I tried:
- Ran ./setup.sh
- Python version: [your version]

How should I properly set up the Python environment for this project?
```

---

### Error 3: `python: command not found` or `python3: command not found`

**What It Means:** Python is not installed or not in your PATH.

**Why It Happens:**
- Python not installed
- WSL doesn't have Python
- PATH not configured

**How To Fix:**

```bash
# Check Python installation
which python3
python3 --version

# If not found, install (Ubuntu/Debian)
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Create alias if needed
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc
```

**Ask Your AI:**
```
@.cursorrules
Python command not found in my terminal.
OS: [Windows WSL2 / macOS / Linux]
What's the correct setup process for this tutorial?
```

---

## Tool Registration Errors

### Error 4: `KeyError: 'search_files'` or `KeyError: '<your_tool_name>'`

**What It Means:** The agent tried to call a tool that isn't in the registry.

**Why It Happens:**
- Tool file not imported (decorator never executed)
- Typo in tool name
- Import statement missing or incorrect

**How To Fix:**

**Step 1:** Verify the import in `simple_agent.py`:
```python
# This import MUST be present for your tool to register
from .tools import file_search  # noqa: F401
```

**Step 2:** Check `tools/__init__.py` exports the tool:
```python
from . import file_search

__all__ = ['file_search']
```

**Step 3:** Test registration:
```bash
python -c "
from src.agent.tool_registry import registry
from src.agent import simple_agent  # Triggers imports
tools = [s['function']['name'] for s in registry.get_schemas()]
print('Registered tools:', tools)
print('search_files registered:', 'search_files' in tools)
"
```

**Ask Your AI:**
```
@.cursorrules
I'm getting KeyError: 'search_files' in Exercise 2.

My file structure:
src/agent/tools/
├── __init__.py
└── file_search.py

My file_search.py has @registry.register decorator.

According to the project's tool registration pattern, what am I missing?
```

---

### Error 5: Tool Function Called But Returns `None`

**What It Means:** Your tool function executed but didn't return a value.

**Why It Happens:**
- Missing `return` statement
- Function returns `None` on some code paths
- Logic error in your tool

**How To Fix:**

Check your tool always returns a string:

```python
@registry.register
def search_files(directory: str, pattern: str) -> str:
    """Search for files."""
    try:
        # Your logic here
        results = find_files(directory, pattern)
        return f"Found {len(results)} files: {', '.join(results)}"  # ✅ Always return
    except Exception as e:
        return f"Error: {str(e)}"  # ✅ Return error message, don't raise
    # ❌ No implicit None return
```

**Ask Your AI:**
```
@.cursorrules
My tool is being called but returns None.

Here's my function:
[paste your code]

According to agentic code practices, what should tools return?
```

---

### Error 6: `TypeError: <tool_name>() got an unexpected keyword argument`

**What It Means:** The LLM passed an argument your function doesn't accept.

**Why It Happens:**
- Function signature doesn't match docstring
- Type hints missing or incorrect
- LLM hallucinated a parameter

**How To Fix:**

Ensure function signature matches docstring exactly:

```python
@registry.register
def search_files(directory: str, pattern: str) -> str:  # ✅ Parameters match docstring
    """
    Search for files matching a pattern.
    
    Args:
        directory: Path to search in
        pattern: File pattern (e.g., "*.py")
    
    Returns:
        Description of files found
    """
    # Implementation
```

**Ask Your AI:**
```
@.cursorrules
Getting TypeError for unexpected keyword argument.

Tool signature:
[paste your function signature]

Tool docstring:
[paste your docstring]

What's the mismatch?
```

---

## Import & Module Errors

### Error 7: `ModuleNotFoundError: No module named 'src.agent.tools'`

**What It Means:** Python can't find the `tools` package.

**Why It Happens:**
- Missing `__init__.py` in tools directory
- Running from wrong directory
- Python path not set correctly

**How To Fix:**

**Step 1:** Ensure `__init__.py` exists:
```bash
# Create if missing
touch src/agent/tools/__init__.py
```

**Step 2:** Verify directory structure:
```bash
ls -la src/agent/tools/
# Should show:
# -rw-r--r-- __init__.py
# -rw-r--r-- file_search.py
```

**Step 3:** Run from project root:
```bash
# Always run from here
cd /path/to/tutorials
python -m src.agent.simple_agent
```

**Ask Your AI:**
```
@.cursorrules
Getting ModuleNotFoundError for 'src.agent.tools'

Directory structure:
[paste output of 'tree src/' or 'ls -R src/']

What's wrong with my package structure?
```

---

### Error 8: `ImportError: attempted relative import with no known parent package`

**What It Means:** You're trying to use relative imports (`.tools`) but Python doesn't know the package context.

**Why It Happens:**
- Running file directly: `python simple_agent.py` ❌
- Should use module syntax: `python -m src.agent.simple_agent` ✅

**How To Fix:**

```bash
# Wrong
python src/agent/simple_agent.py

# Correct
python -m src.agent.simple_agent
```

**Ask Your AI:**
```
@.cursorrules
Getting "attempted relative import with no known parent package"

How should I run the agent according to the project structure?
```

---

### Error 9: `ImportError: cannot import name 'registry' from 'src.agent.tool_registry'`

**What It Means:** The `registry` object doesn't exist or isn't exported.

**Why It Happens:**
- Typo in import statement
- `tool_registry.py` has syntax errors
- Circular import issue

**How To Fix:**

**Step 1:** Check the import:
```python
# Correct
from src.agent.tool_registry import registry

# Wrong
from src.agent.tool_registry import Registry  # Capital R
```

**Step 2:** Verify `tool_registry.py` has no syntax errors:
```bash
python -c "import src.agent.tool_registry"
# Should have no output if OK
```

**Ask Your AI:**
```
@.cursorrules
Can't import 'registry' from tool_registry module.

Error: [paste full error]

What's the correct import pattern for the registry?
```

---

## Agent Behavior Issues

### Error 10: Agent Loops Forever / Infinite Tool Calls

**What It Means:** The agent keeps calling the same tool or never finishes.

**Why It Happens:**
- LLM output doesn't match expected JSON schema
- System prompt causes confusion
- Tool returns invalid format
- Temperature too high (agent is "creative")

**How To Fix:**

**Step 1:** Lower temperature in `agent_config.py`:
```python
temperature: float = 0.1  # or even 0.0 for max determinism
```

**Step 2:** Check tool output format:
```python
# Tools must return strings, not None or objects
return f"Found 3 files: a.py, b.py, c.py"  # ✅ Good
return ["a.py", "b.py", "c.py"]  # ❌ Bad - agent can't process lists
return None  # ❌ Bad - causes loops
```

**Step 3:** Simplify system prompt temporarily:
```python
system_prompt = "You are a helpful assistant with access to tools. Use tools when appropriate."
```

**Ask Your AI:**
```
@.cursorrules
My agent loops forever calling the same tool.

Temperature: [your setting]
System prompt: [paste your prompt]
Tool output format: [paste example]

What's causing the loop according to best practices?
```

---

### Error 11: Agent Ignores Tool Outputs

**What It Means:** Agent calls tools but doesn't use the returned data in its response.

**Why It Happens:**
- System prompt doesn't emphasize using tool data
- Tool output not in messages list
- Second LLM call not happening

**How To Fix:**

**Step 1:** Update system prompt in `agent_config.py`:
```python
system_prompt = """You are a helpful assistant with access to tools.

IMPORTANT: When you use a tool, you MUST include the specific data 
from the tool's output in your response to the user.

Example:
User: "Find Python files"
Tool returns: "Found 3 files: a.py, b.py, c.py"
Your response: "I found 3 Python files: a.py, b.py, and c.py"
"""
```

**Step 2:** Verify second LLM call happens (check debug output).

**Ask Your AI:**
```
@.cursorrules
Agent calls tools but doesn't mention the results in its response.

Current system prompt: [paste prompt]

How should I phrase the prompt to make it use tool outputs?
```

---

### Error 12: Agent Hallucinates Tool Names

**What It Means:** Agent tries to call tools that don't exist (e.g., `search_python_files` instead of `search_files`).

**Why It Happens:**
- Tool name not clear from docstring
- Temperature too high
- System prompt suggests non-existent tools

**How To Fix:**

**Step 1:** Make tool names explicit in docstring:
```python
@registry.register
def search_files(directory: str, pattern: str) -> str:
    """
    search_files: Search for files matching a pattern in a directory.
    
    Use this tool when user asks to find, search, or locate files.
    
    Args:
        directory: Path to search (e.g., "src/", "tests/")
        pattern: File pattern (e.g., "*.py", "*.txt")
    """
```

**Step 2:** Lower temperature to 0.1.

**Step 3:** Add few-shot example to system prompt.

**Ask Your AI:**
```
@.cursorrules
Agent tries to call "search_python_files" but my tool is named "search_files".

My docstring: [paste docstring]

How can I make the tool name clearer to the LLM?
```

---

## Testing Issues

### Error 13: `AssertionError` in Tests (Tests Fail)

**What It Means:** Your code doesn't match test expectations.

**Why It Happens:**
- Tool behavior doesn't match test assumptions
- Test is checking for wrong thing
- Probabilistic failure (agent behavior varies)

**How To Fix:**

**Step 1:** Run test in verbose mode:
```bash
pytest tests/unit/test_file_search.py -v -s
```

**Step 2:** Check what the test expects:
```python
# Read the test file and look at assertions
# Example:
assert result.passed_validation
# What validation is failing? Check result.validation_errors
```

**Step 3:** Add debug output to your test:
```python
result = runner.run(case)
print(f"Agent response: {result.response}")
print(f"Tool calls: {result.tool_calls}")
print(f"Validation errors: {result.validation_errors}")
assert result.passed_validation
```

**Ask Your AI:**
```
@.cursorrules
Test failing with AssertionError.

Test code: [paste test]
Tool code: [paste tool implementation]
Error: [paste assertion error]

What's the mismatch?
```

---

### Error 14: Tests Pass Sometimes, Fail Others (Flakiness)

**What It Means:** Your tests are non-deterministic (probabilistic).

**Why It Happens:**
- LLMs are inherently probabilistic
- Temperature too high
- System prompt is ambiguous
- Test expectations too strict

**How To Fix:**

**Step 1:** Lower temperature to 0.0 or 0.1:
```python
temperature: float = 0.1
```

**Step 2:** Make system prompt more explicit:
```python
system_prompt = """You are a helpful assistant.
When user asks to find files, you MUST use the search_files tool.
Always include tool results in your response."""
```

**Step 3:** Relax test assertions:
```python
# Too strict
assert response == "Found 3 files: a.py, b.py, c.py"

# Better
assert "3 files" in response.lower()
assert "a.py" in response
```

**Step 4:** Run flakiness check:
```bash
for i in {1..5}; do pytest tests/unit/test_file_search.py; done
```

Target: 5/5 passes = robust test.

**Ask Your AI:**
```
@.cursorrules
Test passes 3 out of 5 times.

Temperature: [setting]
Test code: [paste test]

How do I make agent behavior deterministic?
```

---

### Error 15: `pytest: command not found`

**What It Means:** pytest is not installed.

**Why It Happens:**
- Virtual environment not activated
- Dependencies not installed

**How To Fix:**

```bash
# Activate venv
source venv/bin/activate

# Install pytest
pip install pytest

# Or install all dependencies
pip install -r requirements.txt

# Verify
pytest --version
```

---

## Ollama & Model Errors

### Error 16: `httpx.ConnectError: Connection refused` (Port 11434)

**What It Means:** Ollama server is not running.

**Why It Happens:**
- Ollama not started
- Ollama crashed
- Port 11434 blocked by firewall

**How To Fix:**

```bash
# Check if Ollama is running
curl localhost:11434
# Expected: "Ollama is running"

# If not running, start it
ollama serve &

# Or in separate terminal
ollama serve

# Verify
ollama list
```

**In WSL:** Ollama might be running on Windows, not WSL. Access via:
```python
# In agent_config.py or where ollama.chat is called
ollama.chat(
    model=config.model_name,
    messages=self.messages,
    host="http://localhost:11434"  # Explicit host
)
```

**Ask Your AI:**
```
@.cursorrules
Getting "Connection refused" on port 11434.

OS: [Windows WSL2 / macOS / Linux]
Ollama installed: [yes/no]

How should Ollama be configured for this tutorial?
```

---

### Error 17: `ollama.ResponseError: model not found: llama3.1:8b`

**What It Means:** The Llama 3.1 model is not downloaded.

**Why It Happens:**
- Model not pulled
- Wrong model name
- Ollama not fully initialized

**How To Fix:**

```bash
# Pull the model (this downloads ~4.7GB)
ollama pull llama3.3:8b

# Verify
ollama list
# Should show:
# NAME          ID           SIZE
# llama3.1:8b   ...          4.7GB

# Test the model
ollama run llama3.1:8b "Hello"
```

**Ask Your AI:**
```
@.cursorrules
Getting "model not found: llama3.1:8b"

Output of 'ollama list': [paste output]

What model should I use for this tutorial?
```

---

### Error 18: Slow Response Times (10+ seconds per query)

**What It Means:** Model is running slowly.

**Why It Happens:**
- Large model for your hardware
- High temperature causing more tokens
- Long context window
- System under load

**How To Fix:**

**Option 1:** Use smaller model:
```bash
# Try the 7B parameter version
ollama pull llama3.1:8b

# Update agent_config.py
model_name: str = "llama3.1:7b"
```

**Option 2:** Reduce context:
```python
# In simple_agent.py, limit message history
def chat(self, user_input: str) -> str:
    # Keep only last 10 messages
    if len(self.messages) > 10:
        self.messages = self.messages[:1] + self.messages[-9:]  # Keep system prompt + last 9
```

**Option 3:** Lower temperature:
```python
temperature: float = 0.1  # Fewer tokens = faster
```

**Ask Your AI:**
```
@.cursorrules
Agent responses take 10+ seconds.

Hardware: [RAM, CPU]
Model: llama3.1:8b
Temperature: [setting]

How can I optimize for performance?
```

---

## WSL-Specific Issues

### Error 19: `bad interpreter: /bin/bash^M: no such file or directory`

**What It Means:** Script has Windows line endings (CRLF) instead of Unix (LF).

**Why It Happens:**
- Files edited in Windows
- Git not configured for line endings

**How To Fix:**

```bash
# Fix the file
dos2unix setup.sh
# Or
sed -i 's/\r$//' setup.sh

# Configure Git for future
git config --global core.autocrlf input
```

**Ask Your AI:**
```
@.cursorrules
Getting "bad interpreter" error in WSL.

Error: [paste error]

How should line endings be handled in this project?
```

---

### Error 20: WSL Can't Find Windows Ollama

**What It Means:** Ollama running on Windows, but WSL trying to connect to localhost.

**Why It Happens:**
- Ollama installed on Windows host
- WSL networking not configured

**How To Fix:**

**Option 1:** Install Ollama in WSL (recommended):
```bash
# Inside WSL
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.3:8b
```

**Option 2:** Connect to Windows host:
```python
# Find Windows host IP in WSL
# cat /etc/resolv.conf | grep nameserver

# In Python code, use Windows host IP
# Usually: 172.x.x.x
```

**Ask Your AI:**
```
@.cursorrules
WSL can't connect to Ollama running on Windows.

WSL version: [WSL1 or WSL2]

Should I install Ollama in WSL or connect to Windows?
```

---

### Error 21: File Paths Not Found (Windows vs Linux paths)

**What It Means:** Path separator mismatch (\ vs /).

**Why It Happens:**
- Hard-coded Windows paths in WSL
- Not using `os.path.join`

**How To Fix:**

```python
# Bad
path = "src\\agent\\tools"  # Windows style

# Good
import os
path = os.path.join("src", "agent", "tools")  # Cross-platform

# Also good
from pathlib import Path
path = Path("src") / "agent" / "tools"
```

**Ask Your AI:**
```
@.cursorrules
File paths not working in WSL.

My code: [paste path construction]

What's the cross-platform way to handle paths?
```

---

## Performance Issues

### Error 22: High Memory Usage (8GB+ RAM)

**What It Means:** Model is consuming too much memory.

**Why It Happens:**
- Large context window
- Multiple agents running
- Model size

**How To Fix:**

```bash
# Check memory usage
free -h

# Kill other Ollama processes
pkill ollama
ollama serve

# Use smaller model
ollama pull llama3.1:8b
```

---

### Error 23: Disk Space Error

**What It Means:** Not enough disk space for model.

**Why It Happens:**
- Models are large (4-8GB each)
- Multiple models downloaded

**How To Fix:**

```bash
# Check disk space
df -h

# Remove unused models
ollama list
ollama rm <unused-model>

# Keep only what you need
ollama list
```

---

## Rollback Strategies

### When Nothing Works: Reset Everything

**Level 1: Soft Reset** (undo uncommitted changes)
```bash
git status  # See what changed
git diff  # Review changes
git checkout -- .  # Undo all changes
```

**Level 2: Hard Reset** (go back to last commit)
```bash
git reset --hard HEAD
```

**Level 3: Reset to Specific Point**
```bash
git log --oneline  # Find working commit
git reset --hard <commit-hash>
```

**Level 4: Fresh Start**
```bash
cd ..
mv tutorials tutorials_backup
git clone <repo-url> tutorials
cd tutorials
./setup.sh
```

Then carefully restore your working code from backup.

---

## Still Stuck?

### Use the Getting Unstuck Guide

Follow the systematic 5-step process: [Getting Unstuck](./getting-unstuck.md)

### Check the FAQ

Common questions answered: [FAQ](./FAQ.md)

### Ask Your AI Assistant

Remember to include `.cursorrules` context:

```
@.cursorrules

I've tried troubleshooting but still stuck.

Problem: [describe issue]
Error: [paste error]
What I tried: [list attempts]
Expected: [what should happen]
Actual: [what's happening]

According to the project guidelines, what should I check next?
```

### Create a GitHub Issue

Use the minimal reproducible example template in the [Getting Unstuck Guide](./getting-unstuck.md#create-a-minimal-reproducible-example).

---

**Remember:** Every error is a learning opportunity. Debugging is a skill that improves with practice. You've got this! 🚀
