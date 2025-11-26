# Tutorial 1: Reading Guide & Documentation Order

This guide provides the recommended reading order for Tutorial 1. Follow this sequence to build your understanding progressively.

## Reading Path Overview

The tutorial is organized into **5 phases** with **16 core documents**. Each phase builds on the previous one.

**Estimated Reading Time**: ~3 hours for all documentation
**Recommended Approach**: Read concepts before coding, then reference guides as you build.

---

## Phase 1: The Context (Pages 1-2)

### Page 1: The Big Picture
**📄 [Software Engineering Evolution](./concepts/software-engineering-evolution.md)** (10 min)
- Why software engineering is changing
- The new development loop
- Why iteration beats perfection
- **Why First**: Sets the mental model for everything that follows

### Page 2: Architecture Mindset
**📄 [Architecture in AI Era](./concepts/architecture-in-ai-era.md)** (10 min)
- The shift from specification to iteration
- How to partner with AI for design
- **Why**: Frames the mindset before diving into technical details

---

## Phase 2: Core Concepts - "The What" (Pages 3-6)

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

### Page 6: Testing Philosophy
**📄 [Testing Agents](./concepts/testing-agents.md)** (15 min)
- Why traditional testing fails
- The Observe-Validate-Evaluate methodology
- Test harness overview
- **Important**: Read before writing tests

---

## Phase 3: Deep Dives - "The Why" (Pages 7-9)

### Page 7: Evolution of Dev Patterns
**📄 [Architecture Evolution](./architecture/evolution.md)** (20 min)
- From Waterfall to AI Discovery
- LLM-First patterns (Small Contexts, Self-Describing Code)
- Case Study: How we built this tutorial

### Page 8: Design Methodology
**📄 [LLM Driven Design](./architecture/llm-driven-design.md)** (25 min)
- Prompting for architecture vs. implementation
- Using AI for trade-off analysis
- The Refactor Prompt template

### Page 9: Visualization
**📄 [Visualization Tools](./architecture/visualization-tools.md)** (30 min)
- Why diagrams reduce hallucinations
- Mermaid.js for documentation
- AI-Native tools (Claude Artifacts, Cursor)
- Hands-on: Generating diagrams for this codebase

---

## Phase 4: Implementation Guides - "The How" (Pages 10-14)

### Page 10: Prompting Your Agent
**📄 [Prompting Techniques](./guides/prompting.md)** (15 min)
- System prompts: The agent's "OS"
- Few-shot prompting for tools
- Chain of Thought (CoT)
- Iterative refinement
- **When to Read**: Before writing your first system prompt

### Page 11: Managing Context
**📄 [Context Management](./guides/context-management.md)** (10 min)
- The context bucket metaphor
- Best practices for Cursor IDE
- When to reset conversations
- **Practical**: Read when you start using Cursor actively

### Page 12: Engineering Practices
**📄 [Engineering Best Practices](./guides/engineering.md)** (10 min)
- Terminal productivity (aliases, history)
- Git workflow for AI-assisted development
- Code review practices
- Observability
- **Reference**: Keep this handy while coding

### Page 13: Writing Agentic Code
**📄 [Agentic Code Practices](./guides/agentic-practices.md)** (10 min)
- Tool design principles
- Robustness and error handling
- Modularity
- Determinism
- **Reference**: Read before adding new tools

### Page 14: Python Package Structure
**📄 [Package Structure Guide](./guides/package-structure.md)** (10 min)
- Why `__init__.py` matters
- Package-level exports
- Side-effect imports (`# noqa: F401`)
- Best practices for agentic projects
- **Reference**: Read when organizing code or seeing import issues

---

## Phase 5: Code & Lab - "The Practice" (Pages 15-16)

### Page 15: Code Exploration
**📄 Source Code** (30-60 min)
- `src/agent/simple_agent.py` - The main agent
- `src/agent/tool_registry.py` - How tools are registered
- `src/agent/mcp_tool_bridge.py` - MCP integration
- `tests/test_framework.py` - Testing framework
- **Action**: Read code with documentation open

### Page 16: Lab Exercises
**📄 [Lab 1](../lab-1/README.md)** (3-5 hours)
- Build your first agent
- Add custom tools
- Implement tests using O.V.E. methodology
- **Action**: Put theory into practice

---

## Quick Reference: By Topic

### If you want to understand...
- **Why software development is changing**: Page 1 (Software Engineering Evolution)
- **How to think about AI architecture**: Page 2 (Architecture in AI Era)
- **How LLMs work**: Page 3 (LLM Fundamentals)
- **How tool calling works**: Page 4 (Tool Calling Architecture)
- **How to test agents**: Page 6 (Testing Agents)
- **How to write good prompts**: Page 10 (Prompting Techniques)
- **How to use Cursor effectively**: Page 11 (Context Management)
- **How to write tools**: Page 13 (Agentic Code Practices)
- **How to structure Python packages**: Page 14 (Package Structure)
- **How to design systems with AI**: Pages 7-9 (Architecture Deep Dives)

---

## Navigation

Each document includes:
- **Previous**: Link to the previous page in sequence
- **Next**: Link to the next page in sequence
- **Up**: Link back to this reading guide

---

## Reading Strategies

### Strategy 1: Linear (Recommended for Beginners)
Read pages 1-16 in order. This builds understanding progressively from context → concepts → philosophy → practice.

### Strategy 2: Concept-First
Read Context (1-2), Core Concepts (3-6), then jump to Code (15-16), referencing guides as needed.

### Strategy 3: Just-in-Time
Read Context (1-2) and Core Concepts (3-6), then reference specific guides as you encounter problems in the lab.

---

## Optional References

These documents are available but not part of the main reading flow:

- **📄 [Tech Stack Decisions](../../docs/tech-stack.md)** - Why we chose Llama, Ollama, Python, TypeScript
- **📄 [Progress Tracker](../progress.md)** - Track your learning journey

---

## Document Status

- ✅ All core concepts documented
- ✅ All guides written
- ✅ Architecture section complete
- ✅ Code examples included
- ✅ Navigation links added

---

**Ready to start?** Begin with [Page 1: Software Engineering Evolution](./concepts/software-engineering-evolution.md)
