# Lab 2: Troubleshooting Guide

Common errors in multi-agent systems and how to fix them.

## Table of Contents

- [Coordinator Errors](#coordinator-errors)
- [Agent Communication Errors](#agent-communication-errors)
- [State Management Errors](#state-management-errors)
- [Specialization Errors](#specialization-errors)
- [Testing Errors](#testing-errors)
- [Import and Setup Errors](#import-and-setup-errors)

---

## Coordinator Errors

### Error: "Coordinator waiting forever, no response"

**What it means:** Coordinator sent message to worker but never received response.

**Why it happens:**
- Worker crashed before sending response
- Worker sent response to wrong recipient
- Message protocol not implemented correctly

**How to fix:**

1. **Check worker executed:**
```bash
grep "task_started.*research" .agent_logs/agent.log
grep "task_completed.*research" .agent_logs/agent.log
# If no task_completed, worker crashed
```

2. **Add timeout:**
```python
def delegate(self, agent, action, payload, timeout=30):
    try:
        result = agent.execute(action, payload)
        return result
    except Timeout Error:
        return Response(status="error", error="Agent timeout")
```

3. **Ensure worker sends response:**
```python
class WorkerAgent:
    def execute(self, action, payload):
        try:
            result = self._do_work(action, payload)
            return Response(status="success", payload=result)
        except Exception as e:
            # Always return response, even on error!
            return Response(status="error", error=str(e))
```

**Ask Your AI:**
```
@.cursorrules @src/multi_agent/coordinator.py

My coordinator waits forever for worker response. The worker executes but doesn't return properly.

Show me how to implement timeout and ensure workers always respond.
```

---

### Error: "AttributeError: 'Coordinator' object has no attribute 'research'"

**What it means:** Coordinator trying to access agent that wasn't initialized.

**Why it happens:**
- Forgot to assign agents in `__init__`
- Typo in agent name

**How to fix:**

```python
class Coordinator:
    def __init__(self, shared_state):
        self.shared_state = shared_state
        
        # MUST initialize all agents!
        self.research = ResearchAgent(shared_state)
        self.data = DataAgent(shared_state)
        self.writer = WriterAgent(shared_state)
```

**Quick check:**
```python
coordinator = Coordinator(shared_state)
print(hasattr(coordinator, 'research'))  # Should be True
```

---

### Error: "Agents executing in wrong order"

**What it means:** Data agent runs before research agent completes.

**Why it happens:**
- Coordinator not waiting for previous agent to finish
- Using parallel execution incorrectly

**How to fix:**

```python
# BAD: Not waiting
def generate_report(self, query):
    self.research.gather_info(query)  # Starts, but don't wait!
    self.data.analyze()  # Runs immediately, no data yet!

# GOOD: Sequential execution
def generate_report(self, query):
    research_result = self.research.gather_info(query)  # Wait for completion
    if research_result.status != "success":
        return f"Research failed: {research_result.error}"
    
    data_result = self.data.analyze()  # Only runs after research complete
    # ... etc
```

---

## Agent Communication Errors

### Error: "Message missing required field 'message_id'"

**What it means:** Message doesn't follow protocol specification.

**Why it happens:**
- Forgot to include required fields
- Manual message construction without validation

**How to fix:**

```python
# BAD: Manual dict construction
message = {
    "to": "research",
    "action": "gather_info"
    # Missing: message_id, timestamp, from_agent, message_type
}

# GOOD: Use Message class
from src.multi_agent.message_protocol import Message

message = Message(
    from_agent="coordinator",
    to_agent="research",
    action="gather_info",
    payload={"query": query}
)
# Message class adds message_id, timestamp automatically
```

**Validation helper:**
```python
def validate_message(msg: dict) -> bool:
    required = ["message_id", "timestamp", "from_agent", "to_agent", "message_type"]
    return all(field in msg for field in required)
```

---

### Error: "KeyError: 'in_reply_to' when processing response"

**What it means:** Response message doesn't link to original request.

**Why it happens:**
- Response not including `in_reply_to` field
- Request `message_id` not being passed to worker

**How to fix:**

```python
# When sending request, save message_id
request_id = str(uuid.uuid4())
request = Message(
    message_id=request_id,
    from_agent="coordinator",
    to_agent="research",
    message_type="request",
    action="gather_info"
)

# Worker includes in_reply_to in response
response = Message(
    from_agent="research",
    to_agent="coordinator",
    message_type="response",
    in_reply_to=request_id,  # Link to original request
    payload={"findings": findings}
)
```

---

## State Management Errors

### Error: "KeyError: 'research_findings' in shared_state"

**What it means:** Trying to read state key that doesn't exist.

**Why it happens:**
- Research agent didn't write to state
- Key name mismatch (typo)
- Reading before writing

**How to fix:**

```python
# BAD: Assume key exists
findings = shared_state.get("research_findings")
for f in findings:  # Crashes if findings is None!
    process(f)

# GOOD: Check existence
findings = shared_state.get("research_findings", [])
if not findings:
    return "No research findings available"

for f in findings:
    process(f)
```

**Debug who wrote:**
```bash
grep "state_write.*research_findings" .agent_logs/agent.log
# Shows which agent (if any) wrote this key
```

---

### Error: "[Errno 2] No such file or directory: '.agent_state/shared_state.json'"

**What it means:** State directory doesn't exist.

**Why it happens:**
- First run, directory not created
- Directory was deleted

**How to fix:**

```bash
# Create directory
mkdir -p .agent_state

# Or in code
from pathlib import Path

state_dir = Path(".agent_state")
state_dir.mkdir(exist_ok=True)
```

**Update SharedState __init__:**
```python
class SharedState:
    def __init__(self, state_dir: str = ".agent_state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(exist_ok=True)  # Create if missing
        # ... rest of init
```

---

### Error: "State changes lost between agents"

**What it means:** Agent A writes to state, Agent B can't see it.

**Why it happens:**
- Agent B reading cached state instead of file
- File writes not flushing
- Race condition (both reading at same time)

**How to fix:**

```python
# BAD: Caching state
class BadAgent:
    def __init__(self, shared_state):
        self.cached_state = shared_state.get_all()  # Cached at init!
    
    def work(self):
        # Uses stale cache
        data = self.cached_state.get("findings")

# GOOD: Fresh reads
class GoodAgent:
    def __init__(self, shared_state):
        self.shared_state = shared_state  # Store reference, not data
    
    def work(self):
        # Fresh read every time
        data = self.shared_state.get("findings")
```

---

## Specialization Errors

### Error: "Research agent calling calculate tool"

**What it means:** Agent using tools outside its specialization.

**Why it happens:**
- Agent has access to all tools (not filtered)
- System prompt not enforcing boundaries

**How to fix:**

1. **Register only relevant tools:**
```python
class ResearchAgent:
    def __init__(self):
        # Only register research tools
        self.tools = {
            "web_search": web_search,
            "read_file": read_file
        }
        # NOT: calculate, format_markdown, etc.
```

2. **Enforce in system prompt:**
```text
You are a Research Specialist.

TOOLS AVAILABLE:
- web_search: Search for information
- read_file: Read documents

IMPORTANT: You ONLY gather information. If you need calculations, 
respond "I can gather the data, but analysis requires the Data Agent."
```

---

### Error: "Agent output includes analysis when it should only gather data"

**What it means:** Research agent analyzing instead of just gathering.

**Why it happens:**
- System prompt not clear about boundaries
- LLM interpreting task too broadly

**How to fix:**

```python
# Update system prompt with explicit DON'Ts
system_prompt = """
You are a Research Specialist.

Your job: Gather information, cite sources.

YOU DO:
- Search for data
- Extract facts
- Provide citations

YOU DO NOT:
- Analyze trends (Data Agent's job)
- Calculate growth rates (Data Agent's job)
- Write reports (Writer Agent's job)
- Interpret findings (Data Agent's job)

Output format: List of findings with sources only.
"""
```

**Test for role adherence:**
```python
def test_research_agent_stays_in_role():
    agent = ResearchAgent()
    result = agent.gather_info("EV market trends")
    
    # Should NOT contain analysis keywords
    forbidden = ["indicates", "suggests", "trend shows", "growth rate"]
    output = str(result).lower()
    for phrase in forbidden:
        assert phrase not in output, f"Research agent is analyzing (found '{phrase}')"
```

---

## Testing Errors

### Error: "Tests pass individually but fail when run together"

**What it means:** Tests have shared state or side effects.

**Why it happens:**
- Shared state file not cleaned between tests
- Mock agents persisting across tests

**How to fix:**

```python
import pytest

@pytest.fixture(autouse=True)
def clean_state():
    """Clean shared state before each test."""
    state_file = Path(".agent_state/shared_state.json")
    if state_file.exists():
        state_file.unlink()
    
    yield  # Run test
    
    # Cleanup after test
    if state_file.exists():
        state_file.unlink()
```

**Or use unique state per test:**
```python
def test_something():
    shared_state = SharedState(state_dir=f".agent_state_test_{uuid.uuid4()}")
    # Each test has isolated state
```

---

### Error: "Integration test times out"

**What it means:** Full workflow takes too long or hangs.

**Why it happens:**
- LLM calls are slow
- Agent stuck in loop
- No timeout set

**How to fix:**

1. **Mock LLM for integration tests:**
```python
class MockLLM:
    def chat(self, messages):
        # Instant, deterministic responses
        return {"role": "assistant", "content": "Mock response"}

def test_integration():
    coordinator = Coordinator(llm=MockLLM())
    # Fast test without real LLM calls
```

2. **Add test timeouts:**
```python
@pytest.mark.timeout(10)  # Fail if takes >10 seconds
def test_workflow():
    coordinator.generate_report("test")
```

---

## Import and Setup Errors

### Error: "ModuleNotFoundError: No module named 'src.multi_agent'"

**What it means:** Python can't find the multi_agent package.

**Why it happens:**
- Running from wrong directory
- `src/multi_agent/__init__.py` missing
- PYTHONPATH not set

**How to fix:**

1. **Run from project root:**
```bash
cd /path/to/tutorials
python -m pytest tests/multi_agent/
```

2. **Check __init__.py exists:**
```bash
ls src/multi_agent/__init__.py
# Should exist
```

3. **Add to PYTHONPATH:**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python -m pytest tests/multi_agent/
```

---

### Error: "ImportError: cannot import name 'Message' from 'src.multi_agent'"

**What it means:** Message class not exported from package.

**Why it happens:**
- `__init__.py` doesn't export Message
- Import statement wrong

**How to fix:**

```python
# src/multi_agent/__init__.py
from .message_protocol import Message, MessageType

__all__ = [
    'Coordinator',
    'WorkerAgent',
    'Message',
    'MessageType',
    'SharedState'
]
```

**Then import like:**
```python
from src.multi_agent import Message  # Correct
# Not: from src.multi_agent.message_protocol import Message
```

---

## Quick Diagnostic Commands

```bash
# Check if all modules importable
python -c "from src.multi_agent import Coordinator, WorkerAgent, Message, SharedState; print('✓ All imports OK')"

# Check state directory
ls -la .agent_state/

# View recent logs
tail -20 .agent_logs/agent.log | jq '.'

# Count messages by type
grep "message_sent" .agent_logs/agent.log | wc -l
grep "message_received" .agent_logs/agent.log | wc -l

# Find errors in logs
grep -i "error" .agent_logs/agent.log | jq '.'

# Test specific agent
python -m pytest tests/multi_agent/test_coordinator.py -v

# Run with debug logging
pytest tests/multi_agent/ -v --log-cli-level=DEBUG
```

---

## Still Stuck?

1. **Check FAQ:** [FAQ.md](./FAQ.md) - 40+ common questions
2. **Systematic Debugging:** [Getting Unstuck Guide](./getting-unstuck.md)
3. **Ask AI:** Include `@.cursorrules` and error message
4. **Community:** Post in forums with logs and code snippet

**Remember:** Most multi-agent bugs are coordination or message flow issues. Use logs and trace IDs to debug systematically.

