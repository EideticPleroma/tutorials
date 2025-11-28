# Exercise 1B: Message Protocol

| Duration | Difficulty | Prerequisites | Skills Practiced |
|----------|------------|---------------|------------------|
| ~60 min | Intermediate | Exercise 1A (Coordinator Basics) | Message design, Protocol implementation, Traceability |

## Objective

Refactor the coordinator from Exercise 1A to use a structured message protocol instead of direct function calls. This enables traceability, async communication, and proper error handling.

## Context

In Exercise 1A, delegation looked like this:

```python
# Direct function call - simple but limited
result = agent.execute(action, payload)
```

**Problems with direct calls:**
- **No traceability**: Can't follow a request through the system
- **No timestamps**: Don't know when things happened  
- **No linking**: Can't connect a response to its request
- **No structured errors**: Just strings or exceptions

**Message protocol solves these:**

```python
# Structured message - traceable and extensible
request = Message(
    message_id="msg-001",
    timestamp="2024-01-15T10:30:00Z",
    from_agent="coordinator",
    to_agent="research",
    message_type=MessageType.REQUEST,
    action="gather_info",
    payload={"query": "EVs"},
    trace_id="trace-abc-123"
)

response = agent.execute_message(request)
# Response has in_reply_to="msg-001" linking it back!
```

**Why this matters for real systems:**
- **Debugging**: "Show me all messages in trace-abc-123"
- **Auditing**: "What happened at 10:30am?"
- **Async**: Messages can be queued and processed later
- **Recovery**: Replay messages after a failure

## Prerequisites

- [ ] Completed Exercise 1A (Coordinator working with direct calls)
- [ ] Read [Agent Communication](../../tutorial-2/concepts/agent-communication.md)
- [ ] Review `src/multi_agent/message_protocol.py` scaffold

## What You'll Build

1. **MessageType enum**: REQUEST, RESPONSE, ERROR
2. **Message class**: Structured communication with all required fields
3. **Serialization**: JSON for logging and debugging
4. **Updated delegate()**: Uses messages instead of direct calls

## Tasks

### Task 1: Implement MessageType Enum

Create the message types in `src/multi_agent/message_protocol.py`.

**Requirements:**
- REQUEST: Agent asking for work
- RESPONSE: Agent returning results
- ERROR: Something went wrong

**Code:**
```python
"""
Message protocol for agent communication.

All agent-to-agent communication uses structured messages
for traceability, debugging, and future async support.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid
import json

class MessageType(Enum):
    """Types of messages in agent communication."""
    REQUEST = "request"    # Coordinator asking agent to do something
    RESPONSE = "response"  # Agent returning results
    ERROR = "error"        # Something went wrong
```

**Validation:**
```python
from src.multi_agent.message_protocol import MessageType

assert MessageType.REQUEST.value == "request"
assert MessageType.RESPONSE.value == "response"
assert MessageType.ERROR.value == "error"
```

### Task 2: Implement Message Class

The Message class captures all communication metadata.

**Required fields:**
- `message_id`: Unique identifier (auto-generated UUID)
- `timestamp`: When message was created (auto-generated)
- `from_agent`: Who sent it
- `to_agent`: Who receives it
- `message_type`: REQUEST, RESPONSE, or ERROR
- `action`: What to do (for REQUEST)
- `payload`: Data for the action
- `in_reply_to`: Links response to request (optional)
- `trace_id`: Groups related messages (optional)

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/message_protocol.py

I'm working on Exercise 1B (Message Protocol).

I need to implement a Message dataclass with:
1. message_id: str (default: auto-generated UUID)
2. timestamp: str (default: ISO format datetime)
3. from_agent: str
4. to_agent: str
5. message_type: MessageType
6. action: str (default: "")
7. payload: Dict[str, Any] (default: empty dict)
8. in_reply_to: Optional[str] (default: None)
9. trace_id: Optional[str] (default: None)

Use @dataclass with field() defaults for auto-generated values.

Generate the Message class.
```

**Implementation:**
```python
@dataclass
class Message:
    """
    Structured message for agent communication.
    
    Attributes:
        message_id: Unique identifier (auto-generated)
        timestamp: ISO format creation time (auto-generated)
        from_agent: Sending agent name
        to_agent: Receiving agent name  
        message_type: REQUEST, RESPONSE, or ERROR
        action: What to do (for requests)
        payload: Data for the action
        in_reply_to: Links to original request (for responses)
        trace_id: Groups related messages for debugging
    """
    from_agent: str
    to_agent: str
    message_type: MessageType
    action: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    in_reply_to: Optional[str] = None
    trace_id: Optional[str] = None
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
```

**Validation:**
```python
from src.multi_agent.message_protocol import Message, MessageType

