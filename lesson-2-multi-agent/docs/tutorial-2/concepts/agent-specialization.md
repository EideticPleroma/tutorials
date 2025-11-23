# Agent Specialization

**Page 2 of 9** | [← Previous: Multi-Agent Architecture](./multi-agent-architecture.md) | [Next: Agent Communication →](./agent-communication.md) | [↑ Reading Guide](../READING_GUIDE.md)

In Tutorial 1, you built a single "generalist" agent that could handle many types of tasks. In multi-agent systems, we create "specialist" agents that excel at specific domains. This is the key to making multi-agent systems more effective than a single powerful agent.

## The Specialist vs. Generalist Trade-off

### Generalist Agent (Tutorial 1)

```python
system_prompt = """
You are a helpful assistant.
You can search files, read files, do calculations, search the web, and answer questions.
Use the appropriate tool for each task.
"""
```

**Characteristics:**
- ✅ Flexible: Handles many task types
- ✅ Simple: One agent to manage
- ❌ Jack of all trades, master of none
- ❌ Context dilution: Prompt tries to cover everything
- ❌ Tool confusion: Might choose wrong tool for edge cases

### Specialist Agent

```python
research_agent_prompt = """
You are a Research Specialist.
Your ONLY job is to gather information from multiple sources.

CAPABILITIES:
- Search the web for current information
- Extract key facts and data points
- Cite sources with URLs
- Flag information quality (primary source vs. blog)

CONSTRAINTS:
- DO NOT analyze data (that's the Data Agent's job)
- DO NOT write reports (that's the Writer Agent's job)
- Focus on breadth and accuracy of information gathering
"""
```

**Characteristics:**
- ✅ Expert: Optimized for one task type
- ✅ Focused: Clear boundaries and constraints
- ✅ Better tool selection: Fewer options = fewer mistakes
- ❌ Inflexible: Can't handle other tasks
- ❌ Requires coordination: Needs other agents to complete work

## Designing Focused Agents

### The Three Pillars of Specialization

1. **Focused System Prompt** - Defines persona and boundaries
2. **Limited Tool Set** - Only tools relevant to specialty
3. **Domain-Specific Examples** - Few-shot prompts for common scenarios

### Example: Research, Data, Writer Agents

Let's design a three-agent team for generating analytical reports.

#### 1. Research Agent

**Purpose:** Gather raw information from various sources

**System Prompt:**
```text
You are a Research Specialist focused on information gathering.

MISSION: Find relevant, accurate information on the given topic.

TOOLS AVAILABLE:
- web_search: Search for current information
- read_file: Access local documents
- list_files: Discover available data sources

APPROACH:
1. Understand the research question
2. Identify 3-5 key sources
3. Extract specific facts, statistics, quotes
4. Return structured findings with citations

IMPORTANT:
- Always cite sources with URLs or file paths
- Flag the date/recency of information
- Note conflicting information from different sources
- DO NOT interpret or analyze - just gather facts
```

**Tool Set:**
- `web_search(query: str)`
- `read_file(path: str)`
- `list_files(directory: str, pattern: str)`

**Example Output:**
```
Research Findings on Electric Vehicle Market:

1. Global EV sales reached 10.5M units in 2022 (+55% YoY)
   Source: IEA Global EV Outlook 2023 (iea.org/reports/...)
   Date: May 2023

2. Tesla holds 65% US market share, down from 71% in 2021
   Source: Cox Automotive Q4 2022 Report
   Date: January 2023

3. Average EV price premium over ICE vehicles: $7,200
   Source: Kelley Blue Book Market Analysis
   Date: March 2023

Note: Sources 1 and 3 are primary data; Source 2 is industry analysis.
```

#### 2. Data Agent

**Purpose:** Analyze data, calculate trends, find patterns

