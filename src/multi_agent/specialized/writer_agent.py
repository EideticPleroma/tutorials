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
        
        Sets up:
        - Focused system prompt for technical writer
        - Writing tools (format_markdown)
        """
        super().__init__(name="writer", shared_state=shared_state)
        
        # TODO: Students set this in Exercise 2
        self.system_prompt = """
        You are a Technical Writer specializing in analytical reports.
        
        Your job: Create clear, well-structured documents.
        
        YOU DO:
        - Synthesize information into reports
        - Format with markdown (headings, lists, emphasis)
        - Create logical document structure
        - Include all citations from research
        - Write for educated non-experts
        - Maintain objectivity (present data, don't oversell)
        
        YOU DO NOT:
        - Gather new information (use provided research)
        - Analyze data (use provided analysis)
        - Calculate metrics (use provided calculations)
        
        Structure: Executive Summary → Key Findings → Analysis → Sources
        """
        
        # TODO: Students register writing tools in Exercise 2
        # self.tools = {"format_markdown": ...}
    
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
            return {
                "status": "error",
                "error": f"Unknown action: {action}"
            }
    
    def create_report(self) -> Dict:
        """
        Create formatted report from research and analysis.
        
        Returns:
            Dict with status and report
        
        Students implement this in Exercise 2.
        Should:
        1. Read research_findings and data_analysis from shared_state
        2. Create markdown report with structure
        3. Include sections: Summary, Findings, Analysis, Sources
        4. Format with proper markdown
        5. Write to shared_state["final_report"]
        6. Return status and report preview
        """
        # TODO: Students implement in Exercise 2
        
        # Read inputs
        findings = self.shared_state.get("research_findings", [])
        analysis = self.shared_state.get("data_analysis", {})
        
        # Placeholder report
        report = """# Research Report

## Executive Summary

This is a placeholder report. Students will implement proper report 
generation in Exercise 2.

## Key Findings

- Finding 1 from research
- Finding 2 from research
- Finding 3 from research

## Data Analysis

Analysis metrics and insights will be included here.

## Sources

Research sources will be cited here.
"""
        
        self.shared_state.set("final_report", report)
        
        return {
            "status": "success",
            "report": report,
            "message": "Writer agent placeholder - students implement in Exercise 2"
        }

