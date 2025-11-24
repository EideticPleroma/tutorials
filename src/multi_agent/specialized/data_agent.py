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

        Sets up:
        - Focused system prompt for data analyst
        - Allowed tools for analysis tasks
        """
        # Pass allowed_tools to parent - only calculation tool
        super().__init__(
            name="data", shared_state=shared_state, allowed_tools=["calculate"]
        )

        # Override system prompt for data analysis specialization
        self.messages[0] = {
            "role": "system",
            "content": """You are a Data Analyst AI agent in a multi-agent system.

ROLE: Your sole responsibility is quantitative analysis of research data.

YOUR CAPABILITIES:
- Analyze numerical data and statistics from research findings
- Calculate growth rates, percentages, ratios, and averages using calculate tool
- Identify trends and patterns in data sets
- Compute year-over-year changes and comparative metrics
- Present statistical insights with full transparency
- Show all calculations and methodology
- Validate data quality and flag inconsistencies

STRICT BOUNDARIES (Do NOT do these):
- Do NOT gather or search for new information (Research Agent's responsibility)
- Do NOT write narrative reports or prose (Writer Agent's responsibility)
- Do NOT make qualitative judgments or subjective interpretations
- Do NOT provide recommendations or opinions
- Do NOT speculate beyond the data provided

OUTPUT REQUIREMENTS:
- Present findings as quantitative metrics with clear labels
- Show calculations explicitly (e.g., "Growth: (2023-2022)/2022 = 55%")
- Organize metrics logically (counts, percentages, trends, comparisons)
- Use precise numbers from source data
- Flag any assumptions or limitations in the analysis
- Structure output as: {"metrics": {...}, "insights": ["quantitative insight 1", ...]}

FOCUS: Accuracy and transparency. Extract every quantifiable insight from the data and show your work. Pass structured metrics to the Writer Agent for narrative synthesis.""",
        }

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

        TODO: Students implement this in Lab 2 Exercise 2

        Implementation Steps:
        1. Read research_findings from shared_state
        2. Use self.chat() to ask LLM to analyze the findings
        3. LLM can use calculate tool for computations
        4. Parse LLM response to extract structured metrics
        5. Save analysis to shared_state["data_analysis"]
        6. Return status dictionary

        Returns:
            Dict with status and metrics
            Example: {"status": "success", "metrics_count": 5}

        Hints:
        - Get findings with: self.shared_state.get("research_findings", [])
        - Build prompt asking LLM to analyze trends, calculate metrics
        - The LLM has access to calculate tool for computations
        - Parse response into structured format: {"metrics": {...}, "insights": [...]}
        - Use self.shared_state.set("data_analysis", analysis)
        - Handle case where no findings exist

        Example Implementation Pattern:
            findings = self.shared_state.get("research_findings", [])
            if not findings:
                return {"status": "error", "error": "No research findings available"}

            prompt = f"Analyze these research findings and calculate metrics: {findings}"
            response = self.chat(prompt)
            # Parse response, structure analysis
            analysis = {"metrics": {...}, "insights": [...]}
            self.shared_state.set("data_analysis", analysis)
            return {"status": "success", "metrics_count": len(analysis["metrics"])}
        """
        self.logger.info("Starting data analysis")

        # TODO: Students implement actual LLM-based analysis here
        raise NotImplementedError(
            "Students implement analyze_trends() in Lab 2 Exercise 2. "
            "Use self.chat() to call LLM with calculate tool for analysis."
        )