msg = Message(
    from_agent="coordinator",
    to_agent="research",
    message_type=MessageType.REQUEST,
    action="gather_info",
    payload={"query": "test"}
)

assert msg.message_id is not None  # Auto-generated
assert msg.timestamp is not None   # Auto-generated
assert msg.from_agent == "coordinator"
assert msg.to_agent == "research"
assert msg.message_type == MessageType.REQUEST
```

### Task 3: Add JSON Serialization

Messages need to be serializable for logging and debugging.

**Requirements:**
- `to_json()`: Convert message to JSON string
- `from_json()`: Create message from JSON string
- Handle MessageType enum properly

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/message_protocol.py

I need to add serialization methods to the Message class.

Requirements:
1. to_json() -> str: Serialize message to JSON
   - Convert message_type enum to string value
   - Return JSON string
   
2. from_json(json_str: str) -> Message: Deserialize from JSON
   - Parse JSON string
   - Convert message_type string back to enum
   - Return Message instance

Generate both methods as part of the Message class.
```

**Implementation:**
```python
def to_json(self) -> str:
    """Serialize message to JSON string."""
    data = {
        "message_id": self.message_id,
        "timestamp": self.timestamp,
        "from_agent": self.from_agent,
        "to_agent": self.to_agent,
        "message_type": self.message_type.value,  # Enum to string
        "action": self.action,
        "payload": self.payload,
        "in_reply_to": self.in_reply_to,
        "trace_id": self.trace_id
    }
    return json.dumps(data)

@classmethod
def from_json(cls, json_str: str) -> "Message":
    """Deserialize message from JSON string."""
    data = json.loads(json_str)
    data["message_type"] = MessageType(data["message_type"])  # String to enum
    return cls(**data)
```

**Validation:**
```python
# Create a message
original = Message(
    from_agent="coordinator",
    to_agent="research",
    message_type=MessageType.REQUEST,
    action="gather_info",
    payload={"query": "test"},
    trace_id="trace-123"
)

# Serialize
json_str = original.to_json()
print(json_str)  # Should be valid JSON

# Deserialize
restored = Message.from_json(json_str)
assert restored.from_agent == original.from_agent
assert restored.action == original.action
assert restored.trace_id == original.trace_id
assert restored.message_type == MessageType.REQUEST
```

### Task 4: Add Helper Methods

Add convenience methods for creating responses and errors.

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/message_protocol.py

I need to add helper methods to Message class.

Requirements:
1. create_response(self, payload: Dict) -> Message
   - Creates RESPONSE message
   - Sets in_reply_to = self.message_id
   - Swaps from_agent and to_agent
   - Copies trace_id
   
2. create_error(self, error: str) -> Message
   - Creates ERROR message  
   - Sets in_reply_to = self.message_id
   - Swaps from_agent and to_agent
   - Sets payload = {"error": error}
   - Copies trace_id

Generate both methods.
```

**Implementation:**
```python
def create_response(self, payload: Dict[str, Any]) -> "Message":
    """Create a response to this message."""
    return Message(
        from_agent=self.to_agent,      # Swap sender/receiver
        to_agent=self.from_agent,
        message_type=MessageType.RESPONSE,
        action=self.action,
        payload=payload,
        in_reply_to=self.message_id,   # Link to original
        trace_id=self.trace_id         # Keep trace context
    )

def create_error(self, error: str) -> "Message":
    """Create an error response to this message."""
    return Message(
        from_agent=self.to_agent,
        to_agent=self.from_agent,
        message_type=MessageType.ERROR,
        action=self.action,
        payload={"error": error},
        in_reply_to=self.message_id,
        trace_id=self.trace_id
    )
```

**Validation:**
```python
request = Message(
    from_agent="coordinator",
    to_agent="research",
    message_type=MessageType.REQUEST,
    action="gather_info",
    payload={"query": "test"},
    trace_id="trace-123"
)

# Create response
response = request.create_response({"findings": ["fact1", "fact2"]})
assert response.from_agent == "research"
assert response.to_agent == "coordinator"
assert response.message_type == MessageType.RESPONSE
assert response.in_reply_to == request.message_id
assert response.trace_id == "trace-123"

