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

        Sets up:
        - Focused system prompt for research specialist
        - Allowed tools for research tasks
        """
        # Pass allowed_tools to parent - only research-related tools
        super().__init__(
            name="research",
            shared_state=shared_state,
            allowed_tools=["search_files", "read_file"],
        )

        # Override system prompt for research specialization
        # This replaces the default Tutorial 1 system prompt
        self.messages[0] = {
            "role": "system",
            "content": """You are a Research Specialist AI agent in a multi-agent system.

ROLE: Your sole responsibility is information gathering and source documentation.

YOUR CAPABILITIES:
- Search for information using search_files and read_file tools
- Extract specific facts, statistics, and data points from sources
- Identify key information relevant to the research query
- Document source file paths and citations
- Assess information quality and recency
- Gather information comprehensively across multiple sources

STRICT BOUNDARIES (Do NOT do these):
- Do NOT analyze data or identify trends (Data Agent's responsibility)
- Do NOT calculate metrics, percentages, or statistics (Data Agent's responsibility)
- Do NOT write formatted reports or narratives (Writer Agent's responsibility)
- Do NOT interpret or draw conclusions from findings (Data Agent's responsibility)
- Do NOT make recommendations or provide opinions

OUTPUT REQUIREMENTS:
- Provide findings as structured facts with sources
- Each finding must include: fact/data point + source citation (file path)
- Note publication date or last updated date when available
- Flag any concerns about data quality, outdated information, or missing sources
- Organize findings by relevance to the query

FOCUS: Breadth and accuracy. Gather comprehensive, well-sourced information and pass it to the Data Agent for analysis.""",
        }

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

        TODO: Students implement this in Lab 2 Exercise 2

        Implementation Steps:
        1. Use self.chat(prompt) to engage the LLM with research query
        2. LLM will automatically call allowed tools (file_search, read_file)
        3. Parse the LLM response to extract structured findings
        4. Save findings to shared_state["research_findings"]
        5. Return status dictionary

        Args:
            query: Research topic/question
            max_sources: Maximum number of sources to gather

        Returns:
            Dict with status and summary
            Example: {"status": "success", "findings_count": 5}

        Hints:
        - Build a prompt that asks the LLM to research the topic
        - The LLM has access to file_search and read_file tools
        - Parse the response and structure as list of dicts with "fact" and "source" keys
        - Use self.shared_state.set("research_findings", findings)
        - Handle exceptions and return error status if needed

        Example Implementation Pattern:
            prompt = f"Research the following topic: {query}. Find key facts and cite sources."
            response = self.chat(prompt)
            # Parse response, structure findings
            findings = [{"fact": "...", "source": "..."}, ...]
            self.shared_state.set("research_findings", findings)
            return {"status": "success", "findings_count": len(findings)}
        """
        self.logger.info("Starting research for query: %s", query)

        # TODO: Students implement actual LLM-based research here
        raise NotImplementedError(
            "Students implement gather_info() in Lab 2 Exercise 2. "
            "Use self.chat() to call LLM with allowed tools (file_search, read_file)."
        )
