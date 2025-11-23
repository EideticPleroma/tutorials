# State Management

**Page 4 of 9** | [← Previous: Agent Communication](./agent-communication.md) | [Next: Designing Agent Teams →](../guides/designing-agent-teams.md) | [↑ Reading Guide](../READING_GUIDE.md)

Agents need to remember things. A single agent keeps state in memory (conversation history, context). But what happens when multiple agents need to access the same information? This is the state management problem.

## Shared vs. Isolated Agent State

### Isolated State (Simple)

Each agent maintains its own state, no sharing.

```python
class ResearchAgent:
    def __init__(self):
        self.conversation_history = []  # Only this agent sees this
        self.sources_found = []
        
class DataAgent:
    def __init__(self):
        self.conversation_history = []  # Different history
        self.calculations_cache = {}
```

**Characteristics:**
- ✅ Simple: No coordination needed
- ✅ Safe: No race conditions or conflicts
- ✅ Debuggable: Each agent's state is independent
- ❌ Wasteful: Duplicating data across agents
- ❌ Inconsistent: Agents can have different views of the world

**Use when:** Agents don't need to reference each other's work

### Shared State (Complex but Powerful)

Multiple agents access common data.

```python
class SharedState:
    def __init__(self):
        self.task_context = {}      # All agents can read
        self.research_findings = []  # Research writes, Data reads
        self.final_report = None     # Writer writes, Coordinator reads

# All agents have access to shared_state
coordinator = Coordinator(shared_state)
research = ResearchAgent(shared_state)
data = DataAgent(shared_state)
```

**Characteristics:**
- ✅ Efficient: Single source of truth
- ✅ Consistent: All agents see same data
- ✅ Collaborative: Agents build on each other's work
- ❌ Complex: Need to manage access and conflicts
- ❌ Risky: One agent's bug can corrupt state for all
- ❌ Debugging: Harder to trace who changed what

**Use when:** Agents need to build on shared context

## File-Based State (Tutorial 2 Approach)

For Tutorial 2, we use a simple file-based state system. It's easy to understand and debug.

### Why Files?

**Alternatives:**
1. **In-Memory Dictionary** - Fast but lost on crash, hard to inspect
2. **Database (SQLite, Redis)** - Overkill for learning, adds dependencies
3. **Files (JSON)** - ✅ Simple, inspectable, persistent, no dependencies

### Implementation

```python
# src/multi_agent/shared_state.py
import json
import os
from pathlib import Path
from typing import Any, Optional
import fcntl  # File locking on Unix
import time

class SharedState:
    """
    File-based shared state for multi-agent systems.
    
    Uses JSON for simplicity and human-readability.
    Implements file locking to prevent race conditions.
    """
    
    def __init__(self, state_dir: str = ".agent_state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(exist_ok=True)
        self.state_file = self.state_dir / "shared_state.json"
        self._init_state()
    
    def _init_state(self):
        """Initialize state file if it doesn't exist."""
        if not self.state_file.exists():
            self._write({"tasks": {}, "context": {}, "results": {}})
    
    def get(self, key: str, default: Any = None) -> Any:
        """Read a value from shared state."""
        state = self._read()
        return state.get(key, default)
    
    def set(self, key: str, value: Any):
        """Write a value to shared state."""
        state = self._read()
        state[key] = value
        self._write(state)
    
    def update(self, updates: dict):
        """Update multiple keys at once."""
        state = self._read()
        state.update(updates)
        self._write(state)
    
    def _read(self) -> dict:
        """Read state with file locking."""
        with open(self.state_file, 'r') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)  # Shared read lock
            try:
                return json.load(f)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    
    def _write(self, state: dict):
        """Write state with file locking."""
        with open(self.state_file, 'w') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Exclusive write lock
            try:
                json.dump(state, f, indent=2)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
```

### Usage Example

```python
# Coordinator sets up task context
shared_state = SharedState()
shared_state.set("current_task", {
    "task_id": "rpt_001",
    "query": "EV market analysis",
    "deadline": "2023-11-22T15:00:00"
})

# Research agent writes findings
shared_state.set("research_findings", [
    {"fact": "EV sales: 10.5M", "source": "IEA"},
    {"fact": "Tesla share: 65%", "source": "Cox"}
])

# Data agent reads research and writes analysis
findings = shared_state.get("research_findings")
analysis = analyze_data(findings)
shared_state.set("data_analysis", analysis)

# Writer agent reads both to create report
findings = shared_state.get("research_findings")
analysis = shared_state.get("data_analysis")
report = create_report(findings, analysis)
shared_state.set("final_report", report)

# Coordinator retrieves final report
report = shared_state.get("final_report")
return report
```

