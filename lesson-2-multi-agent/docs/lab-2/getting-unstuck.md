# Getting Unstuck: Lab 2

A systematic approach to debugging multi-agent systems when you're stuck.

## The 5-Step Debugging Process

When you hit a wall, follow this process:

### Step 1: Define the Problem (2 minutes)

**Write down:**
- What you're trying to do
- What you expected to happen
- What actually happened
- Error message (if any)

**Example:**
```
Trying to: Generate a report using coordinator
Expected: Coordinator delegates to research → data → writer
Actual: Coordinator hangs after research step
Error: None (just waits forever)
```

### Step 2: Isolate the Problem (5 minutes)

**Test components independently:**

```bash
# Does coordinator initialize?
python -c "from src.multi_agent import Coordinator; c = Coordinator(); print('OK')"

# Does research agent work alone?
python -c "from src.multi_agent.specialized import ResearchAgent; r = ResearchAgent(); print('OK')"

# Do imports work?
python -c "from src.multi_agent import Message; print('OK')"
```

**Find where it breaks:**
- ✓ Imports work
- ✓ Coordinator initializes
- ✓ Research agent works alone
- ✗ Coordinator + research agent together ← Problem is here!

### Step 3: Check the Logs (5 minutes)

**View recent logs:**
```bash
tail -50 .agent_logs/agent.log | jq '.'
```

**Look for:**
- **Error messages:** `grep -i error .agent_logs/agent.log`
- **Last successful event:** What was the last thing that worked?
- **Missing events:** Did research agent start? Complete? Send response?

**Common patterns:**
```json
// Good: Complete message flow
{"event": "task_received", "agent": "coordinator"}
{"event": "message_sent", "to": "research"}
{"event": "task_started", "agent": "research"}
{"event": "task_completed", "agent": "research"}
{"event": "message_received", "from": "research"}

// Bad: Research started but never completed
{"event": "task_received", "agent": "coordinator"}
{"event": "message_sent", "to": "research"}
{"event": "task_started", "agent": "research"}
// ... nothing after this ← Research hung!
```

### Step 4: Use Your AI Assistant (10 minutes)

**Good AI prompt structure:**

```
@.cursorrules @src/multi_agent/coordinator.py

Problem: Coordinator hangs after delegating to research agent.

Context:
- Coordinator sends message to research agent
- Research agent starts execution (see logs)
- Research agent never completes
- Coordinator waits forever

Logs show:
{
  "event": "task_started",
  "agent": "research"
}
// No task_completed event

Expected behavior: Research agent should complete and send response to coordinator.

Based on the project architecture, what could cause research agent to start but not complete? How should I debug this?
```

**AI can help with:**
- Suggesting what to check next
- Pointing out common mistakes
- Generating debug code
- Explaining concepts you might be missing

**AI cannot:**
- Read your logs for you (you must provide relevant snippets)
- Know your specific implementation details
- Debug without context

### Step 5: Try Solutions (Variable time)

**Start with most likely cause:**

1. **Add timeout** (if agent hangs):
```python
def delegate(self, agent, action, payload, timeout=30):
    # Add timeout handling
    pass
```

2. **Ensure agents return responses:**
```python
class WorkerAgent:
    def execute(self, action, payload):
        try:
            result = self._work(action, payload)
            return Response(status="success", result=result)
        except Exception as e:
            # MUST return something, even on error!
            return Response(status="error", error=str(e))
```

3. **Check state reads/writes:**
```bash
grep "state_write.*findings" .agent_logs/agent.log
# Did research agent write findings to state?
```

**If solution doesn't work:** Go back to Step 3, gather more data.

---

## Specific Scenarios

### Scenario 1: "My tests pass but coordinator doesn't work in practice"

**Likely cause:** Tests use mocks, real agents have different behavior.

**Debug process:**
1. Run coordinator with verbose logging
2. Compare test messages vs. real messages
3. Check if real agent output matches mock output format

**Ask AI:**
```
@.cursorrules

My tests pass with MockResearchAgent but fail with real ResearchAgent.

MockResearchAgent returns: {"status": "success", "findings": [...]}
Real ResearchAgent returns: [show actual output]

What's the format mismatch? How do I fix the real agent?
```

