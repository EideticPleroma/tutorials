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

        # Sequential workflow
        report = coordinator.generate_report("Analyze EV market")
        print(report)

        # With trace ID for debugging
        report = coordinator.generate_report(
            "Analyze EV market",
            trace_id="user-123-query-456"
        )
    """

    def __init__(self, shared_state: Optional[SharedState] = None):
        """
        Initialize coordinator with worker agents.

        Args:
            shared_state: Shared state manager (creates new if not provided)
        """
        # Initialize or create shared state for cross-agent data persistence
        self.shared_state = shared_state or SharedState()

        # Setup structured logging for coordination events
        # JSON format enables trace analysis and debugging
        self.logger = logging.getLogger("coordinator")
        self.logger.setLevel(logging.INFO)

        # Ensure we have a handler for logging
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
                '"logger": "%(name)s", "message": "%(message)s"}'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        # Worker agents - placeholder for now
        # These will be assigned actual specialized agents in Exercise 2
        self.research = None  # Research agent for information gathering
        self.data = None  # Data agent for analysis and metrics
        self.writer = None  # Writer agent for report generation

        self.logger.info("Coordinator initialized with shared state")

    def delegate(  # pylint: disable=too-many-arguments
        self,
        agent: WorkerAgent,
        action: str,
        payload: Dict[str, Any],
        *,
        trace_id: Optional[str] = None,
        max_retries: int = 3,
    ) -> Dict:
        """
        Delegate a task to a worker agent.

        Implements:
        - Message creation
        - Error handling
        - Retry logic with exponential backoff
        - Comprehensive logging

        Args:
            agent: Worker agent to delegate to
            action: Action for agent to perform
            payload: Data for the action
            trace_id: Workflow trace ID
            max_retries: Maximum retry attempts

        Returns:
            Response payload from worker

        Raises:
            Exception: If all retries exhausted
        """
        # Generate trace_id if not provided for workflow tracking
        if trace_id is None:
            trace_id = str(uuid.uuid4())

        # Retry loop with exponential backoff
        last_error = None
        for attempt in range(max_retries):
            try:
                # Create request message for the worker agent
                request = Message(
                    from_agent="coordinator",
                    to_agent=agent.name,
                    message_type=MessageType.REQUEST,
                    action=action,
                    payload=payload,
                    trace_id=trace_id,
                )

                # Log delegation
                self.logger.info(
                    "Delegating action '%s' to agent '%s' (attempt %d/%d, trace_id: %s)",
                    action,
                    agent.name,
                    attempt + 1,
                    max_retries,
                    trace_id,
                )

                # Send message to worker agent
                response = agent.execute_message(request)

                # Handle response based on message type
                if response.message_type == MessageType.ERROR:
                    error_msg = response.payload.get("error", "Unknown error")
                    self.logger.error(
                        "Agent '%s' returned error: %s (trace_id: %s)",
                        agent.name,
                        error_msg,
                        trace_id,
                    )
                    raise AgentDelegationError(f"Agent {agent.name} error: {error_msg}")

                if response.message_type == MessageType.RESPONSE:
                    # Success - log and return payload
                    self.logger.info(
                        "Agent '%s' completed action '%s' successfully (trace_id: %s)",
                        agent.name,
                        action,
                        trace_id,
                    )
                    return response.payload

                # Unexpected message type
                raise AgentDelegationError(
                    f"Unexpected message type from agent {agent.name}: "
                    f"{response.message_type}"
                )

            except CoordinatorError as e:
                last_error = e

                # If we haven't exhausted retries, wait and retry
                if attempt < max_retries - 1:
                    backoff_time = 2**attempt  # Exponential backoff: 1s, 2s, 4s
                    self.logger.warning(
                        "Retry %d/%d for agent '%s' after error: %s. Waiting %ds... (trace_id: %s)",
                        attempt + 1,
                        max_retries - 1,
                        agent.name,
                        str(e),
                        backoff_time,
                        trace_id,
                    )
                    time.sleep(backoff_time)
                else:
                    # Final attempt failed
                    self.logger.error(
                        "All %d attempts exhausted for agent '%s'. Final error: %s (trace_id: %s)",
                        max_retries,
                        agent.name,
                        str(e),
                        trace_id,
                    )

        # If we get here, all retries failed
        raise AgentDelegationError(
            f"Failed to delegate to agent {agent.name} after {max_retries} attempts. "
            f"Last error: {str(last_error)}"
        )

    def generate_report(self, query: str, trace_id: Optional[str] = None) -> str:
        """
        Generate a report by orchestrating research, data, and writer agents.

        Implements sequential workflow:
        1. Research agent gathers information
        2. Data agent analyzes findings
        3. Writer agent creates formatted report

        Args:
            query: User's research query
            trace_id: Workflow trace ID (generated if not provided)

        Returns:
            Formatted report string

        Raises:
            Exception: If any agent fails after retries
        """
        # Generate trace_id for tracking this workflow
        if trace_id is None:
            trace_id = str(uuid.uuid4())

        self.logger.info("Starting report generation workflow (trace_id: %s)", trace_id)

        # Step 1: Research Agent - Gather information
        self.logger.info("Step 1/3: Research phase (trace_id: %s)", trace_id)
        research_response = self.delegate(
            self.research, "gather_info", {"query": query}, trace_id=trace_id
        )

        # Validate research success
        if research_response.get("status") != "success":
            error_msg = research_response.get("error", "Research failed")
            self.logger.error(
                "Research phase failed: %s (trace_id: %s)", error_msg, trace_id
            )
            raise WorkflowError(f"Research phase failed: {error_msg}")

        research_findings = research_response.get("findings", [])
        self.logger.info(
            "Research completed: %d findings (trace_id: %s)",
            len(research_findings),
            trace_id,
        )

        # Step 2: Data Agent - Analyze findings
        self.logger.info("Step 2/3: Data analysis phase (trace_id: %s)", trace_id)
        data_response = self.delegate(
            self.data,
            "analyze_trends",
            {"findings": research_findings, "query": query},
            trace_id=trace_id,
        )

        # Validate data analysis success
        if data_response.get("status") != "success":
            error_msg = data_response.get("error", "Data analysis failed")
            self.logger.error(
                "Data analysis phase failed: %s (trace_id: %s)", error_msg, trace_id
            )
            raise WorkflowError(f"Data analysis phase failed: {error_msg}")

        data_analysis = data_response.get("analysis", {})
        self.logger.info("Data analysis completed (trace_id: %s)", trace_id)

        # Step 3: Writer Agent - Create formatted report
        self.logger.info("Step 3/3: Report writing phase (trace_id: %s)", trace_id)
        writer_response = self.delegate(
            self.writer,
            "create_report",
            {"query": query, "findings": research_findings, "analysis": data_analysis},
            trace_id=trace_id,
        )

        # Validate writer success
        if writer_response.get("status") != "success":
            error_msg = writer_response.get("error", "Report writing failed")
            self.logger.error(
                "Report writing phase failed: %s (trace_id: %s)", error_msg, trace_id
            )
            raise WorkflowError(f"Report writing phase failed: {error_msg}")

        report = writer_response.get("report", "")
        self.logger.info(
            "Report generation workflow completed successfully (trace_id: %s)", trace_id
        )

        return report