### Inspecting State (Debugging)

```bash
# View current state
cat .agent_state/shared_state.json

# Watch state changes in real-time
watch -n 1 cat .agent_state/shared_state.json

# Pretty-print with jq
cat .agent_state/shared_state.json | jq '.'
```

## State Consistency Challenges

### Challenge 1: Race Conditions

**Problem:** Two agents write to the same key simultaneously.

```python
# Agent 1 reads
count = shared_state.get("processed_items", 0)  # Gets 5

# Agent 2 reads (before Agent 1 writes)
count = shared_state.get("processed_items", 0)  # Also gets 5

# Agent 1 writes
shared_state.set("processed_items", count + 1)  # Sets to 6

# Agent 2 writes
shared_state.set("processed_items", count + 1)  # Also sets to 6 (should be 7!)
```

**Solution:** File locking (already implemented in our SharedState class).

### Challenge 2: Stale Reads

**Problem:** Agent caches state and doesn't see updates.

```python
class BadAgent:
    def __init__(self, shared_state):
        # DON'T DO THIS: Caching state at init
        self.task_info = shared_state.get("current_task")
    
    def do_work(self):
        # Uses stale task_info - misses updates!
        print(self.task_info)
```

**Solution:** Always read fresh state when needed.

```python
class GoodAgent:
    def __init__(self, shared_state):
        self.shared_state = shared_state  # Store reference, not data
    
    def do_work(self):
        # Fresh read every time
        task_info = self.shared_state.get("current_task")
        print(task_info)
```

### Challenge 3: Partial Writes

**Problem:** Agent writes incomplete data due to crash.

```python
# Agent starts writing complex object
shared_state.set("analysis", {
    "trends": calculate_trends(),  # Success
    "forecasts": calculate_forecasts(),  # Crashes here!
    "recommendations": calculate_recs()  # Never runs
})
```

**Solution:** Write complete objects atomically.

```python
# Prepare complete object first
analysis = {}
analysis["trends"] = calculate_trends()
analysis["forecasts"] = calculate_forecasts()
analysis["recommendations"] = calculate_recs()

# Write once, complete
shared_state.set("analysis", analysis)
```

## When to Use Shared State

### ✅ Good Use Cases

1. **Task Context:** All agents need to know the user's original request
2. **Sequential Workflows:** Data agent needs research agent's output
3. **Progress Tracking:** Coordinator monitors completion status
4. **Configuration:** All agents share common settings

### ❌ Bad Use Cases (Use Messages Instead)

1. **Agent-to-Agent Communication:** Use message protocol, not shared state
2. **Temporary Calculations:** Keep in agent's local memory
3. **Large Data:** Pass references through messages, not full data in state
4. **Frequent Updates:** File I/O is slow; use messages for high-frequency data

## Shared State Patterns

### Pattern 1: Task Context

Coordinator sets context, workers read it.

```python
# Coordinator
shared_state.set("task_context", {
    "task_id": "rpt_001",
    "user_query": "Analyze EV market",
    "max_sources": 5,
    "deadline": "2023-11-22T15:00:00"
})

# Workers read context
class ResearchAgent:
    def gather_info(self):
        context = self.shared_state.get("task_context")
        max_sources = context["max_sources"]
        # Use in search...
```

### Pattern 2: Incremental Build

Each agent adds to shared state.

```python
# Research agent
shared_state.set("research_findings", findings_list)

# Data agent adds analysis
analysis = analyze(shared_state.get("research_findings"))
shared_state.set("data_analysis", analysis)

# Writer agent combines everything
report = create_report(
    shared_state.get("research_findings"),
    shared_state.get("data_analysis")
)
shared_state.set("final_report", report)
```

### Pattern 3: Status Dashboard

Agents report progress, coordinator monitors.

```python
# Each agent updates its status
shared_state.update({
    "agent_status": {
        "research": "completed",
        "data": "in_progress", 
        "writer": "waiting"
    }
})

# Coordinator checks status
status = shared_state.get("agent_status")
if all(s == "completed" for s in status.values()):
    print("All agents done!")
```

---

## 🎯 Common Pitfalls & Solutions

### Pitfall 1: Using State as a Message Queue

```python
# BAD: Using state for messages
shared_state.set("message_to_data_agent", "Please analyze this")
# Data agent polls state looking for messages - SLOW!
```

**Solution:** Use the message protocol for communication, state for persistent data.

