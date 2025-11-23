# Exercise 4: Challenge - Research Workflow

**Duration**: ~120 minutes | **Difficulty**: Advanced | **Optional**

## Objective

Build a complete end-to-end research workflow: user query → research → analysis → formatted report, with advanced features like parallel execution, quality gates, and error recovery.

## Context

Exercises 1-3 gave you the building blocks. Now you'll combine them into a production-quality multi-agent system.

**What you'll build:**
```
User: "Generate a comprehensive analysis of the electric vehicle market including sales trends, market leaders, and future projections."

System:
1. Coordinator receives query
2. Research Agent gathers data (parallel: market data + competitor data)
3. Quality gate: Check if research is sufficient
4. Data Agent analyzes trends
5. Quality gate: Check confidence level
6. Writer Agent creates formatted report
7. Return to user

Total time: ~60-90 seconds
Output: 1500-2000 word formatted report with citations
```

## Prerequisites

- [ ] Completed Exercises 1-3
- [ ] Coordinator, specialized agents, and message protocol working
- [ ] Read [Coordinator Patterns](../../tutorial-2/architecture/coordinator-patterns.md)
- [ ] Read [Designing Agent Teams](../../tutorial-2/guides/designing-agent-teams.md)

## Challenge Requirements

### Core Features (Required)

1. **End-to-End Workflow**
   - Accept user query
   - Execute research → data → writer pipeline
   - Return formatted report
   - Handle errors gracefully

2. **State Management**
   - All intermediate results stored in shared state
   - State inspectable at any point
   - Clean state between runs

3. **Logging**
   - Complete message flow logged
   - Trace ID connects all operations
   - Can reconstruct workflow from logs

4. **Testing**
   - Integration tests for full workflow
   - Error handling tests
   - Quality evaluation tests

### Advanced Features (Choose 2+)

**Option A: Parallel Execution**
- Run independent research tasks in parallel
- Example: market_data + competitor_data + technology_trends simultaneously
- Aggregate results before analysis phase

**Option B: Quality Gates**
- Check research quality before proceeding to analysis
- Check analysis confidence before proceeding to writing
- Retry or refine if quality insufficient

**Option C: Iterative Refinement**
- If initial research insufficient, refine query and retry
- Max 2 iterations
- Track iteration count in logs

**Option D: Progress Reporting**
- Report progress to user: "Researching...", "Analyzing...", "Writing..."
- Estimated time remaining
- Current phase

**Option E: Performance Optimization**
- Cache research results
- Parallel tool calls where possible
- Execution time <90 seconds

**Option F: Multi-Topic Support**
- Support queries about multiple topics
- Parallelize research per topic
- Aggregate in final report

## Suggested Approach

### Phase 1: Basic End-to-End (30 min)

Get the simplest version working:

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/coordinator.py

I need to implement a complete end-to-end workflow in Coordinator.

def generate_comprehensive_report(self, query: str, trace_id: str = None) -> dict:
    """
    Complete workflow: research → data → writer.
    
    Returns dict with:
    - status: "success" | "error"
    - report: formatted report string
    - execution_time: seconds
    - trace_id: for debugging
    """

Generate implementation with:
- Sequential execution (research, then data, then writer)
- Error handling at each step
- Timing tracking
- Comprehensive logging

Based on my existing delegate() method.
```

**Validation:**
```python
coordinator = Coordinator()
result = coordinator.generate_comprehensive_report("Analyze EV market")

assert result["status"] == "success"
assert len(result["report"]) > 1000  # Substantial report
assert result["execution_time"] < 120  # Under 2 minutes
```

### Phase 2: Add Advanced Feature (30-40 min)

Choose one advanced feature and implement it.

**Example: Quality Gates**

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/coordinator.py

Add quality gate after research phase:

After research completes:
1. Check shared_state.get("research_findings")
2. Count findings
3. If < 3 findings: Retry research with broader query
4. If >= 3 findings: Proceed to analysis

Add to generate_comprehensive_report() with max 2 retries.
```

**Example: Parallel Execution**

**AI Assistant Prompt:**
```
@.cursorrules @src/multi_agent/coordinator.py

Modify research phase to run parallel queries:

Instead of single research call:
- Query 1: "EV market sales data"
- Query 2: "EV market competitors"
- Query 3: "EV technology trends"

Run all three in parallel using ThreadPoolExecutor.
Aggregate results before passing to data agent.
```

### Phase 3: Add Second Advanced Feature (30-40 min)

Choose another feature and implement.

### Phase 4: Integration Testing (20 min)

Write comprehensive tests for your system.

**Test Template:**
```python
def test_comprehensive_workflow():
    """Test full end-to-end workflow."""
    coordinator = Coordinator()
    
    # Execute
    result = coordinator.generate_comprehensive_report(
        "Analyze the electric vehicle market including trends and leaders"
    )
    
    # Validate structure
    assert result["status"] == "success"
    assert "report" in result
    assert "execution_time" in result
    assert "trace_id" in result
    
    # Validate content quality (basic)
    report = result["report"]
    assert len(report) > 1000
    assert "electric vehicle" in report.lower() or "ev" in report.lower()
    assert "##" in report  # Has headings
    
    # Validate performance
    assert result["execution_time"] < 120  # Under 2 minutes
    
    # Validate state
    state = coordinator.shared_state.get_all()
    assert "research_findings" in state
    assert "data_analysis" in state
    assert "final_report" in state
```

