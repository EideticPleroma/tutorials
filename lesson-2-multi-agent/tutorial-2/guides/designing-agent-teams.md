# Designing Agent Teams

**Page 5 of 9** | [← Previous: State Management](../concepts/state-management.md) | [Next: Debugging Multi-Agent Systems →](./debugging-multi-agent.md) | [↑ Reading Guide](../READING_GUIDE.md)

> **🎯 Why This Matters**
>
> **Bad multi-agent design wastes weeks.** You build 5 agents, they work
> individually, but together they produce garbage.
> 
> **Common failure modes:**
> - Too many agents (over-engineered)
> - Wrong boundaries (tight coupling)
> - Unclear ownership (who does what?)
> - No error handling (first failure crashes everything)
> 
> **Good multi-agent design is systematic:**
> 1. Understand the task (30 min)
> 2. Identify natural boundaries (20 min)
> 3. Design workflow (20 min)
> 4. Specify each agent (15 min per agent)
> 5. Plan error handling (15 min)
> 
> This 2-hour investment saves 2 weeks of rewriting.
> Follow this process and you'll get it right the first time.

You understand the theory. Now the practical question: "How do I actually design a multi-agent system for MY task?" This guide walks you through a systematic process for decomposing tasks, assigning roles, and designing workflows.

## The Agent Team Design Process

### Step 1: Understand the Task

Before creating agents, deeply understand what you're building.

**Questions to Answer:**
- What is the user's goal? (Final deliverable)
- What are the inputs? (User provides what?)
- What are the outputs? (System produces what?)
- What are the constraints? (Time, resources, quality)
- What tools/data are available? (APIs, databases, files)

**Example: "Build a market research report generator"**

| Aspect              | Details                                                 |
| ------------------- | ------------------------------------------------------- |
| **Goal**            | Generate comprehensive market analysis reports          |
| **Inputs**          | Topic (e.g., "electric vehicles"), industry, region     |
| **Outputs**         | 5-10 page formatted report with data, charts, citations |
| **Constraints**     | Must complete in <5 minutes, use free data sources      |
| **Available Tools** | Web search API, CSV parser, markdown formatter          |

### Step 2: Decompose into Subtasks

Break the task into distinct stages. Look for natural boundaries.

**Decomposition Strategies:**

#### Strategy A: By Process Stage (Pipeline)

Follow the natural workflow sequence.

```
Market Research Report:
1. Gather Information (Research)
2. Analyze Data (Analysis)
3. Create Visualizations (Visualization)
4. Write Report (Writing)
5. Review and Edit (Quality Check)
```

#### Strategy B: By Data Type

Group by the kind of data being handled.

```
Investment Analysis:
1. Quantitative Data (Financial Agent)
2. Qualitative Data (Sentiment Agent)
3. Historical Context (Research Agent)
4. Synthesis (Analysis Agent)
```

#### Strategy C: By Skill/Expertise

Organize by domain knowledge required.

```
Legal Document Analysis:
1. Legal Interpretation (Legal Expert Agent)
2. Technical Accuracy (Technical Expert Agent)
3. Business Impact (Business Analyst Agent)
4. Risk Assessment (Risk Manager Agent)
```

**For our example:** We'll use Strategy A (process stages).

```mermaid
flowchart LR
    User[User Query] --> Research[1. Research<br/>Information Gathering]
    Research --> Data[2. Data Analysis<br/>Quantitative Analysis]
    Data --> Writer[3. Writing<br/>Report Generation]
    Writer --> Output[Formatted Report]
    
    style Research fill:#7ED321
    style Data fill:#F5A623
    style Writer fill:#BD10E0
```

### 🎯 Agent Team Size Decision Matrix

Before defining individual agents, decide how many you need based on task complexity:

