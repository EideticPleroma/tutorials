# Exercise 1A: Coordinator Basics

| Duration | Difficulty | Prerequisites | Skills Practiced |
|----------|------------|---------------|------------------|
| ~60 min | Intermediate | Exercise 0 (Bridge) | Coordinator pattern, Delegation, Error handling |

## Objective

Build a coordinator agent that orchestrates multiple worker agents using direct function calls. This exercise focuses on the coordination pattern before adding message protocol complexity.

## Context

In Exercise 0, you chained two agents with simple function calls. That works for linear workflows, but what about:

- **Branching**: Different agents for different query types?
- **Error recovery**: What if one agent fails?
- **Sequencing**: Ensuring agents run in the right order?

The **Coordinator** pattern solves these problems. The coordinator is the "manager" that:
1. Receives user requests
2. Decides which worker(s) to call
3. Handles errors and retries
4. Aggregates results

```
User: "Analyze the EV market"
    ↓
Coordinator (orchestrates)
    ├─> "This needs research first"
    │   └─> delegate to Research Agent
    ├─> "Now analyze the data"  
    │   └─> delegate to Data Agent
    └─> "Finally, write the report"
        └─> delegate to Writer Agent
    ↓
Return: Complete market analysis
```

**In this exercise**: You'll build the coordinator with direct function calls. Exercise 1B adds the message protocol for structured communication.

## Prerequisites

- [ ] Completed Exercise 0 (Bridge)
- [ ] Read [Multi-Agent Architecture](../../tutorial-2/concepts/multi-agent-architecture.md)
- [ ] Read [Coordinator Patterns](../../tutorial-2/architecture/coordinator-patterns.md)

## Code Scaffold

Open `src/multi_agent/coordinator.py`. You'll implement a simplified version first:

```python
"""
Coordinator agent for orchestrating multi-agent workflows.

This version uses direct function calls for simplicity.
Exercise 1B adds message protocol for structured communication.
"""

from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class CoordinatorError(Exception):
    """Base exception for coordinator errors."""
    pass

class DelegationError(CoordinatorError):
    """Error during delegation to worker agent."""
    pass

class Coordinator:
    """
    Coordinator agent that orchestrates worker agents.
    
    This implementation uses direct function calls.
    Exercise 1B refactors to use message protocol.
    """
    
    def __init__(self):
        """
        Initialize coordinator with worker agents.
        
        TODO:
        - Create worker agents (research, data, writer)
        - Setup logging
        """
        self.logger = logging.getLogger(f"{__name__}.Coordinator")
        
        # TODO: Initialize worker agents
        # For now, use mock agents - Exercise 2 creates real ones
        self.research = None  # MockResearchAgent()
        self.data = None      # MockDataAgent()
        self.writer = None    # MockWriterAgent()
    
    def delegate(self, agent: Any, action: str, payload: Dict) -> Dict:
        """
        Delegate a task to a worker agent (direct function call).
        
        Args:
            agent: Worker agent to delegate to
            action: Action for agent to perform
            payload: Data for the action
        
        Returns:
            Response dict from worker agent
            
        Raises:
            DelegationError: If agent fails after retries
        """
        # TODO: Implement delegation with:
        # 1. Validate agent exists
        # 2. Call agent.execute(action, payload)
        # 3. Log the delegation
        # 4. Handle errors
        pass
    
    def generate_report(self, query: str) -> str:
        """
        Generate a report by orchestrating research, data, and writer agents.
        
        Args:
            query: User's research query
        
        Returns:
            Formatted report string
            
        TODO: Implement sequential workflow:
        1. Research agent gathers information
        2. Data agent analyzes findings  
        3. Writer agent creates formatted report
        
        Handle errors at each step.
        """
        pass
```

## Tasks

### Task 1: Initialize Coordinator with Mock Agents

Before building real agents (Exercise 2), use mocks to test the coordinator pattern.

**Create mock agents:**

