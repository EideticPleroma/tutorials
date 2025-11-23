# Tutorial 1: Reading Guide & Documentation Order

This guide provides the recommended reading order for Tutorial 1. Follow this sequence to build your understanding progressively.

## Reading Path Overview

The tutorial is organized into **5 phases** with **16 core documents**. Each phase builds on the previous one.

**Estimated Reading Time**: ~3 hours for all documentation
**Recommended Approach**: Read concepts before coding, then reference guides as you build.

---

## Phase 1: Foundation (Pages 1-2)

### Page 1: Start Here
**📄 [README.md](../../../README.md)** (5 min)
- Project overview and quick start
- Goals and structure
- **Action**: Run `./setup.sh` after reading

### Page 2: The Big Picture
**📄 [Software Engineering Evolution](./concepts/software-engineering-evolution.md)** (10 min)
- Why software engineering is changing
- The new development loop
- Why iteration beats perfection
- **Why First**: Sets the mental model for everything that follows

---

## Phase 2: Core Concepts (Pages 3-6)

### Page 3: Understanding the Brain
**📄 [LLM Fundamentals](./concepts/llm-fundamentals.md)** (15 min)
- What is an LLM?
- The inference pipeline (tokenization → embedding → attention → generation)
- Key parameters: context window, temperature, system prompts
- Why Llama 3.1?
- **Prerequisite**: Must understand this before building agents

### Page 4: How Agents Work
**📄 [Tool Calling Architecture](./concepts/tool-calling-architecture.md)** (15 min)
- The tool calling loop (7 steps)
- Why this is "agentic"
- Common challenges
- **Critical**: This is the core mechanism of agentic AI

### Page 5: The Integration Layer
**📄 [MCP Introduction](./concepts/mcp-intro.md)** (10 min)
- What is MCP and why it matters
- The N×M problem it solves
- How we use it in Tutorial 1
- **Context**: Read after understanding tool calling

### Page 5a: Tech Stack (Optional Reference)
**📄 [Tech Stack Decisions](../../../docs/tech-stack.md)** (10 min)
- Why Llama over GPT-4?
- Why Ollama?
- Why Python for agents, TypeScript for tools?
- **When to Read**: Reference when you're curious about alternatives

### Page 6: Testing Philosophy
**📄 [Testing Agents](./concepts/testing-agents.md)** (15 min)
- Why traditional testing fails
- The Observe-Validate-Evaluate methodology
- Test harness overview
- **Important**: Read before writing tests

### Page 6a: Architecture Mindset
**📄 [Architecture in AI Era](./concepts/architecture-in-ai-era.md)** (10 min)
- The shift from specification to iteration
- How to partner with AI for design
- **Why**: Bridges the gap between theory and practice

---

## Phase 3: Implementation Guides (Pages 7-10)

### Page 7: Prompting Your Agent
**📄 [Prompting Techniques](./guides/prompting.md)** (15 min)
- System prompts: The agent's "OS"
- Few-shot prompting for tools
- Chain of Thought (CoT)
- Iterative refinement
- **When to Read**: Before writing your first system prompt

### Page 8: Managing Context
**📄 [Context Management](./guides/context-management.md)** (10 min)
- The context bucket metaphor
- Best practices for Cursor IDE
- When to reset conversations
- **Practical**: Read when you start using Cursor actively

### Page 9: Engineering Practices
**📄 [Engineering Best Practices](./guides/engineering.md)** (10 min)
- Terminal productivity (aliases, history)
- Git workflow for AI-assisted development
- Code review practices
- Observability
- **Reference**: Keep this handy while coding

### Page 10: Writing Agentic Code
**📄 [Agentic Code Practices](./guides/agentic-practices.md)** (10 min)
- Tool design principles
- Robustness and error handling
- Modularity
- Determinism
- **Reference**: Read before adding new tools

### Page 10a: Python Package Structure
**📄 [Package Structure Guide](./guides/package-structure.md)** (10 min)
- Why `__init__.py` matters
- Package-level exports
- Side-effect imports (`# noqa: F401`)
- Best practices for agentic projects
- **Reference**: Read when organizing code or seeing import issues

---

## Phase 4: Implementation & Practice

### Page 11: Code Exploration
**📄 Source Code** (30-60 min)
- `src/agent/simple_agent.py` - The main agent
- `src/agent/tool_registry.py` - How tools are registered
- `src/agent/mcp_tool_bridge.py` - MCP integration
- `tests/test_framework.py` - Testing framework
- **Action**: Read code with documentation open

---

## Phase 5: Advanced Topics - Architecture (Pages 13-15)

### Page 13: Evolution
**📄 [Architecture Evolution](./architecture/evolution.md)** (20 min)
- From Waterfall to AI Discovery
- LLM-First patterns (Small Contexts, Self-Describing Code)
- Case Study: How we built this tutorial

### Page 14: Design Methodology
**📄 [LLM Driven Design](./architecture/llm-driven-design.md)** (25 min)
- Prompting for architecture vs. implementation
- Using AI for trade-off analysis
- The Refactor Prompt template

### Page 15: Visualization
**📄 [Visualization Tools](./architecture/visualization-tools.md)** (30 min)
- Why diagrams reduce hallucinations
- Mermaid.js for documentation
- AI-Native tools (Claude Artifacts, Cursor)
- Hands-on: Generating diagrams for this codebase

### Page 16: Progress Tracking
**📄 [Progress Tracker](../progress.md)** (5 min)
- Check off completed phases
- See what's next
- Track your learning journey

---

## Quick Reference: By Topic

### If you want to understand...
- **How LLMs work**: Page 3 (LLM Fundamentals)
- **How tool calling works**: Page 4 (Tool Calling Architecture)
- **How to write good prompts**: Page 7 (Prompting Techniques)
- **How to test agents**: Page 6 (Testing Agents)
- **How to use Cursor effectively**: Page 8 (Context Management)
- **How to write tools**: Page 10 (Agentic Code Practices)
- **How to structure Python packages**: Page 10a (Package Structure)
- **How to design systems with AI**: Pages 13-15 (Architecture Series)

---

## Navigation

Each document includes:
- **Previous**: Link to the previous page in sequence
- **Next**: Link to the next page in sequence
- **Up**: Link back to this reading guide

---

## Reading Strategies

### Strategy 1: Linear (Recommended for Beginners)
Read pages 1-12 in order, then explore the Advanced Architecture section (13-15).

### Strategy 2: Concept-First
Read all concept docs (Pages 2-6a, 13-15), then guides (Pages 7-10), then code.

### Strategy 3: Just-in-Time
Read README, then reference specific guides as you encounter problems.

---

## Document Status

- ✅ All core concepts documented
- ✅ All guides written
- ✅ Architecture section complete
- ✅ Code examples included
- ✅ Navigation links added
- ✅ Progress tracker positioned at end

---

**Next Step**: Start with [Page 1: README.md](../../../README.md)
