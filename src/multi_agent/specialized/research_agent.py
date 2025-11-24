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

from typing import Dict
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

        Inherits from WorkerAgent which inherits from Agent:
        - Gets Ollama LLM via self.chat() method
        - Gets tool calling capability
        - Tools filtered to: search_files, read_file only

        TODO: Students complete this in Exercise 2
        - Call parent __init__ with name, shared_state, allowed_tools
        - Override self.messages[0] to set specialized system prompt
        """
        super().__init__(
            name="research",
            shared_state=shared_state,
            allowed_tools=["search_files", "read_file"],
        )

        # TODO: Override system prompt for research specialization
        # self.messages[0] = {"role": "system", "content": "..."}

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
                query=payload.get("query"), max_sources=payload.get("max_sources", 5)
            )
        else:
            return {"status": "error", "error": f"Unknown action: {action}"}

    def gather_info(self, query: str, max_sources: int = 5) -> Dict:
        """
        Gather information on a topic using inherited LLM and tools.

        Args:
            query: Research topic/question
            max_sources: Maximum number of sources to gather

        Returns:
            Dict with status and summary
            Example: {"status": "success", "findings_count": 5}

        TODO: Students implement this in Lab 2 Exercise 2
        Use self.chat() to call LLM with allowed tools (file_search, read_file).
        """
        self.logger.info("Starting research for query: %s", query)
        raise NotImplementedError(
            "Students implement gather_info() in Lab 2 Exercise 2"
        )