# Create error
error = request.create_error("Agent timeout")
assert error.message_type == MessageType.ERROR
assert error.payload["error"] == "Agent timeout"
assert error.in_reply_to == request.message_id
```

### Task 5: Update Coordinator to Use Messages

Refactor `delegate()` to use the message protocol.

**Requirements:**
- Create REQUEST message with trace_id
- Log message sent (JSON)
- Call `agent.execute_message(request)` instead of `execute()`
- Log message received (JSON)
- Handle RESPONSE and ERROR message types
- Return payload from response

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/coordinator.py @src/multi_agent/message_protocol.py

I need to refactor Coordinator.delegate() to use message protocol.

Requirements:
1. Generate trace_id if not provided (uuid)
2. Create REQUEST Message with all fields
3. Log: "Message sent: {message.to_json()}"
4. Call agent.execute_message(request) 
5. Log: "Message received: {response.to_json()}"
6. If response.message_type == ERROR, raise DelegationError
7. If payload has status="error", raise DelegationError
8. Return response.payload on success

Add trace_id parameter to delegate() signature.

Generate the updated implementation.
```

**Updated Coordinator:**
```python
from .message_protocol import Message, MessageType
import uuid

def delegate(
    self, 
    agent: Any, 
    action: str, 
    payload: Dict,
    trace_id: Optional[str] = None,
    max_retries: int = 3
) -> Dict:
    """
    Delegate task to worker agent using message protocol.
    
    Args:
        agent: Worker agent to delegate to
        action: Action for agent to perform
        payload: Data for the action
        trace_id: Optional trace ID for debugging (auto-generated if not provided)
        max_retries: Number of retry attempts
        
    Returns:
        Response payload from worker agent
    """
    if agent is None:
        raise DelegationError(f"Agent not initialized for action: {action}")
    
    # Generate trace_id if not provided
    if trace_id is None:
        trace_id = str(uuid.uuid4())
    
    # Create request message
    request = Message(
        from_agent="coordinator",
        to_agent=agent.name,
        message_type=MessageType.REQUEST,
        action=action,
        payload=payload,
        trace_id=trace_id
    )
    
    self.logger.info("Message sent: %s", request.to_json())
    
    # Execute with retries
    last_error = None
    for attempt in range(max_retries):
        try:
            response = agent.execute_message(request)
            self.logger.info("Message received: %s", response.to_json())
            
            # Check for error response
            if response.message_type == MessageType.ERROR:
                error = response.payload.get("error", "Unknown error")
                raise DelegationError(f"Agent {agent.name} error: {error}")
            
            # Check for error in payload
            if response.payload.get("status") == "error":
                error = response.payload.get("error", "Unknown error")
                raise DelegationError(f"Agent {agent.name} error: {error}")
            
            return response.payload
            
        except DelegationError:
            raise  # Don't retry delegation errors
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                self.logger.warning(
                    "Retry %d/%d for %s: %s", 
                    attempt + 1, max_retries, agent.name, str(e)
                )
                time.sleep(1)
    
    raise DelegationError(f"Agent {agent.name} failed after {max_retries} retries: {last_error}")
```

### Task 6: Update Worker Agents to Use Messages

Workers need `execute_message()` method that wraps `execute()`.

**Add to WorkerAgent base class or mock agents:**

```python
def execute_message(self, request: Message) -> Message:
    """
    Execute a request message and return response message.
    
    This wraps execute() with message protocol handling.
    """
    try:
        # Call the existing execute method
        result = self.execute(request.action, request.payload)
        
        # Check for error in result
        if result.get("status") == "error":
            return request.create_error(result.get("error", "Unknown error"))
        
        # Return success response
        return request.create_response(result)
        
    except Exception as e:
        return request.create_error(str(e))
```

**Validation:**
```python
from src.multi_agent.coordinator import Coordinator
from src.multi_agent.message_protocol import Message, MessageType

coordinator = Coordinator()

# Test delegation with message protocol
result = coordinator.delegate(
    coordinator.research,
    "gather_info",
    {"query": "test"},
    trace_id="test-trace-001"
)

assert result["status"] == "success"
assert "findings" in result

# Check logs show JSON messages
# Should see: Message sent: {"message_id": "...", "trace_id": "test-trace-001", ...}
# Should see: Message received: {"in_reply_to": "...", "trace_id": "test-trace-001", ...}
```

## Testing Your Implementation

### Unit Tests

Create `tests/multi_agent/test_message_protocol.py`:

