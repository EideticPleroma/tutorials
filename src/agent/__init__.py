"""
Agent implementation for Lesson 1 - Fundamentals.

This module implements a local tool-calling agent using:
- Ollama (local LLM inference)
- Tool Registry pattern for extensibility
- MCP (Model Context Protocol) bridge for TypeScript tools

Main exports:
- Agent: The main agent class with chat() method
- registry: Tool registry singleton for registering new tools
"""

from .simple_agent import Agent
from .tool_registry import registry

__all__ = ['Agent', 'registry']

