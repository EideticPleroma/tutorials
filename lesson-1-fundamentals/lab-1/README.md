# Lab 1: Building Your First Agent

**Prerequisites**: [Tutorial 1 Reading](../tutorial-1/READING_GUIDE.md) | **Time**: 3-4 Hours | **Difficulty**: Beginner

Welcome to the Lab. You've read the theory; now you will build the engine.

## Objectives

In this lab, you will:
1.  **Dissect** a working Agent to understand its internal loop.
2.  **Extend** the Agent with a new tool (`search_files`).
3.  **Engineer** the System Prompt to handle complex queries.
4.  **Validate** your changes using the O.V.E. testing methodology.

## The Philosophy: "Build to Learn"

You are not just copying code. You are acting as the Lead Engineer for an AI Junior Developer.
*   You will write tests *before* the agent passes them.
*   You will debug "hallucinations" (when the agent lies).
*   You will feel the difference between a "good prompt" and a "bad prompt."

## Prerequisites

**👉 [Step-by-Step Setup Guide](./setup-guide.md)** (Read this if you are setting up WSL, Python, or Node from scratch)

Ensure you have completed the setup:
- [ ] Ollama is running (`curl localhost:11434` works)
- [ ] Python environment is active (`source venv/bin/activate` or similar)
- [ ] AI IDE configured ([see IDE setup](./setup-guide.md#ide-setup))
- [ ] You have read the [Core Concepts](../tutorial-1/concepts/tool-calling-architecture.md)

## Getting Started

We track progress using a detailed checklist. This mirrors a real-world engineering "Runbook."

👉 **[Start the Lab Checklist](./lab-checklist.md)**

## Lab Structure

The lab is divided into 4 progressive exercises:
1.  **[Understanding the Agent](./exercises/01-understanding-agent.md)**: Trace the execution flow.
2.  **[Adding a Tool](./exercises/02-adding-tools.md)**: Implement file search.
3.  **[Prompt Engineering](./exercises/03-prompt-engineering.md)**: Teach the agent to think.
4.  **[Testing Methodology](./exercises/04-testing-methodology.md)**: robust validation.

## Need Help?

### 🆘 Getting Support

When you hit a roadblock, you have comprehensive support resources:

**1. Start Here - Getting Unstuck Guide** 🎯
- **[Getting Unstuck Guide](./getting-unstuck.md)** - Systematic 5-step debugging process
- Learn to use your AI assistant effectively with `.cursorrules` context
- Rollback strategies when nothing works

**2. Specific Errors** 🔧
- **[Troubleshooting Guide](./troubleshooting.md)** - 20+ common errors with solutions
- Includes: Setup, imports, tool registration, agent behavior, testing, Ollama issues
- Each error has: What it means, Why it happens, How to fix, Ask Your AI prompt

**3. Common Questions** ❓
- **[FAQ](./FAQ.md)** - 50+ frequently asked questions with answers
- Organized by: Setup, Tools, Agent Behavior, Testing, IDE, Concepts, Performance

**4. Debug Tools** 🛠️
```bash
# Comprehensive diagnostic
python scripts/debug_agent.py

# Show registered tools
python scripts/debug_agent.py --tools

# Test with a query
python scripts/debug_agent.py --test "What is 2+2?"
```

**5. AI Assistant Tips** 🤖
- Always include `@.cursorrules` in your questions (Cursor users)
- Continue/Cline: Reads `.cursorrules` automatically
- See [Setup Guide Section 8](./setup-guide.md#8-pro-tip-always-include-cursorrules-in-ai-context) for details

**6. Reference Documentation** 📚
- [Reading Guide](../tutorial-1/READING_GUIDE.md) - Conceptual documentation
- [Documentation Index](../tutorial-1/INDEX.md) - Quick reference

### Quick Debug Commands

```bash
# Verify setup
curl localhost:11434                    # Check Ollama
ollama list                             # Check models
python scripts/debug_agent.py           # Full diagnostic

# Test components
python -m pytest tests/ -v              # Run all tests
python -m src.agent.simple_agent        # Run agent

# Check tool registration
python -c "from src.agent.tool_registry import registry; from src.agent import simple_agent; print([s['function']['name'] for s in registry.get_schemas()])"
```

### Example: Using Your AI Assistant

```
@.cursorrules

I'm stuck on Exercise [number].

Problem: [describe issue]
Error: [paste error if any]
What I tried: [list attempts]
Expected: [what should happen]
Actual: [what's happening]

According to the project guidelines, what should I check next?
```

