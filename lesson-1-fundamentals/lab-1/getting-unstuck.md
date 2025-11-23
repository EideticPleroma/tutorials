# Getting Unstuck: A Systematic Debugging Guide

When you hit a roadblock, frustration is normal. But you're not alone - you have powerful AI assistants at your disposal. This guide teaches you a systematic approach to debugging that will serve you throughout your career.

## The 5-Step Debugging Process

### Step 1: Ask Your AI Assistant (Do This First!)

Your AI assistant can help debug if you give it proper context. The `.cursorrules` file contains all the project guidelines, coding standards, and debugging approaches.

#### For Cursor Users

1. Open a new chat (Cmd/Ctrl+L)
2. Type `@.cursorrules` to add project context
3. Describe your problem with specifics

**Example Prompt:**
```
@.cursorrules

I'm working on Exercise 2 (adding the file_search tool) and getting this error:

KeyError: 'search_files'

What I've done:
- Created src/agent/tools/file_search.py
- Added @registry.register decorator
- Written docstring with type hints

What I expected: Agent should call the tool
What happened: KeyError when agent tries to use it

According to the project guidelines, what am I missing?
```

#### For Continue Users

Continue automatically reads `.cursorrules`, so just ask:

```
I'm getting a KeyError: 'search_files' in Exercise 2.

Here's my file_search.py:
[paste your code]

And here's the error:
[paste full traceback]

What's wrong according to the project setup?
```

#### For Copilot Users

Copilot doesn't auto-read `.cursorrules`, so include relevant context:

```
I'm following the lesson-1-fundamentals tutorial. The project uses:
- Python with decorators for tool registration
- Ollama for local LLM
- Side-effect imports for decorator execution

My error: KeyError: 'search_files'
[paste code and error]

What am I missing?
```

#### For Manual AI Consultation (ChatGPT, Claude, etc.)

1. Open `.cursorrules` in your editor
2. Copy the relevant sections (Coding Standards, Agentic Development Rules)
3. Paste into your AI chat along with your problem

**Template:**
```
I'm working on an Agentic AI tutorial project. Here are the guidelines:

[Paste relevant .cursorrules sections]

My problem:
- Exercise: [which one]
- Error: [exact error message]
- What I tried: [your attempts]
- Expected behavior: [what should happen]
- Actual behavior: [what's happening]

Please help me debug this following the project's guidelines.
```

### What to Include in Your Debug Request

**Always provide:**
1. Which exercise you're on
2. Exact error message (full traceback)
3. What you expected vs. what happened
4. Recent changes you made
5. Code snippets (relevant sections only)

**Good Example:**
```
Exercise: 2 (Adding Tools)
Error: ModuleNotFoundError: No module named 'src.agent.tools.file_search'

Expected: Agent imports my tool and registers it
Actual: Import fails

Recent changes:
- Created src/agent/tools/file_search.py
- Added import in simple_agent.py: "from .tools import file_search"

Code snippet from simple_agent.py line 9:
from .tools import file_search  # noqa: F401

Question: Why can't Python find my module?
```

**Bad Example:**
```
It doesn't work. Help!
```

---

## Step 2: Enable Debug Mode

Sometimes you need to see what's happening inside the agent loop.

### Option A: Enable Verbose Logging

Add to the top of `src/agent/simple_agent.py`:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Option B: Add Strategic Print Statements

**In `simple_agent.py`, add these debug prints:**

```python
def chat(self, user_input: str) -> str:
    print(f"\n=== DEBUG: User Input ===")
    print(f"{user_input}")
    
    self.messages.append({"role": "user", "content": user_input})
    
    print(f"\n=== DEBUG: Tool Schemas Being Sent ===")
    schemas = registry.get_schemas()
    for schema in schemas:
        print(f"  - {schema['function']['name']}")
    
    # First call to LLM
    response = ollama.chat(
        model=config.model_name,
        messages=self.messages,
        tools=schemas,
        options={"temperature": config.temperature}
    )
    
    print(f"\n=== DEBUG: LLM Response ===")
    print(f"Has tool_calls: {response['message'].get('tool_calls') is not None}")
    if response['message'].get('tool_calls'):
        for tc in response['message']['tool_calls']:
            print(f"  - Tool: {tc['function']['name']}")
            print(f"  - Args: {tc['function']['arguments']}")
```