## Testing Your System

### Manual Testing

```python
from src.multi_agent import Coordinator
import time

coordinator = Coordinator()

print("Starting comprehensive analysis...")
start = time.time()

result = coordinator.generate_comprehensive_report(
    "Analyze the electric vehicle market, including sales trends, "
    "major manufacturers, and future projections for 2024-2025."
)

duration = time.time() - start

print(f"\nStatus: {result['status']}")
print(f"Execution Time: {duration:.1f}s")
print(f"Trace ID: {result['trace_id']}")
print(f"\nReport Length: {len(result['report'])} characters")
print(f"\nReport Preview:\n{result['report'][:500]}...")

# Check state
state = coordinator.shared_state.get_all()
print(f"\nState Keys: {list(state.keys())}")
```

### Performance Testing

```bash
# Run multiple times to test reliability
for i in {1..5}; do
  echo "Run $i:"
  python -m pytest tests/multi_agent/test_challenge.py::test_comprehensive_workflow -v
done
```

### Quality Evaluation

```python
def test_report_quality():
    """Evaluate report quality (requires real LLM)."""
    coordinator = Coordinator()
    result = coordinator.generate_comprehensive_report("EV market analysis")
    
    report = result["report"]
    
    # Structure checks
    assert report.count("##") >= 3  # Multiple sections
    assert "source" in report.lower() or "http" in report  # Has citations
    
    # Content checks (basic)
    keywords = ["electric vehicle", "ev", "market", "sales", "trend"]
    assert any(kw in report.lower() for kw in keywords)
    
    # Formatting checks
    assert report.startswith("#")  # Starts with heading
    assert len(report.split("\n")) > 20  # Multiple paragraphs
```

## Evaluation Criteria

Your challenge is successful if:

### Functionality (40 points)
- [ ] (10 pts) End-to-end workflow completes without errors
- [ ] (10 pts) All three agents execute successfully
- [ ] (10 pts) Report is well-formatted and comprehensive
- [ ] (10 pts) Error handling prevents crashes

### Advanced Features (30 points)
- [ ] (15 pts each) Two advanced features implemented correctly

### Quality (20 points)
- [ ] (5 pts) Code is clean and well-organized
- [ ] (5 pts) Logging is comprehensive
- [ ] (5 pts) Tests are thorough
- [ ] (5 pts) Documentation clear

### Performance (10 points)
- [ ] (5 pts) Executes in <120 seconds
- [ ] (5 pts) Efficient (no unnecessary operations)

**Total: 100 points**
**Pass: 70+ points**

## Common Challenges

**Challenge: "Too slow"**
- Profile to find bottleneck
- Consider parallel execution
- Cache where possible
- Optimize tool calls

**Challenge: "Quality inconsistent"**
- Add quality gates
- Refine system prompts
- Provide more context to agents
- Use iterative refinement

**Challenge: "Errors are cryptic"**
- Add try-catch at each phase
- Return detailed error messages
- Log error context
- Test error paths

**Challenge: "Hard to debug"**
- Use trace IDs consistently
- Log state changes
- Create visualization script
- Use debugging checklist

## Extensions (Beyond Lab 2)

Want to go further?

**Multi-User Support:**
- Handle concurrent user queries
- Separate state per user
- Queue management

**Async Execution:**
- Non-blocking delegation
- Websocket progress updates
- Background job processing

**Advanced Coordination:**
- Conditional branching (if quality low, try alternative approach)
- Hierarchical coordination (sub-coordinators for sub-tasks)
- Dynamic agent selection (choose best agent for task)

**Production Features:**
- Rate limiting
- Caching layer
- Health checks
- Monitoring dashboard

## Submission (If Applicable)

If you're completing this for a course:

1. **Code:**
   - All source files in `src/multi_agent/`
   - Test files in `tests/multi_agent/`

2. **Documentation:**
   - README explaining your advanced features
   - Architecture diagram
   - Performance benchmarks

3. **Demo:**
   - Record execution with sample query
   - Show logs and trace
   - Present report output

4. **Reflection:**
   - What worked well?
   - What was challenging?
   - What would you improve?

## Congratulations!

You've built a complete multi-agent system from scratch! 🎉

**What you've learned:**
- Coordinator-worker architecture
- Agent specialization
- Message protocols
- State management
- Multi-agent testing
- Advanced coordination patterns

**What's next:**
- Tutorial 3: Memory & RAG (long-term memory, vector databases)
- Tutorial 4: Production Patterns (monitoring, scaling, deployment)
- Build your own multi-agent applications!

---

## 💡 Final Tips

**Start Simple:**
- Get basic workflow working first
- Add advanced features incrementally
- Test after each addition

**Measure Everything:**
- Execution time per phase
- Message counts
- State size
- Quality metrics

**Document Decisions:**
- Why you chose certain features
- Trade-offs you made
- What you learned

**Have Fun:**
- Experiment with different approaches
- Try creative coordination patterns
- Build something unique!

