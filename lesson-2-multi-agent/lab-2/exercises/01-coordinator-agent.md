# Exercise 1: Build a Coordinator Agent

**Duration**: ~90 minutes | **Difficulty**: Intermediate

## Objective

Build a coordinator agent that orchestrates multiple worker agents in a sequential workflow (research → data → writer).

## Context

In Tutorial 1, you built single agents that execute tasks themselves. In multi-agent systems, the **coordinator** is the "manager" that delegates work to specialized "worker" agents.

**Coordinator responsibilities:**
1. Receive user request
2. Decompose into subtasks
3. Delegate to appropriate workers
4. Aggregate results
5. Return final response to user

**What you'll build:**
```
User: "Analyze the EV market"
    ↓
Coordinator
    ├→ delegate to Research Agent
    ├→ delegate to Data Agent
    └→ delegate to Writer Agent
    ↓
Return: Complete market analysis report
```

## Prerequisites

- [ ] Read [Multi-Agent Architecture](../../tutorial-2/concepts/multi-agent-architecture.md)
- [ ] Read [Coordinator Patterns](../../tutorial-2/architecture/coordinator-patterns.md)
- [ ] Review `src/multi_agent/coordinator.py` scaffold

## Code Scaffold

Open `src/multi_agent/coordinator.py`. You'll see:

```python
"""
Coordinator agent for orchestrating multi-agent workflows.

The coordinator delegates tasks to specialized worker agents and
aggregates their results into a final response.
"""

from typing import Optional, List
import logging
from .worker_base import WorkerAgent
from .message_protocol import Message, MessageType
from .shared_state import SharedState

class Coordinator:
    """
    Coordinator agent that orchestrates worker agents.
    
    Implements the coordinator-worker pattern from Tutorial 2.
    """
    
    def __init__(self, shared_state: Optional[SharedState] = None):
        """
        Initialize coordinator with worker agents.
        
        Args:
            shared_state: Shared state manager for cross-agent data
        """
        # TODO: Initialize shared state
        # TODO: Initialize worker agents (research, data, writer)
        # TODO: Setup logging
        pass
    
    def delegate(self, agent: WorkerAgent, action: str, payload: dict) -> dict:
        """
        Delegate a task to a worker agent.
        
        Args:
            agent: Worker agent to delegate to
            action: Action for agent to perform
            payload: Data for the action
        
        Returns:
            Response from worker agent
        
        TODO: Implement delegation with:
        - Message creation
        - Error handling
        - Retry logic
        - Logging
        """
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

### Task 1: Initialize Coordinator

Implement the `__init__` method.

**Requirements:**
- Initialize or create SharedState
- Create worker agents (you'll need to mock these for now)
- Set up logging

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/coordinator.py

I need to implement the Coordinator.__init__() method.

Requirements:
- Initialize SharedState (create new if none provided)
- Create placeholder worker agents (research, data, writer)
- Set up structured logging for coordination events

Based on the project architecture, generate the __init__() implementation.
```

**Validation:**
```python
# Test coordinator initialization
coordinator = Coordinator()
assert coordinator.shared_state is not None
assert hasattr(coordinator, 'research')
assert hasattr(coordinator, 'data')
assert hasattr(coordinator, 'writer')
```

### Task 2: Implement Delegation Logic

Implement the `delegate()` method.

**Requirements:**
- Create Message object for request
- Send to worker agent
- Handle response
- Log all steps
- Include error handling

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/coordinator.py @src/multi_agent/message_protocol.py

I need to implement the Coordinator.delegate() method that sends tasks to worker agents.

Requirements:
- Create Message with from_agent="coordinator", to_agent=agent.name
- Call agent.execute(action, payload)
- Handle success, partial, and error responses
- Log message sent and received
- Return response dict

Generate the delegate() implementation with proper error handling.
```

**Validation:**
```python
# Test delegation with mock agent
class MockAgent:
    name = "mock"
    def execute(self, action, payload):
        return {"status": "success", "result": "done"}

