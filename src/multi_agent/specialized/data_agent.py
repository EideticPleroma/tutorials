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
        
        Sets up:
        - Focused system prompt for data analyst
        - Analysis tools (calculate, analyze_trend)
        """
        super().__init__(name="data", shared_state=shared_state)
        
        # TODO: Students set this in Exercise 2
        self.system_prompt = """
        You are a Data Analyst specializing in quantitative analysis.
        
        Your job: Transform data into quantitative insights.
        
        YOU DO:
        - Analyze numerical data
        - Calculate growth rates, percentages, averages
        - Identify trends and patterns
        - Show your calculations (transparency)
        - Present statistical insights
        
        YOU DO NOT:
        - Gather information (that's Research Agent's job)
        - Write narrative reports (that's Writer Agent's job)
        - Make qualitative judgments
        - Search for new data
        
        Output format: Metrics dictionary with calculations shown.
        """
        
        # TODO: Students register analysis tools in Exercise 2
        # self.tools = {"calculate": ..., "analyze_trend": ...}
    
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
            return {
                "status": "error",
                "error": f"Unknown action: {action}"
            }
    
    def analyze_trends(self) -> Dict:
        """
        Analyze research findings for trends and metrics.
        
        Returns:
            Dict with status and metrics
        
        Students implement this in Exercise 2.
        Should:
        1. Read research_findings from shared_state
        2. Extract numerical data
        3. Calculate metrics (counts, percentages, growth)
        4. Identify trends
        5. Write to shared_state["data_analysis"]
        6. Return status and count
        """
        # TODO: Students implement in Exercise 2
        
        # Read research findings
        findings = self.shared_state.get("research_findings", [])
        
        # Placeholder analysis
        analysis = {
            "metrics": {
                "findings_count": len(findings),
                "placeholder_metric": 42
            },
            "insights": [
                "Placeholder insight 1",
                "Placeholder insight 2"
            ]
        }
        
        self.shared_state.set("data_analysis", analysis)
        
        return {
            "status": "success",
            "metrics_count": len(analysis["metrics"]),
            "message": "Data agent placeholder - students implement in Exercise 2"
        }

