"""
Base class for worker agents in multi-agent systems.

Worker agents are specialized agents that perform specific tasks
when delegated to by a coordinator agent.

WorkerAgent extends Tutorial 1's Agent class, inheriting:
- Ollama LLM integration via chat() method
- Tool calling capabilities via tool registry
- Message history management

Tutorial 2 adds:
- Agent specialization through filtered tool access
- Shared state management across agents
- Message protocol for coordination
"""

from typing import Dict, Any, Optional, List
import logging
from ..agent.simple_agent import Agent
from ..agent.tool_registry import registry
from .shared_state import SharedState
from .message_protocol import Message, MessageType


class WorkerAgent(Agent):
    """
    Base class for specialized worker agents.
    
    Inherits from Tutorial 1's Agent class, gaining:
    - LLM integration via self.chat() method
    - Tool calling through tool registry
    - Message history in self.messages
    
    Tutorial 2 adds:
    - Agent specialization (focused system prompts)
    - Tool filtering (only allowed_tools are accessible)
    - Shared state for inter-agent data sharing
    - Message protocol for coordinator communication
    
    Subclass this to create specialized agents:
    
    Example:
        class ResearchAgent(WorkerAgent):
            def __init__(self, shared_state):
                super().__init__(
                    name="research",
                    shared_state=shared_state,
                    allowed_tools=["file_search", "read_file"]
                )
                # Override system prompt for specialization
                self.messages[0] = {
                    "role": "system",
                    "content": "You are a research specialist..."
                }
            
            def gather_info(self, query: str) -> Dict:
                # Use inherited self.chat() to call LLM with tools
                response = self.chat(f"Research: {query}")
                # Process and structure findings
                return {"status": "success", "findings": response}
    """
    
    def __init__(self, name: str, shared_state: SharedState, allowed_tools: List[str]):
        """
        Initialize worker agent with specialization.
        
        Args:
            name: Agent name (e.g., "research", "data", "writer")
            shared_state: Shared state manager for inter-agent data
            allowed_tools: List of tool names this agent can use
                          (filters Tutorial 1's tool registry)
        
        Example:
            research = ResearchAgent(
                shared_state=state,
                allowed_tools=["file_search", "read_file"]
            )
        """
        # Initialize parent Agent class (gets Ollama + tool calling)
        super().__init__()
        
        self.name = name
        self.shared_state = shared_state
        self.allowed_tools = allowed_tools
        self.logger = logging.getLogger(f"agent.{name}")
        
        # Filter tool registry to only allowed tools
        # This enforces specialization - research agent only gets research tools
        all_tools = registry.get_schemas()
        self.available_tools = [
            schema for schema in all_tools
            if schema['function']['name'] in allowed_tools
        ]
        
        self.logger.info(
            "Initialized %s agent with %d allowed tools: %s",
            name,
            len(self.available_tools),
            allowed_tools
        )
        
        # Subclasses should override self.messages[0] to set specialized system prompt
    
    def chat(self, user_input: str) -> str:
        """
        Override parent chat() to use filtered tools instead of all tools.
        
        This ensures specialized agents only use their allowed_tools.
        
        Args:
            user_input: The user's message or query
        
        Returns:
            The agent's response as a string
        """
        import ollama
        from ..agent.agent_config import config
        
        self.messages.append({"role": "user", "content": user_input})
        
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Call LLM with FILTERED tools (only allowed_tools)
            response = ollama.chat(
                model=config.model_name,
                messages=self.messages,
                tools=self.available_tools,  # Filtered, not all tools
                options={"temperature": config.temperature},
            )
            
            self.messages.append(response["message"])
            
            if response["message"].get("tool_calls"):
                for tool_call in response["message"]["tool_calls"]:
                    function_name = tool_call["function"]["name"]
                    arguments = tool_call["function"]["arguments"]
                    
                    self.logger.info(
                        "Agent %s calling tool: %s with %s",
                        self.name,
                        function_name,
                        arguments
                    )
                    
                    tool_func = registry.get_tool(function_name)
                    if tool_func:
                        try:
                            result = tool_func(**arguments)
                            self.messages.append({
                                "role": "tool",
                                "content": str(result),
                            })
                            self.logger.info("Tool %s returned: %s", function_name, str(result)[:100])
                        except Exception as e:
                            error_msg = f"Error executing tool: {str(e)}"
                            self.messages.append({
                                "role": "tool",
                                "content": error_msg,
                            })
                            self.logger.error("Tool %s error: %s", function_name, str(e))
                    else:
                        self.logger.error("Tool %s not found in registry", function_name)
                
                continue
            else:
                return response["message"]["content"]
        
        return response["message"]["content"]
    
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

