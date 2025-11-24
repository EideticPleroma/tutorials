# Lab 2: Setup Guide

This guide helps you set up your environment for Tutorial 2: Multi-Agent Systems.

## Prerequisites

**You must complete Tutorial 1 first.** Lab 2 builds on:
- Tutorial 1's agent implementation
- Existing tool registry
- O.V.E. testing framework
- Your working Python + Ollama environment

**If you haven't completed Tutorial 1:** Go to [Lab 1 Setup](../../../lesson-1-fundamentals/lab-1/setup-guide.md)

## Quick Verification

Check if you're ready:

```bash
# 1. Ollama running?
curl localhost:11434
# Should return: "Ollama is running"

# 2. Python environment active?
python --version
# Should show: Python 3.10+

# 3. Can import Tutorial 1 code?
python -c "from src.agent.simple_agent import Agent; print('OK')"
# Should print: OK

# 4. Tests work?
python -m pytest tests/unit/ -v
# Should pass Tutorial 1 tests
```

**All working?** Skip to [Lab 2 Specific Setup](#lab-2-specific-setup)

**Something broken?** Continue reading for detailed setup.

---

## Lab 2 Specific Setup

### Step 1: Verify Directory Structure

Tutorial 2 code lives alongside Tutorial 1:

```
tutorials/
├── src/
│   ├── agent/           (Tutorial 1 - already exists)
│   └── multi_agent/     (Tutorial 2 - new)
├── tests/
│   ├── unit/            (Tutorial 1 - already exists)
│   └── multi_agent/     (Tutorial 2 - new)
└── lesson-2-multi-agent/
    └── docs/
        ├── tutorial-2/  (Concepts you just read)
        └── lab-2/       (This guide)
```

**Verify:**
```bash
# From project root
ls src/multi_agent/
# Should show: __init__.py, coordinator.py, worker_base.py, etc.

ls tests/multi_agent/
# Should show: __init__.py, test_coordinator.py, etc.
```

**Missing directories?** They should have been created during Tutorial 2 setup. If not:
```bash
mkdir -p src/multi_agent/specialized
mkdir -p tests/multi_agent
```

### Step 2: Install Additional Dependencies

Tutorial 2 has no new external dependencies! Everything uses the same stack:
- Python 3.10+
- Ollama (already installed)
- pytest (already installed)
- requests (already installed)

**Verify:**
```bash
pip list | grep -E "pytest|requests"
# Should show both packages
```

### Step 3: Verify Tool Registry

Before starting Lab 2, verify all Tutorial 1 tools are registered and available:

```bash
python -c "from src.agent.tool_registry import registry; tools = [t['function']['name'] for t in registry.get_schemas()]; print('Registered tools:', tools); assert 'search_files' in tools, 'search_files missing!'; assert 'read_file' in tools, 'read_file missing!'; assert 'calculate' in tools, 'calculate missing!'; print('✓ All Tutorial 2 tools available')"
```

**Expected output:**
```
Registered tools: ['calculate', 'get_weather', 'read_file', 'list_directory', 'search_files']
✓ All Tutorial 2 tools available
```

**Why this matters:** Tutorial 2 agents filter Tutorial 1's tool registry. If tools are missing or misnamed, agents will have zero tools and fail silently.

**Common issues:**
- Tools not imported in `src/agent/simple_agent.py`
- Tool files missing from `src/agent/tools/`
- Tool name mismatch (e.g., looking for `file_search` but it's registered as `search_files`)

**See:** [Tool Bridge Documentation](../../tutorial-2/concepts/tool-bridge.md) for complete tool reference.

### Step 4: Create State Directory

Multi-agent systems use shared state:

```bash
# From project root
mkdir -p .agent_state
mkdir -p .agent_logs
```

**Add to `.gitignore` (if not already):**
```bash
echo ".agent_state/" >> .gitignore
echo ".agent_logs/" >> .gitignore
```

### Step 5: Verify Multi-Agent Imports

```bash
python -c "
from src.multi_agent import Coordinator, WorkerAgent, Message
print('✓ Multi-agent imports work')
"
```

**Error?** See [Troubleshooting](#troubleshooting-setup) below.

### Step 6: Run Multi-Agent Tests

```bash
# Run all multi-agent tests
python -m pytest tests/multi_agent/ -v

# Expected: Some tests may be marked as TODO/skipped
# This is normal - you'll implement them in Lab 2
```

### Step 7: Configure AI Assistant

**For Cursor Users:**
1. `.cursorrules` should already be in your project root
2. Verify it's up to date: Should mention "Tutorial 2" and "multi-agent"
3. When asking questions, use: `@.cursorrules @src/multi_agent/coordinator.py`

**For VS Code + Continue Users:**
1. Continue reads `.cursorrules` automatically
2. No additional setup needed

**For VS Code + Cline Users:**
1. Cline reads `.cursorrules` automatically
2. No additional setup needed

**For GitHub Copilot Users:**
1. Copilot doesn't read `.cursorrules`
2. Include context manually in comments:
   ```python
   # Context: This is a coordinator agent for a multi-agent system
   # It delegates to research, data, and writer agents sequentially
   # Suggest implementation for delegate() method
   ```

---

## IDE Configuration for Multi-Agent Debugging

### Recommended Settings

**Enable Structured Logging:**

Create `.vscode/settings.json` (or update existing):
```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests",
    "-v",
    "--log-cli-level=INFO"
  ],
  "files.associations": {
    "*.json": "jsonc"  // For viewing agent logs
  }
}
```

### Debugging Multi-Agent Workflows

**Option 1: Structured Logs**
```python
# In your agent code
import logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
    handlers=[
        logging.FileHandler('.agent_logs/agent.log'),
        logging.StreamHandler()
    ]
)
```

**Option 2: Trace Viewer (Recommended)**
```bash
# Watch logs in real-time
tail -f .agent_logs/agent.log | jq '.'

# View specific trace
python scripts/view_trace.py <trace_id>
```

**Option 3: IDE Debugger**
Set breakpoints in:
- `src/multi_agent/coordinator.py` → `delegate()` method
- `src/multi_agent/worker_base.py` → `execute()` method
- Test files to step through workflows

---

## Environment Variables

Tutorial 2 uses the same environment as Tutorial 1. No new variables needed.

**Verify:**
```bash
# Should show Ollama URL (usually http://localhost:11434)
echo $OLLAMA_HOST
```

**If not set:**
```bash
export OLLAMA_HOST=http://localhost:11434
# Add to ~/.bashrc or ~/.zshrc to persist
```

---

## Troubleshooting Setup

### Issue: "Cannot import Coordinator"

**Error:**
```
ImportError: cannot import name 'Coordinator' from 'src.multi_agent'
```

**Solution:**
1. Check file exists: `ls src/multi_agent/coordinator.py`
2. Check `__init__.py` exports it:
   ```python
   # src/multi_agent/__init__.py
   from .coordinator import Coordinator
   ```
3. Try: `python -c "import src.multi_agent; print(dir(src.multi_agent))"`

### Issue: "Ollama connection refused"

**Error:**
```
requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionRefusedError(111, 'Connection refused'))
```

**Solution:**
1. Start Ollama: `ollama serve` (in separate terminal)
2. Verify: `curl localhost:11434`
3. Check port: `netstat -an | grep 11434`

### Issue: Tests fail with "No module named 'src'"

**Error:**
```
ModuleNotFoundError: No module named 'src'
```

**Solution:**
1. Run from project root, not subdirectory
2. Add project to PYTHONPATH:
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```
3. Or install in editable mode:
   ```bash
   pip install -e .
   ```

### Issue: ".cursorrules not being read"

**Symptom:** AI gives generic answers, doesn't follow project conventions

**Solution:**
1. Cursor: Use `@.cursorrules` explicitly in prompts
2. Continue/Cline: Should read automatically, check settings
3. Verify file exists: `cat .cursorrules | head`
4. For Copilot: Include context in code comments instead

---

## Performance Tips

### Speed Up Testing

```bash
# Run only fast tests (skip integration)
python -m pytest tests/multi_agent/ -m "not slow" -v

# Run in parallel (install pytest-xdist)
pip install pytest-xdist
python -m pytest tests/multi_agent/ -n auto
```

### Optimize Ollama

```bash
# Use smaller model for faster iteration
ollama pull llama3.1:8b  # Instead of 70b

# Increase concurrent requests
export OLLAMA_NUM_PARALLEL=4
```

### Faster State I/O

For development, consider using in-memory state instead of files:
```python
# In tests only!
shared_state = SharedState(state_dir=":memory:")
```

---

## Verification Checklist

Before starting Lab 2 exercises:
- [ ] Tutorial 1 completed and working
- [ ] Ollama running (`curl localhost:11434` works)
- [ ] Python environment active
- [ ] Tool registry verified (search_files, read_file, calculate available)
- [ ] Can import `Coordinator`, `WorkerAgent`, `Message`
- [ ] Tests directory exists: `tests/multi_agent/`
- [ ] State directory exists: `.agent_state/`
- [ ] AI assistant configured and responding to project context
- [ ] Read at least Tutorial 2 concepts (Pages 1-4)

**All checked?** You're ready! 

👉 **[Start Exercise 1: Build a Coordinator Agent](./exercises/01-coordinator-agent.md)**

---

## Additional Resources

- [Tutorial 1 Setup Guide](../../../lesson-1-fundamentals/lab-1/setup-guide.md) - If environment needs repair
- [Lab 2 FAQ](./FAQ.md) - Common setup questions
- [Troubleshooting](./troubleshooting.md) - Multi-agent specific issues

