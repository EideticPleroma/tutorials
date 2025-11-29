"""
Multi-Agent Bridge Module - Exercise 0 (Tutorial 2)

This module extends Tutorial 1's single agent into a simple two-agent system,
bridging the gap before introducing full coordinator-worker patterns.

The agents here inherit directly from the Agent class you built in Tutorial 1.
No message protocols yet - just simple function calls between agents.

Classes:
    GathererAgent: Collects information using search/read tools
    ReporterAgent: Summarizes gathered information (LLM only)

Functions:
    run_two_agent_workflow: Chains gatherer -> reporter for a query
"""

from .gatherer import GathererAgent
from .reporter import ReporterAgent
from .runner import run_two_agent_workflow

__all__ = [
    "GathererAgent",
    "ReporterAgent",
    "run_two_agent_workflow",
]