### Option C: Use the Debug Script

Run the provided debug helper:

```bash
python scripts/debug_agent.py
```

This will show:
- All registered tools
- System prompt being used
- Ollama connection status
- Model availability

---

## Step 3: Systematic Diagnosis

Work through this checklist systematically:

### Is Ollama Running?

```bash
# Check if Ollama is responsive
curl localhost:11434

# Expected output: "Ollama is running"
# If it hangs or errors: Ollama is not running
```

**Fix if not running:**
```bash
ollama serve &
```

### Is the Model Available?

```bash
ollama list

# Look for: llama3.3:8b
# If missing: ollama pull llama3.3:8b
```

### Are Your Tools Registered?

**Quick Test Script** (save as `test_registry.py`):

```python
from src.agent.tool_registry import registry
from src.agent import simple_agent  # This triggers imports

print("Registered tools:")
for schema in registry.get_schemas():
    print(f"  - {schema['function']['name']}")
    print(f"    Description: {schema['function']['description']}")
```

Run it:
```bash
python test_registry.py
```

Expected: Your custom tools appear in the list
If missing: Your tool isn't being imported

### Is Your Import Correct?

**Check these locations:**

1. **Tool file exists:**
   ```bash
   ls -la src/agent/tools/file_search.py
   ```

2. **`__init__.py` exists:**
   ```bash
   ls -la src/agent/tools/__init__.py
   ```

3. **Import is in `simple_agent.py`:**
   ```bash
   grep "file_search" src/agent/simple_agent.py
   ```
   
   Should see: `from .tools import file_search  # noqa: F401`

### Is Your System Prompt Causing Issues?

**Test with minimal prompt:**

Temporarily replace your system prompt in `agent_config.py`:

```python
system_prompt: str = """You are a helpful assistant with access to tools.
Use tools when appropriate."""
```

Run agent again. If it works now, your prompt was the issue.

---

## Step 4: Rollback Strategies

Sometimes you need to undo changes. Here's how:

### Strategy 1: Git Reset (Safe)

See what changed:
```bash
git status
git diff
```

Undo uncommitted changes to a file:
```bash
git checkout -- path/to/file.py
```

Go back to last commit:
```bash
git reset --hard HEAD
```

Go back to specific commit:
```bash
git log --oneline  # Find the commit hash
git reset --hard <commit-hash>
```

### Strategy 2: Comment Out Changes

Instead of deleting, comment out your new code:

```python
# My new code (not working yet)
# @registry.register
# def my_tool():
#     pass

# Old working code below...
```

This lets you compare working vs. not-working states.

### Strategy 3: Start Exercise Over

1. Check the exercise guide for the complete solution approach
2. Create a new file (e.g., `file_search_v2.py`)
3. Implement step-by-step, testing after each change
4. Compare with your original attempt

### Strategy 4: Nuclear Option (Fresh Clone)

When everything is broken:

```bash
cd ..
mv tutorials tutorials_broken
git clone <repository-url> tutorials
cd tutorials
./setup.sh
```

Then carefully port over your working code.

---

## Step 5: Ask the Community

If you're still stuck after trying the above:

### Create a Minimal Reproducible Example

**Good Bug Report Structure:**

```markdown
## Problem Summary
Brief description of the issue

## Environment
- OS: Windows 11 WSL2 / macOS / Linux
- Python: 3.x.x
- Ollama: x.x.x
- Model: llama3.3:8b

## Steps to Reproduce
1. Created file_search.py with [code]
2. Added import to simple_agent.py
3. Ran `python -m src.agent.simple_agent`
4. Asked "Find Python files in tests/"

## Expected Behavior
Agent should call file_search tool and return results

## Actual Behavior
KeyError: 'search_files'

## Error Message
[Full traceback here]

## What I've Tried
- Checked __init__.py exists
- Verified import in simple_agent.py
- Ran test_registry.py - tool doesn't appear
- Asked AI assistant - suggestion didn't work

## Code
[Relevant code snippets]
```

