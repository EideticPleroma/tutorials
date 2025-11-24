import os
from pydantic import BaseModel, ConfigDict


class AgentConfig(BaseModel):
    model_name: str = "llama3.1:8b"
    ollama_base_url: str = "http://localhost:11434/api"
    temperature: float = 0.1
    system_prompt: str = """You are a helpful AI assistant with access to tools.
    When answering questions, use the available tools when needed.
    For simple conversation and greetings, respond naturally without using tools.
    Provide clear and accurate responses that incorporate the information from all tools you've used."""

    model_config = ConfigDict(env_prefix="AGENT_")


# Default instance
config = AgentConfig()
