# Exercise 0: Bridge - From Single Agent to Multi-Agent

| Duration | Difficulty | Prerequisites | Skills Practiced |
|----------|------------|---------------|------------------|
| ~45 min | Beginner | Tutorial 1 complete | Responsibility splitting, Agent collaboration basics |

## Objective

Refactor your Tutorial 1 single agent into a simple two-agent system without adding complexity. This bridges the gap between single-agent thinking and multi-agent architecture.

## Context

In Tutorial 1, your agent did everything: search files, read content, and summarize findings. That works fine for simple tasks, but imagine an agent with 15+ tools - it gets confused about which tool to use when.

**The core insight**: Instead of one agent doing everything, split responsibilities.

```
Tutorial 1 (Single Agent):
User: "Find Python files and summarize them"
  ↓
Agent (does everything)
  - Searches files
  - Reads content  
  - Summarizes findings
  ↓
Response

Tutorial 2 Bridge (Two Agents):
User: "Find Python files and summarize them"
  ↓
Gatherer Agent (search + read)
  - Searches files
  - Reads content
  ↓
Reporter Agent (summarize)
  - Creates summary from gathered data
  ↓
Response
```

**Why this matters**: This exercise teaches the fundamental pattern of multi-agent systems - separation of concerns - without the complexity of coordinators, message protocols, or shared state. You'll add those in Exercises 1A and 1B.

## Prerequisites

- [ ] Completed Tutorial 1 (single agent works)
- [ ] Understand the `Agent` class in `src/agent/simple_agent.py`
- [ ] Comfortable with tool registration pattern

## What You'll Build

Two simple agent classes that work together:

1. **GathererAgent**: Uses `search_files` and `read_file` tools to collect information
2. **ReporterAgent**: Takes gathered data and creates a summary (LLM only, no tools)

No message protocol yet - just simple function calls between agents.

## Tasks

### Task 1: Create the Gatherer Agent

Create a new file `src/multi_agent/bridge/gatherer_agent.py`.

**Requirements:**
- Inherit from Tutorial 1's `Agent` class (gets LLM and tool calling)
- Limit tools to just `search_files` and `read_file`
- Add a focused system prompt for gathering information

**AI Assistant Prompt:**
```
@.cursorrules @src/agent/simple_agent.py

I'm working on Exercise 0 (Bridge) in Tutorial 2.

I need to create a GathererAgent that:
1. Inherits from the Agent class in simple_agent.py
2. Only has access to search_files and read_file tools
3. Has a system prompt focused on finding and collecting information
4. Has a gather(query: str) method that returns collected information

The agent should NOT summarize or analyze - just gather.

Generate a simple implementation without message protocols (we'll add those later).
```

**Scaffold:**
```python
"""
Gatherer Agent - Collects information using file tools.

This is a bridge exercise showing how to split responsibilities
before introducing coordinators and message protocols.
"""

from typing import List, Optional
from src.agent.simple_agent import Agent

class GathererAgent(Agent):
    """Agent specialized in gathering information from files."""
    
    def __init__(self):
        """Initialize gatherer with limited tools."""
        super().__init__()
        
        # Override system prompt for gathering focus
        self.messages[0] = {
            "role": "system",
            "content": """You are a Gatherer Agent. Your ONLY job is to find and collect information.

What you DO:
- Search for files matching patterns
- Read file contents
- Extract relevant facts
- Report what you found with sources

What you DO NOT do:
- Summarize or analyze (Reporter Agent does that)
- Make recommendations
- Draw conclusions

Always cite which file each piece of information came from."""
        }
        
        # TODO: Filter tools to only allowed ones
        # Hint: self.tools contains all registered tools
        # You need to filter to just ["search_files", "read_file"]
    
    def gather(self, query: str) -> dict:
        """
        Gather information about a query.
        
        Args:
            query: What to search for
            
        Returns:
            Dict with status and gathered information
            Example: {"status": "success", "findings": [...], "sources": [...]}
        """
        # TODO: Implement gathering logic
        # 1. Build a prompt asking the LLM to search and read files
        # 2. Call self.chat(prompt) - LLM will use tools automatically
        # 3. Parse response to extract findings
        # 4. Return structured dict
        pass
```