**System Prompt:**
```text
You are a Data Analyst specializing in quantitative analysis.

MISSION: Transform raw data into insights and trends.

TOOLS AVAILABLE:
- calculate: Perform mathematical operations
- analyze_trend: Calculate growth rates, averages, correlations
- create_chart_data: Structure data for visualization

APPROACH:
1. Receive data from Research Agent (via Coordinator)
2. Identify key metrics and trends
3. Perform calculations (growth rates, percentages, etc.)
4. Highlight significant patterns or anomalies
5. Return structured analysis with numbers

IMPORTANT:
- Focus on quantitative insights, not qualitative interpretation
- Show your calculations (transparency)
- Flag data quality issues or missing information
- DO NOT make recommendations - just present analysis
```

**Tool Set:**
- `calculate(expression: str)`
- `analyze_trend(data: list, metric: str)`
- `compare_values(a: float, b: float, context: str)`

**Example Output:**
```
Data Analysis:

MARKET GROWTH:
- 2022 sales: 10.5M units
- YoY growth: +55%
- 3-year CAGR (2020-2022): 67%

MARKET SHARE SHIFT:
- Tesla 2021: 71% → 2022: 65% (-6 percentage points)
- Indicates growing competition (new entrants capturing 6% share)

PRICING:
- Price premium: $7,200 (18% above ICE average of $40,000)
- Premium declining: Was $10,000 in 2021 (-28% YoY)

KEY INSIGHT: Market growing rapidly (+55%) while prices converge with ICE.
```

#### 3. Writer Agent

**Purpose:** Synthesize information into polished reports

**System Prompt:**
```text
You are a Technical Writer specializing in analytical reports.

MISSION: Create clear, well-structured documents from research and analysis.

TOOLS AVAILABLE:
- format_markdown: Structure content with headings, lists, tables
- check_grammar: Ensure professional writing
- cite_source: Format citations consistently

APPROACH:
1. Receive research findings and data analysis (via Coordinator)
2. Create logical document structure
3. Write clear narrative connecting data points
4. Format for readability (headings, bullets, emphasis)
5. Include all citations from research

IMPORTANT:
- Write for educated non-experts (explain jargon)
- Use active voice and clear language
- Structure: Executive Summary → Findings → Analysis → Conclusion
- Maintain objectivity - present data, don't oversell
```

**Tool Set:**
- `format_markdown(text: str)`
- `create_table(data: dict)`
- `format_citation(source: str, style: str)`

**Example Output:**
```markdown
# Electric Vehicle Market Analysis Report

## Executive Summary

The global electric vehicle market demonstrated exceptional growth in 2022,
with sales reaching 10.5 million units—a 55% increase year-over-year. While
Tesla remains the dominant player in the US market, its share declined from
71% to 65%, signaling increased competition. Simultaneously, EV prices are
converging with traditional vehicles, dropping from a $10,000 premium to
$7,200.

## Market Growth Trends

[... formatted synthesis of research and data ...]

## Sources

1. International Energy Agency (2023). Global EV Outlook 2023.
2. Cox Automotive (2023). Q4 2022 Market Report.
3. Kelley Blue Book (2023). EV Pricing Analysis.
```

## Tool Assignment Strategies

### Strategy 1: Exclusive Tools (Simplest)

Each agent gets completely different tools:
- Research: `web_search`, `read_file`
- Data: `calculate`, `analyze_trend`
- Writer: `format_markdown`, `create_table`

**Pros:** Clear boundaries, no confusion
**Cons:** Inflexible if agent needs to cross boundaries

### Strategy 2: Shared Core Tools

Common tools available to all, plus specializations:
- All: `read_file`, `write_file`
- Research: `web_search`, `list_files`
- Data: `calculate`, `analyze_trend`
- Writer: `format_markdown`, `check_grammar`

**Pros:** Agents can access reference data
**Cons:** Risk of agents overstepping roles

### Strategy 3: Hierarchical Access

Tools organized by complexity:
- Level 1 (All): Basic I/O
- Level 2 (Research/Data): Analysis tools
- Level 3 (Data only): Advanced calculations

**Pros:** Gradual capability increase
**Cons:** Complex to implement

**For Tutorial 2:** We use Strategy 1 (Exclusive Tools) for clarity.

## Prompt Engineering for Specialized Behavior

### The Specialization Prompt Template

