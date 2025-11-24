# Exercise 2: Create Specialized Agents

**Duration**: ~90 minutes | **Difficulty**: Intermediate

## Objective

Build three specialized worker agents: Research Agent (gathers information), Data Agent (analyzes trends), and Writer Agent (creates reports).

## Context

In Exercise 1, you built a coordinator that delegates to mock agents. Now you'll create real specialized agents with:
- **Inheritance from Tutorial 1's Agent class** (gets LLM and tool calling automatically)
- **Tool filtering** (each agent only has access to specific tools via `allowed_tools`)
- **Focused system prompts** (defines agent persona and boundaries)
- **Clear responsibilities** (one job per agent)

**The three agents:**
1. **Research Agent**: Gathers information using search_files and read_file tools
2. **Data Agent**: Analyzes data using calculate tool
3. **Writer Agent**: Creates formatted reports using LLM only (no tools)

**Key Concept:** `WorkerAgent` inherits from Tutorial 1's `Agent` class, so you get `self.chat()` method and tool calling for free. You just filter which tools each specialist can use.

## Prerequisites

- [ ] Completed Exercise 1 (Coordinator)
- [ ] Read [Agent Specialization](../../tutorial-2/concepts/agent-specialization.md)
- [ ] Review agent scaffolds in `src/multi_agent/specialized/`

## Part 1: Research Agent

### Code Scaffold

Open `src/multi_agent/specialized/research_agent.py`:

```python
"""
Research Agent - Specialized in information gathering.

Responsibilities:
- Search for information
- Extract key facts
- Cite sources
- Flag data quality

Does NOT analyze or interpret data (that's Data Agent's job).
"""

from typing import List, Dict
from ..worker_base import WorkerAgent
from ..shared_state import SharedState

class ResearchAgent(WorkerAgent):
    """Agent specialized in gathering information from sources."""
    
    def __init__(self, shared_state: SharedState):
        """
        Initialize research agent.
        
        Inherits from WorkerAgent which inherits from Agent:
        - Gets self.chat() method from Tutorial 1's Agent
        - Gets tool calling capabilities automatically
        - Tools filtered to allowed_tools only
        
        TODO:
        - Call parent __init__ with name, shared_state, and allowed_tools
        - Override self.messages[0] to set specialized system prompt
        """
        # Pass allowed_tools to parent - only research tools
        super().__init__(
            name="research",
            shared_state=shared_state,
            allowed_tools=["search_files", "read_file"]  # TODO: Verify these tools exist
        )
        
        # TODO: Override system prompt for research specialization
        # self.messages[0] = {"role": "system", "content": "..."}
    
    def gather_info(self, query: str, max_sources: int = 5) -> Dict:
        """
        Gather information using inherited LLM and tools.
        
        Args:
            query: Research topic/question
            max_sources: Maximum number of sources to gather
        
        Returns:
            Dict with status, findings, and sources
        
        TODO: Implement research workflow:
        1. Build prompt for LLM with research task
        2. Call self.chat(prompt) - LLM will use file_search/read_file tools
        3. Parse LLM response to extract structured findings
        4. Write findings to shared_state["research_findings"]
        5. Return status dictionary
        
        Example pattern:
            prompt = f"Research the following topic: {query}. Find facts and cite sources."
            response = self.chat(prompt)  # LLM uses tools automatically
            findings = parse_response(response)
            self.shared_state.set("research_findings", findings)
            return {"status": "success", "findings_count": len(findings)}
        """
        raise NotImplementedError("Students implement in this exercise")
```

### Tasks

**Task 1: Design System Prompt**

Create a focused system prompt for research specialist.

**AI Assistant Prompt:**
```
@.cursorrules @src/agent/simple_agent.py @src/multi_agent/specialized/research_agent.py

I need to override the system prompt for ResearchAgent that inherits from WorkerAgent (which inherits from Tutorial 1's Agent).

The agent should specialize in:
- Gathering information using search_files and read_file tools
- Extracting specific facts and data points
- Citing all sources with file paths
- Focus on breadth and accuracy

The agent should NOT:
- Analyze data (that's Data Agent's job)
- Write reports (that's Writer Agent's job)
- Calculate metrics

Generate a focused system prompt that I'll set by overriding self.messages[0].
```

**Task 2: Implement gather_info() using inherited self.chat()**

Implement the information gathering workflow using the inherited LLM.

**Requirements:**
- Build a prompt for the LLM explaining the research task
- Call self.chat(prompt) - the LLM will automatically use search_files/read_file tools
- Parse the LLM response to extract structured findings
- Each finding should have "fact" and "source" keys
- Write to shared_state under "research_findings"
- Return summary

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/specialized/research_agent.py

Implement ResearchAgent.gather_info() that:
1. Uses search_files and read_file tools to find information on query
2. Extracts key facts from file contents
3. Creates findings list: [{"fact": "...", "source": "file_path"}]
4. Writes to shared_state.set("research_findings", findings)
5. Returns {"status": "success", "findings_count": len(findings)}

Generate the implementation.
```

**Validation:**
```python
research = ResearchAgent(shared_state)
result = research.gather_info("electric vehicles")