### Pitfall 2: Storing Everything in State

```python
# BAD: Storing 10MB of research data in state
shared_state.set("all_research_data", huge_list_of_articles)
# File becomes bloated, slow to read/write
```

**Solution:** Store large data in separate files, put file paths in state.

```python
# GOOD: Store reference, not data
data_file = save_research_data(findings)  # Save to .agent_state/research_001.json
shared_state.set("research_data_file", data_file)
```

### Pitfall 3: Not Handling Missing Keys

```python
# BAD: Assumes key exists
findings = shared_state.get("research_findings")
for f in findings:  # Crashes if None!
    process(f)
```

**Solution:** Always provide defaults and check.

```python
# GOOD: Safe access
findings = shared_state.get("research_findings", [])
if findings:
    for f in findings:
        process(f)
else:
    log_warning("No research findings available")
```

---

## 🎯 Knowledge Check

**Question 1:** When should you use shared state vs. message passing?

<details>
<summary>Show Answer</summary>

**Use Shared State For:**
- Persistent data multiple agents need (task context, configuration)
- Results that need to be accessed multiple times
- Progress tracking and status monitoring
- Data that outlives individual messages

**Use Message Passing For:**
- Agent-to-agent communication
- Task delegation and responses
- Temporary data transfers
- High-frequency updates

**Rule of Thumb:** If it's **data**, use shared state. If it's **communication**, use messages.

**Example:**
```python
# Task context: Shared state (multiple agents read repeatedly)
shared_state.set("task_id", "rpt_001")

# Delegation: Message (one-time communication)
coordinator.send_message(research_agent, "gather_info", {...})

# Results: Shared state (writer needs to read research results)
shared_state.set("research_findings", findings)

# Status update: Message (coordinator needs immediate notification)
research_agent.send_message(coordinator, "task_complete", {...})
```
</details>

**Question 2:** What happens if two agents call `shared_state.set("result", ...)` at the same time?

<details>
<summary>Show Answer</summary>

**With our file-locking implementation:** Safe, but one overwrites the other.

**Sequence:**
1. Agent A acquires write lock, writes "result_A", releases lock
2. Agent B acquires write lock, writes "result_B", releases lock
3. Final state: `result = "result_B"` (Agent A's write is lost)

**This is still a problem!** File locking prevents corruption but doesn't prevent overwrites.

**Solutions:**

1. **Use namespaced keys:**
```python
shared_state.set("research_agent_result", result_A)
shared_state.set("data_agent_result", result_B)
# Both preserved
```

2. **Use lists for multiple values:**
```python
results = shared_state.get("results", [])
results.append(result_A)
shared_state.set("results", results)
# Requires read-modify-write locking (more complex)
```

3. **Coordinator manages writes:**
```python
# Agents send results via messages
# Only coordinator writes to state
# No conflicts possible
```

**Best Practice:** Design your state schema to avoid conflicts (namespaced keys, coordinator-managed writes).
</details>

**Question 3:** Design a state schema for the EV market report task (research → data → writer).

<details>
<summary>Show Example Schema</summary>

```json
{
  "task_context": {
    "task_id": "rpt_001",
    "user_query": "Analyze EV market trends",
    "created_at": "2023-11-22T10:00:00",
    "deadline": "2023-11-22T15:00:00"
  },
  
  "agent_status": {
    "research": "completed",
    "data": "in_progress",
    "writer": "waiting"
  },
  
  "research": {
    "status": "completed",
    "findings_file": ".agent_state/research_001.json",
    "sources_count": 5,
    "completed_at": "2023-11-22T10:15:00"
  },
  
  "data_analysis": {
    "status": "in_progress",
    "metrics": {
      "growth_rate": 55.2,
      "market_size": 10.5
    },
    "started_at": "2023-11-22T10:16:00"
  },
  
  "writer": {
    "status": "waiting"
  },
  
  "final_report": null
}
```

**Design Principles:**
1. **Namespaced:** Each agent has its own section
2. **Status tracking:** Easy to see progress
3. **Timestamps:** Track workflow timing
4. **File references:** Large data in separate files
5. **Null for pending:** Clear what's not ready yet
</details>

---

**Ready?** If you understand state management, you're ready for [Designing Agent Teams](../guides/designing-agent-teams.md) to learn how to architect multi-agent workflows.

**Page 4 of 9** | [← Previous: Agent Communication](./agent-communication.md) | [Next: Designing Agent Teams →](../guides/designing-agent-teams.md) | [↑ Reading Guide](../READING_GUIDE.md)

