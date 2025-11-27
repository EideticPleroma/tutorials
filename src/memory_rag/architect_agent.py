"""
Architect agent for planning and validation.

The Architect uses Llama 3.1 to:
- Understand user requirements
- Query RAG for existing patterns
- Create detailed task plans
- Validate Builder implementations
"""

import json
import logging
from typing import Optional

from .config import get_architect_llm
from .rag_engine import RAGEngine

logger = logging.getLogger(__name__)


class ArchitectAgent:
    """
    Architect agent that plans code changes using Llama 3.1.
    
    Responsibilities:
    - Understand user requirements
    - Query RAG for existing patterns
    - Create detailed task plans
    - Validate implementations
    
    Example:
        >>> architect = ArchitectAgent(rag_engine)
        >>> plan = architect.plan("Add a greeting tool to the agent")
        >>> print(plan)
        [{'id': 1, 'description': '...', 'file': '...', 'spec': '...'}]
    """
    
    SYSTEM_PROMPT = """You are an Architect agent that plans code changes.

When planning:
1. Understand what the user wants to accomplish
2. Search for existing patterns in the codebase (context provided)
3. Break down into specific, implementable tasks
4. Each task should modify ONE file and have clear acceptance criteria

Output your plan as JSON:
{
    "tasks": [
        {
            "id": 1,
            "description": "Human-readable description of what to do",
            "file": "path/to/file.py",
            "spec": "Detailed specification for implementation",
            "acceptance_criteria": ["Criterion 1", "Criterion 2"]
        }
    ]
}

Important:
- Reference specific files and patterns from the context
- Each task should be small enough to implement in one pass
- Include type hints and docstrings in requirements
- Follow the project's coding standards

Output ONLY valid JSON, no other text."""
    
    VALIDATION_PROMPT = """You are an Architect validating an implementation.

Task: {task_description}
Specification: {spec}
Acceptance Criteria: {criteria}

Implementation:
```python
{code}
```

Evaluate if this implementation meets ALL acceptance criteria.

Respond with JSON:
{{
    "approved": true/false,
    "feedback": "Detailed feedback explaining your decision",
    "issues": ["List of specific issues if not approved"]
}}

Output ONLY valid JSON."""
    
    def __init__(self, rag_engine: RAGEngine):
        """
        Initialize Architect agent.
        
        Args:
            rag_engine: RAGEngine instance for querying codebase.
        """
        # TODO: Initialize LLM
        # self.llm = get_architect_llm()
        self.llm = None
        self.rag_engine = rag_engine
        
        logger.info("ArchitectAgent initialized")
    
    def plan(self, request: str) -> list:
        """
        Create a task plan from user request.
        
        Args:
            request: Natural language description of what to build/change.
            
        Returns:
            List of task dictionaries with keys:
            - id: Task number
            - description: Human-readable description
            - file: File to modify
            - spec: Detailed specification
            - acceptance_criteria: List of criteria
        
        Example:
            >>> plan = architect.plan("Add logging to tool execution")
            >>> print(plan[0]['description'])
            'Add structlog initialization to Agent class'
        """
        # TODO: Implement planning
        # 1. Query RAG for context
        # 2. Build prompt with context
        # 3. Call LLM
        # 4. Parse JSON response
        
        logger.info("Creating plan for: %s", request[:100])
        
        # Get context from RAG
        context = self._get_context(request)
        
        # Build prompt
        prompt = f"""{self.SYSTEM_PROMPT}

Context from codebase:
{context}

User request: {request}

Create a detailed task plan:"""
        
        # TODO: Call LLM
        # response = str(self.llm.complete(prompt))
        response = '{"tasks": []}'  # Placeholder
        
        # Parse response
        return self._parse_plan(response)
    
    def validate(self, task: dict, code: str) -> dict:
        """
        Validate that implementation meets task requirements.
        
        Args:
            task: Task dictionary from the plan.
            code: Generated code to validate.
            
        Returns:
            Validation result with keys:
            - approved: bool
            - feedback: str
            - issues: list (if not approved)
        
        Example:
            >>> result = architect.validate(task, code)
            >>> if result['approved']:
            ...     print("Implementation accepted!")
            >>> else:
            ...     print(f"Issues: {result['issues']}")
        """
        # TODO: Implement validation
        # 1. Build validation prompt
        # 2. Call LLM
        # 3. Parse response
        
        logger.info("Validating implementation for task %d", task.get("id", 0))
        
        prompt = self.VALIDATION_PROMPT.format(
            task_description=task.get("description", ""),
            spec=task.get("spec", ""),
            criteria=task.get("acceptance_criteria", []),
            code=code,
        )
        
        # TODO: Call LLM
        # response = str(self.llm.complete(prompt))
        response = '{"approved": true, "feedback": "TODO: Implement"}'  # Placeholder
        
        return self._parse_validation(response)
    
    def _get_context(self, request: str) -> str:
        """Get relevant context from RAG for planning."""
        try:
            results = self.rag_engine.retrieve(request, top_k=5)
            
            context_parts = []
            for r in results:
                file_path = r["metadata"].get("file_path", "unknown")
                text = r["text"][:800]  # Truncate
                context_parts.append(f"File: {file_path}\n{text}")
            
            return "\n\n---\n\n".join(context_parts)
        except Exception as e:
            logger.warning("Failed to get RAG context: %s", str(e))
            return "No context available."
    
    def _parse_plan(self, response: str) -> list:
        """Parse LLM response into task list."""
        try:
            # Try direct parse
            data = json.loads(response)
            return data.get("tasks", [])
        except json.JSONDecodeError:
            # Try to find JSON in response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group())
                    return data.get("tasks", [])
                except json.JSONDecodeError:
                    pass
            
            logger.warning("Failed to parse plan from response")
            return []
    
    def _parse_validation(self, response: str) -> dict:
        """Parse LLM validation response."""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.warning("Failed to parse validation response")
            return {
                "approved": False,
                "feedback": "Failed to parse validation response",
                "issues": ["Parse error"],
            }

