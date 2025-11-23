# Lab 2: Frequently Asked Questions (FAQ)

Common questions about building multi-agent systems in Tutorial 2.

## Table of Contents

- [Setup & Prerequisites](#setup--prerequisites)
- [Coordinator Logic](#coordinator-logic)
- [Agent Communication](#agent-communication)
- [Specialization](#specialization)
- [State Management](#state-management)
- [Testing Multi-Agent Systems](#testing-multi-agent-systems)
- [Performance & Debugging](#performance--debugging)
- [Conceptual Questions](#conceptual-questions)
- [AI Assistant Usage](#ai-assistant-usage)

---

## Setup & Prerequisites

### Q: Do I need to complete Tutorial 1 first?

**Yes, absolutely.** Tutorial 2 builds directly on Tutorial 1:
- Uses the same agent base (`simple_agent.py`)
- Extends the tool registry
- Builds on O.V.E. testing
- Assumes you understand tool calling

**If you skip Tutorial 1:** You'll be confused by basic concepts like tool registration, system prompts, and agent loops.

### Q: Can I use a different LLM (GPT-4, Claude)?

**For learning**: Stick with Ollama + Llama 3.1 (tutorial's focus).
**For production**: Yes, but you'll need to adapt the API calls. The multi-agent patterns remain the same.

### Q: My imports fail: "cannot import name 'Coordinator'"

**Solution:**
1. Ensure `src/multi_agent/__init__.py` exports `Coordinator`
2. Run from project root: `python -m pytest`, not `cd tests && pytest`
3. Add to PYTHONPATH: `export PYTHONPATH="${PYTHONPATH}:$(pwd)"`

### Q: Do I need additional dependencies for Tutorial 2?

**No.** Tutorial 2 uses the same stack as Tutorial 1:
- Python 3.10+
- Ollama
- pytest
- requests

No new pip install required.

---

## Coordinator Logic

### Q: What's the difference between a coordinator and a regular agent?

**Regular Agent (Tutorial 1):**
- Receives user request
- Calls tools directly
- Returns result to user

**Coordinator (Tutorial 2):**
- Receives user request
- Delegates to worker agents (who call tools)
- Aggregates worker results
- Returns synthesized result to user

Think of it as: Agent = worker, Coordinator = manager.

### Q: Should the coordinator have tools?

**Generally no.** The coordinator's job is orchestration, not execution.

**Bad:**
```python
coordinator = Coordinator()
coordinator.tools = [web_search, calculate, format_markdown]  # Too many responsibilities!
```

**Good:**
```python
coordinator = Coordinator()
coordinator.research = ResearchAgent()  # Has web_search
coordinator.data = DataAgent()          # Has calculate
coordinator.writer = WriterAgent()      # Has format_markdown
```

**Exception:** Coordinator might have meta-tools like `evaluate_quality()` or `select_best_result()`.

### Q: How does the coordinator know which agent to call?

**Option 1: Fixed workflow (Tutorial 2 approach)**
```python
def generate_report(self, query):
    # Always: research → data → writer
    findings = self.research.gather_info(query)
    analysis = self.data.analyze(findings)
    report = self.writer.create_report(analysis)
```

**Option 2: Dynamic routing (advanced)**
```python
def route_task(self, task):
    if task.requires_web_search:
        return self.research
    elif task.requires_calculation:
        return self.data
    # ... etc
```

Tutorial 2 focuses on Option 1 (simpler, more predictable).

### Q: What if a worker agent fails?

**Coordinator should handle gracefully:**

```python
def delegate(self, agent, action, payload):
    try:
        result = agent.execute(action, payload)
        if result.status == "success":
            return result
        elif result.status == "partial":
            # Decide: is partial good enough?
            return result if result.confidence > 0.5 else self.retry(agent, action, payload)
    except TimeoutError:
        # Retry with longer timeout or fail gracefully
        return self.retry(agent, action, payload, timeout=60)
    except Exception as e:
        # Log and return error
        self.logger.error(f"Agent {agent.name} failed: {e}")
        return Response(status="error", error=str(e))
```

### Q: Should I retry failed tasks?

**Yes, but with limits:**
- Max 2-3 retries
- Use exponential backoff (wait 1s, 2s, 4s)
- After max retries, return error to user
- Log all retry attempts

**Don't:** Retry infinitely (creates infinite loops).

### Q: Can the coordinator run agents in parallel?

**Yes**, but Tutorial 2 starts with sequential for simplicity.

**Sequential (Exercise 1):**
```python
r = research.execute()  # Wait
d = data.execute()      # Wait
w = writer.execute()    # Wait
```

**Parallel (Exercise 4):**
```python
import concurrent.futures

with ThreadPoolExecutor() as executor:
    futures = [
        executor.submit(research.execute),
        executor.submit(data.execute)
    ]
    results = [f.result() for f in futures]
```

---

## Agent Communication

### Q: Why use messages instead of direct function calls?

**Direct calls (what you might think):**
```python
result = research_agent.gather_info(query)  # Simple!
```

**Problems:**
- Hard to log (what was sent?)
- Hard to debug (where did it fail?)
- Tight coupling (coordinator knows agent internals)
- Can't distribute across machines later

**Messages (what we use):**
```python
message = Message(
    from_agent="coordinator",
    to_agent="research",
    action="gather_info",
    payload={"query": query}
)
result = send_message(message)  # Trackable, loggable, flexible
```

### Q: What fields should every message have?

**Required fields:**
- `message_id` - Unique identifier
- `timestamp` - When sent
- `from_agent` - Sender
- `to_agent` - Recipient
- `message_type` - request | response | error
- `action` - What to do (for requests)
- `payload` - Data

**Optional but useful:**
- `trace_id` - Trace entire workflow
- `in_reply_to` - Link response to request

See [Agent Communication](../tutorial-2/concepts/agent-communication.md) for full spec.

### Q: Do workers send messages back to coordinator?

**Yes.** Every request should get a response:

```python
# Coordinator sends request
coordinator.send_message(research_agent, "gather_info", {"query": "EV market"})

# Research agent sends response
research_agent.send_message(coordinator, "result", {
    "status": "success",
    "findings": [...]
})
```

**Don't:** Just return values. Use the message protocol for traceability.

### Q: How do I debug message flow?

**Step 1: Log all messages**
```python
def send_message(self, to_agent, action, payload):
    msg_id = str(uuid.uuid4())
    self.logger.info(json.dumps({
        "event": "message_sent",
        "message_id": msg_id,
        "to": to_agent,
        "action": action
    }))
    # ... send message
```

**Step 2: Use trace viewer**
```bash
python scripts/view_trace.py <trace_id>
```

**Step 3: Visualize with mermaid**
Extract message flow from logs and create sequence diagram.

---

## Specialization

### Q: How specialized should agents be?

**Too general (bad):**
```python
# Research agent doing everything
research_agent.gather_info()
research_agent.analyze_data()  # Should be data agent's job!
research_agent.write_report()  # Should be writer's job!
```

**Too specific (also bad):**
```python
# Separate agents for every tiny task
tech_news_research_agent
auto_news_research_agent
energy_news_research_agent
# Could be one research agent with parameter
```

**Just right:**
```python
# Clear, focused responsibilities
research_agent.gather_info(topic="any topic")  # Broad enough
data_agent.analyze(data)                       # One clear job
writer_agent.create_report(data)               # One clear job
```

**Rule of thumb:** One agent per major skill/tool set, not per data type.

### Q: Should agents know about each other?

**No.** Agents should only know about:
1. The coordinator
2. Shared state
3. Their own tools

**Bad:**
```python
class ResearchAgent:
    def gather_info(self):
        findings = self.search()
        # BAD: Calling data agent directly
        analysis = self.data_agent.analyze(findings)
```

**Good:**
```python
class ResearchAgent:
    def gather_info(self):
        findings = self.search()
        # Write to shared state
        self.shared_state.set("findings", findings)
        # Let coordinator handle next step
```

### Q: Can one agent use another agent's tools?

**Technically yes, but don't do it.**

**Why?** It defeats the purpose of specialization. If research agent needs calculation, that's a sign you should delegate to data agent (via coordinator).

**Exception:** Common tools like `read_file` might be shared if all agents need to read reference documents.

### Q: How do I prevent agents from overstepping?

**In system prompt:**
```text
You are a Research Specialist.

IMPORTANT: You gather information only. You DO NOT:
- Analyze data (that's the Data Agent's job)
- Write reports (that's the Writer Agent's job)
- Calculate metrics (that's the Data Agent's job)

If the user asks for analysis, respond: "I can gather the data, but the Data Agent will handle analysis."
```

**In tools:**
- Only register relevant tools for each agent
- Research: web_search, read_file
- Data: calculate, analyze_trend
- Writer: format_markdown

---

## State Management

### Q: When should I use shared state vs. messages?

**Use Shared State For:**
- Persistent data (research findings, analysis results)
- Data accessed by multiple agents
- Context that outlives individual messages

**Use Messages For:**
- Agent-to-agent communication
- Task delegation
- Status updates
- Temporary data

**Example:**
```python
# Shared state: Research findings (data agent needs to read later)
shared_state.set("findings", findings_list)

# Message: Notify coordinator that research is done (one-time event)
send_message(coordinator, "task_complete", {"agent": "research"})
```

### Q: What if two agents write to the same state key simultaneously?

**Problem: Race condition**
```python
# Agent A
count = shared_state.get("count")  # Gets 5
shared_state.set("count", count + 1)  # Sets 6

# Agent B (simultaneously)
count = shared_state.get("count")  # Also gets 5
shared_state.set("count", count + 1)  # Also sets 6 (should be 7!)
```

**Solution 1: File locking** (already implemented in our SharedState class)
**Solution 2: Namespaced keys**
```python
# Each agent has its own namespace
shared_state.set("research_findings", findings)
shared_state.set("data_analysis", analysis)
# No conflict!
```

**Solution 3: Coordinator manages writes** (best)
Only coordinator writes to shared state, agents send results via messages.

### Q: Should I use JSON or pickle for state?

**JSON** (recommended for Tutorial 2):
- Human-readable
- Easy to inspect: `cat .agent_state/shared_state.json | jq`
- Language-agnostic
- Safe (can't execute code)

**Pickle** (avoid):
- Binary (can't inspect easily)
- Python-only
- Security risk (can execute code)
- Harder to debug

### Q: How do I debug state issues?

**Step 1: Inspect state file**
```bash
cat .agent_state/shared_state.json | jq '.'
```

**Step 2: Check state logs**
```bash
grep "state_write" .agent_logs/agent.log
grep "state_read" .agent_logs/agent.log
```

**Step 3: Who wrote what?**
```bash
grep "state_write" .agent_logs/agent.log | jq -r '[.timestamp, .agent, .data.key] | @tsv'
```

---

## Testing Multi-Agent Systems

### Q: How is multi-agent testing different from single agent?

**Single Agent Testing:**
- Test agent → tools → response
- One execution path
- Linear trace

**Multi-Agent Testing:**
- Test coordinator → agents → messages → state → response
- Multiple execution paths
- Complex interactions

**New test types needed:**
- Coordination logic tests
- Message protocol tests
- State consistency tests
- Integration tests (full workflows)

### Q: Should I test agents independently or together?

**Both!**

**Unit Tests:** Each agent independently with mocks
```python
def test_research_agent():
    agent = ResearchAgent(shared_state=MockSharedState())
    result = agent.gather_info("test query")
    assert result.status == "success"
```

**Integration Tests:** Full workflow
```python
def test_full_workflow():
    coordinator = Coordinator()
    result = coordinator.generate_report("test query")
    # Tests all agents working together
```

**Ratio:** 70% unit, 30% integration

### Q: How do I mock an agent?

```python
class MockResearchAgent:
    """Predictable research agent for testing."""
    def gather_info(self, query):
        return Response(
            status="success",
            findings=[
                {"fact": "Mock fact 1", "source": "mock"},
                {"fact": "Mock fact 2", "source": "mock"}
            ]
        )

# Use in tests
def test_coordinator():
    coordinator = Coordinator()
    coordinator.research = MockResearchAgent()  # Replace with mock
    # Now test coordinator logic without depending on real research
```

### Q: How do I test error handling?

```python
class FailingAgent:
    """Agent that always fails (for testing error handling)."""
    def execute(self, *args):
        raise TimeoutError("Simulated timeout")

def test_coordinator_handles_failure():
    coordinator = Coordinator()
    coordinator.research = FailingAgent()
    
    result = coordinator.generate_report("test")
    
    # Coordinator should handle gracefully, not crash
    assert result.status == "error"
    assert "timeout" in result.error.lower()
```

### Q: Should I test with real LLM calls?

**For most tests: No.** Use mocks for speed and determinism.

**For evaluation tests: Yes.** A few end-to-end tests with real LLM to check quality.

**Ratio:** 
- 95% mocked LLM (fast, deterministic)
- 5% real LLM (slow, quality checks)

---

## Performance & Debugging

### Q: My multi-agent system is slow. How do I speed it up?

**Step 1: Profile to find bottleneck**
```python
import time

start = time.time()
research_result = research.execute()
print(f"Research: {time.time() - start}s")

start = time.time()
data_result = data.execute()
print(f"Data: {time.time() - start}s")

start = time.time()
writer_result = writer.execute()
print(f"Writer: {time.time() - start}s")
```

**If research is slow:** Optimize search queries, cache results
**If data is slow:** Optimize calculations, use faster algorithms
**If coordinator is slow:** Reduce message overhead, use parallel execution

**Step 2: Parallelize independent tasks**
If research and historical_data agents don't depend on each other, run in parallel.

### Q: How do I debug "silent failures" (agent doesn't respond)?

**Add timeouts:**
```python
def send_message(self, agent, action, payload, timeout=30):
    try:
        result = agent.execute(action, payload)
        # Wrap in timeout
        return result
    except TimeoutError:
        self.logger.error(f"Agent {agent.name} timed out after {timeout}s")
        return Response(status="error", error="Agent timeout")
```

**Check logs:**
```bash
# Did agent start execution?
grep "task_started" .agent_logs/agent.log

# Did agent complete?
grep "task_completed" .agent_logs/agent.log

# Gap between start and complete = agent is stuck
```

### Q: Message logs are too verbose. How do I filter?

**By trace ID:**
```bash
grep '"trace_id": "abc-123"' .agent_logs/agent.log | jq '.'
```

**By agent:**
```bash
grep '"agent": "research"' .agent_logs/agent.log | jq '.'
```

**By event type:**
```bash
grep '"event": "message_sent"' .agent_logs/agent.log | jq '.'
```

**Create trace viewer** (see [Debugging Guide](../tutorial-2/guides/debugging-multi-agent.md))

---

## Conceptual Questions

### Q: When should I use multi-agent vs. single agent?

**Use Multi-Agent When:**
- Task has distinct subtasks (research, analysis, writing)
- Subtasks need different tools/expertise
- Can benefit from parallel execution
- System will scale (add more agents later)

**Use Single Agent When:**
- Task is simple and linear
- No clear subtask boundaries
- Speed/simplicity more important than modularity
- Learning (Tutorial 1 scope)

See [Multi-Agent Architecture](../tutorial-2/concepts/multi-agent-architecture.md#when-to-use-multi-agent-vs-single-agent) decision tree.

### Q: What's the difference between coordinator and hierarchical?

**Coordinator-Worker (Tutorial 2):**
```
Coordinator
├── Worker 1
├── Worker 2
└── Worker 3
```
One level, 3-10 agents total.

**Hierarchical (Tutorial 3+):**
```
Master Coordinator
├── Sub-Coordinator A
│   ├── Worker 1
│   └── Worker 2
└── Sub-Coordinator B
    ├── Worker 3
    └── Worker 4
```
Multiple levels, 10-100+ agents.

**Use hierarchical when:** >10 agents, natural team divisions.

### Q: Can agents have conversations with each other?

**In peer-to-peer:** Yes, agents negotiate directly.
**In coordinator-worker:** No, all communication through coordinator.

**Tutorial 2 uses coordinator-worker** (simpler to debug).

---

## AI Assistant Usage

### Q: How should I use AI assistant in Lab 2?

**Do:**
- ✅ Use AI to implement functions from scaffolds
- ✅ Ask AI to explain concepts: "What is a coordinator agent?"
- ✅ Request code reviews: "Check this delegation logic"
- ✅ Generate tests: "Write a test for error handling"
- ✅ Include `@.cursorrules` for project context

**Don't:**
- ❌ Ask AI to do entire exercises without understanding
- ❌ Copy-paste without reviewing
- ❌ Skip reading tutorial pages (AI can't replace learning)
- ❌ Forget to test AI-generated code

**You are the architect. AI is your senior developer.**

### Q: What if AI generates code that doesn't follow project conventions?

**Review and correct:**
```python
# AI generated:
def process(data):
    return data  # No type hints! No docstring!

# You fix:
def process(data: dict) -> dict:
    """
    Process data according to project conventions.
    
    Args:
        data: Input data dictionary
    
    Returns:
        Processed data dictionary
    """
    return data
```

**Remind AI:**
```
@.cursorrules

Please regenerate with:
- Type hints (mandatory per project guidelines)
- Google-style docstrings
- Error handling
```

### Q: AI is not reading .cursorrules. What do I do?

**Cursor:**
- Explicitly use `@.cursorrules` in every prompt

**Continue/Cline:**
- Should read automatically; check settings
- Verify file exists and is readable

**Copilot:**
- Doesn't read `.cursorrules`
- Include context in code comments instead:
  ```python
  # This project uses Google-style docstrings
  # Type hints are mandatory
  # All tools must be decorated with @registry.register
  ```

---

## Still Stuck?

See:
- [Troubleshooting Guide](./troubleshooting.md) - Specific errors
- [Getting Unstuck Guide](./getting-unstuck.md) - Systematic debugging
- [Tutorial 2 Concepts](../tutorial-2/READING_GUIDE.md) - Core concepts
- Community forums - Ask questions

