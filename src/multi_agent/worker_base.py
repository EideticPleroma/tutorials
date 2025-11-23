"""
Base class for worker agents in multi-agent systems.

Worker agents are specialized agents that perform specific tasks
when delegated to by a coordinator agent.
"""

from typing import Dict, Any, Optional
import logging
from .shared_state import SharedState
from .message_protocol import Message, MessageType


class WorkerAgent:
    """
    Base class for specialized worker agents.
    
    Worker agents:
    - Have a specialized role (research, data analysis, writing, etc.)
    - Execute specific actions when delegated to
    - Read/write to shared state
    - Communicate via message protocol
    
    Subclass this to create specialized agents:
    
    Example:
        class ResearchAgent(WorkerAgent):
            def __init__(self, shared_state):
                super().__init__(name="research", shared_state=shared_state)
                self.system_prompt = "You are a research specialist..."
                self.tools = ["web_search", "read_file"]
            
            def gather_info(self, query: str) -> Dict:
                # Implement research logic
                pass
    """
    
    def __init__(self, name: str, shared_state: SharedState):
        """
        Initialize worker agent.
        
        Args:
            name: Agent name (e.g., "research", "data", "writer")
            shared_state: Shared state manager
        """
        self.name = name
        self.shared_state = shared_state
        self.logger = logging.getLogger(f"agent.{name}")
        
        # Subclasses should set these
        self.system_prompt: Optional[str] = None
        self.tools: Dict[str, Any] = {}
    
    def execute(self, action: str, payload: Dict) -> Dict:
        """
        Execute an action with given payload.
        
        This is the main entry point for agent execution.
        Subclasses should implement specific action methods.
        
        Args:
            action: Action name (e.g., "gather_info", "analyze", "write")
            payload: Action parameters
        
        Returns:
            Result dictionary with status and data
        
        Example:
            result = agent.execute("gather_info", {"query": "EV market"})
            # Returns: {"status": "success", "findings": [...]}
        """
        # TODO: Students implement this
        # Should:
        # 1. Log action start
        # 2. Route to appropriate method based on action
        # 3. Handle errors and return status
        # 4. Log completion
        
        raise NotImplementedError(
            f"Agent {self.name} must implement execute() method"
        )
    
    def execute_message(self, request: Message) -> Message:
        """
        Execute action from message and return response message.
        
        This wraps execute() with message protocol handling.
        
        Args:
            request: Request message
        
        Returns:
            Response message with results or error
        """
        try:
            # Extract action and payload from request
            action = request.action
            payload = request.payload
            
            # Execute action
            result = self.execute(action, payload)
            
            # Create response message
            response = Message(
                from_agent=self.name,
                to_agent=request.from_agent,
                message_type=MessageType.RESPONSE,
                payload=result,
                in_reply_to=request.message_id,
                trace_id=request.trace_id
            )
            
            return response
            
        except Exception as e:
            # Return error message
            error_response = Message(
                from_agent=self.name,
                to_agent=request.from_agent,
                message_type=MessageType.ERROR,
                payload={"error": str(e)},
                in_reply_to=request.message_id,
                trace_id=request.trace_id
            )
            
            return error_response

