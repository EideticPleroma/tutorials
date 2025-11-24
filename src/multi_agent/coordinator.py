"""
Coordinator agent for orchestrating multi-agent workflows.

The coordinator delegates tasks to specialized worker agents
and aggregates their results into a final response.
"""

from typing import Optional, Dict, Any
import logging
import time
import uuid
from .worker_base import WorkerAgent
from .message_protocol import Message, MessageType
from .shared_state import SharedState


class CoordinatorError(Exception):
    """Base exception for coordinator errors."""


class AgentDelegationError(CoordinatorError):
    """Raised when agent delegation fails."""


class WorkflowError(CoordinatorError):
    """Raised when workflow execution fails."""


class Coordinator:
    """
    Coordinator agent that orchestrates worker agents.

    Implements the coordinator-worker pattern where:
    - Coordinator receives user requests
    - Coordinator decomposes into subtasks
    - Coordinator delegates to specialized workers
    - Coordinator aggregates results
    - Coordinator returns final response

    Example:
        coordinator = Coordinator()
        report = coordinator.generate_report("Analyze EV market")
        print(report)
    """

    def __init__(self, shared_state: Optional[SharedState] = None):
        """
        Initialize coordinator with worker agents.

        Args:
            shared_state: Shared state manager (creates new if not provided)
        """
        # TODO: Students complete this in Exercise 1
        pass

    def delegate(self, agent: WorkerAgent, action: str, payload: Dict[str, Any]) -> Dict:
        """
        Delegate a task to a worker agent.

        Args:
            agent: Worker agent to delegate to
            action: Action for agent to perform
            payload: Data for the action

        Returns:
            Response payload from worker

        TODO: Students implement delegation with:
        - Message creation
        - Error handling
        - Retry logic
        - Logging
        """
        pass

    def generate_report(self, query: str) -> str:
        """
        Generate a report by orchestrating research, data, and writer agents.

        Implements sequential workflow:
        1. Research agent gathers information
        2. Data agent analyzes findings
        3. Writer agent creates formatted report

        Args:
            query: User's research query

        Returns:
            Formatted report string

        TODO: Students implement sequential workflow in Exercise 1
        """
        pass
