"""
Data Agent - Specialized in quantitative analysis.

Responsibilities:
- Analyze numerical data and statistics
- Calculate trends, growth rates, metrics
- Identify patterns in data
- Present quantitative insights with transparency

Does NOT gather data (that's Research Agent's job).
Does NOT write prose reports (that's Writer Agent's job).
"""

from typing import Dict
from ..worker_base import WorkerAgent
from ..shared_state import SharedState


class DataAgent(WorkerAgent):
    """
    Agent specialized in data analysis and metrics calculation.

    Example:
        data = DataAgent(shared_state)
        # Assumes research_findings already in shared_state
        result = data.analyze_trends()

        # Writes to shared_state["data_analysis"]
        # Returns: {"status": "success", "metrics_count": 3}
    """

    def __init__(self, shared_state: SharedState):
        """
        Initialize data agent.

        Inherits from WorkerAgent which inherits from Agent:
        - Gets Ollama LLM via self.chat() method
        - Gets tool calling capability
        - Tools filtered to: calculate only

        TODO: Students complete this in Exercise 2
        - Call parent __init__ with name, shared_state, allowed_tools
        - Override self.messages[0] to set specialized system prompt
        """
        super().__init__(
            name="data", shared_state=shared_state, allowed_tools=["calculate"]
        )

        # TODO: Override system prompt for data analysis specialization
        # self.messages[0] = {"role": "system", "content": "..."}

    def execute(self, action: str, payload: Dict) -> Dict:
        """
        Execute data analysis actions.

        Args:
            action: Action name (e.g., "analyze_trends")
            payload: Action parameters

        Returns:
            Result dictionary
        """
        if action == "analyze_trends":
            return self.analyze_trends()
        else:
            return {"status": "error", "error": f"Unknown action: {action}"}

    def analyze_trends(self) -> Dict:
        """
        Analyze research findings for trends and metrics using inherited LLM and tools.

        Returns:
            Dict with status and metrics
            Example: {"status": "success", "metrics_count": 5}

        TODO: Students implement this in Lab 2 Exercise 2
        Use self.chat() to call LLM with calculate tool for analysis.
        """
        self.logger.info("Starting data analysis")
        raise NotImplementedError(
            "Students implement analyze_trends() in Lab 2 Exercise 2"
        )
