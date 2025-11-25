"""
Tool registry for managing agent-callable functions.

This module provides a central registry for tools (functions) that agents
can call. Tools are registered using a decorator pattern, and the registry
automatically generates JSON schemas for the LLM to understand how to call them.

The registry is core to Tutorial 1's architecture, enabling agents to:
- Discover available tools at runtime
- Generate schemas from Python type hints and docstrings
- Route tool calls from LLM responses to actual function implementations
"""

from typing import Callable, Dict, Any, List
import inspect
import functools

class ToolRegistry:
    """
    Central registry for agent tools with automatic schema generation.

    The ToolRegistry maintains a collection of callable functions (tools) that
    agents can use, along with their JSON schemas for LLM tool calling. Tools
    are registered using the @registry.register decorator.

    Attributes:
        _tools: Dictionary mapping tool names to their callable functions
        _schemas: List of JSON schemas describing each tool's interface

    Example:
        registry = ToolRegistry()

        @registry.register
        def my_tool(param: str) -> str:
            '''Tool description.'''
            return f"Result: {param}"

        # Agent can now discover and call my_tool
        schemas = registry.get_schemas()
        tool = registry.get_tool("my_tool")
    """

    def __init__(self):
        """
        Initialize an empty tool registry.

        Creates empty dictionaries for storing tools and their schemas.
        Tools are added later via the @register decorator.
        """
        self._tools: Dict[str, Callable] = {}
        self._schemas: List[Dict[str, Any]] = []

    def register(self, func: Callable):
        """
        Decorator to register a function as an agent tool.

        This decorator adds a function to the registry and generates its
        JSON schema for LLM tool calling. The schema is created from the
        function's type hints and docstring.

        Args:
            func: The function to register as a tool. Must have type hints
                 and a docstring for proper schema generation

        Returns:
            A wrapper function that preserves the original function's
            behavior while enabling it to be called by agents

        Example:
            @registry.register
            def calculate(a: float, b: float) -> float:
                '''Add two numbers.'''
                return a + b
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        schema = self._generate_schema(func)
        self._tools[schema["function"]["name"]] = func
        self._schemas.append(schema)
        return wrapper

    def get_tool(self, name: str) -> Callable:
        """
        Retrieve a registered tool by name.

        Args:
            name: The name of the tool to retrieve (matches function name)

        Returns:
            The callable function if found, None otherwise

        Example:
            calc_func = registry.get_tool("calculate")
            result = calc_func(5, 3)  # Calls the tool directly
        """
        return self._tools.get(name)

    def get_schemas(self) -> List[Dict[str, Any]]:
        """
        Get JSON schemas for all registered tools.

        Returns a list of tool schemas in the format expected by LLMs
        for function/tool calling. Each schema includes the function name,
        description, and parameter specifications.

        Returns:
            List of JSON schema dictionaries, one per registered tool

        Example:
            schemas = registry.get_schemas()
            # Pass to LLM: ollama.chat(model=..., tools=schemas)
        """
        return self._schemas

    def _generate_schema(self, func: Callable) -> Dict[str, Any]:
        """
        Generate a JSON schema for a function using its type hints and docstring.

        Inspects the function's signature to extract parameter names, types,
        and required/optional status. Uses the docstring as the tool description
        that the LLM will read to understand the tool's purpose.

        Args:
            func: The function to generate a schema for

        Returns:
            A JSON schema dictionary in the format expected by LLMs for
            tool/function calling, containing:
            - function.name: The function name
            - function.description: From the docstring
            - function.parameters: Type and requirement info for each parameter

        Note:
            Currently maps Python types to JSON schema types (int->integer,
            float->number, bool->boolean, default->string). In production,
            consider parsing docstrings for parameter descriptions.
        """
        sig = inspect.signature(func)
        doc = inspect.getdoc(func) or "No description provided."
        
        parameters = {
            "type": "object",
            "properties": {},
            "required": []
        }

        for name, param in sig.parameters.items():
            param_type = "string" # Default
            if param.annotation == int:
                param_type = "integer"
            elif param.annotation == float:
                param_type = "number"
            elif param.annotation == bool:
                param_type = "boolean"
            
            parameters["properties"][name] = {
                "type": param_type,
                "description": f"Parameter {name}" # In a real app, parse docstring for this
            }
            if param.default == inspect.Parameter.empty:
                parameters["required"].append(name)

        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": doc,
                "parameters": parameters
            }
        }

registry = ToolRegistry()

