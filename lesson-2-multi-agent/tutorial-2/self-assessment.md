# Tutorial 2: Self-Assessment Quiz

**Before Starting Tutorial 2**, complete this self-assessment to verify you're ready for multi-agent systems.

**Time:** ~10 minutes | **Passing Score:** 80% (16/20 correct)

---

## Prerequisites Check

Before taking the quiz:
- [ ] Completed [Tutorial 1: Fundamentals](../../../lesson-1-fundamentals/tutorial-1/INDEX.md)
- [ ] Built at least one working agent with custom tools
- [ ] Comfortable with Python, type hints, and async concepts

**Not ready?** Complete Tutorial 1 first, then return here.

---

## Section 1: Tool Calling & Agent Basics (5 questions)

### Q1. What is the 7-step tool calling loop?

- A) User → LLM → Tool → LLM → User (that's 5 steps)
- B) User → Agent → Parse → LLM → Tool Decision → Execute → Format → Response
- C) Init → Prompt → Call → Parse → Tool → LLM → Response
- D) Request → Agent → Tool → Result → Format → Return → Log

<details>
<summary>Show Answer</summary>

**B) User → Agent → Parse → LLM → Tool Decision → Execute → Format → Response**

From Tutorial 1, the loop is:
1. User sends request
2. Agent receives and parses
3. Agent calls LLM with system prompt + tools
4. LLM decides which tool to call (or respond directly)
5. Agent executes tool
6. Agent formats result
7. Agent returns response to user

If you missed this, review [Tool Calling Architecture](../../../lesson-1-fundamentals/tutorial-1/concepts/tool-calling-architecture.md).
</details>

---

### Q2. What decorator is used to register a tool?

```python
def web_search(query: str) -> str:
    """Search the web for information."""
    # implementation
```

- A) `@tool`
- B) `@register_tool`
- C) `@registry.register`
- D) `@agent.tool`

<details>
<summary>Show Answer</summary>

**C) `@registry.register`**

Example:
```python
@registry.register
def web_search(query: str) -> str:
    """Search the web for information."""
    return search_results
```

The registry pattern from Tutorial 1 is used throughout.
</details>

---

### Q3. What's the purpose of type hints in agent tools?

- A) Optional - for code documentation only
- B) Required - LLMs read them to understand parameters
- C) Performance - makes Python faster
- D) Security - prevents type errors

<details>
<summary>Show Answer</summary>

**B) Required - LLMs read them to understand parameters**

Type hints tell the LLM:
- What parameters the tool expects
- What type each parameter is
- What the tool returns

Without type hints, the LLM can't reliably call your tools.

**From .cursorrules:** "Type hints: MANDATORY for all function signatures (Agents rely on them)."
</details>

---

### Q4. What does O.V.E. testing stand for?

- A) Observe, Verify, Execute
- B) Organize, Validate, Evaluate
- C) Observe, Validate, Evaluate
- D) Output, Validation, Execution

<details>
<summary>Show Answer</summary>

**C) Observe, Validate, Evaluate**

- **Observe:** Run the agent, capture inputs/outputs
- **Validate:** Check deterministic behaviors (tool calls, formats)
- **Evaluate:** Check probabilistic outputs (answer quality)

This methodology extends to multi-agent testing in Tutorial 2.
</details>

---

### Q5. Why use Google-style docstrings for tools?

- A) Project convention only
- B) LLMs read them to understand what the tool does
- C) Required by Python
- D) Better than other styles

<details>
<summary>Show Answer</summary>

**B) LLMs read them to understand what the tool does**

Example:
```python
@registry.register
def calculate(expression: str) -> float:
    """
    Perform mathematical calculations.
    
    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 2")
    
    Returns:
        Result of the calculation
    """
    return eval(expression)
```

The LLM reads the docstring to know WHEN and HOW to use the tool.
</details>

---

## Section 2: Multi-Agent Concepts (5 questions)

### Q6. When should you use multi-agent instead of single agent?

- A) Always - multi-agent is better
- B) When task can be decomposed into distinct subtasks with different expertise
- C) When you need faster execution
- D) When single agent fails

<details>
<summary>Show Answer</summary>

**B) When task can be decomposed into distinct subtasks with different expertise**

Use multi-agent when:
- ✅ Task has clear subtasks (research → analyze → report)
- ✅ Subtasks need different tools/expertise
- ✅ Parallel execution helps
- ✅ Specialization improves quality