assert result["status"] == "success"
assert shared_state.get("research_findings") is not None
assert len(shared_state.get("research_findings")) >= 3
```

---

## Part 2: Data Agent

### Code Scaffold

Open `src/multi_agent/specialized/data_agent.py`:

```python
"""
Data Agent - Specialized in quantitative analysis.

Responsibilities:
- Analyze numerical data
- Calculate trends and metrics
- Identify patterns
- Present statistical insights

Does NOT gather data (Research Agent) or write reports (Writer Agent).
"""

from typing import Dict
from ..worker_base import WorkerAgent
from ..shared_state import SharedState

class DataAgent(WorkerAgent):
    """Agent specialized in data analysis and metrics calculation."""
    
    def __init__(self, shared_state: SharedState):
        """
        Initialize data agent.
        
        TODO:
        - Call parent __init__ with name="data"
        - Set focused system prompt
        - Register analysis tools (calculate, analyze_trend)
        """
        super().__init__(name="data", shared_state=shared_state)
        # TODO: Set system_prompt
        # TODO: Register tools
    
    def analyze_trends(self) -> Dict:
        """
        Analyze research findings for trends and metrics.
        
        Returns:
            Dict with status and analysis results
        
        TODO: Implement analysis workflow:
        1. Read research_findings from shared state
        2. Extract numerical data
        3. Calculate metrics (growth rates, averages, etc.)
        4. Identify trends
        5. Write analysis to shared state
        6. Return status and summary
        """
        pass
```

### Tasks

**Task 1: System Prompt**

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/specialized/data_agent.py

Generate a system prompt for a Data Agent specializing in quantitative analysis.

The agent should:
- Analyze numerical data and statistics
- Calculate growth rates, percentages, trends
- Provide quantitative insights
- Show calculations for transparency

The agent should NOT:
- Gather information (that's Research Agent)
- Make qualitative judgments
- Write prose reports (that's Writer Agent)

Generate focused system prompt.
```

**Task 2: Implement analyze_trends()**

**Requirements:**
- Read "research_findings" from shared_state
- Extract numbers from findings
- Calculate metrics (counts, percentages, growth)
- Write to shared_state under "data_analysis"

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/specialized/data_agent.py

Implement DataAgent.analyze_trends() that:
1. Reads research_findings from shared_state
2. Extracts numerical data from findings
3. Calculates metrics: count, percentages, simple trends
4. Creates analysis dict: {"metrics": {...}, "insights": [...]}
5. Writes to shared_state.set("data_analysis", analysis)
6. Returns {"status": "success", "metrics_count": X}

Generate implementation.
```

---

## Part 3: Writer Agent

> **Implementation Note**: The WriterAgent implementation uses direct markdown generation rather than LLM-based generation. This design choice provides deterministic output that's easier to test and validate. In production, you might use LLM generation for more sophisticated report formatting, but the direct approach is ideal for learning multi-agent patterns without LLM variability.

### Code Scaffold

Open `src/multi_agent/specialized/writer_agent.py`:

```python
"""
Writer Agent - Specialized in report generation.

Responsibilities:
- Synthesize research and analysis into reports
- Format content (markdown, headings, lists)
- Create clear narrative structure
- Include all citations

Does NOT gather data or analyze (uses outputs from other agents).
"""

from typing import Dict
from ..worker_base import WorkerAgent
from ..shared_state import SharedState

class WriterAgent(WorkerAgent):
    """Agent specialized in creating formatted reports."""
    
    def __init__(self, shared_state: SharedState):
        """
        Initialize writer agent.
        
        Note: WriterAgent uses no tools (LLM-only for pure synthesis).
        In this implementation, we use direct markdown generation
        for deterministic testing rather than LLM generation.
        """
        super().__init__(
            name="writer",
            shared_state=shared_state,
            allowed_tools=[]  # No tools - synthesis only
        )
        
        # System prompt for writer specialization
        # (Not actively used in direct generation, but documents the role)
        self.messages[0] = {
            "role": "system",
            "content": """You are a Writer Agent specialized in report creation.
            
Your job: Synthesize information into clear, structured reports.

How to work:
1. Read research_findings and data_analysis from shared state
2. Create logical structure (Summary → Findings → Analysis → Sources)
3. Use markdown formatting (headings, lists, emphasis)
4. Include all source citations
5. Maintain objectivity

What you DO NOT do:
- NO information gathering (Research Agent does this)
- NO data analysis (Data Agent does this)
- ONLY synthesize existing information"""
        }
    
    def execute(self, action: str, payload: Dict) -> Dict:
        """Route actions to appropriate methods."""
        if action == "create_report":
            return self.create_report()
        else:
            return {"status": "error", "error": f"Unknown action: {action}"}
    
    def create_report(self) -> Dict:
        """
        Create formatted markdown report from research and analysis.
        
        Implementation: Uses direct markdown generation for deterministic output.
        Production alternative: Could use self.chat() for LLM-generated prose.
        
        Returns:
            Dict with status and report
            Example: {"status": "success", "report": "# Report...", "message": "..."}
        """
        # Implementation details in actual file...
        # Pattern: Read from shared_state, format as markdown, write result
        pass
