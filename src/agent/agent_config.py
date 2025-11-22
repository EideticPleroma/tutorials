import os
from pydantic import BaseModel, ConfigDict

class AgentConfig(BaseModel):
    model_name: str = "llama3.1:8b"
    ollama_base_url: str = "http://localhost:11434/api"
    temperature: float = 0.1
    system_prompt: str = """You are a helpful AI assistant capable of using tools.

    When you need information, use the available tools.
    IMPORTANT: After a tool returns results, include the specific details 
    from the tool's output in your response. Don't just summarize - provide 
    the actual data the tool returned.

    Always answer concisely and accurately."""

    model_config = ConfigDict(env_prefix="AGENT_")

# Default instance
config = AgentConfig()

