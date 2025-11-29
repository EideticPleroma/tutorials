"""
Gatherer Agent - Collects information using file tools.

This is a bridge exercise showing how to split responsibilities
before introducing coordinators and message protocols.

Exercise 0: Students extend the Agent class from Tutorial 1 to create
a specialized agent that only gathers information (doesn't analyze or summarize).
"""

from typing import Dict, List, Optional
from ..simple_agent import Agent


class GathererAgent(Agent):
    """
    Agent specialized in gathering information from files.
    
    Inherits from Tutorial 1's Agent class, getting:
    - LLM integration (self.client, self.model)
    - Tool calling capability (self.chat())
    - Message history (self.messages)
    
    Specialization:
    - Only uses search_files and read_file tools
    - Focused system prompt for information gathering
    - Does NOT analyze or summarize (that's ReporterAgent's job)
    
    Example:
        gatherer = GathererAgent()
        result = gatherer.gather("Find Python files in src/")
        # Returns: {"status": "success", "findings": [...], "sources": [...]}
    """
    
    # Tools this agent is allowed to use
    ALLOWED_TOOLS = ["search_files", "read_file"]
    
    def __init__(self):
        """
        Initialize gatherer with limited tools and focused system prompt.
        
        TODO (Exercise 0, Task 1):
        1. Call parent __init__ to get Agent capabilities
        2. Filter self.tools to only include ALLOWED_TOOLS
        3. Override self.messages[0] with gathering-focused system prompt
        """
        # Step 1: Initialize parent Agent class
        super().__init__()
        
        # Step 2: Filter tools to only allowed ones
        # TODO: Implement tool filtering
        # Hint: self.tools is a list of tool schemas from registry
        # Filter to keep only tools where name is in ALLOWED_TOOLS
        # self.tools = [t for t in self.tools if ...]
        
        # Step 3: Override system prompt for gathering focus
        # TODO: Replace the system prompt with one focused on gathering
        # self.messages[0] = {"role": "system", "content": "..."}
        
        raise NotImplementedError(
            "Exercise 0, Task 1: Implement GathererAgent.__init__()\n"
            "See lesson-2-multi-agent/lab-2/exercises/00-bridge-refactoring.md"
        )
    
    def gather(self, query: str, max_sources: int = 5) -> Dict:
        """
        Gather information about a query using file tools.
        
        Args:
            query: What to search for (e.g., "Python files in src/")
            max_sources: Maximum number of sources to collect
            
        Returns:
            Dict with:
            - status: "success" or "error"
            - findings: List of facts found (if success)
            - sources: List of file paths searched (if success)
            - error: Error message (if error)
            
        TODO (Exercise 0, Task 1):
        1. Build a prompt asking the LLM to search and gather information
        2. Call self.chat(prompt) - LLM will use tools automatically
        3. Parse the response to extract structured findings
        4. Return a dict with status, findings, and sources
        
        Example implementation pattern:
            prompt = f"Search for and gather information about: {query}"
            response = self.chat(prompt)
            # Parse response to extract findings...
            return {"status": "success", "findings": [...], "sources": [...]}
        """
        # TODO: Implement gathering logic
        # 
        # Hints:
        # - Use self.chat() to interact with the LLM (it handles tool calls)
        # - The LLM will automatically use search_files and read_file
        # - Parse the LLM's response to extract structured information
        # - Return a dict, not raw text
        
        raise NotImplementedError(
            "Exercise 0, Task 1: Implement GathererAgent.gather()\n"
            "See lesson-2-multi-agent/lab-2/exercises/00-bridge-refactoring.md"
        )