| Task Complexity | Data Sources | Processing Steps | Recommended Agents | Example Task |
|----------------|--------------|------------------|-------------------|--------------|
| **Simple** | 1-2 | Linear (1-2 steps) | **1** Single agent | Summarize document |
| **Moderate** | 3-5 | Mixed (3-4 steps) | **3** Input → Process → Output | Blog post from research |
| **Complex** | 6-10 | Parallel + Sequential | **4-5** Specialized per domain | Market analysis report |
| **Enterprise** | 10+ | Multi-stage pipelines | **6-8** + sub-coordinators | Competitive intelligence dashboard |

**Guidelines by Agent Count:**

**1 Agent (Single):**
- ✅ Best for: Learning, prototyping, simple tasks
- ✅ Advantages: Fast to build, easy to debug
- ❌ Limitations: Can get overwhelmed, tool confusion

**2 Agents:**
- ⚠️ **Rarely optimal** - Either task is simple enough for 1, or complex enough for 3
- Only use if clear split (e.g., "Fetch" + "Process")

**3 Agents (Sweet Spot):**
- ✅ Best for: Most multi-agent needs
- Pattern: **Input Agent** → **Processing Agent** → **Output Agent**
- Example: Research → Data Analysis → Writer
- Balance of specialization without coordination overhead

**4-5 Agents:**
- ✅ Best for: Complex domains needing specialization
- Pattern: Multiple input agents + processor + output
- Example: Market Research + Competitor Analysis + Tech Analysis → Data Agent → Writer
- Coordination becomes significant (15-20% overhead)

**6-8 Agents:**
- ⚠️ Approaching complexity limit for single coordinator
- Pattern: Sub-teams with team coordinators
- Example: Research Team (3 agents) + Analysis Team (2 agents) + Reporting Team (2 agents)
- Consider hierarchical architecture (Tutorial 3)

**9+ Agents:**
- ❌ Single coordinator pattern breaks down
- Use hierarchical multi-level coordination
- See [Hierarchical vs. Peer-to-Peer](../architecture/hierarchical-vs-peer.md)

**Rule of Thumb:** 
1. Start with 3 agents (Input, Process, Output)
2. Add agents only when you hit clear bottlenecks
3. Never add agents "just in case" - measure first

### Step 3: Define Agent Roles

For each subtask, create an agent specification.

**Agent Specification Template:**

```markdown
## [Agent Name]

**Purpose:** [One sentence - what is this agent's job?]

**Inputs:** [What does it receive?]
- Input 1
- Input 2

**Outputs:** [What does it produce?]
- Output 1
- Output 2

**Tools Needed:**
- tool_name: description
- tool_name: description

**Success Criteria:** [How do we know it succeeded?]
- Criterion 1
- Criterion 2

**Failure Modes:** [What can go wrong?]
- Failure 1: mitigation
- Failure 2: mitigation
```

**Example: Research Agent Spec**

```markdown
## Research Agent

**Purpose:** Gather relevant information from web sources and documents.

**Inputs:**
- Research topic (string)
- Focus areas (list)
- Max sources (integer)

**Outputs:**
- List of findings (structured data)
- Source citations (URLs/paths)
- Confidence scores per finding

**Tools Needed:**
- web_search(query): Search the web
- read_file(path): Read local documents
- extract_data(html): Parse web pages

**Success Criteria:**
- Found at least 5 relevant sources
- Each finding has a citation
- Sources are from last 2 years (recency)

**Failure Modes:**
- No sources found: Broaden search terms, try alternative queries
- Rate limit hit: Wait and retry, use cached results
- Sources outdated: Flag as warning, use best available
```

### Step 4: Map Dependencies

Identify which agents depend on others.

```mermaid
graph TD
    A[Coordinator] --> B[Research Agent]
    A --> C[Data Agent]
    B --> C
    A --> D[Writer Agent]
    C --> D
    
    style A fill:#4A90E2
    style B fill:#7ED321
    style C fill:#F5A623
    style D fill:#BD10E0
```

**Dependency Analysis:**
- **Research** → Independent (can start immediately)
- **Data** → Depends on Research (needs findings to analyze)
- **Writer** → Depends on Research + Data (needs both for report)
- **Coordinator** → Orchestrates all

