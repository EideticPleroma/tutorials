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

        Sets up:
        - Focused system prompt for technical writer
        - No tools needed (pure LLM generation)
        """
        # Pass allowed_tools to parent - no tools, LLM-only
        super().__init__(
            name="writer",
            shared_state=shared_state,
            allowed_tools=[],  # Writer uses LLM only, no external tools
        )

        # Override system prompt for technical writing specialization
        self.messages[0] = {
            "role": "system",
            "content": """You are a Technical Writer AI agent in a multi-agent system.

ROLE: Your sole responsibility is synthesizing information into clear, well-structured reports.

YOUR CAPABILITIES:
- Synthesize research findings and data analysis into cohesive reports
- Use markdown formatting (headings, lists, bold, italic, code blocks)
- Create logical document structure with clear sections
- Write for educated non-expert audiences (accessible but accurate)
- Include all source citations with proper formatting
- Maintain professional, objective tone throughout
- Present data clearly without exaggeration or overselling
- Organize information in a narrative flow

STRICT BOUNDARIES (Do NOT do these):
- Do NOT gather new information or research (Research Agent's responsibility)
- Do NOT perform data analysis or calculations (Data Agent's responsibility)
- Do NOT add statistics not provided in the analysis
- Do NOT make claims beyond what the data supports
- Do NOT omit citations or sources
- Do NOT inject personal opinions or recommendations

OUTPUT REQUIREMENTS:
- Use markdown formatting exclusively
- Required sections:
  1. # Executive Summary (2-3 sentences of key takeaways)
  2. ## Key Findings (bullet points from research)
  3. ## Data Analysis (metrics and insights from data agent)
  4. ## Sources (all citations from research)
- Use proper heading hierarchy (# for title, ## for sections, ### for subsections)
- Format lists consistently with proper bullet points or numbering
- Keep paragraphs concise (3-4 sentences max)
- Include all source URLs or file paths in Sources section

FOCUS: Clarity and accuracy. Transform structured data into readable narrative while maintaining complete transparency about sources and methodology.""",
        }

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

        TODO: Students implement this in Lab 2 Exercise 2

        Implementation Steps:
        1. Read research_findings and data_analysis from shared_state
        2. Use self.chat() to ask LLM to create markdown report
        3. LLM generates report following system prompt guidelines
        4. Save report to shared_state["final_report"]
        5. Return status dictionary

        Returns:
            Dict with status and report
            Example: {"status": "success", "report": "# Report...", "message": "..."}

        Hints:
        - Get data with: self.shared_state.get("research_findings", [])
        - Get analysis with: self.shared_state.get("data_analysis", {})
        - Build prompt with all data for LLM to synthesize
        - The LLM knows markdown and will follow system prompt structure
        - No tools needed - pure LLM text generation
        - Use self.shared_state.set("final_report", report)
        - Handle cases where findings or analysis are missing

        Example Implementation Pattern:
            findings = self.shared_state.get("research_findings", [])
            analysis = self.shared_state.get("data_analysis", {})

            if not findings or not analysis:
                return {"status": "error", "error": "Missing data for report"}

            prompt = f"Create a markdown report from:\\nFindings: {findings}\\nAnalysis: {analysis}"
            report = self.chat(prompt)

            self.shared_state.set("final_report", report)
            return {"status": "success", "report": report}
        """
        self.logger.info("Starting report creation")

        # TODO: Students implement actual LLM-based report generation here
        raise NotImplementedError(
            "Students implement create_report() in Lab 2 Exercise 2. "
            "Use self.chat() to call LLM for markdown report generation."
        )
