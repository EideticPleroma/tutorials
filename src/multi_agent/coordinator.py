"""
Coordinator agent for orchestrating multi-agent workflows.

The coordinator delegates tasks to specialized worker agents
and aggregates their results into a final response.
"""

from typing import Optional, Dict, Any
import logging
import uuid
from .worker_base import WorkerAgent
from .message_protocol import Message, MessageType
from .shared_state import SharedState


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
        # TODO: Students complete this in Exercise 1
        # Should:
        # - Initialize or create shared_state
        # - Initialize worker agents (research, data, writer)
        # - Setup logging
        
        self.shared_state = shared_state or SharedState()
        self.logger = logging.getLogger("coordinator")
        
        # Worker agents - students will implement these in Exercise 2
        # For now, these are None (students will assign actual agents)
        self.research = None
        self.data = None
        self.writer = None
    
    def delegate(
        self, 
        agent: WorkerAgent, 
        action: str, 
        payload: Dict[str, Any],
        trace_id: Optional[str] = None,
        max_retries: int = 3
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
        # TODO: Students complete this in Exercise 1
        # Should:
        # 1. Create request Message
        # 2. Log message sent
        # 3. Call agent.execute_message()
        # 4. Handle response or error
        # 5. Implement retry logic
        # 6. Return result
        
        raise NotImplementedError(
            "Students implement delegate() in Exercise 1"
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
        # TODO: Students complete this in Exercise 1
        # Should:
        # 1. Generate or use provided trace_id
        # 2. Delegate to research agent
        # 3. Check success, handle error
        # 4. Delegate to data agent
        # 5. Check success, handle error
        # 6. Delegate to writer agent
        # 7. Return final report
        
        raise NotImplementedError(
            "Students implement generate_report() in Exercise 1"
        )

