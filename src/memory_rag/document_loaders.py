"""
Document loaders for code and documentation files.

This module provides functions to load project files with appropriate
metadata for indexing in the RAG system.
"""

import logging
from pathlib import Path
from typing import Optional

# TODO: Import LlamaIndex components
# from llama_index.core import SimpleDirectoryReader, Document

logger = logging.getLogger(__name__)

# Directories to exclude
EXCLUDE_DIRS = {
    "__pycache__",
    ".git",
    ".env",
    ".agent_state",
    ".agent_logs",
    ".cursor",
    "node_modules",
    ".venv",
    "venv",
    "storage",
}

# File extensions
CODE_EXTENSIONS = [".py"]
DOC_EXTENSIONS = [".md"]


def load_code_files(base_path: str) -> list:
    """
    Load Python files from src/ and tests/ directories.
    
    Args:
        base_path: Root path of the project.
        
    Returns:
        List of Document objects with metadata:
        - file_path: Full path to the file
        - file_type: "python"
        - category: "code" or "test"
    
    Example:
        >>> docs = load_code_files(".")
        >>> print(f"Loaded {len(docs)} code files")
    """
    # TODO: Implement code file loading
    # 1. Use SimpleDirectoryReader for src/
    # 2. Use SimpleDirectoryReader for tests/
    # 3. Add metadata to each document
    # 4. Combine and return
    
    logger.info("Loading code files from %s", base_path)
    return []


def load_documentation(base_path: str) -> list:
    """
    Load Markdown files from lesson-*/ directories.
    
    Args:
        base_path: Root path of the project.
        
    Returns:
        List of Document objects with metadata:
        - file_path: Full path to the file
        - file_type: "markdown"
        - category: "docs"
        - tutorial: Tutorial number (1, 2, or 3)
    
    Example:
        >>> docs = load_documentation(".")
        >>> print(f"Loaded {len(docs)} documentation files")
    """
    # TODO: Implement documentation loading
    # 1. Find lesson-*/ directories
    # 2. Load .md files from each
    # 3. Add metadata including tutorial number
    # 4. Combine and return
    
    logger.info("Loading documentation from %s", base_path)
    return []


def load_all_project_files(base_path: str) -> list:
    """
    Load all code and documentation files from the project.
    
    Args:
        base_path: Root path of the project.
        
    Returns:
        Combined list of all Document objects.
    
    Example:
        >>> docs = load_all_project_files(".")
        >>> code = [d for d in docs if d.metadata.get("file_type") == "python"]
        >>> docs = [d for d in docs if d.metadata.get("file_type") == "markdown"]
        >>> print(f"Code: {len(code)}, Docs: {len(docs)}")
    """
    # TODO: Implement combined loading
    # 1. Load code files
    # 2. Load documentation
    # 3. Print summary
    # 4. Return combined list
    
    logger.info("Loading all project files from %s", base_path)
    
    code_docs = load_code_files(base_path)
    doc_docs = load_documentation(base_path)
    
    all_docs = code_docs + doc_docs
    
    logger.info(
        "Loaded %d total documents (%d code, %d docs)",
        len(all_docs), len(code_docs), len(doc_docs)
    )
    
    return all_docs

