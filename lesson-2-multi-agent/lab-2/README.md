# Lab 2: Building Multi-Agent Systems

**Prerequisites**: [Tutorial 2 Reading](../tutorial-2/READING_GUIDE.md) | **Time**: 4-6 Hours | **Difficulty**: Intermediate

Welcome to Lab 2. You've built single agents; now you will orchestrate teams.

## Objectives

In this lab, you will:
1. **Design** a coordinator agent that delegates to specialized workers
2. **Implement** three specialized agents (research, data analysis, writing)
3. **Connect** agents using a message protocol
4. **Test** multi-agent interactions using extended O.V.E. methodology

## The Philosophy: "Build with AI"

**Tutorial 2 is AI-native by design.** Unlike Lab 1's step-by-step guidance, Lab 2 provides:
- ✅ Code scaffolds (not full solutions)
- ✅ Design specifications (not implementation details)
- ✅ AI assistant prompts (leverage your IDE's AI)
- ✅ Conceptual guidance (not procedural steps)

**Why?** By Tutorial 2, you should be comfortable using AI to generate code. We focus on **what** to build and **why**, letting AI help with **how**.

### Using Your AI Assistant Effectively

Every exercise includes an **AI Assistant Prompts** section with ready-to-use prompts like:

```
@.cursorrules

I'm working on Exercise 1: Build a Coordinator Agent.

Context: I need to implement the delegation logic that sends tasks to worker agents.

Requirements:
- Sequential execution (research → data → writer)
- Error handling with retries
- Message tracking

Based on the project architecture, generate the coordinator's delegate() method.
```

**Tips for Success:**
- Always include `@.cursorrules` (Cursor) or ensure `.cursorrules` is in context (Continue, Cline)
- Reference specific files when asking for code: `@src/multi_agent/coordinator.py`
- Start with scaffolds provided, ask AI to complete specific functions
- Review AI-generated code critically - you're the engineer

## Prerequisites

**👉 [Step-by-Step Setup Guide](./setup-guide.md)** (If you need environment help)

Ensure you have completed Tutorial 1:
- [ ] Ollama is running (`curl localhost:11434` works)
- [ ] Python environment is active
- [ ] AI IDE configured (Cursor, Continue, Cline, or Copilot)
- [ ] You completed Lab 1 exercises
- [ ] You understand O.V.E. testing

**Not ready?** Complete [Tutorial 1](../../lesson-1-fundamentals/lab-1/README.md) first.

## Lab Structure

The lab follows an **evolution approach** - your code grows from single agent to multi-agent:

```
src/agent/              →    src/agent/multi/         →    src/multi_agent/
(Tutorial 1)                 (Exercise 0)                  (Exercises 1-4)
Single Agent                 Two Agents                    Coordinator-Worker
```

**Bridge Exercise (Start Here):**
0. **[Bridge: From Single to Multi-Agent](./exercises/00-bridge-refactoring.md)** (~45 min)
   - Extends `src/agent/` with a `multi/` subfolder
   - Creates GathererAgent and ReporterAgent
   - Shows why you need coordination patterns

**Core Exercises:**
1. **[Coordinator Basics](./exercises/01a-coordinator-basics.md)** (~60 min) - Build coordinator with direct calls
2. **[Message Protocol](./exercises/01b-message-protocol.md)** (~60 min) - Add structured communication
3. **[Create Specialized Agents](./exercises/02-specialized-agents.md)** (~90 min) - Research, data, writer agents
4. **[Review Agent Communication](./exercises/03-agent-communication.md)** (~60 min) - Validate protocol

**Challenge:**
5. **[Challenge: Research Workflow](./exercises/04-challenge-workflow.md)** (~120 min, optional) - End-to-end system

> **Why Evolution?** You don't start from scratch - you extend what you built in Tutorial 1. The bridge exercise shows your single agent "growing up" into multiple coordinated agents.

## Getting Started

### Quick Start Checklist

Before beginning:
1. [ ] Read [Tutorial 2 Concepts](../tutorial-2/READING_GUIDE.md) (at minimum Pages 1-4)
2. [ ] Review the [Lab Checklist](./lab-checklist.md) to see all tasks
3. [ ] Set up testing environment: [Testing Setup Guide](./testing-setup.md)
4. [ ] Verify your setup with `python -m pytest tests/ -v`
5. [ ] Open your AI IDE and ensure `.cursorrules` is working

### Recommended Workflow

**For each exercise:**
1. Read the exercise objective and context
2. Study the provided code scaffold
3. Use the AI assistant prompts to generate implementations
4. Review and modify the generated code
5. Run tests to validate (we provide test scaffolds too)
6. Debug using the troubleshooting guides

**Remember:** You're the architect. AI is your senior developer. You design, review, and approve.

## What's Different from Lab 1?

| Aspect | Lab 1 | Lab 2 |
|--------|-------|-------|
| **Guidance** | Step-by-step | AI-native scaffolds |
| **Code Provided** | Minimal | Scaffolds with TODOs |
| **AI Prompts** | Occasional | Every exercise |
| **Complexity** | Single agent | Multiple coordinated agents |
| **Testing** | Basic O.V.E. | Multi-agent O.V.E. |
| **Independence** | Guided | You architect with AI |

## Need Help?

### 🆘 Support Resources

**1. Start Here - Getting Unstuck Guide** 🎯
- **[Getting Unstuck Guide](./getting-unstuck.md)** - Systematic debugging with AI
- Includes AI-specific troubleshooting strategies
- How to ask your AI for help effectively

**2. Specific Errors** 🔧
- **[Troubleshooting Guide](./troubleshooting.md)** - Common multi-agent errors
- Message protocol issues
- State management problems
- Coordination failures
- Each error includes AI diagnostic prompts

**3. Common Questions** ❓
- **[FAQ](./FAQ.md)** - 40+ frequently asked questions
- Organized by: Coordinator, Communication, State, Testing
- Includes conceptual explanations

**4. Debug Tools** 🛠️
```bash
# View trace for a specific task
python scripts/view_trace.py <trace_id>

# Test multi-agent system
python -m pytest tests/multi_agent/ -v

# Check message flow
grep "message_sent" .agent_logs/agent.log | jq
```

**5. AI Assistant Tips** 🤖
```
# Good prompt structure:
@.cursorrules @src/multi_agent/coordinator.py

I'm implementing [specific function].

Context: [what you're trying to achieve]
Current code: [relevant snippet]
Error: [if any]

Based on the project architecture, how should I [specific question]?
```

**6. Reference Documentation** 📚
- [Tutorial 2 Concepts](../tutorial-2/READING_GUIDE.md)
- [Multi-Agent Architecture](../tutorial-2/concepts/multi-agent-architecture.md)
- [Coordinator Patterns](../tutorial-2/architecture/coordinator-patterns.md)

### Quick Debug Commands

```bash
# Verify all imports work
python -c "from src.multi_agent import Coordinator, WorkerAgent, Message"

# Run specific test
python -m pytest tests/multi_agent/test_coordinator.py::test_sequential_execution -v

# Check agent state
cat .agent_state/shared_state.json | jq '.'

# View recent logs
tail -f .agent_logs/agent.log | jq '.'
```

## Lab Completion Criteria

You've successfully completed Lab 2 when:
- [ ] Coordinator delegates tasks to workers sequentially
- [ ] Three specialized agents (research, data, writer) work correctly
- [ ] Message protocol handles requests, responses, and errors
- [ ] Shared state persists data across agents
- [ ] All tests pass (unit + integration)
- [ ] End-to-end workflow completes: user query → report

**Optional Challenge:**
- [ ] Complete Exercise 4: Full research workflow with parallel execution

## Time Management

**Recommended Schedule:**

- **Session 1 (2 hours):** 
  - Read Tutorial 2 concepts (Pages 1-4)
  - Complete Exercise 1 (Coordinator Agent)

- **Session 2 (2 hours):**
  - Complete Exercise 2 (Specialized Agents)

- **Session 3 (1.5 hours):**
  - Complete Exercise 3 (Agent Communication)
  - Run integration tests

- **Session 4 (2-3 hours, optional):**
  - Complete Exercise 4 (Challenge)

**Total:** 4-6 hours for core exercises, 7-9 hours with challenge

## What You'll Build

By the end of Lab 2, you'll have:

```
User: "Analyze the electric vehicle market"
  ↓
Coordinator Agent
  ├─> Research Agent: Gathers market data, sources
  │   Returns: Findings with citations
  ├─> Data Agent: Analyzes trends, calculates growth
  │   Returns: Metrics and insights
  └─> Writer Agent: Creates formatted report
      Returns: Markdown document with sections
  ↓
User receives: Complete market analysis report
```

## Next Steps After Lab 2

Once you complete Lab 2:
1. **Experiment**: Build your own multi-agent workflows
2. **Optimize**: Try parallel execution patterns
3. **Scale**: Explore hierarchical coordination (Tutorial 3 preview)
4. **Share**: Post your projects in the community

**Continue Learning**: Tutorial 3 will add memory and RAG to your agents.

---

👉 **[Start with Exercise 0: Bridge from Tutorial 1](./exercises/00-bridge-refactoring.md)** - Recommended for all students

👉 **[Skip to Exercise 1A: Coordinator Basics](./exercises/01a-coordinator-basics.md)** - If you understand two-agent patterns

👉 **[View Lab Checklist](./lab-checklist.md)** for detailed task tracking

---

**Remember:** This lab is about learning to architect with AI assistance. Don't aim for perfection - aim for understanding and iteration.

Good luck, and enjoy building your agent teams! 🤖🚀