**Execution Strategy:**
- Parallel: None (each depends on previous)
- Sequential: Research → Data → Writer
- Total time: Sum of all agents

### Step 5: Design the Workflow

Create a detailed sequence of operations.

#### Workflow Example: Market Research Report

```mermaid
sequenceDiagram
    participant User
    participant Coordinator
    participant Research
    participant Data
    participant Writer
    
    User->>Coordinator: "Analyze EV market"
    
    Note over Coordinator: Parse request, set up task
    
    Coordinator->>Research: gather_info(topic="EV market")
    Note over Research: Web search, data gathering
    Research->>Coordinator: findings[5 sources, 20 data points]
    
    Note over Coordinator: Validate research output
    
    Coordinator->>Data: analyze(findings)
    Note over Data: Calculate trends, statistics
    Data->>Coordinator: analysis[growth rates, trends]
    
    Note over Coordinator: Validate analysis output
    
    Coordinator->>Writer: create_report(findings, analysis)
    Note over Writer: Format markdown, add charts
    Writer->>Coordinator: report[1500 words, formatted]
    
    Note over Coordinator: Quality check
    
    Coordinator->>User: "Here's your report: [content]"
```

### Step 6: Handle Edge Cases

Plan for what happens when things go wrong.

**Common Edge Cases:**

| Scenario         | Impact              | Mitigation                          |
| ---------------- | ------------------- | ----------------------------------- |
| Agent timeout    | Workflow stalled    | Retry with relaxed parameters       |
| Partial failure  | Incomplete results  | Use partial data, flag quality      |
| Invalid input    | Can't proceed       | Validate early, ask user to clarify |
| Tool failure     | Agent can't execute | Fallback to alternative tool        |
| Conflicting data | Inconsistent output | Flag conflicts, ask user to resolve |

**Example: Research Agent Finds No Sources**

```python
# Coordinator workflow with error handling
try:
    findings = research_agent.gather_info(topic="EV market")
    
    if len(findings) == 0:
        # Mitigation: Broaden search
        findings = research_agent.gather_info(
            topic="electric vehicles OR battery vehicles",
            max_sources=10  # Increase limit
        )
    
    if len(findings) < 3:
        # Still not enough - report to user
        return "I couldn't find enough recent information on this topic. Try a different search term?"
    
    # Proceed to analysis
    analysis = data_agent.analyze(findings)
    
except TimeoutError:
    return "Research is taking longer than expected. Try again in a moment."
```

---

## 🎯 Design Challenge

**Scenario:** Build a code review system
- Review code quality (complexity, readability)
- Check security vulnerabilities
- Run automated tests
- Generate a final review report

**Your Task:**

**Part 1:** How would you decompose this into agents?
- How many agents?
- What would each specialize in?
- What tools would each need?

<details>
<summary>Show Recommended Design</summary>

**Agent Team Design:**

1. **Quality Agent**
   - Tools: `analyze_complexity()`, `check_style()`, `measure_coverage()`
   - Focus: Code metrics and readability
   - Output: Quality score + recommendations

2. **Security Agent**
   - Tools: `scan_dependencies()`, `check_patterns()`, `validate_inputs()`
   - Focus: Vulnerability detection
   - Output: Security issues + severity ratings

3. **Test Agent**
   - Tools: `run_tests()`, `analyze_coverage()`, `check_edge_cases()`
   - Focus: Test execution and coverage
   - Output: Test results + coverage metrics

4. **Writer Agent**
   - Tools: `format_markdown()`, `prioritize_issues()`, `create_summary()`
   - Focus: Report generation
   - Output: Formatted review document

**Why 4 agents?**
- Each has distinct domain expertise
- Can run Quality/Security/Test in parallel (faster)
- Writer sequential (needs all data first)
</details>

**Part 2:** Design the workflow - sequential, parallel, or mixed?

<details>
<summary>Show Recommended Workflow</summary>

