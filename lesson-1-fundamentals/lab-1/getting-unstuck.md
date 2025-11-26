# Getting Unstuck: A Systematic Debugging Guide

[← Back to Lab 1](./README.md)

Getting stuck is part of the process. This guide provides a systematic approach to debugging agentic systems, updated for the modern AI tool stack (2024/2025).

---

## 🛡️ Prevention: Core Habits (Read This First)

The best way to debug is to avoid bugs in the first place. Adopt these 5 habits immediately:

### Habit 1: Commit Micro-Steps
Don't write 100 lines before committing. Commit after every *single* working component.
```bash
git add .
git commit -m "feat: add empty tool function"
# ... verify ...
git commit -m "feat: add tool logic"
```
*Why?* You can always `git revert` to the last working state in 1 second.

### Habit 2: Test Interactively
Don't just run the full test suite. Use a "REPL" mindset.
1. Write the tool function.
2. Call it manually in a separate script (`test_tool.py`).
3. Only then hook it up to the agent.

### Habit 3: Read Error Messages Aloud
Error messages in Python are surprisingly literal.
`ModuleNotFoundError: No module named 'src'` means Python literally cannot find the folder. It's rarely a ghost in the machine; it's usually a path issue.

### Habit 4: Proactive AI Consultation
Don't wait until you're broken. Ask **before** you build.
> "I'm about to implement the `read_file` tool. Based on `@.cursorrules`, what are the 3 most common mistakes students make here?"

---

## 🤖 The AI IDE Debugging Workflow

Your IDE is your primary debugger. Here's how to use it effectively depending on your tool.

### 1. Cursor (The Native Approach)
Cursor indexes your codebase. Use it to context-aware debug.

**The "Fix" Flow:**
1. Highlight the error message in the terminal.
2. Press `Cmd+K` (or `Ctrl+K`).
3. Type: "Fix this error based on `@simple_agent.py` logic."

**The "Context" Flow (Chat):**
1. Open Chat (`Cmd+L`).
2. Type: `@.cursorrules @src/agent/simple_agent.py I'm getting this KeyError...`
3. **Tip:** Cursor can see your open files. Keep the relevant file focused.

### 2. Windsurf (Cascade Flow)
Windsurf's "Cascade" understands deep context and flow.

**The Cascade Flow:**
1. Open Cascade.
2. Ask: "Trace the execution flow of `chat()` when I ask for weather. Where could the JSON parsing fail?"
3. Windsurf is excellent at *predictive* debugging—ask it "What happens if the tool output is empty?"

### 3. VS Code + Copilot / Continue
Standard VS Code setup requires more manual context management.

**The Explicit Context Flow:**
1. You must explicitly reference files.
2. **Copilot:** Open the file, highlight the broken code, ask in Chat.
3. **Continue:** Use `@file` to explicitly add `simple_agent.py` and `tool_registry.py` to context before asking about an error.

---

## 🔍 The 5-Step Debugging Process

If the AI didn't fix it instantly, follow this manual protocol:

### Step 1: Enable "X-Ray Mode" (Verbose Logging)
You can't fix what you can't see. Add print statements to `simple_agent.py` to see the *raw* LLM output.

```python
# In simple_agent.py -> chat()
print(f"DEBUG RAW RESPONSE: {response}") # SEE what the LLM actually sent
```
*90% of "Agent Bugs" are just the LLM outputting bad JSON or text instead of JSON.*

### Step 2: Check the Plumbing (Registry)
Is your tool actually registered?
Create a script `debug_registry.py`:
```python
from src.agent.tool_registry import registry
import src.agent.simple_agent # Force imports
print(registry.get_schemas())
```
If your tool isn't there, you forgot the `@register` decorator or the import side-effect.

### Step 3: Isolation Test
Does the function work *without* the Agent?
Call the function directly in python:
```python
from src.agent.tools.my_new_tool import my_tool
print(my_tool(arg="test"))
```
If this fails, it's a Python bug, not an Agent bug.

### Step 4: The "System Prompt" Reset
Did you confuse the LLM?
Temporarily simplify your system prompt to:
`"You are a helpful assistant. Use tools."`
If it works now, your complex prompt was confusing the model.

### Step 5: The Nuclear Option
If your environment is hopeless:
1. `deactivate` (Exit venv)
2. `rm -rf venv` (Delete venv)
3. `./setup.sh` (Fresh install)

---

## 🆘 Still Stuck?

### Constructing a Perfect Help Request
If you ask a human (or Discord), use this template to get an answer in minutes, not days.

**The "Unstuck" Template:**
> **Goal**: I'm trying to [Goal, e.g., add a Calculator tool].
> **Expectation**: Agent should call `calc(5, 5)`.
> **Reality**: Agent replies "I can't do math" text.
> **Logs**: Here is the raw JSON output: `[Paste Logs]`
> **Code**: Here is my decorator code: `[Paste Snippet]`
> **Tried**: I already tried [X] and [Y].

### Where to Go
- **GitHub Issues**: Check for existing tags `lesson-1`
- **Discord/Community**: Post your "Unstuck Template"

---

**Remember**: Debugging *is* the job. Every error is just a mismatch between your mental model and the machine's state. Align them, and the bug vanishes.