**Validation:**
```python
from src.multi_agent.bridge.gatherer_agent import GathererAgent

gatherer = GathererAgent()

# Check tool filtering works
assert "search_files" in [t["function"]["name"] for t in gatherer.tools]
assert "read_file" in [t["function"]["name"] for t in gatherer.tools]
assert len(gatherer.tools) == 2  # Only these two tools

# Check gathering works
result = gatherer.gather("Python files in src/")
assert result["status"] == "success"
assert len(result["findings"]) > 0
```

### Task 2: Create the Reporter Agent

Create `src/multi_agent/bridge/reporter_agent.py`.

**Requirements:**
- Inherit from `Agent` class
- No tools (LLM-only for pure synthesis)
- System prompt focused on summarization
- Takes gathered data as input, produces summary

**AI Assistant Prompt:**
```
@.cursorrules @src/agent/simple_agent.py

I'm working on Exercise 0 (Bridge) in Tutorial 2.

I need to create a ReporterAgent that:
1. Inherits from the Agent class
2. Has NO tools (empty tools list) - LLM only
3. Has a system prompt focused on creating clear summaries
4. Has a report(gathered_data: dict) method that returns a summary string

The agent receives data from GathererAgent and creates a readable summary.

Generate a simple implementation.
```

**Scaffold:**
```python
"""
Reporter Agent - Summarizes gathered information.

This is a bridge exercise showing agent collaboration
before introducing message protocols.
"""

from src.agent.simple_agent import Agent

class ReporterAgent(Agent):
    """Agent specialized in creating summaries from gathered data."""
    
    def __init__(self):
        """Initialize reporter with no tools (LLM only)."""
        super().__init__()
        
        # Override system prompt for reporting focus
        self.messages[0] = {
            "role": "system",
            "content": """You are a Reporter Agent. Your ONLY job is to summarize information.

What you DO:
- Create clear, organized summaries
- Highlight key findings
- Include source citations
- Structure information logically

What you DO NOT do:
- Search for information (Gatherer Agent does that)
- Make things up - only summarize what you're given
- Add speculation or analysis beyond the data

Be concise and factual."""
        }
        
        # No tools - LLM only
        self.tools = []
    
    def report(self, gathered_data: dict) -> str:
        """
        Create a summary from gathered information.
        
        Args:
            gathered_data: Dict from GathererAgent with findings and sources
            
        Returns:
            Formatted summary string
        """
        # TODO: Implement reporting logic
        # 1. Build a prompt with the gathered data
        # 2. Ask LLM to create a summary
        # 3. Return the summary
        pass
```

**Validation:**
```python
from src.multi_agent.bridge.reporter_agent import ReporterAgent

reporter = ReporterAgent()

# Check no tools
assert len(reporter.tools) == 0

# Check reporting works
test_data = {
    "status": "success",
    "findings": ["Found 3 Python files", "Main file is simple_agent.py"],
    "sources": ["src/agent/"]
}
summary = reporter.report(test_data)
assert len(summary) > 0
assert "Python" in summary or "files" in summary
```

### Task 3: Wire Them Together

Create a simple runner that chains the two agents.

**File:** `src/multi_agent/bridge/two_agent_runner.py`