```

### Understanding the Implementation

The WriterAgent is already implemented. Let's understand how it works:

**Key Design Decisions:**

1. **No Tools**: WriterAgent has `allowed_tools=[]` because it only synthesizes existing information
2. **Direct Generation**: Uses Python string formatting instead of LLM for deterministic output
3. **Structured Format**: Always produces consistent markdown structure
4. **Shared State**: Reads from "research_findings" and "data_analysis", writes to "final_report"

**Review the Implementation:**

Open `src/multi_agent/specialized/writer_agent.py` and trace through `create_report()`:

```python
def create_report(self) -> Dict:
    # Step 1: Read inputs from shared state
    research_findings = self.shared_state.get("research_findings")
    data_analysis = self.shared_state.get("data_analysis")
    
    # Step 2: Validate inputs exist
    if not research_findings or not data_analysis:
        return {"status": "error", "error": "Missing inputs"}
    
    # Step 3: Build markdown sections
    # - Title from query
    # - Executive Summary with counts
    # - Key Findings (enumerate research findings)
    # - Data Analysis (metrics and insights)
    # - Sources (unique sources from findings)
    
    # Step 4: Write to shared state
    self.shared_state.set("final_report", report)
    
    # Step 5: Return success with report
    return {"status": "success", "report": report, "message": "..."}
```

**Why Direct Generation vs LLM?**

| Approach | Pros | Cons | When to Use |
|----------|------|------|-------------|
| **Direct Generation** (current) | Deterministic, fast, no LLM errors, easy to test | Less flexible formatting, no creative prose | Learning, testing, consistent structure |
| **LLM Generation** (alternative) | Natural prose, adaptive formatting, can summarize | Non-deterministic, slower, may hallucinate | Production with quality checks |

**For Tutorial 2**, direct generation is ideal because:
- Tests can validate exact structure
- No variability from LLM temperature
- Students focus on multi-agent patterns, not report formatting
- Faster execution in workflows

---

## Integration Testing

### Test All Three Agents Together

```python
from src.multi_agent import SharedState
from src.multi_agent.specialized import ResearchAgent, DataAgent, WriterAgent

# Setup
shared_state = SharedState()

# Step 1: Research
research = ResearchAgent(shared_state)
r_result = research.gather_info("electric vehicles")
print(f"Research: {r_result['status']}, {r_result['findings_count']} findings")

# Step 2: Data Analysis
data = DataAgent(shared_state)
d_result = data.analyze_trends()
print(f"Data: {d_result['status']}, {d_result['metrics_count']} metrics")

# Step 3: Writing
writer = WriterAgent(shared_state)
w_result = writer.create_report()
print(f"Writer: {w_result['status']}")
print("\nReport Preview:")
print(w_result['report'][:500])
```

### Run Tests

```bash
python -m pytest tests/multi_agent/test_specialized_agents.py -v
```

## Checkpoint Questions

**Verify Your Understanding:**

- [ ] Does each agent have a focused system prompt? *(Yes - check each __init__)*
- [ ] Does each agent use only its assigned tools? *(Yes - Research: 2, Data: 1, Writer: 0)*
- [ ] Does research agent write findings to shared state? *(Yes - under "research_findings")*
- [ ] Does data agent read research, write analysis? *(Yes - reads "research_findings", writes "data_analysis")*
- [ ] Does writer agent read both, create report? *(Yes - reads both, writes "final_report")*
- [ ] Do agents stay within their specialization boundaries? *(Test this with evaluation tests)*

**Test Results:**

Run the specialized agent tests:
```bash
python -m pytest tests/multi_agent/test_specialized_agents.py -v
```

Expected: **9/9 tests passing**
- 3 initialization tests (one per agent)
- 3 tool filtering tests (correct tool counts)
- 3 execution tests (gather_info, analyze_trends, create_report)

## Common Issues

**Issue: "Agent doing multiple jobs"**
- Review system prompt - make boundaries explicit
- Use "DO" and "DO NOT" sections
- Test with questions that would trigger overstepping

**Issue: "Agent can't find data in shared state"**
- Check key names match exactly
- Ensure previous agent completed successfully
- Use `shared_state.get(key, default)` to avoid KeyError

**Issue: "Tests pass but quality is poor"**
- This is normal for mocked LLMs
- Add evaluation tests with real LLM for quality
- Focus validation tests on structure, not content quality

See [Troubleshooting - Specialization Errors](../troubleshooting.md#specialization-errors).

## Next Steps

Once all three agents work:

👉 **Continue to [Exercise 3: Implement Agent Communication](./03-agent-communication.md)**

You'll formalize the message protocol and integrate it with your coordinator and agents.

---

## 💡 Design Tips

**Specialization:**
- One clear job per agent
- Explicit boundaries in prompt
- Limited tool set matches job

**State Management:**
- Write with descriptive keys
- Read with defaults
- Check data exists before processing

**Testing:**
- Test each agent independently first
- Then test sequential flow
- Finally test with coordinator

**Tool Assignment:**
- Research: search_files, read_file
- Data: calculate
- Writer: (no tools, LLM-only)
- Keep tools separated!