**Mixed Workflow (Optimal):**

```
Phase 1 (Parallel - 3 agents):
├── Quality Agent  → analyze code
├── Security Agent → scan for issues  
└── Test Agent     → run test suite

Phase 2 (Sequential - 1 agent):
└── Writer Agent → aggregate all results → final report
```

**Timing:**
- Phase 1: ~MAX(quality_time, security_time, test_time) ≈ 5s
- Phase 2: ~2s
- **Total: ~7s** (vs 10s sequential)

**Why this workflow?**
- Parallelizing Phase 1 saves 3-5 seconds
- Writer needs all inputs, so must be sequential
- Clean separation: analysis vs. synthesis
</details>

**Part 3:** What could go wrong? Design error handling.

<details>
<summary>Show Error Scenarios</summary>

**Failure Modes:**

1. **Test Agent Fails**
   - Tests crash or timeout
   - **Handling:** Writer reports "Tests incomplete - manual review needed"
   - **Alternative:** Rerun tests with smaller subset

2. **Security Scan Takes Too Long**
   - External API timeout
   - **Handling:** Set 30s timeout, continue with partial results
   - **Alert:** Flag for manual security review

3. **Coordinator Can't Merge Conflicting Reports**
   - Quality says "Good" but Security says "Critical issues"
   - **Handling:** Writer prioritizes security, adds quality as secondary

4. **All Agents Succeed But Output is Inconsistent**
   - Each agent formats data differently
   - **Prevention:** Define shared data schema in state
   - **Validation:** Coordinator checks schema compliance
</details>

---

## 🎯 Practical Exercise: Design Your Own Agent Team

**Scenario:** Build a "Meeting Summarizer" that processes Zoom transcripts.

**Requirements:**
- Input: Zoom transcript (text file, 30-60 minutes of conversation)
- Output: Executive summary, action items, decisions made, next steps
- Constraint: Must highlight who said what

**Your Task:** Design the agent team.

**Worksheet:**

```markdown
## Step 1: Task Understanding
- Goal: 
- Inputs:
- Outputs:
- Constraints:

## Step 2: Subtasks
1.
2.
3.

## Step 3: Agent Specs
### Agent 1: [Name]
- Purpose:
- Inputs:
- Outputs:
- Tools:

### Agent 2: [Name]
...

## Step 4: Dependencies
[Draw or describe agent dependencies]

## Step 5: Workflow
[Sequence of operations]

## Step 6: Edge Cases
- Scenario 1:
- Mitigation 1:
```

<details>
<summary>Show Example Solution</summary>

## Step 1: Task Understanding
- **Goal:** Generate structured meeting summary from transcript
- **Inputs:** Transcript file (text), meeting metadata (date, participants)
- **Outputs:** Executive summary, action items list, decisions list, next steps
- **Constraints:** Must attribute statements to speakers, handle 30-60 min transcripts

## Step 2: Subtasks
1. **Parse Transcript** - Extract speakers and statements
2. **Categorize Content** - Identify action items, decisions, discussions
3. **Summarize** - Create concise executive summary
4. **Format** - Structure output for readability

## Step 3: Agent Specs

### Agent 1: Parser Agent
- **Purpose:** Extract structured data from raw transcript
- **Inputs:** Transcript file path, speaker list
- **Outputs:** Structured conversation (list of {speaker, timestamp, text})
- **Tools:** read_file, parse_transcript, identify_speakers

### Agent 2: Analyzer Agent
- **Purpose:** Categorize statements into action items, decisions, discussions
- **Inputs:** Structured conversation
- **Outputs:** Categorized statements
- **Tools:** classify_text, extract_action_items, identify_decisions

### Agent 3: Summary Agent
- **Purpose:** Create concise executive summary
- **Inputs:** Categorized statements
- **Outputs:** 2-3 paragraph summary
- **Tools:** summarize_text, calculate_key_topics