coordinator = Coordinator()
result = coordinator.delegate(MockAgent(), "test_action", {"data": "test"})
assert result["status"] == "success"
```

### Task 3: Implement Sequential Workflow

Implement the `generate_report()` method.

**Requirements:**
- Call research → data → writer in sequence
- Each step waits for previous to complete
- Handle errors at any step (retry or fail gracefully)
- Return final report

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/coordinator.py

I need to implement the Coordinator.generate_report() method for sequential workflow.

Requirements:
1. Delegate "gather_info" to research agent with query
2. Check research succeeded, return error if not
3. Delegate "analyze_trends" to data agent
4. Check data succeeded, return error if not
5. Delegate "create_report" to writer agent
6. Return final report

Generate the generate_report() implementation with error handling at each step.
```

**Validation:**
```python
# Test full workflow with mock agents
coordinator = Coordinator()
coordinator.research = MockResearchAgent()
coordinator.data = MockDataAgent()
coordinator.writer = MockWriterAgent()

report = coordinator.generate_report("Test query")
assert "research" in report.lower()
assert "analysis" in report.lower()
```

### Task 4: Add Retry Logic (Advanced)

Add retry capability for failed delegations.

**Requirements:**
- Max 3 retries
- Exponential backoff (1s, 2s, 4s)
- Log each retry attempt
- After max retries, return error

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/coordinator.py

I need to add retry logic to the delegate() method.

Requirements:
- Wrap delegation in retry loop (max 3 attempts)
- Use exponential backoff: wait 2^attempt seconds
- Log each retry: "Retry {attempt} for {agent.name}"
- After max retries, return error response

Generate updated delegate() with retry logic.
```

## Testing Your Implementation

### Unit Tests

Run the coordinator tests:
```bash
python -m pytest tests/multi_agent/test_coordinator.py -v
```

### Manual Testing

Test your coordinator interactively:
```python
from src.multi_agent import Coordinator

coordinator = Coordinator()

# Test with mock agents (you'll create real agents in Exercise 2)
class MockResearch:
    name = "research"
    def execute(self, action, payload):
        return {"status": "success", "findings": ["fact 1", "fact 2"]}

coordinator.research = MockResearch()

# Test delegation
result = coordinator.delegate(coordinator.research, "gather_info", {"query": "test"})
print(f"Result: {result}")
```

### Check Logs

Verify message flow:
```bash
# View coordination logs
tail -20 .agent_logs/agent.log | jq '.'

# Should see:
# - "task_received" from user
# - "message_sent" to research
# - "message_received" from research
# - etc.
```

## Checkpoint Questions

Before moving to Exercise 2, verify:

- [ ] Can your coordinator initialize with worker agents?
- [ ] Does `delegate()` send messages and receive responses?
- [ ] Does `generate_report()` execute agents in correct order?
- [ ] Are errors handled gracefully (no crashes)?
- [ ] Do logs show clear message flow?

## Common Issues

**Issue: "Agents not found"**
- Ensure worker agents are created in `__init__`
- Check attribute names match (self.research, self.data, self.writer)

**Issue: "Delegation never returns"**
- Add timeout to worker calls
- Check workers are sending responses

**Issue: "Tests fail with AttributeError"**
- Check all required attributes exist (shared_state, agents, logger)

See [Troubleshooting - Coordinator Errors](../troubleshooting.md#coordinator-errors) for more.

## Next Steps

Once your coordinator works with mock agents:

👉 **Continue to [Exercise 2: Create Specialized Agents](./02-specialized-agents.md)**

You'll implement real worker agents that the coordinator can orchestrate.

---

## 💡 Design Tips

**Keep coordinator simple:** 
- Coordinator orchestrates, workers execute
- Coordinator shouldn't have tools (workers have tools)
- Coordinator manages flow, not business logic

**Log everything:**
- Every delegation
- Every response
- Every error
- Makes debugging 10x easier

**Handle errors gracefully:**
- Don't crash on worker failure
- Return meaningful error messages to user
- Consider retrying before giving up

**Test incrementally:**
- Test `__init__` first
- Then `delegate()` with mock
- Then `generate_report()` with mocks
- Finally, integration with real agents (Exercise 2)

