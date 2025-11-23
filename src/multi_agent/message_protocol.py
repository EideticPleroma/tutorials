"""
Message protocol for inter-agent communication.

Provides structured messaging with JSON serialization for
traceability, debugging, and standardization across agents.
"""

from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime
import json
import uuid


class MessageType(Enum):
    """Types of messages in the multi-agent system."""
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"


class Message:
    """
    Structured message for agent-to-agent communication.
    
    Every message includes:
    - Unique ID for tracking
    - Timestamp for ordering
    - From/to agents for routing
    - Message type (request/response/error)
    - Payload with actual data
    - Optional trace ID for workflow tracking
    
    Example:
        request = Message(
            from_agent="coordinator",
            to_agent="research",
            message_type=MessageType.REQUEST,
            action="gather_info",
            payload={"query": "EV market"}
        )
        
        json_str = request.to_json()
        # Send over network or log
        
        received = Message.from_json(json_str)
    """
    
    def __init__(
        self,
        from_agent: str,
        to_agent: str,
        message_type: MessageType,
        payload: Dict[str, Any],
        action: Optional[str] = None,
        in_reply_to: Optional[str] = None,
        trace_id: Optional[str] = None,
        message_id: Optional[str] = None,
        timestamp: Optional[str] = None
    ):
        """
        Create a new message.
        
        Args:
            from_agent: Sender agent name
            to_agent: Recipient agent name
            message_type: Type of message (REQUEST, RESPONSE, ERROR)
            payload: Message data
            action: Action to perform (for requests)
            in_reply_to: Message ID this is replying to (for responses)
            trace_id: Workflow trace ID (generated if not provided)
            message_id: Unique message ID (generated if not provided)
            timestamp: ISO timestamp (generated if not provided)
        """
        self.message_id = message_id or str(uuid.uuid4())
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.message_type = message_type
        self.action = action
        self.payload = payload
        self.in_reply_to = in_reply_to
        self.trace_id = trace_id or str(uuid.uuid4())
    
    def to_dict(self) -> Dict:
        """
        Convert message to dictionary for serialization.
        
        Returns:
            Dictionary representation of message
        """
        return {
            "message_id": self.message_id,
            "timestamp": self.timestamp,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "message_type": self.message_type.value,
            "action": self.action,
            "payload": self.payload,
            "in_reply_to": self.in_reply_to,
            "trace_id": self.trace_id
        }
    
    def to_json(self) -> str:
        """
        Serialize message to JSON string.
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Message':
        """
        Deserialize message from dictionary.
        
        Args:
            data: Dictionary with message fields
        
        Returns:
            Message instance
        """
        return cls(
            message_id=data.get("message_id"),
            timestamp=data.get("timestamp"),
            from_agent=data["from_agent"],
            to_agent=data["to_agent"],
            message_type=MessageType(data["message_type"]),
            action=data.get("action"),
            payload=data["payload"],
            in_reply_to=data.get("in_reply_to"),
            trace_id=data.get("trace_id")
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Message':
        """
        Deserialize message from JSON string.
        
        Args:
            json_str: JSON string representation
        
        Returns:
            Message instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return (f"Message(id={self.message_id[:8]}..., "
                f"from={self.from_agent}, to={self.to_agent}, "
                f"type={self.message_type.value})")

