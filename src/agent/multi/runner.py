"""
Two-Agent Runner - Chains Gatherer and Reporter.

This shows the simplest form of multi-agent collaboration:
one agent's output becomes another's input.

Exercise 0: Students wire together the GathererAgent and ReporterAgent
to complete a query -> gather -> report workflow.
"""

from typing import Optional
from .gatherer import GathererAgent
from .reporter import ReporterAgent


def run_two_agent_workflow(query: str) -> str:
    """
    Execute a two-agent workflow: gather information, then report.
    
    This is the bridge pattern before coordinator-worker:
    - No message protocol (just function calls)
    - No shared state (just passing data)
    - No retry logic (simple error handling)
    
    Args:
        query: What to research (e.g., "Find Python files in src/")
        
    Returns:
        Summary string from reporter, or error message
        
    Workflow:
        1. GathererAgent searches and collects information
        2. If gathering succeeds, pass data to ReporterAgent
        3. ReporterAgent creates summary
        4. Return summary to user
        
    TODO (Exercise 0, Task 3):
    1. Create GathererAgent instance
    2. Call gatherer.gather(query)
    3. Check if gathering succeeded (status == "success")
    4. If failed, return error message
    5. Create ReporterAgent instance
    6. Call reporter.report(gathered_data)
    7. Return the summary
    
    Example:
        result = run_two_agent_workflow("Python files in src/agent/")
        print(result)
        # "Summary: Found 5 Python files in src/agent/: simple_agent.py, ..."
    """
    # TODO: Implement the two-agent workflow
    #
    # Pattern:
    #   gatherer = GathererAgent()
    #   gathered = gatherer.gather(query)
    #   
    #   if gathered["status"] != "success":
    #       return f"Gathering failed: {gathered.get('error', 'Unknown error')}"
    #   
    #   reporter = ReporterAgent()
    #   summary = reporter.report(gathered)
    #   
    #   return summary
    
    raise NotImplementedError(
        "Exercise 0, Task 3: Implement run_two_agent_workflow()\n"
        "See lesson-2-multi-agent/lab-2/exercises/00-bridge-refactoring.md"
    )


# Quick test when running directly
if __name__ == "__main__":
    print("Testing two-agent workflow...")
    print("-" * 40)
    
    try:
        result = run_two_agent_workflow("Find Python files in src/agent/")
        print("Result:")
        print(result)
    except NotImplementedError as e:
        print(f"Not implemented yet: {e}")
    except Exception as e:
        print(f"Error: {e}")

