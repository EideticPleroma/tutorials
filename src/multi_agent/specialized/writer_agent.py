"""
Writer Agent - Specialized in report generation.

Responsibilities:
- Synthesize research and analysis into reports
- Format content with markdown (headings, lists, emphasis)
- Create clear narrative structure
- Include all source citations
- Maintain objectivity

Does NOT gather data (uses Research Agent's output).
Does NOT analyze data (uses Data Agent's output).
"""

from typing import Dict
from ..worker_base import WorkerAgent
from ..shared_state import SharedState


class WriterAgent(WorkerAgent):
    """
    Agent specialized in creating formatted reports.

    Example:
        writer = WriterAgent(shared_state)
        # Assumes research_findings and data_analysis in shared_state
        result = writer.create_report()

        # Writes to shared_state["final_report"]
        # Returns: {"status": "success", "report": "# Report..."}
    """

    def __init__(self, shared_state: SharedState):
        """
        Initialize writer agent.

        Inherits from WorkerAgent which inherits from Agent:
        - Gets Ollama LLM via self.chat() method
        - Gets tool calling capability
        - Tools filtered to: none (LLM-only for prose generation)

        TODO: Students complete this in Exercise 2
        - Call parent __init__ with name, shared_state, allowed_tools
        - Override self.messages[0] to set specialized system prompt
        """
        super().__init__(
            name="writer",
            shared_state=shared_state,
            allowed_tools=[],  # Writer uses LLM only, no external tools
        )

        # TODO: Override system prompt for technical writing specialization
        # self.messages[0] = {"role": "system", "content": "..."}

    def execute(self, action: str, payload: Dict) -> Dict:
        """
        Execute writing actions.

        Args:
            action: Action name (e.g., "create_report")
            payload: Action parameters

        Returns:
            Result dictionary
        """
        if action == "create_report":
            return self.create_report()
        else:
            return {"status": "error", "error": f"Unknown action: {action}"}

    def create_report(self) -> Dict:
        """
        Create formatted report from research and analysis using inherited LLM.

        Returns:
            Dict with status and report
            Example: {"status": "success", "report": "# Report...", "message": "..."}

        TODO: Students implement this in Lab 2 Exercise 2
        Use self.chat() to call LLM for markdown report generation.
        """
        self.logger.info("Starting report creation")
        raise NotImplementedError(
            "Students implement create_report() in Lab 2 Exercise 2"
        )