```python
# In coordinator.py or a separate file

class MockWorkerAgent:
    """Base mock for testing coordinator logic."""
    
    def __init__(self, name: str):
        self.name = name
    
    def execute(self, action: str, payload: Dict) -> Dict:
        """Override in subclasses."""
        raise NotImplementedError

class MockResearchAgent(MockWorkerAgent):
    def __init__(self):
        super().__init__("research")
    
    def execute(self, action: str, payload: Dict) -> Dict:
        if action == "gather_info":
            return {
                "status": "success",
                "findings": [
                    {"fact": "EV market growing 25% annually", "source": "market_data.txt"},
                    {"fact": "Tesla leads with 20% market share", "source": "competitors.txt"}
                ]
            }
        return {"status": "error", "error": f"Unknown action: {action}"}

class MockDataAgent(MockWorkerAgent):
    def __init__(self):
        super().__init__("data")
    
    def execute(self, action: str, payload: Dict) -> Dict:
        if action == "analyze_trends":
            return {
                "status": "success",
                "metrics": {"growth_rate": "25%", "market_leader": "Tesla"},
                "insights": ["Market consolidating", "Battery costs declining"]
            }
        return {"status": "error", "error": f"Unknown action: {action}"}

class MockWriterAgent(MockWorkerAgent):
    def __init__(self):
        super().__init__("writer")
    
    def execute(self, action: str, payload: Dict) -> Dict:
        if action == "create_report":
            findings = payload.get("findings", [])
            analysis = payload.get("analysis", {})
            report = f"""# Market Analysis Report

## Summary
Analysis based on {len(findings)} findings.

## Key Metrics
- Growth Rate: {analysis.get('metrics', {}).get('growth_rate', 'N/A')}

## Findings
{chr(10).join(f"- {f['fact']}" for f in findings)}
"""
            return {"status": "success", "report": report}
        return {"status": "error", "error": f"Unknown action: {action}"}
```

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/coordinator.py

I'm working on Exercise 1A (Coordinator Basics).

I need to implement Coordinator.__init__() that:
1. Creates logger with coordinator name
2. Initializes mock worker agents (research, data, writer)
3. Stores agents as instance attributes

Generate the __init__() implementation using the mock agents provided.
```

**Validation:**
```python
coordinator = Coordinator()
assert coordinator.research is not None
assert coordinator.data is not None
assert coordinator.writer is not None
assert coordinator.research.name == "research"
```

### Task 2: Implement Delegation with Error Handling

The `delegate()` method is the core of coordination. It calls a worker and handles failures.

**Requirements:**
- Validate agent exists
- Call `agent.execute(action, payload)`
- Log delegation attempts
- Raise `DelegationError` on failure

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/coordinator.py

I need to implement Coordinator.delegate() for Exercise 1A.

Requirements:
1. Check agent is not None, raise DelegationError if missing
2. Log: "Delegating {action} to {agent.name}"
3. Call agent.execute(action, payload)
4. Check response["status"] == "success"
5. If error, log and raise DelegationError with details
6. Return response on success

Generate the implementation. Use direct function calls (no message protocol yet).
```

**Implementation Pattern:**
```python
def delegate(self, agent: Any, action: str, payload: Dict) -> Dict:
    """Delegate task to worker agent."""
    # Validate
    if agent is None:
        raise DelegationError(f"Agent not initialized for action: {action}")
    
    # Log
    self.logger.info("Delegating %s to %s", action, agent.name)
    
    # Execute
    try:
        response = agent.execute(action, payload)
    except Exception as e:
        self.logger.error("Agent %s failed: %s", agent.name, str(e))
        raise DelegationError(f"Agent {agent.name} failed: {str(e)}")
    
    # Check status
    if response.get("status") != "success":
        error = response.get("error", "Unknown error")
        self.logger.error("Agent %s returned error: %s", agent.name, error)
        raise DelegationError(f"Agent {agent.name} error: {error}")
    
    self.logger.info("Agent %s completed successfully", agent.name)
    return response
```