Don't use multi-agent when:
- ❌ Simple linear tasks
- ❌ High interactivity needed
- ❌ Tight coupling between steps
- ❌ Development time critical

See [Multi-Agent Architecture decision tree](./concepts/multi-agent-architecture.md).
</details>

---

### Q7. What's the main job of a coordinator agent?

- A) Execute all tasks and tools
- B) Delegate to workers and aggregate results
- C) Monitor system performance
- D) Handle user authentication

<details>
<summary>Show Answer</summary>

**B) Delegate to workers and aggregate results**

Coordinator responsibilities:
1. Receive user request
2. Decompose into subtasks
3. Delegate to appropriate workers
4. Aggregate results
5. Return final response

**Key:** Coordinator orchestrates, workers execute.
</details>

---

### Q8. In coordinator-worker pattern, can workers communicate directly?

- A) Yes, always - it's faster
- B) No, never - coordinator is required
- C) Generally no - all communication through coordinator (for Tutorial 2)
- D) Yes, but only for errors

<details>
<summary>Show Answer</summary>

**C) Generally no - all communication through coordinator (for Tutorial 2)**

**Pure Coordinator-Worker:**
- All messages flow through coordinator
- Workers don't know other workers exist
- Simpler debugging and control flow

**Why Tutorial 2 uses this:**
- Easier to understand
- Predictable behavior
- Clear message tracing

**Advanced patterns** (Tutorial 3+) might allow direct communication for performance.
</details>

---

### Q9. What's the cost implication of multi-agent vs single agent?

- A) Same cost - just different architecture
- B) Cheaper - shared resources
- C) 2-5x higher cost due to more LLM calls
- D) Depends on tools used

<details>
<summary>Show Answer</summary>

**C) 2-5x higher cost due to more LLM calls**

**Cost Breakdown:**
- Single Agent: 1-3 LLM calls per task
- Multi-Agent: 7-10+ LLM calls per task
- **Cost multiplier:** 3-5x higher

**Why?**
- Coordinator makes LLM calls
- Each worker makes LLM calls
- More coordination = more calls

**Trade-off:** Higher cost for better quality (typically 40%+ improvement).

See [Cost Analysis](./concepts/multi-agent-architecture.md#cost-considerations).
</details>

---

### Q10. What's agent specialization?

- A) Training agents on specific domains
- B) Giving each agent focused system prompt and limited tools
- C) Using different LLM models for each agent
- D) Optimizing agent performance

<details>
<summary>Show Answer</summary>

**B) Giving each agent focused system prompt and limited tools**

**Specialization = Three Pillars:**
1. Focused system prompt (defines role and boundaries)
2. Limited tool set (only relevant tools)
3. Domain-specific examples (few-shot prompts)

**Example:**
- Research Agent: Only has web_search, read_file tools
- Data Agent: Only has calculate, analyze_trend tools
- Writer Agent: Only has format_markdown tool

**Benefit:** Specialists outperform generalists at their specific task.
</details>

---

## Section 3: State & Communication (5 questions)

### Q11. When should you use shared state vs messages?

- A) Always use shared state - it's persistent
- B) Always use messages - they're traceable
- C) Shared state for data, messages for communication
- D) Doesn't matter - they're equivalent

<details>
<summary>Show Answer</summary>

**C) Shared state for data, messages for communication**

**Use Shared State For:**
- Persistent data (research_findings, analysis)
- Data accessed by multiple agents
- Context that outlives messages

**Use Messages For:**
- Agent-to-agent communication
- Task delegation
- Status updates
- Temporary data

**Example:**
```python
# Shared state: Research findings (data agent needs later)
shared_state.set("research_findings", findings)

# Message: Notify coordinator (one-time event)
send_message(coordinator, "task_complete", {...})
```
</details>

---

### Q12. What fields are required in every message?

- A) message_id, timestamp, content
- B) from, to, action, payload
- C) message_id, timestamp, from_agent, to_agent, message_type, payload
- D) id, sender, receiver, data

<details>
<summary>Show Answer</summary>

**C) message_id, timestamp, from_agent, to_agent, message_type, payload**

**Required Fields:**
```python
{
    "message_id": "unique-id",
    "timestamp": "2025-11-23T10:30:00",
    "from_agent": "coordinator",
    "to_agent": "research",
    "message_type": "request",  # request | response | error
    "payload": {...}
}
```

**Optional but useful:**
- `trace_id` - Track entire workflow
- `in_reply_to` - Link response to request
- `action` - What to do (for requests)

