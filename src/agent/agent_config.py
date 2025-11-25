"""
Agent configuration management using Pydantic.

This module provides centralized configuration for agent behavior including
model selection, API endpoints, temperature settings, and system prompts.
Configuration can be overridden via environment variables with AGENT_ prefix.

Example:
    # Use defaults
    from agent.agent_config import config
    agent = Agent()  # Uses config.model_name, config.temperature, etc.

    # Override via environment
    export AGENT_MODEL_NAME=llama3.1:70b
    export AGENT_TEMPERATURE=0.7
"""

import os
from pydantic import BaseModel, ConfigDict


class AgentConfig(BaseModel):
    """
    Configuration settings for agent behavior and LLM integration.

    Uses Pydantic for validation and environment variable support.
    All fields can be overridden via environment variables with the
    AGENT_ prefix (e.g., AGENT_MODEL_NAME).

    Attributes:
        model_name: Name of the Ollama model to use for the agent
        ollama_base_url: Base URL for the Ollama API endpoint
        temperature: Sampling temperature for LLM responses (0.0-1.0).
                    Lower values are more deterministic
        system_prompt: Initial system message that defines the agent's role
                      and behavior

    Example:
        config = AgentConfig(
            model_name="llama3.1:70b",
            temperature=0.2
        )

        # Or use environment variables
        # AGENT_MODEL_NAME=llama3.1:70b
        # AGENT_TEMPERATURE=0.2
    """

    model_name: str = "llama3.1:8b"
    ollama_base_url: str = "http://localhost:11434/api"
    temperature: float = 0.1
    system_prompt: str = """You are a helpful AI assistant with access to tools.
    When answering questions, use the available tools when needed.
    For simple conversation and greetings, respond naturally without using tools.
    When tools provide information, preserve the specific terms they use in your response."""

    model_config = ConfigDict(env_prefix="AGENT_")


# Default instance
config = AgentConfig()
