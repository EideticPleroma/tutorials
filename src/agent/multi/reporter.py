"""
Reporter Agent - Summarizes gathered information.

This is a bridge exercise showing agent collaboration
before introducing message protocols.

Exercise 0: Students extend the Agent class to create a specialist
that only summarizes - no information gathering (that's GathererAgent's job).
"""

from typing import Dict
from ..simple_agent import Agent


class ReporterAgent(Agent):
    """
    Agent specialized in creating summaries from gathered data.
    
    Inherits from Tutorial 1's Agent class, getting:
    - LLM integration (self.client, self.model)
    - Message history (self.messages)
    
    Specialization:
    - NO tools (LLM-only for pure synthesis)
    - Focused system prompt for summarization
    - Takes gathered data as input, produces summary as output
    - Does NOT gather information (that's GathererAgent's job)
    
    Example:
        reporter = ReporterAgent()
        summary = reporter.report(gathered_data)
        # Returns: "Summary: Found 3 Python files..."
    """
    
    def __init__(self):
        """
        Initialize reporter with no tools (LLM only) and focused system prompt.
        
        TODO (Exercise 0, Task 2):
        1. Call parent __init__ to get Agent capabilities
        2. Clear self.tools (reporter has no tools)
        3. Override self.messages[0] with summarization-focused system prompt
        """
        # Step 1: Initialize parent Agent class
        super().__init__()
        
        # Step 2: Remove all tools (reporter is LLM-only)
        # TODO: Clear the tools list
        # self.tools = []
        
        # Step 3: Override system prompt for reporting focus
        # TODO: Replace the system prompt with one focused on summarization
        # The prompt should:
        # - Focus on creating clear, organized summaries
        # - Emphasize using ONLY the provided data (no making things up)
        # - Include source citations
        # - Be concise and factual
        
        raise NotImplementedError(
            "Exercise 0, Task 2: Implement ReporterAgent.__init__()\n"
            "See lesson-2-multi-agent/lab-2/exercises/00-bridge-refactoring.md"
        )
    
    def report(self, gathered_data: Dict) -> str:
        """
        Create a summary from gathered information.
        
        Args:
            gathered_data: Dict from GathererAgent containing:
                - findings: List of facts/information gathered
                - sources: List of file paths that were searched
                
        Returns:
            Formatted summary string
            
        TODO (Exercise 0, Task 2):
        1. Validate gathered_data has required fields
        2. Build a prompt with the gathered data for the LLM
        3. Call self.chat(prompt) to generate summary
        4. Return the summary string
        
        Example implementation pattern:
            findings = gathered_data.get("findings", [])
            sources = gathered_data.get("sources", [])
            prompt = f"Summarize these findings: {findings}\\nSources: {sources}"
            summary = self.chat(prompt)
            return summary
        """
        # TODO: Implement reporting logic
        #
        # Hints:
        # - Extract findings and sources from gathered_data
        # - Handle case where data is missing or empty
        # - Build a clear prompt that includes the data to summarize
        # - Use self.chat() to get the LLM's summary
        # - Return the summary as a string
        
        raise NotImplementedError(
            "Exercise 0, Task 2: Implement ReporterAgent.report()\n"
            "See lesson-2-multi-agent/lab-2/exercises/00-bridge-refactoring.md"
        )