**Validation:**
```python
coordinator = Coordinator()

# Test successful delegation
result = coordinator.delegate(coordinator.research, "gather_info", {"query": "EVs"})
assert result["status"] == "success"
assert len(result["findings"]) > 0

# Test error handling
try:
    coordinator.delegate(None, "test", {})
    assert False, "Should have raised DelegationError"
except DelegationError:
    pass  # Expected
```

### Task 3: Implement Sequential Workflow

The `generate_report()` method orchestrates three agents in sequence.

**Requirements:**
- Call research agent with query
- Pass research findings to data agent
- Pass both to writer agent
- Handle errors at each step
- Return final report

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/coordinator.py

I need to implement Coordinator.generate_report() for Exercise 1A.

Requirements:
1. Delegate "gather_info" to research agent with {"query": query}
2. If research fails, return error message (don't crash)
3. Delegate "analyze_trends" to data agent with {"findings": research_findings}
4. If data fails, return error message
5. Delegate "create_report" to writer with {"findings": findings, "analysis": analysis}
6. Return the report string

Use try/except around each delegation to handle DelegationError gracefully.

Generate the implementation.
```

**Implementation Pattern:**
```python
def generate_report(self, query: str) -> str:
    """Generate report through sequential workflow."""
    self.logger.info("Starting report generation for: %s", query)
    
    # Step 1: Research
    try:
        research_result = self.delegate(
            self.research, 
            "gather_info", 
            {"query": query}
        )
        findings = research_result.get("findings", [])
    except DelegationError as e:
        return f"Research failed: {str(e)}"
    
    # Step 2: Data Analysis
    try:
        data_result = self.delegate(
            self.data,
            "analyze_trends",
            {"findings": findings}
        )
        analysis = data_result
    except DelegationError as e:
        return f"Data analysis failed: {str(e)}"
    
    # Step 3: Writing
    try:
        writer_result = self.delegate(
            self.writer,
            "create_report",
            {"findings": findings, "analysis": analysis}
        )
        report = writer_result.get("report", "No report generated")
    except DelegationError as e:
        return f"Report writing failed: {str(e)}"
    
    self.logger.info("Report generation complete")
    return report
```

**Validation:**
```python
coordinator = Coordinator()
report = coordinator.generate_report("electric vehicle market")

assert "# Market Analysis Report" in report
assert "Growth Rate" in report
assert "Findings" in report
print(report)  # Should be a formatted markdown report
```

### Task 4: Add Basic Retry Logic

Real systems need retry capability for transient failures.

**Requirements:**
- Add `max_retries` parameter (default 3)
- Retry on failure before giving up
- Log each retry attempt

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/coordinator.py

I need to add retry logic to Coordinator.delegate() for Exercise 1A.

Requirements:
1. Add max_retries parameter (default 3)
2. Wrap execution in retry loop
3. On failure, log "Retry {attempt}/{max_retries} for {agent.name}"
4. After max retries, raise DelegationError
5. On success, return immediately

Generate updated delegate() with retry logic. Use simple time.sleep(1) between retries.
```

**Validation:**
```python
# Create a flaky agent for testing
class FlakyAgent:
    def __init__(self):
        self.name = "flaky"
        self.attempts = 0
    
    def execute(self, action, payload):
        self.attempts += 1
        if self.attempts < 3:
            return {"status": "error", "error": "Temporary failure"}
        return {"status": "success", "result": "Eventually worked"}

coordinator = Coordinator()
flaky = FlakyAgent()

# Should succeed after retries
result = coordinator.delegate(flaky, "test", {}, max_retries=5)
assert result["status"] == "success"
assert flaky.attempts == 3  # Failed twice, succeeded third time
```

## Testing Your Implementation

### Unit Tests

Create `tests/multi_agent/test_coordinator_basics.py`:

```python
import pytest
from src.multi_agent.coordinator import Coordinator, DelegationError

def test_coordinator_initialization():
    """Coordinator initializes with all agents."""
    coordinator = Coordinator()
    assert coordinator.research is not None
    assert coordinator.data is not None
    assert coordinator.writer is not None

def test_delegation_success():
    """Successful delegation returns result."""
    coordinator = Coordinator()
    result = coordinator.delegate(
        coordinator.research, 
        "gather_info", 
        {"query": "test"}
    )
    assert result["status"] == "success"

def test_delegation_error_handling():
    """Delegation raises DelegationError on failure."""
    coordinator = Coordinator()
    with pytest.raises(DelegationError):
        coordinator.delegate(None, "test", {})

def test_generate_report_success():
    """Full workflow produces a report."""
    coordinator = Coordinator()
    report = coordinator.generate_report("test query")
    assert "Report" in report
    assert len(report) > 100
```

Run tests:
```bash
python -m pytest tests/multi_agent/test_coordinator_basics.py -v
```

Expected: 4/4 tests passing

### Manual Testing

```python
from src.multi_agent.coordinator import Coordinator

coordinator = Coordinator()

# Test the full workflow
report = coordinator.generate_report("electric vehicle market analysis")
print(report)

# Should see:
# - Markdown formatted report
# - Summary section
# - Key metrics
# - Findings list
```

## Checkpoint Questions

Before moving to Exercise 1B, verify:

- [ ] Coordinator initializes with three worker agents?
- [ ] `delegate()` calls agent and handles errors?
- [ ] `generate_report()` chains three agents in sequence?
- [ ] Retry logic works for transient failures?
- [ ] All tests pass?

**Understanding Check:**
1. Why does the coordinator not have its own tools?
2. What's the benefit of catching `DelegationError` in `generate_report()`?
3. What information is lost when using direct function calls vs. structured messages?

<details>
<summary>Show Answers</summary>

1. **No tools for coordinator**: The coordinator orchestrates - workers execute. If the coordinator had tools, it would be tempted to do work itself instead of delegating. This separation keeps responsibilities clear.

2. **Catching DelegationError**: Allows graceful degradation. If research fails, the user gets a helpful error message instead of a stack trace. Each step can fail independently.

3. **Information lost without messages**:
   - No timestamps (when did things happen?)
   - No trace IDs (how do you follow a request across agents?)
   - No message history (what was the conversation?)
   - No structured error types (was it a timeout? validation error? system error?)

Exercise 1B adds message protocol to solve these problems.

</details>

## What's Next

You've built a working coordinator with direct function calls. But you noticed:

- **No traceability**: Can't follow a request through the system
- **No timestamps**: Don't know when things happened
- **Basic error info**: Just strings, no structured error types
- **No async potential**: Direct calls are synchronous

Exercise 1B introduces the **Message Protocol** - structured communication that solves these problems and enables future features like parallel execution.

---

## Common Issues

**Issue: "NoneType has no attribute 'execute'"**
- Agent not initialized in `__init__`
- Check mock agents are created properly

**Issue: "Delegation always fails"**
- Check agent's `execute()` returns `{"status": "success", ...}`
- Verify action name matches what agent expects

**Issue: "Tests fail with import error"**
- Run from project root directory
- Check `__init__.py` files exist in `src/multi_agent/`

---

## Design Tips

**Keep coordinator simple:**
- Coordinator orchestrates, workers execute
- Coordinator makes decisions, workers have capabilities
- If coordinator gets complex, you probably need more workers

**Log everything:**
- Every delegation attempt
- Every response (success or failure)
- Makes debugging 10x easier

**Fail gracefully:**
- Catch errors at each step
- Return meaningful messages to users
- Don't let one failure crash everything

---

**Next: [Exercise 1B: Message Protocol](./01b-message-protocol.md)** - Add structured communication to your coordinator.