See [Message Protocol](./concepts/agent-communication.md).
</details>

---

### Q13. Why use JSON messages instead of direct function calls?

- A) JSON is faster
- B) Traceability, debugging, and flexibility
- C) Required by Python
- D) Better security

<details>
<summary>Show Answer</summary>

**B) Traceability, debugging, and flexibility**

**Benefits of JSON Messages:**
1. **Traceability:** Every message logged
2. **Debugging:** Can replay messages
3. **Serialization:** Works across languages/networks
4. **Testing:** Easy to mock and replay
5. **Flexibility:** Can intercept, transform, reroute

**Trade-off:** More overhead than direct calls, but better architecture.

**Direct calls hide:** What was sent? When? What failed?
</details>

---

### Q14. What's a race condition in shared state?

- A) Agents competing for processing time
- B) Two agents writing to same key simultaneously, causing data loss
- C) Agent execution order is wrong
- D) Network latency issues

<details>
<summary>Show Answer</summary>

**B) Two agents writing to same key simultaneously, causing data loss**

**Problem:**
```python
# Agent A reads count=5, writes 6
# Agent B reads count=5 (before A writes), writes 6
# Result: count=6 (should be 7!)
```

**Solutions:**
1. File locking (implemented in SharedState)
2. Namespaced keys (agent_A_result, agent_B_result)
3. Coordinator manages all writes

Our SharedState uses file locking to prevent this.
</details>

---

### Q15. Where is shared state stored in Tutorial 2?

- A) In-memory dictionary
- B) SQLite database
- C) JSON file with file locking
- D) Redis cache

<details>
<summary>Show Answer</summary>

**C) JSON file with file locking**

**Why JSON files?**
- ✅ Human-readable (easy to debug)
- ✅ No dependencies (no database needed)
- ✅ Persistent (survives crashes)
- ✅ Simple (good for learning)

**Location:** `.agent_state/shared_state.json`

**Debug:** `cat .agent_state/shared_state.json | jq '.'`

**For production:** Consider Redis or database for scale.
</details>

---

## Section 4: Testing & Debugging (5 questions)

### Q16. What are the three levels of multi-agent testing?

- A) Unit, System, Acceptance
- B) Unit, Integration, End-to-End
- C) Unit, Agent Interaction, Integration
- D) Mock, Real, Production

<details>
<summary>Show Answer</summary>

**C) Unit, Agent Interaction, Integration**

**Testing Pyramid:**
```
    Integration Tests (5-10)
         /\
        /  \
  Agent Interaction (15-20)
       /    \
      /      \
  Unit Tests (30-50)
```

1. **Unit:** Test each agent independently with mocks
2. **Agent Interaction:** Test agent pairs (research→data)
3. **Integration:** Test full workflows (coordinator→all agents→report)

**Ratio:** 70% unit, 20% interaction, 10% integration
</details>

---

### Q17. What's a trace ID used for?

- A) Performance profiling
- B) Tracking all messages in a single workflow
- C) User authentication
- D) Error reporting

<details>
<summary>Show Answer</summary>

**B) Tracking all messages in a single workflow**

**Usage:**
```python
trace_id = str(uuid.uuid4())  # Generated once per user request

# All messages in this workflow use same trace_id
coordinator.send(research, action="gather_info", trace_id=trace_id)
research.send(coordinator, action="result", trace_id=trace_id)
```

**Debugging:**
```bash
# View entire workflow
grep '"trace_id": "abc-123"' agent.log | jq '.'

# Or use trace viewer
python scripts/view_trace.py abc-123
```

**Benefit:** Reconstruct complete workflow across multiple agents.
</details>

---

### Q18. What's the first step when debugging a multi-agent failure?

- A) Restart the system
- B) Check logs for errors
- C) Find the trace ID and extract all events
- D) Test each agent individually

<details>
<summary>Show Answer</summary>

**C) Find the trace ID and extract all events**

**Systematic Debugging:**
1. Get trace ID for failing request
2. Extract all logs for that trace
3. Identify which agent produced unexpected behavior
4. Check message flow (sent vs received)
5. Inspect state changes
6. Review agent execution details

**Commands:**
```bash
# Get trace ID
grep "task_received" agent.log | tail -1 | jq -r .trace_id

# Extract all events
python scripts/view_trace.py <trace_id>
```

See [Debugging Checklist](./guides/debugging-multi-agent.md).
</details>

---

### Q19. How should you test agent specialization boundaries?

