"""
Knowledge tool for agents to search the codebase.

This module provides a tool that agents can use to query the RAG
system and retrieve relevant code and documentation.
"""

import logging
from typing import Optional

# TODO: Import tool registry
# from src.agent.tool_registry import registry

from .rag_engine import RAGEngine

logger = logging.getLogger(__name__)

# Global engine instance (lazy loaded)
_engine: Optional[RAGEngine] = None


def get_engine() -> RAGEngine:
    """
    Get or create the RAG engine singleton.
    
    Returns:
        Initialized RAGEngine with loaded index.
        
    Raises:
        RuntimeError: If index cannot be loaded.
    """
    global _engine
    
    if _engine is None:
        logger.info("Initializing RAG engine...")
        _engine = RAGEngine()
        _engine.load_index()
        logger.info("RAG engine ready")
    
    return _engine


# TODO: Uncomment and implement when tool registry is available
# @registry.register
def search_codebase(query: str) -> str:
    """
    Search the tutorial codebase for relevant code and documentation.
    
    Use this tool when you need to:
    - Find how something is implemented in this project
    - Look up existing patterns or conventions
    - Understand how components work together
    - Get code examples for similar functionality
    
    Args:
        query: Natural language description of what to find.
               Examples: 
               - "How does the coordinator delegate tasks?"
               - "What is the message protocol format?"
               - "Show me examples of tool registration"
               - "How is logging configured?"
    
    Returns:
        Formatted search results including:
        - Relevant code snippets
        - Documentation excerpts  
        - File paths for reference
        
        If nothing relevant is found, returns a message saying so.
    
    Example:
        >>> result = search_codebase("How does tool calling work?")
        >>> print(result)
        Found 3 relevant results:
        
        [1] src/agent/simple_agent.py (score: 0.89)
        def execute_tool(self, tool_name, arguments):
            ...
    """
    # TODO: Implement search using RAGEngine
    # 1. Get engine singleton
    # 2. Retrieve relevant chunks
    # 3. Format results nicely for the agent
    
    logger.info("search_codebase called with query: %s", query[:100])
    
    try:
        engine = get_engine()
        results = engine.retrieve(query, top_k=5)
        
        if not results:
            return f"No relevant results found for: {query}"
        
        # Format results
        output = f"Found {len(results)} relevant results:\n\n"
        
        for i, result in enumerate(results, 1):
            file_path = result["metadata"].get("file_path", "unknown")
            score = result["score"]
            text = result["text"][:500]  # Truncate long content
            
            output += f"[{i}] {file_path} (score: {score:.2f})\n"
            output += f"{text}\n"
            output += "-" * 40 + "\n\n"
        
        return output
        
    except Exception as e:
        logger.error("Error in search_codebase: %s", str(e))
        return f"Error searching codebase: {str(e)}"


def find_similar_code(code_snippet: str) -> str:
    """
    Find code similar to the given snippet.
    
    Use this tool when you have a code snippet and want to find
    similar implementations in the codebase.
    
    Args:
        code_snippet: A piece of code to find similar examples for.
    
    Returns:
        Similar code snippets from the codebase.
    """
    # TODO: Implement similarity search
    # This is a convenience wrapper around search_codebase
    
    logger.info("find_similar_code called with %d chars", len(code_snippet))
    
    return search_codebase(code_snippet)