### Agent 4: Formatter Agent
- **Purpose:** Create final formatted document
- **Inputs:** All analysis outputs
- **Outputs:** Markdown document with sections
- **Tools:** format_markdown, create_list, add_attributions

## Step 4: Dependencies
```
Parser → Analyzer → Summary
                 ↘ Formatter
```

## Step 5: Workflow
1. Coordinator → Parser: parse transcript
2. Coordinator → Analyzer: categorize statements
3. Coordinator → Summary: create executive summary
4. Coordinator → Formatter: create final doc (needs Analyzer + Summary)
5. Return to user

## Step 6: Edge Cases
- **Transcript unclear:** Parser flags low confidence sections
- **No action items found:** Formatter notes this explicitly
- **Very long meeting (2+ hours):** Chunk into segments, process separately
</details>

---

## Example Workflows

### Workflow 1: Sequential Pipeline (Research → Analyze → Report)

**Characteristics:**
- Each agent processes entire dataset before passing to next
- Simple coordination logic
- Slower but reliable

**Use when:** Tasks have clear stages, quality > speed

```mermaid
flowchart LR
    Input[Raw Data] -->|Complete| Agent1[Process]
    Agent1 -->|Complete| Agent2[Analyze]
    Agent2 -->|Complete| Agent3[Report]
    Agent3 --> Output[Final Report]
```

### Workflow 2: Parallel Independent Tasks

**Characteristics:**
- Multiple agents work simultaneously on independent tasks
- Coordinator merges results at end
- Fast but requires careful result aggregation

**Use when:** Subtasks don't depend on each other

```mermaid
flowchart TD
    Input[Task] --> Agent1[Research Markets]
    Input --> Agent2[Research Competitors]
    Input --> Agent3[Research Technology]
    Agent1 --> Merge[Coordinator<br/>Merges Results]
    Agent2 --> Merge
    Agent3 --> Merge
    Merge --> Output[Complete Report]
```

### Workflow 3: Conditional Branching

**Characteristics:**
- Next agent depends on results of previous agent
- Coordinator makes routing decisions
- Flexible but complex coordination

**Use when:** Workflow varies based on data

```mermaid
flowchart TD
    Input[Data] --> Check[Validator Agent]
    Check -->|Valid| Process[Processing Agent]
    Check -->|Invalid| Clean[Cleanup Agent]
    Clean --> Process
    Process --> Output[Result]
```

---

## 🎯 Design Checklist

Before implementing your multi-agent system, verify:

**Task Decomposition:**
- [ ] Each subtask has a clear, single purpose
- [ ] Subtasks have natural boundaries (distinct inputs/outputs)
- [ ] No subtask is trying to do multiple jobs
- [ ] Decomposition follows a logical pattern (process, data type, or expertise)

**Agent Specifications:**
- [ ] Each agent has a clear mission statement
- [ ] Inputs and outputs are explicitly defined
- [ ] Tool sets match agent responsibilities
- [ ] Success criteria are measurable
- [ ] Failure modes are identified with mitigations

**Dependencies:**
- [ ] Dependencies are explicitly mapped
- [ ] No circular dependencies
- [ ] Parallel opportunities are identified
- [ ] Critical path is understood (longest sequence)

**Workflow:**
- [ ] Sequence of operations is clearly defined
- [ ] Message types are specified (what data flows where)
- [ ] Error handling is planned for each step
- [ ] Quality gates are defined (validation points)

**Edge Cases:**
- [ ] Timeout scenarios are handled
- [ ] Partial failure recovery is planned
- [ ] Invalid input handling is defined
- [ ] Conflicting data resolution is specified

---

**Ready?** If you can design agent teams, you're ready for [Debugging Multi-Agent Systems](./debugging-multi-agent.md) to learn how to troubleshoot when things go wrong.

**Page 5 of 9** | [← Previous: State Management](../concepts/state-management.md) | [Next: Debugging Multi-Agent Systems →](./debugging-multi-agent.md) | [↑ Reading Guide](../READING_GUIDE.md)

