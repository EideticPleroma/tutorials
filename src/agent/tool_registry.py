from typing import Callable, Dict, Any, List
import inspect
import functools

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._schemas: List[Dict[str, Any]] = []

    def register(self, func: Callable):
        """Decorator to register a function as a tool."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        schema = self._generate_schema(func)
        self._tools[schema["function"]["name"]] = func
        self._schemas.append(schema)
        return wrapper

    def get_tool(self, name: str) -> Callable:
        return self._tools.get(name)

    def get_schemas(self) -> List[Dict[str, Any]]:
        return self._schemas

    def _generate_schema(self, func: Callable) -> Dict[str, Any]:
        """Generates a simple JSON schema for the function from type hints."""
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

