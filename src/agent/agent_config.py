import os
from pydantic import BaseModel, ConfigDict


class AgentConfig(BaseModel):
    model_name: str = "llama3.3:8b"
    ollama_base_url: str = "http://localhost:11434/api"
    temperature: float = 0.1
    system_prompt: str = """You are a helpful AI assistant with access to tools.
    When answering questions, use the available tools when needed.

    You can chain multiple tools together to complete complex tasks. For example:
    - If asked to find and read a file, first use search_files to locate it, then use read_file to read its contents
    - If you need information from multiple sources, use the appropriate tools in sequence
    - After each tool call, evaluate if you need additional tools to fully answer the question

    After using tools, always include the tool's results in your response to the user.
    Provide clear and accurate responses that incorporate the information from all tools you've used."""

    model_config = ConfigDict(env_prefix="AGENT_")


# Default instance
config = AgentConfig()
