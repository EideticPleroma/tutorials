"""
Specialized agent implementations for Tutorial 2.

These are scaffold implementations that students will complete in Lab 2:
- ResearchAgent: Gathers information from various sources
- DataAgent: Analyzes and processes data
- WriterAgent: Generates formatted reports and summaries
"""

from .research_agent import ResearchAgent
from .data_agent import DataAgent
from .writer_agent import WriterAgent

__all__ = [
    'ResearchAgent',
    'DataAgent',
    'WriterAgent',
]

