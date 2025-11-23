# Exercise 3: Implement Agent Communication

**Duration**: ~60 minutes | **Difficulty**: Intermediate

## Objective

Implement a formal message protocol for agent-to-agent communication and integrate it with your coordinator and worker agents.

## Context

In Exercises 1-2, you likely passed data directly between agents. Now you'll formalize communication using a **message protocol** that provides:
- ✅ Traceability (every message is logged)
- ✅ Structure (consistent format)
- ✅ Error handling (explicit error messages)
- ✅ Debuggability (can reconstruct entire workflow from logs)

## Prerequisites

- [ ] Completed Exercises 1 & 2
- [ ] Read [Agent Communication](../../tutorial-2/concepts/agent-communication.md)
- [ ] Review `src/multi_agent/message_protocol.py` scaffold

## Code Scaffold

Open `src/multi_agent/message_protocol.py`:

```python
"""
Message protocol for inter-agent communication.

Provides structured messaging with JSON serialization.
"""

from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime
import json
import uuid

class MessageType(Enum):
    """Types of messages in the system."""
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"

class Message:
    """
    Structured message for agent communication.
    
    Every message includes:
    - Unique ID for tracking
    - Timestamp for ordering
    - From/to agents for routing
    - Message type (request/response/error)
    - Payload with actual data
    """
    
    def __init__(
        self,
        from_agent: str,
        to_agent: str,
        message_type: MessageType,
        payload: Dict[str, Any],
        action: Optional[str] = None,
        in_reply_to: Optional[str] = None,
        trace_id: Optional[str] = None
    ):
        """
        Create a new message.
        
        TODO: Initialize all fields including:
        - message_id (generate UUID)
        - timestamp (ISO format)
        - All parameters
        """
        pass
    
    def to_dict(self) -> Dict:
        """
        Convert message to dictionary for serialization.
        
        TODO: Return dict with all message fields
        """
        pass
    
    def to_json(self) -> str:
        """
        Serialize message to JSON string.
        
        TODO: Use to_dict() and json.dumps()
        """
        pass
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Message':
        """
        Deserialize message from dictionary.
        
        TODO: Create Message from dict fields
        """
        pass
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Message':
        """
        Deserialize message from JSON string.
        
        TODO: Use json.loads() and from_dict()
        """
        pass
```

## Tasks

### Task 1: Implement Message Class

Implement all Message methods.

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/message_protocol.py

Implement the Message class for inter-agent communication.

Requirements:
- __init__: Generate message_id (UUID), timestamp (ISO format), store all params
- to_dict(): Return dict with all fields (message_id, timestamp, from_agent, to_agent, message_type, action, payload, in_reply_to, trace_id)
- to_json(): Convert to_dict() to JSON string
- from_dict(): Create Message from dict
- from_json(): Parse JSON and use from_dict()

Generate complete implementation following the protocol specification.
```

**Validation:**
```python
# Test message creation and serialization
msg = Message(
    from_agent="coordinator",
    to_agent="research",
    message_type=MessageType.REQUEST,
    action="gather_info",
    payload={"query": "test"}
)

assert msg.message_id is not None
assert msg.timestamp is not None

# Test serialization
json_str = msg.to_json()
msg2 = Message.from_json(json_str)
assert msg2.from_agent == "coordinator"
assert msg2.payload["query"] == "test"
```

### Task 2: Update Coordinator to Use Messages

Update your coordinator from Exercise 1 to use the Message protocol.

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/coordinator.py @src/multi_agent/message_protocol.py

Update Coordinator.delegate() to use Message protocol:

Current (direct call):
result = agent.execute(action, payload)

New (with messages):
1. Create request Message(from="coordinator", to=agent.name, type=REQUEST, action=action, payload=payload)
2. Log message as JSON: self.logger.info(request.to_json())
3. Call agent.execute_message(request)
4. Receive response Message
5. Log response
6. Return response.payload

Generate updated delegate() method using Message protocol.
```

### Task 3: Update Worker Agents

Update worker base class to handle messages.

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/worker_base.py

Add execute_message() method to WorkerAgent:

def execute_message(self, request: Message) -> Message:
    """
    Execute action from request message, return response message.
    
    Args:
        request: Request message with action and payload
    
    Returns:
        Response message with results or error
    """
    try:
        # Extract action and payload from request
        # Call existing execute() method
        # Wrap result in response Message
        # Return response
    except Exception as e:
        # Return error Message
    
Generate implementation.
```

### Task 4: Add Message Logging

Add structured logging for all messages.

**Requirements:**
- Log when coordinator sends message
- Log when agent receives message
- Log when agent sends response
- Include trace_id in all logs

**Implementation:**
```python
def delegate(self, agent, action, payload, trace_id=None):
    if trace_id is None:
        trace_id = str(uuid.uuid4())
    
    request = Message(
        from_agent="coordinator",
        to_agent=agent.name,
        message_type=MessageType.REQUEST,
        action=action,
        payload=payload,
        trace_id=trace_id
    )
    
    # Log message sent
    self.logger.info(f"MESSAGE_SENT: {request.to_json()}")
    
    response = agent.execute_message(request)
    
    # Log message received
    self.logger.info(f"MESSAGE_RECEIVED: {response.to_json()}")
    
    return response
```

## Integration Testing

### Test Message Flow

```python
from src.multi_agent import Coordinator, SharedState
from src.multi_agent.specialized import ResearchAgent

# Setup
shared_state = SharedState()
coordinator = Coordinator(shared_state)
research = ResearchAgent(shared_state)
coordinator.research = research

# Execute with message protocol
import uuid
trace_id = str(uuid.uuid4())

result = coordinator.delegate(
    agent=research,
    action="gather_info",
    payload={"query": "test"},
    trace_id=trace_id
)

# Check logs
import subprocess
logs = subprocess.run(
    ["grep", trace_id, ".agent_logs/agent.log"],
    capture_output=True,
    text=True
)
print(logs.stdout)
# Should show request and response messages
```

### Visualize Message Flow

```bash
# Extract message flow for a trace
grep "MESSAGE_SENT\|MESSAGE_RECEIVED" .agent_logs/agent.log | \
  grep "<trace_id>" | \
  jq -r '[.timestamp, .message.from_agent, .message.to_agent, .message.message_type] | @tsv'
```

## Run Tests

```bash
python -m pytest tests/multi_agent/test_message_protocol.py -v
```

## Checkpoint Questions

- [ ] Can messages be serialized to/from JSON?
- [ ] Does coordinator create request messages?
- [ ] Do workers return response messages?
- [ ] Are all messages logged with trace_id?
- [ ] Can you reconstruct workflow from logs?

## Common Issues

**Issue: "Message fields missing"**
- Ensure all required fields in to_dict()
- Check MessageType is enum value, not string

**Issue: "JSON serialization fails"**
- MessageType needs to be converted to string: `message_type.value`
- Datetime needs ISO format: `datetime.utcnow().isoformat()`

**Issue: "Can't match requests to responses"**
- Use `in_reply_to` field in response
- Response should reference request.message_id

See [Troubleshooting - Communication Errors](../troubleshooting.md#agent-communication-errors).

## Next Steps

👉 **Continue to [Exercise 4: Challenge - Research Workflow](./04-challenge-workflow.md)**

Build a complete end-to-end multi-agent system!

---

## 💡 Design Tips

**Message Protocol:**
- Every interaction is a message
- Logs are your debugging superpower
- Trace IDs connect related messages

**Serialization:**
- JSON for human readability
- ISO timestamps for sorting
- UUIDs for unique identification

**Integration:**
- Update one component at a time
- Test after each change
- Use trace_id to track workflows