### Where to Get Help

**Option 1: GitHub Issues**

Create an issue on the tutorial repository with the template above.

**Option 2: AI Assistant (Again)**

Sometimes rephrasing helps:

```
I'm still stuck on [problem] after trying:
1. [what you tried]
2. [what happened]

Here's my complete code:
[paste everything relevant]

Can you spot what I'm missing?
```

**Option 3: Check Existing Issues**

Search GitHub issues for similar problems:
```bash
# In browser:
https://github.com/<repo>/issues?q=is%3Aissue+KeyError
```

---

## Common "Stuck" Patterns

### "I Changed Something and Now Nothing Works"

**Quick fix:**
```bash
git diff  # See what changed
git checkout -- .  # Undo ALL changes (careful!)
```

**Better approach:**
```bash
git diff  # Review changes
git checkout -- file1.py  # Undo specific file
# Keep debugging with other changes intact
```

### "Tests Worked Yesterday, Fail Today"

**Possible causes:**
1. Model updated (rare): `ollama pull llama3.3:8b` might have gotten a new version
2. Prompt changed: Check git diff on agent_config.py
3. Probabilistic failure: Run 5 times to check consistency
4. Environment issue: Restart terminal, reactivate venv

**Quick fix:**
```bash
# Restart everything
deactivate  # Exit venv
source venv/bin/activate  # Re-enter venv
python -m pytest tests/  # Run tests
```

### "Error Message Makes No Sense"

**Strategy:**
1. Copy entire error message
2. Ask AI: "Explain this error in the context of Python tool registration"
3. Search GitHub issues for the error
4. Break the error down: What's the last line? What file?

### "Following Tutorial Exactly, Still Broken"

**Possible causes:**
1. Typo in filename (file_search.py vs filesearch.py)
2. Wrong directory level
3. Missed a step in setup
4. Platform difference (Windows vs Linux paths)

**Quick check:**
```bash
# Verify file structure matches tutorial
tree src/agent/tools/
# Should show:
# src/agent/tools/
# ├── __init__.py
# └── file_search.py
```

---

## Prevention: Staying Unstuck

### Habit 1: Commit Often

After each working step:
```bash
git add .
git commit -m "Exercise 2: Added file_search tool (working)"
```

Now you always have a safe rollback point.

### Habit 2: Test Immediately

Don't write 50 lines then test. Write 5 lines, test, repeat.

### Habit 3: Read Error Messages Carefully

Error messages tell you exactly what's wrong:
```
ModuleNotFoundError: No module named 'src.agent.tools.file_search'
                                      ^^^^^^^^^^^^^^^^^^^^^^^^^
                                      This exact module path failed
```

### Habit 4: Use the AI Assistant Proactively

Don't wait until stuck. Ask before implementing:
```
I'm about to implement file_search tool. 
According to @.cursorrules, what are the critical steps I must not forget?
```

### Habit 5: Keep Notes

When you solve a problem, document it:
```markdown
## Problem: Tool not registering
**Solution:** Forgot to import in simple_agent.py
**Lesson:** Decorators only run when module is imported
**Date:** 2024-01-15
```

---

## Remember

**Getting stuck is part of learning.** Every senior engineer you admire has been stuck thousands of times. The difference is they've developed systematic debugging skills.

This guide teaches you those skills. Use it, practice it, and soon you'll debug like a pro.

**When in doubt:**
1. Ask your AI assistant (with `.cursorrules` context)
2. Enable debug mode
3. Work through the checklist
4. Rollback if needed
5. Ask the community

**You've got this!** 🚀

---

**Next Steps:**
- Return to your exercise: [Lab Exercises](./exercises/)
- Check specific errors: [Troubleshooting Guide](./troubleshooting.md)
- Common questions: [FAQ](./FAQ.md)

