"""
Builder agent for code implementation.

The Builder uses DeepSeek-Coder to:
- Implement code according to specifications
- Follow patterns from the codebase
- Generate tests for implementations
"""

import logging
import re
from typing import Optional

from .config import get_builder_llm
from .rag_engine import RAGEngine

logger = logging.getLogger(__name__)


class BuilderAgent:
    """
    Builder agent that implements code using DeepSeek-Coder.
    
    Responsibilities:
    - Receive task specifications from Architect
    - Query RAG for code examples
    - Generate clean, well-documented code
    - Follow codebase conventions
    
    Example:
        >>> builder = BuilderAgent(rag_engine)
        >>> task = {
        ...     "id": 1,
        ...     "description": "Add greeting function",
        ...     "file": "src/agent/simple_agent.py",
        ...     "spec": "Function that takes name and returns greeting"
        ... }
        >>> result = builder.implement(task)
        >>> print(result['code'])
    """
    
    SYSTEM_PROMPT = """You are a Builder agent that implements code.

Code standards for this project:
- Type hints on ALL function parameters and return types
- Google-style docstrings for ALL functions and classes
- Logging with lazy % formatting: logger.info("msg %s", var)
- Follow patterns from the provided examples
- Clean, readable code with meaningful variable names

Output only the code implementation, no explanations or markdown.
Do NOT wrap code in ```python``` blocks."""
    
    def __init__(self, rag_engine: RAGEngine):
        """
        Initialize Builder agent.
        
        Args:
            rag_engine: RAGEngine instance for getting code examples.
        """
        # TODO: Initialize LLM
        # self.llm = get_builder_llm()
        self.llm = None
        self.rag_engine = rag_engine
        
        logger.info("BuilderAgent initialized")
    
    def implement(self, task: dict) -> dict:
        """
        Implement a task according to specification.
        
        Args:
            task: Task dictionary with keys:
                - id: Task number
                - description: What to implement
                - file: File to modify
                - spec: Detailed specification
                - acceptance_criteria: List of criteria (optional)
                - previous_errors: Error from previous attempt (optional)
                - previous_feedback: Architect feedback (optional)
        
        Returns:
            Implementation result with keys:
            - task_id: Task number
            - status: "complete" or "error"
            - code: Generated code
            - tests: Generated tests (optional)
            - file: Target file
            - notes: Implementation notes
        
        Example:
            >>> result = builder.implement(task)
            >>> if result['status'] == 'complete':
            ...     print(result['code'])
        """
        # TODO: Implement code generation
        # 1. Get code examples from RAG
        # 2. Build prompt with examples and spec
        # 3. Call LLM
        # 4. Clean up output
        # 5. Generate tests
        
        logger.info(
            "Implementing task %d: %s",
            task.get("id", 0),
            task.get("description", "")[:50]
        )
        
        # Get examples from RAG
        examples = self._get_examples(task)
        
        # Build prompt
        prompt = self._build_prompt(task, examples)
        
        # TODO: Call LLM
        # code = str(self.llm.complete(prompt))
        code = "# TODO: Implement"  # Placeholder
        
        # Clean up code
        code = self._clean_code(code)
        
        # Generate tests
        tests = self._generate_tests(task, code)
        
        return {
            "task_id": task.get("id", 0),
            "status": "complete",
            "code": code,
            "tests": tests,
            "file": task.get("file", ""),
            "notes": "",
        }
    
    def _get_examples(self, task: dict) -> str:
        """Get relevant code examples from RAG."""
        try:
            # Build query from task
            query = f"code example: {task.get('spec', task.get('description', ''))}"
            
            results = self.rag_engine.retrieve(query, top_k=3)
            
            # Filter to only Python files
            python_results = [
                r for r in results
                if r["metadata"].get("file_type") == "python"
            ]
            
            if not python_results:
                python_results = results[:3]
            
            examples_parts = []
            for r in python_results:
                file_path = r["metadata"].get("file_path", "unknown")
                text = r["text"][:600]
                examples_parts.append(f"# From {file_path}:\n{text}")
            
            return "\n\n".join(examples_parts)
        except Exception as e:
            logger.warning("Failed to get examples: %s", str(e))
            return "No examples available."
    
    def _build_prompt(self, task: dict, examples: str) -> str:
        """Build the prompt for code generation."""
        prompt_parts = [self.SYSTEM_PROMPT]
        
        prompt_parts.append(f"\nExamples from codebase:\n{examples}")
        
        prompt_parts.append(f"\nTask: {task.get('description', '')}")
        prompt_parts.append(f"File: {task.get('file', '')}")
        prompt_parts.append(f"Specification: {task.get('spec', '')}")
        
        if task.get("acceptance_criteria"):
            criteria = "\n".join(f"- {c}" for c in task["acceptance_criteria"])
            prompt_parts.append(f"\nAcceptance criteria:\n{criteria}")
        
        # Add error context if retrying
        if task.get("previous_errors"):
            prompt_parts.append(
                f"\nPrevious attempt failed. Error:\n{task['previous_errors']}"
            )
            prompt_parts.append("Fix the error and try again.")
        
        if task.get("previous_feedback"):
            prompt_parts.append(
                f"\nArchitect feedback:\n{task['previous_feedback']}"
            )
            prompt_parts.append("Address the feedback in your implementation.")
        
        prompt_parts.append("\nImplementation:")
        
        return "\n".join(prompt_parts)
    
    def _clean_code(self, code: str) -> str:
        """Clean up LLM output to get pure code."""
        code = code.strip()
        
        # Remove markdown code fences
        if code.startswith("```"):
            lines = code.split("\n")
            # Remove first line (```python or ```)
            lines = lines[1:]
            # Remove last line if it's a closing fence
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]
            code = "\n".join(lines)
        
        return code.strip()
    
    def _generate_tests(self, task: dict, code: str) -> str:
        """Generate basic tests for the implementation."""
        # TODO: Implement test generation
        # 1. Build prompt asking for tests
        # 2. Call LLM
        # 3. Clean up output
        
        # For now, return a placeholder
        func_names = re.findall(r'def (\w+)\(', code)
        
        if not func_names:
            return ""
        
        test_parts = ["import pytest\n"]
        for func_name in func_names:
            test_parts.append(f"""
def test_{func_name}():
    \"\"\"Test {func_name} function.\"\"\"
    # TODO: Implement test
    pass
""")
        
        return "\n".join(test_parts)

