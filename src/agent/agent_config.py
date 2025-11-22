import os
from pydantic import BaseModel, ConfigDict

class AgentConfig(BaseModel):
    model_name: str = "llama3.1:8b"
    ollama_base_url: str = "http://localhost:11434/api"
    temperature: float = 0.1
    # Updated prompt to help with the "Sunny" test failure as well
    system_prompt: str = """You are a helpful AI assistant capable of using tools.
When a user asks a question that requires a tool, you must use the available tools.
IMPORTANT: After using a tool, you must use the return value of the tool to answer the user's question directly.
Always answer concisely and accurately."""

    model_config = ConfigDict(env_prefix="AGENT_")

# Default instance
config = AgentConfig()