- A) Manual inspection
- B) Check that agent only uses assigned tools
- C) Verify agent output doesn't contain forbidden analysis keywords
- D) Both B and C

<details>
<summary>Show Answer</summary>

**D) Both B and C**

**Test Tool Boundaries:**
```python
def test_research_agent_tools():
    agent = ResearchAgent()
    allowed = {"web_search", "read_file"}
    used = set(agent.tools.keys())
    assert used == allowed
```

**Test Role Adherence:**
```python
def test_research_stays_in_role():
    agent = ResearchAgent()
    result = agent.gather_info("EV trends")
    
    # Should NOT contain analysis keywords
    forbidden = ["indicates", "suggests", "trend shows"]
    for phrase in forbidden:
        assert phrase not in str(result).lower()
```

**Why both?** Tools prevent capability, but prompts enforce behavior.
</details>

---

### Q20. What's the recommended ratio of mocked vs real LLM tests?

- A) 50/50 - balanced approach
- B) 100% real - test production conditions
- C) 95% mocked, 5% real - speed + quality checks
- D) 100% mocked - always deterministic

<details>
<summary>Show Answer</summary>

**C) 95% mocked, 5% real - speed + quality checks**

**Mocked LLM Tests (95%):**
- Fast (milliseconds)
- Deterministic
- Test coordination logic
- No API costs
- Run in CI/CD

**Real LLM Tests (5%):**
- Slow (seconds)
- Probabilistic
- Test actual quality
- Cost money
- Run before releases

**Example:**
```python
# 95% - Mock LLM
def test_coordination_logic():
    coordinator = Coordinator(llm=MockLLM())
    # Test message flow, error handling, etc.

# 5% - Real LLM
@pytest.mark.slow
def test_report_quality():
    coordinator = Coordinator(llm=RealLLM())
    report = coordinator.generate_report("EV market")
    # Evaluate quality with human metrics
```
</details>

---

## Scoring Guide

**Count your correct answers:**

- **18-20 correct (90-100%):** ✅ **Excellent!** You're ready for Tutorial 2. Start with [Reading Guide](./READING_GUIDE.md).

- **16-17 correct (80-85%):** ✅ **Good!** You have the foundation. Review the questions you missed, then start Tutorial 2.

- **13-15 correct (65-75%):** ⚠️ **Borderline.** Review these topics from Tutorial 1 before continuing:
  - Tool calling and registration
  - O.V.E. testing methodology
  - Type hints and docstrings
  - Agent architecture basics

- **<13 correct (<65%):** ❌ **Not ready yet.** Complete [Tutorial 1](../../../lesson-1-fundamentals/tutorial-1/INDEX.md) first, then retake this quiz.

---

## Topic Review Guide

If you scored low in a section:

### Section 1 (Tool Calling): Review Tutorial 1
- [Tool Calling Architecture](../../../lesson-1-fundamentals/tutorial-1/concepts/tool-calling-architecture.md)
- [Adding Custom Tools](../../../lesson-1-fundamentals/lab-1/exercises/02-adding-tools.md)
- [Testing Methodology](../../../lesson-1-fundamentals/tutorial-1/guides/testing-agents.md)

### Section 2 (Multi-Agent Concepts): Read Tutorial 2 Concepts
- [Multi-Agent Architecture](./concepts/multi-agent-architecture.md)
- [Agent Specialization](./concepts/agent-specialization.md)
- [Coordinator Patterns](./architecture/coordinator-patterns.md)

### Section 3 (State & Communication): Read Communication Docs
- [Agent Communication](./concepts/agent-communication.md)
- [State Management](./concepts/state-management.md)

### Section 4 (Testing & Debugging): Read Testing Guides
- [Testing Multi-Agent Systems](./guides/testing-multi-agent.md)
- [Debugging Multi-Agent Systems](./guides/debugging-multi-agent.md)

---

## Next Steps

**If you passed (16+ correct):**
1. ✅ Bookmark this page (you might reference it later)
2. ✅ Start with [Reading Guide](./READING_GUIDE.md)
3. ✅ Read concepts (Pages 1-4)
4. ✅ Begin [Lab 2](../../lab-2/README.md)

**If you didn't pass:**
1. ❌ Review the topics you missed
2. ❌ Complete or review Tutorial 1
3. ❌ Retake this quiz
4. ✅ Start Tutorial 2 when ready

---

**Good luck!** 🚀

[← Back to Tutorial 2 Index](./INDEX.md) | [Start Reading Guide →](./READING_GUIDE.md)

