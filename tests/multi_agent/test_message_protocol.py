"""
Tests for message protocol using O.V.E. methodology.

Students complete these tests as they implement message protocol in Exercise 3.
"""

import pytest
import json
from src.multi_agent.message_protocol import Message, MessageType


def test_message_creation():
    """
    Observe: Message created with all required fields.
    Validate: Fields are correctly set, IDs generated.
    """
    message = Message(
        from_agent="coordinator",
        to_agent="research",
        message_type=MessageType.REQUEST,
        action="gather_info",
        payload={"query": "test"}
    )
    
    assert message.from_agent == "coordinator"
    assert message.to_agent == "research"
    assert message.message_type == MessageType.REQUEST
    assert message.action == "gather_info"
    assert message.payload == {"query": "test"}
    assert message.message_id is not None
    assert message.timestamp is not None
    assert message.trace_id is not None


def test_message_serialization():
    """
    Observe: Message can be serialized to/from JSON.
    Validate: All fields preserved, format correct.
    """
    original = Message(
        from_agent="coordinator",
        to_agent="research",
        message_type=MessageType.REQUEST,
        action="gather_info",
        payload={"query": "EV market"}
    )
    
    # Serialize to JSON
    json_str = original.to_json()
    assert isinstance(json_str, str)
    
    # Can parse as JSON
    data = json.loads(json_str)
    assert "message_id" in data
    assert "timestamp" in data
    assert data["from_agent"] == "coordinator"
    assert data["to_agent"] == "research"
    
    # Deserialize back to Message
    restored = Message.from_json(json_str)
    assert restored.from_agent == original.from_agent
    assert restored.to_agent == original.to_agent
    assert restored.action == original.action
    assert restored.payload == original.payload


def test_response_message_links_to_request():
    """
    Observe: Response message references original request.
    Validate: in_reply_to field correctly set.
    """
    request = Message(
        from_agent="coordinator",
        to_agent="research",
        message_type=MessageType.REQUEST,
        action="gather_info",
        payload={"query": "test"}
    )
    
    response = Message(
        from_agent="research",
        to_agent="coordinator",
        message_type=MessageType.RESPONSE,
        payload={"status": "success", "findings": []},
        in_reply_to=request.message_id,
        trace_id=request.trace_id
    )
    
    assert response.in_reply_to == request.message_id
    assert response.trace_id == request.trace_id


def test_error_message_format():
    """
    Observe: Error messages have appropriate structure.
    Validate: MessageType.ERROR, error info in payload.
    """
    error_msg = Message(
        from_agent="research",
        to_agent="coordinator",
        message_type=MessageType.ERROR,
        payload={
            "error": "Rate limit exceeded",
            "retry_after": "60s"
        }
    )
    
    assert error_msg.message_type == MessageType.ERROR
    assert "error" in error_msg.payload

