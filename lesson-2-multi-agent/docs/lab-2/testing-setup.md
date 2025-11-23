# Testing Setup Guide for Multi-Agent Systems

**Duration**: ~20 minutes | **Prerequisites**: pytest basics, Tutorial 1 testing

This guide shows you how to set up a robust testing environment for multi-agent systems using pytest fixtures, mocks, and test organization strategies.

---

## Table of Contents

1. [Project Test Structure](#project-test-structure)
2. [Essential pytest Fixtures](#essential-pytest-fixtures)
3. [Mock Agents for Testing](#mock-agents-for-testing)
4. [Test Organization](#test-organization)
5. [Running Tests](#running-tests)
6. [Common Patterns](#common-patterns)

---

## Project Test Structure

```
tutorials/
├── tests/
│   ├── conftest.py                    # Shared fixtures
│   ├── unit/                          # Tutorial 1 tests
│   │   └── test_simple_agent.py
│   └── multi_agent/                   # Tutorial 2 tests
│       ├── conftest.py                # Multi-agent specific fixtures
│       ├── test_coordinator.py        # Coordinator unit tests
│       ├── test_message_protocol.py   # Message protocol tests
│       ├── test_shared_state.py       # State management tests
│       ├── test_specialized_agents.py # Agent interaction tests
│       └── test_integration.py        # Full workflow tests
├── src/
│   ├── agent/                         # Tutorial 1
│   └── multi_agent/                   # Tutorial 2
└── pytest.ini                         # pytest configuration
```

---

## Essential pytest Fixtures

### 1. conftest.py - Root Level

Location: `tests/conftest.py`

```python
"""
Shared fixtures for all tests.

Fixtures defined here are available to all test files.
"""

import pytest
import logging
from pathlib import Path


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Configure logging for tests."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


@pytest.fixture
def test_data_dir():
    """Return path to test data directory."""
    return Path(__file__).parent / "test_data"


@pytest.fixture
def temp_dir(tmp_path):
    """Provide temporary directory for test files."""
    return tmp_path
```

### 2. conftest.py - Multi-Agent Specific

Location: `tests/multi_agent/conftest.py`

```python
"""
Fixtures specific to multi-agent testing.

These fixtures provide clean state, mock agents, and test utilities
for multi-agent system tests.
"""

import pytest
import json
from pathlib import Path
from src.multi_agent import SharedState, Coordinator, Message, MessageType
from src.multi_agent.worker_base import WorkerAgent


@pytest.fixture
def clean_state_dir(tmp_path):
    """
    Provide clean state directory for each test.
    
    Ensures no state pollution between tests.
    """
    state_dir = tmp_path / ".agent_state"
    state_dir.mkdir(exist_ok=True)
    return state_dir


@pytest.fixture
def shared_state(clean_state_dir):
    """
    Provide fresh SharedState instance for each test.
    
    Usage:
        def test_something(shared_state):
            shared_state.set("key", "value")
            assert shared_state.get("key") == "value"
    """
    return SharedState(state_dir=str(clean_state_dir))


@pytest.fixture(autouse=True)
def cleanup_state(shared_state):
    """
    Automatically clean up state after each test.
    
    This fixture runs automatically for all tests in this directory.
    """
    yield  # Test runs here
    
    # Cleanup after test
    shared_state.clear()


@pytest.fixture
def mock_llm():
    """
    Provide mock LLM that returns deterministic responses.
    
    Usage:
        def test_agent(mock_llm):
            agent = ResearchAgent(llm=mock_llm)
            result = agent.gather_info("query")
            # Fast, deterministic testing
    """
    class MockLLM:
        def __init__(self):
            self.call_count = 0
            self.last_messages = None
        
        def chat(self, messages, tools=None):
            """Return deterministic response."""
            self.call_count += 1
            self.last_messages = messages
            
            # Simple pattern matching for different agent types
            system_msg = messages[0]["content"].lower()
            
            if "research" in system_msg:
                return {
                    "role": "assistant",
                    "content": "I found 3 sources about electric vehicles."
                }
            elif "data" in system_msg:
                return {
                    "role": "assistant",
                    "content": "Growth rate: 55%. Market size: 10.5M units."
                }
            elif "writer" in system_msg:
                return {
                    "role": "assistant",
                    "content": "# Report\n\nEV market is growing rapidly."
                }
            else:
                return {
                    "role": "assistant",
                    "content": "Task completed successfully."
                }
    
    return MockLLM()


@pytest.fixture
def mock_research_agent(shared_state):
    """
    Provide mock research agent with predictable behavior.
    
    Usage:
        def test_coordinator(mock_research_agent):
            coordinator = Coordinator()
            coordinator.research = mock_research_agent
            # Test coordination logic without real agent
    """
    class MockResearchAgent:
        name = "research"
        
        def __init__(self):
            self.executed_actions = []
        
        def execute(self, action, payload):
            self.executed_actions.append((action, payload))
            return {
                "status": "success",
                "findings": [
                    {"fact": "EV sales: 10.5M", "source": "mock"},
                    {"fact": "Growth: 55%", "source": "mock"}
                ],
                "sources_count": 2
            }
        
        def execute_message(self, request: Message) -> Message:
            result = self.execute(request.action, request.payload)
            return Message(
                from_agent=self.name,
                to_agent=request.from_agent,
                message_type=MessageType.RESPONSE,
                payload=result,
                in_reply_to=request.message_id
            )
    
    return MockResearchAgent()


@pytest.fixture
def mock_data_agent(shared_state):
    """Provide mock data agent."""
    class MockDataAgent:
        name = "data"
        
        def execute(self, action, payload):
            return {
                "status": "success",
                "analysis": {
                    "growth_rate": 55.0,
                    "market_size": 10.5
                },
                "metrics_count": 2
            }
        
        def execute_message(self, request: Message) -> Message:
            result = self.execute(request.action, request.payload)
            return Message(
                from_agent=self.name,
                to_agent=request.from_agent,
                message_type=MessageType.RESPONSE,
                payload=result,
                in_reply_to=request.message_id
            )
    
    return MockDataAgent()


@pytest.fixture
def mock_writer_agent(shared_state):
    """Provide mock writer agent."""
    class MockWriterAgent:
        name = "writer"
        
        def execute(self, action, payload):
            return {
                "status": "success",
                "report": "# EV Market Report\n\nMarket is growing.",
                "word_count": 50
            }
        
        def execute_message(self, request: Message) -> Message:
            result = self.execute(request.action, request.payload)
            return Message(
                from_agent=self.name,
                to_agent=request.from_agent,
                message_type=MessageType.RESPONSE,
                payload=result,
                in_reply_to=request.message_id
            )
    
    return MockWriterAgent()


@pytest.fixture
def mock_coordinator(shared_state, mock_research_agent, mock_data_agent, mock_writer_agent):
    """
    Provide fully mocked coordinator with all agents.
    
    Usage:
        def test_workflow(mock_coordinator):
            report = mock_coordinator.generate_report("test query")
            assert "report" in report
    """
    coordinator = Coordinator(shared_state)
    coordinator.research = mock_research_agent
    coordinator.data = mock_data_agent
    coordinator.writer = mock_writer_agent
    return coordinator


@pytest.fixture
def failing_agent():
    """
    Provide agent that always fails (for error handling tests).
    
    Usage:
        def test_error_handling(failing_agent):
            coordinator.research = failing_agent
            result = coordinator.generate_report("query")
            assert result["status"] == "error"
    """
    class FailingAgent:
        name = "failing"
        
        def execute(self, action, payload):
            raise TimeoutError("Agent timed out")
        
        def execute_message(self, request: Message) -> Message:
            return Message(
                from_agent=self.name,
                to_agent=request.from_agent,
                message_type=MessageType.ERROR,
                payload={"error": "Agent timed out"},
                in_reply_to=request.message_id
            )
    
    return FailingAgent()


@pytest.fixture
def message_capture():
    """
    Capture messages sent during test for inspection.
    
    Usage:
        def test_messages(message_capture):
            with message_capture:
                coordinator.generate_report("query")
            
            assert len(message_capture.messages) == 6
            assert message_capture.messages[0]["action"] == "gather_info"
    """
    class MessageCapture:
        def __init__(self):
            self.messages = []
        
        def __enter__(self):
            # Hook into message sending
            return self
        
        def __exit__(self, *args):
            pass
        
        def capture(self, message):
            self.messages.append(message.to_dict())
    
    return MessageCapture()


@pytest.fixture
def trace_id():
    """Provide consistent trace ID for tests."""
    return "test-trace-12345"
```

---

## Mock Agents for Testing

### Pattern 1: Simple Mock

```python
def test_coordinator_delegation():
    """Test coordinator delegates correctly."""
    coordinator = Coordinator()
    
    # Create simple mock
    class MockAgent:
        name = "test"
        def execute(self, action, payload):
            return {"status": "success", "result": "done"}
    
    coordinator.test_agent = MockAgent()
    result = coordinator.delegate(coordinator.test_agent, "test_action", {})
    
    assert result["status"] == "success"
```

### Pattern 2: Spy Mock (Track Calls)

```python
def test_coordinator_calls_all_agents():
    """Test coordinator calls all agents in sequence."""
    coordinator = Coordinator()
    
    # Create spy mock that tracks calls
    class SpyAgent:
        def __init__(self, name):
            self.name = name
            self.calls = []
        
        def execute(self, action, payload):
            self.calls.append((action, payload))
            return {"status": "success"}
    
    coordinator.research = SpyAgent("research")
    coordinator.data = SpyAgent("data")
    coordinator.writer = SpyAgent("writer")
    
    coordinator.generate_report("test query")
    
    # Verify all agents were called
    assert len(coordinator.research.calls) == 1
    assert len(coordinator.data.calls) == 1
    assert len(coordinator.writer.calls) == 1
    
    # Verify call order
    assert coordinator.research.calls[0][0] == "gather_info"
```

### Pattern 3: Configurable Mock

```python
@pytest.fixture
def configurable_agent():
    """Agent with configurable responses."""
    class ConfigurableAgent:
        def __init__(self, name):
            self.name = name
            self.responses = {}
        
        def set_response(self, action, response):
            self.responses[action] = response
        
        def execute(self, action, payload):
            if action in self.responses:
                return self.responses[action]
            return {"status": "success", "default": True}
    
    return ConfigurableAgent


def test_with_configurable_agent(configurable_agent):
    """Test with specific agent responses."""
    agent = configurable_agent("test")
    agent.set_response("gather_info", {
        "status": "success",
        "findings": ["fact1", "fact2"]
    })
    
    result = agent.execute("gather_info", {})
    assert len(result["findings"]) == 2
```

---

## Test Organization

### Unit Tests (30-50 tests)

Test individual components in isolation:

```python
# tests/multi_agent/test_message_protocol.py
def test_message_creation():
    """Test creating a message."""
    msg = Message(
        from_agent="coordinator",
        to_agent="research",
        message_type=MessageType.REQUEST,
        action="gather_info",
        payload={"query": "test"}
    )
    
    assert msg.from_agent == "coordinator"
    assert msg.message_id is not None
    assert msg.timestamp is not None


def test_message_serialization():
    """Test message to/from JSON."""
    msg = Message(
        from_agent="agent_a",
        to_agent="agent_b",
        message_type=MessageType.RESPONSE,
        payload={"result": "done"}
    )
    
    json_str = msg.to_json()
    restored = Message.from_json(json_str)
    
    assert restored.from_agent == msg.from_agent
    assert restored.payload == msg.payload
```

### Agent Interaction Tests (15-20 tests)

Test pairs of agents working together:

```python
# tests/multi_agent/test_specialized_agents.py
def test_research_to_data_flow(shared_state):
    """Test research agent output feeds data agent."""
    # Setup
    research = ResearchAgent(shared_state)
    data = DataAgent(shared_state)
    
    # Research gathers data
    research.gather_info("EV market")
    
    # Verify research wrote to state
    findings = shared_state.get("research_findings")
    assert findings is not None
    assert len(findings) > 0
    
    # Data agent analyzes
    analysis = data.analyze_trends()
    
    # Verify data agent read correctly
    assert analysis["status"] == "success"
    assert "growth_rate" in analysis["analysis"]
```

### Integration Tests (5-10 tests)

Test full workflows:

```python
# tests/multi_agent/test_integration.py
def test_full_report_workflow(mock_coordinator):
    """Test complete report generation."""
    report = mock_coordinator.generate_report("EV market trends")
    
    # Validate coordination
    assert mock_coordinator.research.executed_actions
    assert mock_coordinator.data.executed_actions
    assert mock_coordinator.writer.executed_actions
    
    # Validate output
    assert isinstance(report, str)
    assert len(report) > 100
    assert "#" in report  # Has markdown headings


@pytest.mark.slow
def test_full_workflow_with_real_llm():
    """Integration test with real LLM (slow)."""
    coordinator = Coordinator()  # Real agents, real LLM
    
    report = coordinator.generate_report("EV market")
    
    # Quality checks
    assert len(report) > 500
    assert "electric vehicle" in report.lower()
    assert "market" in report.lower()
```

---

## Running Tests

### pytest.ini Configuration

```ini
[pytest]
# Test discovery
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Output
addopts = 
    -v
    --strict-markers
    --tb=short
    --disable-warnings

# Markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    real_llm: marks tests that use real LLM (cost money)

# Coverage
#--cov=src/multi_agent
#--cov-report=html
#--cov-report=term-missing
```

### Common Test Commands

```bash
# Run all tests
pytest tests/multi_agent/

# Run specific test file
pytest tests/multi_agent/test_coordinator.py

# Run specific test
pytest tests/multi_agent/test_coordinator.py::test_delegation

# Run with verbose output
pytest tests/multi_agent/ -v

# Run fast tests only (skip slow)
pytest tests/multi_agent/ -m "not slow"

# Run with coverage
pytest tests/multi_agent/ --cov=src/multi_agent --cov-report=html

# Run and show print statements
pytest tests/multi_agent/ -s

# Run and drop into debugger on failure
pytest tests/multi_agent/ --pdb

# Run tests matching pattern
pytest tests/multi_agent/ -k "coordinator"
```

---

## Common Patterns

### Pattern 1: Parametrized Tests

Test same logic with different inputs:

```python
@pytest.mark.parametrize("query,expected_sources", [
    ("EV market", 5),
    ("Tesla sales", 3),
    ("Battery technology", 4),
])
def test_research_with_different_queries(shared_state, query, expected_sources):
    """Test research agent with various queries."""
    agent = ResearchAgent(shared_state)
    result = agent.gather_info(query, max_sources=expected_sources)
    
    assert result["status"] == "success"
    assert len(result["findings"]) <= expected_sources
```

### Pattern 2: Fixture Composition

Build complex fixtures from simpler ones:

```python
@pytest.fixture
def coordinator_with_mocks(shared_state, mock_research_agent, mock_data_agent):
    """Coordinator with some mocked agents."""
    coordinator = Coordinator(shared_state)
    coordinator.research = mock_research_agent
    coordinator.data = mock_data_agent
    # Writer is real agent for testing
    return coordinator
```

### Pattern 3: Test Context Managers

Clean setup and teardown:

```python
@pytest.fixture
def test_workflow():
    """Context for testing workflows."""
    class WorkflowContext:
        def __init__(self):
            self.messages = []
            self.state_snapshots = []
        
        def __enter__(self):
            # Setup: Start capturing
            return self
        
        def __exit__(self, *args):
            # Teardown: Cleanup
            pass
    
    return WorkflowContext()


def test_with_context(test_workflow):
    """Test using workflow context."""
    with test_workflow as ctx:
        # Test code here
        assert len(ctx.messages) == 0
```

---

## Best Practices

### 1. Test Isolation

```python
# GOOD: Each test is independent
def test_a(shared_state):
    shared_state.set("key", "a")
    assert shared_state.get("key") == "a"

def test_b(shared_state):
    # Fresh state, test_a didn't affect this
    assert shared_state.get("key") is None
```

### 2. Descriptive Test Names

```python
# BAD
def test_1():
    pass

# GOOD
def test_coordinator_retries_failed_agent_with_exponential_backoff():
    pass
```

### 3. AAA Pattern (Arrange, Act, Assert)

```python
def test_message_protocol():
    # Arrange
    msg = Message(
        from_agent="a",
        to_agent="b",
        message_type=MessageType.REQUEST,
        payload={}
    )
    
    # Act
    json_str = msg.to_json()
    restored = Message.from_json(json_str)
    
    # Assert
    assert restored.from_agent == "a"
```

### 4. One Assertion Per Concept

```python
# GOOD: Clear what's being tested
def test_message_has_required_fields():
    msg = Message(...)
    assert msg.message_id is not None

def test_message_generates_timestamp():
    msg = Message(...)
    assert msg.timestamp is not None

# Instead of combining into one test
```

---

## Next Steps

Now that you have testing infrastructure:

1. ✅ Write unit tests for each agent
2. ✅ Add interaction tests for agent pairs
3. ✅ Create integration tests for workflows
4. ✅ Run tests before committing code

**See Also:**
- [Testing Multi-Agent Systems](../tutorial-2/guides/testing-multi-agent.md) - Testing methodology
- [Debugging Multi-Agent Systems](../tutorial-2/guides/debugging-multi-agent.md) - When tests fail

---

[← Back to Lab 2](./README.md) | [Testing Guide →](../tutorial-2/guides/testing-multi-agent.md)

