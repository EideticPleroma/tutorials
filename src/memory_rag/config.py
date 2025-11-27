"""
LlamaIndex and multi-model configuration for Tutorial 3.

This module configures:
- LLM settings for Ollama (Llama 3.1 and DeepSeek-Coder)
- Embedding model settings for local embeddings
- Chunking parameters for code and documentation
"""

import logging
from typing import Optional

# TODO: Import LlamaIndex components
# from llama_index.core import Settings
# from llama_index.llms.ollama import Ollama
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding

logger = logging.getLogger(__name__)

# Model configuration
ARCHITECT_MODEL = "llama3.1:8b"
BUILDER_MODEL = "deepseek-coder:6.7b"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# Chunking configuration
CODE_CHUNK_SIZE = 1024
CODE_CHUNK_OVERLAP = 100
DOC_CHUNK_SIZE = 512
DOC_CHUNK_OVERLAP = 50


def configure() -> None:
    """
    Configure LlamaIndex with default settings.
    
    Sets up:
    - Ollama LLM with Llama 3.1
    - HuggingFace embeddings with bge-small
    - Default chunking parameters
    
    Call this before using any LlamaIndex functionality.
    
    Example:
        >>> from src.memory_rag.config import configure
        >>> configure()
        >>> # Now use LlamaIndex
    """
    # TODO: Implement configuration
    # Settings.llm = Ollama(model=ARCHITECT_MODEL, request_timeout=120.0)
    # Settings.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
    # Settings.chunk_size = DOC_CHUNK_SIZE
    # Settings.chunk_overlap = DOC_CHUNK_OVERLAP
    
    logger.info("LlamaIndex configured with model %s", ARCHITECT_MODEL)
    pass


def configure_for_project() -> None:
    """
    Configure LlamaIndex optimized for indexing the tutorial project.
    
    Uses larger chunk sizes for code to keep functions together.
    
    Example:
        >>> from src.memory_rag.config import configure_for_project
        >>> configure_for_project()
    """
    # TODO: Implement project-specific configuration
    # Settings.llm = Ollama(model=ARCHITECT_MODEL, request_timeout=120.0, temperature=0.1)
    # Settings.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
    # Settings.chunk_size = CODE_CHUNK_SIZE
    # Settings.chunk_overlap = CODE_CHUNK_OVERLAP
    
    logger.info("LlamaIndex configured for project indexing")
    pass


def get_architect_llm():
    """
    Get LLM configured for planning and reasoning tasks.
    
    Returns:
        Ollama instance configured with Llama 3.1, low temperature for consistency.
    
    Example:
        >>> llm = get_architect_llm()
        >>> response = llm.complete("Create a plan for...")
    """
    # TODO: Return configured Ollama instance
    # return Ollama(
    #     model=ARCHITECT_MODEL,
    #     request_timeout=120.0,
    #     temperature=0.1,
    # )
    pass


def get_builder_llm():
    """
    Get LLM configured for code generation tasks.
    
    Returns:
        Ollama instance configured with DeepSeek-Coder, slightly higher
        temperature for more creative code generation.
    
    Example:
        >>> llm = get_builder_llm()
        >>> response = llm.complete("def sort_list(items):")
    """
    # TODO: Return configured Ollama instance for DeepSeek
    # return Ollama(
    #     model=BUILDER_MODEL,
    #     request_timeout=120.0,
    #     temperature=0.2,
    # )
    pass

