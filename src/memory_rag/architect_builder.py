"""
Architect-Builder coordinator for the complete workflow.

This module orchestrates the full Architect-Builder pattern:
1. User request -> Architect plans
2. For each task: Builder implements -> O.V.E. validates -> Architect reviews
3. Retry on failure (max 3 times)
4. Return summary of completed work
"""

import logging
from typing import Optional

from .rag_engine import RAGEngine
from .architect_agent import ArchitectAgent
from .builder_agent import BuilderAgent
from .ove_harness import OVETestHarness

logger = logging.getLogger(__name__)


class ArchitectBuilderCoordinator:
    """
    Coordinates the Architect-Builder workflow.
    
    Flow:
    1. User request -> Architect plans
    2. For each task: Builder implements -> O.V.E. validates -> Architect reviews
    3. Retry on failure (max 3 times)
    4. Return summary of completed work
    
    Example:
        >>> coordinator = ArchitectBuilderCoordinator()
        >>> result = coordinator.process_request("Add a greeting tool")
        >>> print(f"Success: {result['overall_success']}")
        >>> print(f"Completed: {result['successful_tasks']}/{result['total_tasks']}")
    """
    
    MAX_RETRIES = 3
    
    def __init__(self, persist_dir: str = "./storage/project_index"):
        """
        Initialize the coordinator with all components.
        
        Args:
            persist_dir: Directory where the RAG index is stored.
        """
        logger.info("Initializing ArchitectBuilderCoordinator...")
        
        # Initialize RAG engine
        self.rag_engine = RAGEngine(persist_dir)
        
        try:
            self.rag_engine.load_index()
            logger.info("RAG index loaded")
        except FileNotFoundError:
            logger.warning(
                "RAG index not found at %s. "
                "Run build_index() first or queries will fail.",
                persist_dir
            )
        
        # Initialize agents
        self.architect = ArchitectAgent(self.rag_engine)
        self.builder = BuilderAgent(self.rag_engine)
        self.harness = OVETestHarness()
        
        logger.info("ArchitectBuilderCoordinator initialized")
    
    def process_request(self, request: str) -> dict:
        """
        Process a user request through the full workflow.
        
        Args:
            request: Natural language description of what to build/change.
            
        Returns:
            Summary dict with keys:
            - request: Original request
            - total_tasks: Number of tasks in plan
            - successful_tasks: Number completed successfully
            - failed_tasks: Number that failed after retries
            - results: List of per-task results
            - overall_success: True if all tasks succeeded
        
        Example:
            >>> result = coordinator.process_request(
            ...     "Add a function that returns the current timestamp"
            ... )
            >>> if result['overall_success']:
            ...     print("All tasks completed!")
            >>> else:
            ...     print(f"Failed tasks: {result['failed_tasks']}")
        """
        logger.info("Processing request: %s", request[:100])
        
        # 1. Architect creates plan
        plan = self.architect.plan(request)
        logger.info("Plan created with %d tasks", len(plan))
        
        if not plan:
            return self._create_summary(request, [], [])
        
        # 2. Process each task
        results = []
        for task in plan:
            result = self._process_task(task)
            results.append(result)
            
            if not result["success"]:
                logger.warning(
                    "Task %d failed after %d retries",
                    task.get("id", 0),
                    self.MAX_RETRIES
                )
        
        # 3. Create summary
        return self._create_summary(request, plan, results)
    
    def _process_task(self, task: dict) -> dict:
        """
        Process a single task with retries.
        
        Args:
            task: Task dictionary from the plan.
            
        Returns:
            Result dict with keys:
            - task_id: Task number
            - success: Whether task completed successfully
            - implementation: Code if successful
            - attempts: Number of attempts made
            - last_error: Error message if failed
        """
        task_id = task.get("id", 0)
        
        for attempt in range(self.MAX_RETRIES):
            logger.info(
                "Task %d, attempt %d/%d",
                task_id, attempt + 1, self.MAX_RETRIES
            )
            
            # Builder implements
            implementation = self.builder.implement(task)
            
            # O.V.E. validates
            ove_result = self.harness.run(implementation)
            
            if ove_result["overall_passed"]:
                logger.info("Task %d passed O.V.E. validation", task_id)
                
                # Architect validates
                validation = self.architect.validate(task, implementation["code"])
                
                if validation.get("approved", False):
                    logger.info("Task %d approved by Architect", task_id)
                    return {
                        "task_id": task_id,
                        "success": True,
                        "implementation": implementation,
                        "attempts": attempt + 1,
                    }
                else:
                    # Add architect feedback for retry
                    task["previous_feedback"] = validation.get("feedback", "")
                    logger.info(
                        "Task %d rejected by Architect: %s",
                        task_id,
                        validation.get("feedback", "")[:100]
                    )
            else:
                # Add O.V.E. errors for retry
                task["previous_errors"] = str(ove_result.get("validation", {}))
                logger.info(
                    "Task %d failed O.V.E.: %s",
                    task_id,
                    str(ove_result.get("validation", {}))[:100]
                )
        
        # All retries exhausted
        return {
            "task_id": task_id,
            "success": False,
            "attempts": self.MAX_RETRIES,
            "last_error": task.get(
                "previous_errors",
                task.get("previous_feedback", "Unknown error")
            ),
        }
    
    def _create_summary(
        self,
        request: str,
        plan: list,
        results: list
    ) -> dict:
        """Create summary of workflow execution."""
        successful = [r for r in results if r.get("success", False)]
        failed = [r for r in results if not r.get("success", False)]
        
        return {
            "request": request,
            "total_tasks": len(plan),
            "successful_tasks": len(successful),
            "failed_tasks": len(failed),
            "results": results,
            "overall_success": len(failed) == 0 and len(plan) > 0,
        }