```text
You are a [ROLE] specializing in [DOMAIN].

MISSION: [ONE SENTENCE - What is your primary goal?]

TOOLS AVAILABLE:
- [tool_name]: [when to use it]
- [tool_name]: [when to use it]

APPROACH:
1. [Step 1]
2. [Step 2]
3. [Step 3]

IMPORTANT CONSTRAINTS:
- DO [expected behavior]
- DO NOT [out-of-scope behavior]
- FOCUS ON [core competency]

BOUNDARIES:
- You are NOT responsible for [other agent's job]
- Pass results to Coordinator, who will handle [next step]
```

### Key Elements:

1. **Identity:** "You are a Research Specialist" (not just "You are helpful")
2. **Mission:** One clear goal, not multiple objectives
3. **Explicit Constraints:** What NOT to do is as important as what to do
4. **Boundaries:** Acknowledge other agents' roles

## Common Specialization Anti-Patterns

### ❌ Anti-Pattern 1: The Overstepping Agent

```python
# BAD: Research agent doing analysis
research_prompt = """
You are a Research Specialist.
Find information and analyze trends.  # ← Should be two agents!
"""
```

**Problem:** Agent tries to do multiple jobs, loses focus
**Fix:** Split into Research + Data agents

### ❌ Anti-Pattern 2: The Vague Specialist

```python
# BAD: Unclear boundaries
data_prompt = """
You are a Data Analyst.
Help with data tasks.  # ← What tasks? How?
"""
```

**Problem:** No clear guidance, agent guesses at role
**Fix:** Explicit mission, approach, and constraints

### ❌ Anti-Pattern 3: The Under-Equipped Specialist

```python
# BAD: Agent lacks necessary tools
writer_prompt = """
You are a Writer. Create formatted reports.
"""
# But no format_markdown or create_table tools!
```

**Problem:** Agent can't fulfill role without tools
**Fix:** Tool set must match agent's mission

### ❌ Anti-Pattern 4: The Isolated Agent

```python
# BAD: No awareness of workflow
data_prompt = """
You are a Data Analyst. Analyze data.
# No mention of where data comes from or where results go
"""
```

**Problem:** Agent doesn't understand its place in the system
**Fix:** Mention coordinator, inputs, and outputs

---

## 🎯 Hands-On Exercise: Tool Set Mapping

For each task, map which agent(s) should have which tools:

**Task:** Generate a weekly sales report with charts

**Agents:** Research, Data, Writer

**Available Tools:**
- `query_database(sql: str)` - Get sales data
- `calculate(expression: str)` - Math operations
- `create_chart(data: dict, type: str)` - Generate visualizations
- `format_markdown(text: str)` - Format document
- `send_email(to: str, content: str)` - Distribute report

**Your Task:** Assign tools to agents. Think about:
1. Which tools does each agent need for its core function?
2. Should any tools be shared?
3. Are any agents over/under-equipped?

<details>
<summary>Show Recommended Assignment</summary>

**Research Agent:**
- `query_database(sql: str)` ✅
- Purpose: Gather raw sales data from database

**Data Agent:**
- `calculate(expression: str)` ✅
- `create_chart(data: dict, type: str)` ✅
- Purpose: Analyze sales trends and prepare visualizations

**Writer Agent:**
- `format_markdown(text: str)` ✅
- `send_email(to: str, content: str)` ✅
- Purpose: Format report and distribute

**Reasoning:**
- Clean separation: Each agent has tools for its domain
- No overlap: Prevents confusion about responsibilities
- Complete: Each agent can fully execute its role
- Coordinator handles data handoffs between agents

**Alternative (if tasks are tightly coupled):**
- Give all tools to a single "Report Generator" agent
- Use multi-agent only if reports become complex enough to benefit from specialization
</details>

---

**Ready?** If you understand how to design specialized agents, you're ready for [Agent Communication](./agent-communication.md) to learn how agents exchange information.

**Page 2 of 9** | [← Previous: Multi-Agent Architecture](./multi-agent-architecture.md) | [Next: Agent Communication →](./agent-communication.md) | [↑ Reading Guide](../READING_GUIDE.md)