```python
"""
Two-Agent Runner - Chains Gatherer and Reporter.

This shows the simplest form of multi-agent collaboration:
one agent's output becomes another's input.
"""

from .gatherer_agent import GathererAgent
from .reporter_agent import ReporterAgent

def run_two_agent_workflow(query: str) -> str:
    """
    Execute a two-agent workflow: gather then report.
    
    Args:
        query: What to research
        
    Returns:
        Final summary from reporter
    """
    # Step 1: Gather information
    gatherer = GathererAgent()
    gathered = gatherer.gather(query)
    
    if gathered["status"] != "success":
        return f"Gathering failed: {gathered.get('error', 'Unknown error')}"
    
    # Step 2: Create report
    reporter = ReporterAgent()
    summary = reporter.report(gathered)
    
    return summary

# Quick test
if __name__ == "__main__":
    result = run_two_agent_workflow("Find Python files in src/agent/")
    print(result)
```

**Validation:**
```bash
python -c "from src.multi_agent.bridge.two_agent_runner import run_two_agent_workflow; print(run_two_agent_workflow('Python files in src/'))"
```

Expected: A summary of Python files found in the src directory.

### Task 4: Reflect on the Pattern

Before moving to Exercise 1A, answer these questions:

**Understanding Check:**
1. What's the main benefit of splitting into two agents?
2. What problems might arise as you add more agents?
3. How would you handle errors between agents?
4. What if the Reporter needs to ask the Gatherer for more information?

<details>
<summary>Show Answers</summary>

1. **Benefit**: Each agent has a clear job and limited tools. The Gatherer is focused on finding, the Reporter on summarizing. Neither gets confused by irrelevant capabilities.

2. **Problems with more agents**:
   - How do they communicate? (Direct function calls don't scale)
   - How do you track what's happening? (No logging/tracing)
   - How do you handle failures? (No retry logic)
   - How do you share data? (Passing dicts around gets messy)

3. **Error handling**: Currently primitive - just check `status`. Real systems need:
   - Retry logic
   - Error propagation
   - Clear error messages
   - Recovery strategies

4. **Back-and-forth communication**: Can't do it easily with direct function calls. Need:
   - A message protocol (Exercise 1B)
   - A coordinator to manage flow (Exercise 1A)
   - Possibly shared state (Exercise 2)

</details>

## Checkpoint Questions

Before moving to Exercise 1A, verify:

- [ ] Two agents created with different responsibilities?
- [ ] Gatherer only has `search_files` and `read_file` tools?
- [ ] Reporter has no tools (LLM only)?
- [ ] Two-agent workflow produces a summary?
- [ ] You understand why direct function calls won't scale?

## What's Next

You've seen the core pattern: split responsibilities between agents. But you've also seen the limitations:

- **No structured communication** (just function calls and dicts)
- **No error handling** (what if Gatherer fails?)
- **No observability** (how do you debug this?)
- **No coordination** (what if you need 5 agents?)

Exercise 1A introduces the **Coordinator** - an agent that orchestrates others.
Exercise 1B introduces the **Message Protocol** - structured communication.

---

## Common Issues

**Issue: "Import error - can't find Agent"**
- Check you're running from project root
- Verify `src/agent/simple_agent.py` exists
- Check your Python path includes the project

**Issue: "Too many tools in Gatherer"**
- Filter `self.tools` after calling `super().__init__()`
- Only keep tools where name is in `["search_files", "read_file"]`

**Issue: "Reporter makes things up"**
- Strengthen system prompt: "ONLY summarize what's in gathered_data"
- Include the actual data in your prompt to the LLM

---

## Design Tips

**Start simple:**
- This exercise intentionally avoids message protocols
- Understand the "why" before adding complexity
- Direct function calls work for 2 agents - they don't scale to 5+

**Clear boundaries:**
- Each agent has ONE job
- System prompts define what agents DO and DON'T do
- Tool filtering enforces boundaries

**Think about failure:**
- What happens if Gatherer finds nothing?
- What if the LLM hallucinates?
- These questions motivate Exercise 1A-1B's patterns

---

**Next: [Exercise 1A: Coordinator Basics](./01a-coordinator-basics.md)** - Learn to orchestrate multiple agents with a coordinator.