### Scenario 2: "Agent A works, Agent B works, but together they fail"

**Likely cause:** Integration issue (messages, state, timing).

**Debug process:**
1. Check message flow: A sends → B receives?
2. Check state: A writes → B reads?
3. Check timing: A completes → B starts?

**Manual integration test:**
```python
# Test agents together step-by-step
shared_state = SharedState()

# Step 1: Agent A
agent_a = AgentA(shared_state)
result_a = agent_a.execute()
print(f"Agent A completed: {result_a}")
print(f"State after A: {shared_state.get_all()}")

# Step 2: Agent B (should use A's output)
agent_b = AgentB(shared_state)
result_b = agent_b.execute()
print(f"Agent B completed: {result_b}")
```

### Scenario 3: "Error message is cryptic or unclear"

**Example:** `TypeError: 'NoneType' object is not subscriptable`

**Debug process:**
1. Find the line number (traceback)
2. Check what's None (add print statements)
3. Work backwards: Why is it None?

**Ask AI:**
```
@.cursorrules

I'm getting this error:
TypeError: 'NoneType' object is not subscriptable at line 47

Line 47: findings = shared_state.get("research_findings")
        for f in findings:  # ← Error here

This means shared_state.get() returned None instead of a list.

Why might research_findings not be in shared state? How do I debug?
```

### Scenario 4: "I don't understand why it's doing X"

**Examples:**
- "Why does coordinator call research twice?"
- "Why is data agent getting wrong input?"
- "Why does writer agent have no data?"

**Debug process:**
1. **Add print statements** (liberally):
```python
def delegate(self, agent, action, payload):
    print(f"DEBUG: Delegating {action} to {agent.name}")
    print(f"DEBUG: Payload: {payload}")
    result = agent.execute(action, payload)
    print(f"DEBUG: Result: {result}")
    return result
```

2. **Use trace viewer:**
```bash
python scripts/view_trace.py <trace_id>
# See complete execution timeline
```

3. **Ask someone to explain:**
```
@.cursorrules

I don't understand why my coordinator is calling research_agent.gather_info() twice.

Here's my code:
[paste relevant code]

Here's what the logs show:
[paste log snippet]

Can you explain the execution flow and why it's calling twice?
```

---

## Using Documentation Effectively

### When to Read vs. Ask AI

**Read Documentation For:**
- ✅ Conceptual understanding ("What is a coordinator?")
- ✅ Design patterns ("How should I structure agents?")
- ✅ Best practices ("How do I test multi-agent?")

**Ask AI For:**
- ✅ Implementation help ("Generate delegate() method")
- ✅ Code review ("Check my error handling")
- ✅ Specific debugging ("Why does this crash?")

### Key Documentation Pages

**Problem: Don't understand multi-agent architecture**
- Read: [Multi-Agent Architecture](../tutorial-2/concepts/multi-agent-architecture.md)
- Read: [Coordinator Patterns](../tutorial-2/architecture/coordinator-patterns.md)

