import ollama
import json
from typing import List, Dict, Any
from .agent_config import config
from .tool_registry import registry

# Import tools to register them (side-effect imports for decorator registration)
from . import mcp_tool_bridge  # noqa: F401

# Students: Add your tool imports here following Exercise 2
# Example: from .tools import your_tool  # noqa: F401
from .tools import file_search  # noqa: F401
from .tools import read_file  # noqa: F401

# --- Define Basic Tools ---


@registry.register
def calculate(operation: str, a: float, b: float) -> float:
    """
    Perform a basic calculation.
    operation: one of 'add', 'subtract', 'multiply', 'divide'
    a: first number
    b: second number
    """
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return "Error: Division by zero"
        return a / b
    else:
        return f"Error: Unknown operation {operation}"


@registry.register
def get_weather(city: str) -> str:
    """
    Get the current weather for a given city.
    city: name of the city
    """
    # Mock response for tutorial
    return f"The weather in {city} is Sunny, 25°C"


# --- Agent Logic ---


class Agent:
    """
    A simple AI agent with tool-calling capabilities.

    The agent uses an LLM (via Ollama) to process user queries and can
    call registered tools to perform actions like file operations,
    calculations, and weather lookups.

    Example:
        agent = Agent()
        response = agent.chat("What's the weather in Paris?")
    """

    def __init__(self):
        self.messages: List[Dict[str, Any]] = [
            {"role": "system", "content": config.system_prompt}
        ]

    def chat(self, user_input: str) -> str:
        """
        Process a user message and return the agent's response.

        The agent may call tools if needed to answer the query. The method
        handles the tool-calling loop: if the LLM requests tools, they are
        executed and the results are fed back to the LLM for a final response.

        Args:
            user_input: The user's message or query.

        Returns:
            The agent's response as a string, incorporating tool results if any
            tools were called.
        """
        self.messages.append({"role": "user", "content": user_input})

        # Loop until no more tool calls are needed
        max_iterations = 10  # Safety limit to prevent infinite loops
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # Call LLM (always pass tools so it can request them if needed)
            response = ollama.chat(
                model=config.model_name,
                messages=self.messages,
                tools=registry.get_schemas(),
                options={"temperature": config.temperature},
            )

            self.messages.append(response["message"])

            # Check if tool calls are present
            if response["message"].get("tool_calls"):
                for tool_call in response["message"]["tool_calls"]:
                    function_name = tool_call["function"]["name"]
                    arguments = tool_call["function"]["arguments"]

                    print(
                        f"  --> Agent deciding to call tool: {function_name} with {arguments}"
                    )

                    tool_func = registry.get_tool(function_name)
                    if tool_func:
                        try:
                            # Call the tool
                            result = tool_func(**arguments)

                            # Add tool result to messages
                            self.messages.append(
                                {
                                    "role": "tool",
                                    "content": str(result),
                                }
                            )
                            print(f"  <-- Tool output: {result}")
                        except Exception as e:
                            self.messages.append(
                                {
                                    "role": "tool",
                                    "content": f"Error executing tool: {str(e)}",
                                }
                            )
                    else:
                        print(f"Error: Tool {function_name} not found")

                # Continue loop to let LLM process tool results and potentially call more tools
                continue
            else:
                # No more tool calls, return the final response
                return response["message"]["content"]

        # Safety: if we hit max iterations, return the last response
        return response["message"]["content"]


if __name__ == "__main__":
    print("Initializing Agent...")
    agent = Agent()
    print("Agent Ready. Type 'exit' to quit.")

    while True:
        user_in = input("\nYou: ")
        if user_in.lower() in ["exit", "quit"]:
            break

        response = agent.chat(user_in)
        print(f"Agent: {response}")
