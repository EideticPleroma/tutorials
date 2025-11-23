"""
Research Agent - Specialized in information gathering.

Responsibilities:
- Search for information from various sources
- Extract key facts and data points
- Cite sources with URLs or file paths
- Flag data quality and recency

Does NOT analyze or interpret data (that's Data Agent's job).
Does NOT write reports (that's Writer Agent's job).
"""

from typing import Dict, List
from ..worker_base import WorkerAgent
from ..shared_state import SharedState


class ResearchAgent(WorkerAgent):
    """
    Agent specialized in gathering information from sources.
    
    Example:
        research = ResearchAgent(shared_state)
        result = research.gather_info("electric vehicle market trends")
        
        # Writes to shared_state["research_findings"]
        # Returns: {"status": "success", "findings_count": 5}
    """
    
    def __init__(self, shared_state: SharedState):
        """
        Initialize research agent.
        
        Sets up:
        - Focused system prompt for research specialist
        - Research tools (web_search, read_file, list_files)
        """
        super().__init__(name="research", shared_state=shared_state)
        
        # TODO: Students set this in Exercise 2
        # Should define agent as research specialist with clear boundaries
        self.system_prompt = """
        You are a Research Specialist.
        
        Your job: Gather information and cite sources.
        
        YOU DO:
        - Search for relevant information
        - Extract specific facts and data points
        - Provide source citations (URLs or file paths)
        - Note the date and quality of information
        
        YOU DO NOT:
        - Analyze trends (that's Data Agent's job)
        - Calculate metrics (that's Data Agent's job)
        - Write reports (that's Writer Agent's job)
        - Interpret findings (that's Data Agent's job)
        
        Output format: List of findings, each with fact and source.
        """
        
        # TODO: Students register tools in Exercise 2
        # self.tools = {"web_search": ..., "read_file": ..., "list_files": ...}
    
    def execute(self, action: str, payload: Dict) -> Dict:
        """
        Execute research actions.
        
        Args:
            action: Action name (e.g., "gather_info")
            payload: Action parameters
        
        Returns:
            Result dictionary
        """
        if action == "gather_info":
            return self.gather_info(
                query=payload.get("query"),
                max_sources=payload.get("max_sources", 5)
            )
        else:
            return {
                "status": "error",
                "error": f"Unknown action: {action}"
            }
    
    def gather_info(self, query: str, max_sources: int = 5) -> Dict:
        """
        Gather information on a topic.
        
        Args:
            query: Research topic/question
            max_sources: Maximum number of sources to gather
        
        Returns:
            Dict with status and summary
        
        Students implement this in Exercise 2.
        Should:
        1. Use tools to find information
        2. Extract key facts
        3. Cite sources
        4. Write to shared_state["research_findings"]
        5. Return status and count
        """
        # TODO: Students implement in Exercise 2
        
        # Placeholder implementation
        findings = [
            {"fact": "Placeholder finding 1", "source": "placeholder"},
            {"fact": "Placeholder finding 2", "source": "placeholder"},
            {"fact": "Placeholder finding 3", "source": "placeholder"}
        ]
        
        self.shared_state.set("research_findings", findings)
        
        return {
            "status": "success",
            "findings_count": len(findings),
            "message": "Research agent placeholder - students implement in Exercise 2"
        }