```python
import pytest
from src.multi_agent.message_protocol import Message, MessageType

def test_message_creation():
    """Message creates with auto-generated fields."""
    msg = Message(
        from_agent="coordinator",
        to_agent="research",
        message_type=MessageType.REQUEST,
        action="gather_info"
    )
    assert msg.message_id is not None
    assert msg.timestamp is not None
    assert msg.from_agent == "coordinator"

def test_message_serialization():
    """Message serializes and deserializes correctly."""
    original = Message(
        from_agent="coordinator",
        to_agent="research",
        message_type=MessageType.REQUEST,
        action="gather_info",
        payload={"query": "test"},
        trace_id="trace-123"
    )
    
    json_str = original.to_json()
    restored = Message.from_json(json_str)
    
    assert restored.from_agent == original.from_agent
    assert restored.message_type == original.message_type
    assert restored.trace_id == original.trace_id

def test_response_message_links_to_request():
    """Response message links back to request."""
    request = Message(
        from_agent="coordinator",
        to_agent="research",
        message_type=MessageType.REQUEST,
        action="test",
        trace_id="trace-123"
    )
    
    response = request.create_response({"result": "done"})
    
    assert response.in_reply_to == request.message_id
    assert response.trace_id == request.trace_id
    assert response.from_agent == "research"
    assert response.to_agent == "coordinator"

def test_error_message_format():
    """Error message has correct structure."""
    request = Message(
        from_agent="coordinator",
        to_agent="research",
        message_type=MessageType.REQUEST,
        action="test"
    )
    
    error = request.create_error("Something broke")
    
    assert error.message_type == MessageType.ERROR
    assert error.payload["error"] == "Something broke"
    assert error.in_reply_to == request.message_id
```

Run tests:
```bash
python -m pytest tests/multi_agent/test_message_protocol.py -v
```

Expected: 4/4 tests passing

### Integration Test

Test coordinator with message protocol:

```python
coordinator = Coordinator()

# Full workflow with trace_id
report = coordinator.generate_report("electric vehicles")

# Check logs show message flow with same trace_id
# All messages in workflow should share trace_id
```

## Checkpoint Questions

Before moving to Exercise 2, verify:

- [ ] MessageType enum has REQUEST, RESPONSE, ERROR?
- [ ] Message class has all required fields?
- [ ] `to_json()` and `from_json()` work correctly?
- [ ] Response messages link to requests via `in_reply_to`?
- [ ] Coordinator `delegate()` uses message protocol?
- [ ] Workers have `execute_message()` method?
- [ ] All tests pass?

**Understanding Check:**

1. Why use `in_reply_to` instead of just checking the trace_id?
2. What does the trace_id enable that message_id doesn't?
3. How would you use the message log to debug a failed workflow?

<details>
<summary>Show Answers</summary>

1. **Why in_reply_to**: Trace_id groups all messages in a workflow, but a workflow might have multiple requests. `in_reply_to` tells you exactly which request a response answers. Example: If coordinator sends 3 requests to research, each response links to its specific request.

2. **Trace_id enables**: Following an entire user request through the system. "Show me everything that happened for trace-abc-123" gives you the full story. Message_id is unique per message, trace_id is shared across all related messages.

3. **Debugging with logs**:
   ```bash
   # Filter logs by trace_id
   grep "trace-abc-123" .agent_logs/agent.log | jq
   
   # See the full flow:
   # 1. REQUEST from coordinator to research
   # 2. RESPONSE from research to coordinator
   # 3. REQUEST from coordinator to data
   # ...
   ```
   You can see exactly what was sent, what was received, and in what order.

</details>

## What's Next

You now have a coordinator with structured message protocol. This enables:

- **Traceability**: Follow requests through the system
- **Debugging**: Log all messages as JSON
- **Error handling**: Structured ERROR messages
- **Future async**: Messages can be queued

Exercise 2 creates real specialized agents (Research, Data, Writer) that work with your coordinator.

---

## Common Issues

**Issue: "MessageType not JSON serializable"**
- Use `.value` when serializing: `message_type.value`
- Use `MessageType(value)` when deserializing

**Issue: "Agent has no execute_message method"**
- Add `execute_message()` to mock agents
- Or update WorkerAgent base class

**Issue: "in_reply_to is None in response"**
- Check `create_response()` sets it from `self.message_id`
- Verify you're calling `request.create_response()` not creating new Message

**Issue: "Logs don't show JSON"**
- Call `message.to_json()` in log statement
- Check logger is configured (not suppressed)

---

## Design Tips

**Message design:**
- Keep payload flexible (dict)
- Required metadata in fixed fields
- Trace_id groups, message_id identifies

**Protocol evolution:**
- Start simple (3 message types)
- Add types as needed (HEARTBEAT, CANCEL, etc.)
- Keep backward compatible

**Logging:**
- Log every message (sent and received)
- Include full JSON for debugging
- Filter by trace_id to follow flows

---

**Next: [Exercise 2: Create Specialized Agents](./02-specialized-agents.md)** - Build real workers that use the coordinator and message protocol.

