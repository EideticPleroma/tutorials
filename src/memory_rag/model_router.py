"""
Model router for directing tasks to appropriate LLMs.

This module provides routing logic to select between:
- Llama 3.1 (Architect): Planning, reasoning, validation
- DeepSeek-Coder (Builder): Code generation, implementation
"""

import logging
from typing import Optional

from .config import get_architect_llm, get_builder_llm

logger = logging.getLogger(__name__)


class ModelRouter:
    """
    Routes tasks to appropriate LLMs based on task type.
    
    Task types and their default models:
    - planning: Llama (Architect)
    - coding: DeepSeek (Builder)
    - reasoning: Llama (Architect)
    - explaining: Llama (Architect)
    - implementing: DeepSeek (Builder)
    - testing: DeepSeek (Builder)
    - unknown: Llama (Architect)
    
    Example:
        >>> router = ModelRouter()
        >>> task_type = router.classify_task("Write a function to sort a list")
        >>> print(task_type)  # "coding"
        >>> llm = router.route(task_type)
        >>> # llm is DeepSeek-Coder
    """
    
    # Task type to model mapping
    TASK_MODELS = {
        "planning": "architect",
        "coding": "builder",
        "reasoning": "architect",
        "explaining": "architect",
        "implementing": "builder",
        "testing": "builder",
        "unknown": "architect",
    }
    
    # Keywords for classification
    CODING_KEYWORDS = [
        "implement", "write", "code", "function", "def ",
        "class ", "create function", "add method", "generate code",
        "fix bug", "refactor",
    ]
    
    PLANNING_KEYWORDS = [
        "plan", "break down", "design", "architect", "organize",
        "structure", "outline", "strategy",
    ]
    
    REASONING_KEYWORDS = [
        "explain", "why", "how does", "what is", "understand",
        "analyze", "evaluate", "compare", "describe",
    ]
    
    def __init__(self):
        """Initialize model router with both LLMs."""
        # TODO: Initialize LLMs
        # self.architect_llm = get_architect_llm()
        # self.builder_llm = get_builder_llm()
        
        self.architect_llm = None
        self.builder_llm = None
        
        logger.info("ModelRouter initialized")
    
    def route(self, task_type: str):
        """
        Get the appropriate LLM for a task type.
        
        Args:
            task_type: One of the defined task types (planning, coding, etc.)
            
        Returns:
            Ollama LLM instance appropriate for the task.
        """
        model_name = self.TASK_MODELS.get(task_type, "architect")
        
        if model_name == "builder":
            logger.info("Routing to Builder (DeepSeek)")
            return self.builder_llm
        else:
            logger.info("Routing to Architect (Llama)")
            return self.architect_llm
    
    def classify_task(self, request: str) -> str:
        """
        Classify a natural language request into a task type.
        
        Args:
            request: Natural language description of the task.
            
        Returns:
            Task type string (planning, coding, reasoning, etc.)
        
        Example:
            >>> router = ModelRouter()
            >>> router.classify_task("Write a sorting function")
            'coding'
            >>> router.classify_task("Explain how RAG works")
            'reasoning'
        """
        # TODO: Implement classification
        # Option 1: Simple keyword matching (implemented below)
        # Option 2: Use LLM to classify (more accurate but slower)
        
        request_lower = request.lower()
        
        # Check for coding keywords
        if any(kw in request_lower for kw in self.CODING_KEYWORDS):
            logger.debug("Classified as 'coding': %s", request[:50])
            return "coding"
        
        # Check for planning keywords
        if any(kw in request_lower for kw in self.PLANNING_KEYWORDS):
            logger.debug("Classified as 'planning': %s", request[:50])
            return "planning"
        
        # Check for reasoning keywords
        if any(kw in request_lower for kw in self.REASONING_KEYWORDS):
            logger.debug("Classified as 'reasoning': %s", request[:50])
            return "reasoning"
        
        # Default to unknown
        logger.debug("Classified as 'unknown': %s", request[:50])
        return "unknown"
    
    def process(self, request: str) -> str:
        """
        Classify and route a request, return the LLM response.
        
        This is a convenience method that:
        1. Classifies the task type
        2. Routes to appropriate LLM
        3. Returns the response
        
        Args:
            request: Natural language request.
            
        Returns:
            LLM response as string.
        """
        task_type = self.classify_task(request)
        llm = self.route(task_type)
        
        logger.info("Processing request (type=%s): %s", task_type, request[:50])
        
        # TODO: Call LLM and return response
        # return str(llm.complete(request))
        
        return f"TODO: Implement LLM call for {task_type}"