**Problem: Agents not communicating properly**
- Read: [Agent Communication](../tutorial-2/concepts/agent-communication.md)
- Check: [Troubleshooting - Communication Errors](./troubleshooting.md#agent-communication-errors)

**Problem: State issues**
- Read: [State Management](../tutorial-2/concepts/state-management.md)
- Check: [Troubleshooting - State Errors](./troubleshooting.md#state-management-errors)

**Problem: Testing failures**
- Read: [Testing Multi-Agent Systems](../tutorial-2/guides/testing-multi-agent.md)
- Check: [Troubleshooting - Testing Errors](./troubleshooting.md#testing-errors)

---

## Rollback Strategies

### Strategy 1: Checkpoint Commits

**Before making changes:**
```bash
git add .
git commit -m "Working state before adding X"
```

**If changes break things:**
```bash
git diff HEAD  # See what changed
git checkout src/multi_agent/coordinator.py  # Revert specific file
# Or
git reset --hard HEAD  # Revert everything (careful!)
```

### Strategy 2: Feature Branches

**For experiments:**
```bash
git checkout -b experiment-parallel-execution
# Make experimental changes
# If it works: merge to main
# If it breaks: delete branch and go back
```

### Strategy 3: Save Scaffold Version

**Before modifying scaffold:**
```bash
cp src/multi_agent/coordinator.py src/multi_agent/coordinator.py.scaffold
# Now you can always diff against original:
diff src/multi_agent/coordinator.py src/multi_agent/coordinator.py.scaffold
```

---

## When to Ask for Human Help

**Ask community/instructor when:**
- ✅ Spent >1 hour debugging with no progress
- ✅ AI gives contradictory answers
- ✅ Error seems like a bug in tutorial code (not your code)
- ✅ Documentation unclear or seems wrong
- ✅ Need concept explained differently

**Before asking, prepare:**
1. **Minimal reproducible example:**
```python
# Smallest code that shows the problem
from src.multi_agent import Coordinator

coordinator = Coordinator()
result = coordinator.delegate(...)  # Breaks here
```

2. **Error message + stack trace:**
```
Traceback (most recent call last):
  File "src/multi_agent/coordinator.py", line 47, in delegate
    ...
TypeError: ...
```

3. **What you've tried:**
- Checked logs: [findings]
- Tried solution X: [result]
- Asked AI: [response]
- Read documentation: [which pages]

4. **Specific question:**
- ❌ "My coordinator doesn't work"
- ✅ "Coordinator hangs when delegating to research agent. Research starts but never completes. Logs show [snippet]. What could cause this?"

---

## Prevention: How to Avoid Getting Stuck

### 1. Test Incrementally

**Don't:**
- Write 200 lines of code
- Run it all at once
- Get 10 errors
- Don't know where to start

**Do:**
- Write 20 lines
- Test it
- Write 20 more lines
- Test it

**For each function:**
```python
def new_function():
    # Write minimal version
    return "TODO"

# Test it works (even if incomplete)
assert new_function() == "TODO"

# Now implement properly
```

### 2. Use Type Hints and Docstrings

**Why:** AI and you both understand code better.

```python
# Hard to debug
def process(data):
    return stuff

# Easy to debug
def process(data: dict) -> list[dict]:
    """
    Process research data into findings.
    
    Args:
        data: Raw research data with 'sources' and 'content' keys
    
    Returns:
        List of finding dicts with 'fact', 'source', 'confidence'
    """
    return findings
```

### 3. Log Liberally

**Add logs to every major operation:**
```python
def delegate(self, agent, action, payload):
    self.logger.info(f"Delegating {action} to {agent.name}")
    
    try:
        result = agent.execute(action, payload)
        self.logger.info(f"Delegation succeeded: {result.status}")
        return result
    except Exception as e:
        self.logger.error(f"Delegation failed: {e}")
        raise
```

### 4. Write Tests First

**TDD for multi-agent:**
```python
# 1. Write test (will fail)
def test_coordinator_delegates_to_research():
    coordinator = Coordinator()
    coordinator.research = MockResearchAgent()
    
    result = coordinator.delegate(coordinator.research, "gather_info", {})
    assert result.status == "success"

# 2. Run test (fails)
# 3. Implement just enough to pass
# 4. Repeat
```

---

## Summary Flowchart

```
┌─────────────────┐
│   STUCK?        │
└────────┬────────┘
         │
         ├─> Define Problem (2 min)
         │   └─> Write down: trying/expected/actual/error
         │
         ├─> Isolate Problem (5 min)
         │   └─> Test components independently
         │
         ├─> Check Logs (5 min)
         │   └─> Find last successful event, errors
         │
         ├─> Ask AI (10 min)
         │   └─> Include @.cursorrules, context, logs
         │
         ├─> Try Solution
         │   └─> If works: ✓ Done
         │   └─> If not: Back to Check Logs
         │
         └─> Still stuck after 1 hour?
             └─> Ask community with full context
```

---

**Remember:** 
- Multi-agent debugging is harder than single agent (more moving parts)
- Logs are your best friend
- AI can help if you give it enough context
- It's okay to ask for help

**You've got this!** 🚀

