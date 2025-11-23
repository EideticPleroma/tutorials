"""
Multi-agent system implementation for Tutorial 2.

This package provides core components for building multi-agent systems:
- Coordinator: Orchestrates multiple specialized agents
- Worker Base: Base class for specialized worker agents
- Message Protocol: Inter-agent communication
- Shared State: State management across agents
"""

from .coordinator import Coordinator
from .worker_base import WorkerAgent
from .message_protocol import Message, MessageType
from .shared_state import SharedState

__all__ = [
    'Coordinator',
    'WorkerAgent',
    'Message',
    'MessageType',
    'SharedState',
]

