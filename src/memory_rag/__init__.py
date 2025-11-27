"""
Memory & RAG module for Tutorial 3.

This module provides RAG (Retrieval-Augmented Generation) capabilities
and multi-model orchestration for the Architect-Builder pattern.

Components:
- config: LlamaIndex and multi-model configuration
- document_loaders: Load code and documentation files
- rag_engine: Main RAG interface for indexing and querying
- knowledge_tool: Agent tool for searching the codebase
- model_router: Route tasks to appropriate LLMs
- architect_agent: Planning agent using Llama 3.1
- builder_agent: Implementation agent using DeepSeek-Coder
- architect_builder: Coordinator for the full workflow
- ove_harness: O.V.E. testing harness for generated code
"""

from .config import configure, configure_for_project

__all__ = [
    "configure",
    "configure_for_project",
]

