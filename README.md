# Lesson 1: Fundamentals of Agentic AI

**Page 1 of 15** | [Next: Software Engineering Evolution →](./lesson-1-fundamentals/docs/tutorial-1/concepts/software-engineering-evolution.md) | [📚 Reading Guide](./lesson-1-fundamentals/docs/tutorial-1/READING_GUIDE.md)

Welcome to the first lesson in the Agentic AI series. This lesson focuses on building a foundational understanding of agentic AI by creating a local agent with tool-calling capabilities, implementing testing methodologies, and establishing best practices for AI-assisted development.

> **📖 New to this lesson?** Start with the [Reading Guide](./lesson-1-fundamentals/docs/tutorial-1/READING_GUIDE.md) to understand the recommended reading order.

## Quick Start

1.  **Prerequisites**:
    *   Windows 11 with WSL2 enabled (or Mac/Linux)
    *   **AI-Capable IDE** (choose one):
        - [Cursor](https://cursor.sh/) - AI-first IDE, best for learning
        - [VS Code](https://code.visualstudio.com/) with [Continue](https://continue.dev/) - Free, powerful
        - [VS Code](https://code.visualstudio.com/) with [Cline](https://github.com/cline/cline) - Agentic AI (formerly Claude Dev)
        - [VS Code](https://code.visualstudio.com/) with [GitHub Copilot](https://github.com/features/copilot) - Quick suggestions
        - Any text editor (manual AI consultation)
    *   [Ollama](https://ollama.com/) installed (for running local LLMs)

2.  **Setup**:
    Run the setup script to configure your environment:
    ```bash
    ./setup.sh
    ```
    
    **IDE-Specific Setup**: See [IDE Setup Guide](./lesson-1-fundamentals/docs/lab-1/setup-guide.md#ide-setup) for configuration instructions.

3.  **Run the Agent**:
    ```bash
    python -m src.agent.simple_agent
    ```

## Structure

*   `src/agent/`: Source code for the agent and tools.
*   `tests/`: Unit and integration tests.
*   `lesson-1-fundamentals/docs/tutorial-1/`: Conceptual documentation and guides.
*   `lesson-1-fundamentals/docs/lab-1/`: Hands-on exercises and checklist.
*   `scripts/`: Helper scripts.

## Documentation

This lesson includes comprehensive documentation organized into concepts, guides, and advanced architecture.

**📚 [Start with the Reading Guide](./lesson-1-fundamentals/docs/tutorial-1/READING_GUIDE.md)** - Recommended reading order and navigation
**📑 [Documentation Index](./lesson-1-fundamentals/docs/tutorial-1/INDEX.md)** - Quick reference to all documents

### Documentation Overview

**Concepts** (Pages 2-6a): Foundation knowledge
- [Software Engineering Evolution](./lesson-1-fundamentals/docs/tutorial-1/concepts/software-engineering-evolution.md)
- [LLM Fundamentals](./lesson-1-fundamentals/docs/tutorial-1/concepts/llm-fundamentals.md)
- [Tool Calling Architecture](./lesson-1-fundamentals/docs/tutorial-1/concepts/tool-calling-architecture.md)
- [Architecture in AI Era](./lesson-1-fundamentals/docs/tutorial-1/concepts/architecture-in-ai-era.md)

**Guides** (Pages 7-10): Practical techniques
- [Prompting Techniques](./lesson-1-fundamentals/docs/tutorial-1/guides/prompting.md)
- [Context Management](./lesson-1-fundamentals/docs/tutorial-1/guides/context-management.md)
- [Engineering Best Practices](./lesson-1-fundamentals/docs/tutorial-1/guides/engineering.md)

**Advanced Architecture** (Pages 13-15):
- [Evolution](./lesson-1-fundamentals/docs/tutorial-1/architecture/evolution.md)
- [LLM Driven Design](./lesson-1-fundamentals/docs/tutorial-1/architecture/llm-driven-design.md)
- [Visualization Tools](./lesson-1-fundamentals/docs/tutorial-1/architecture/visualization-tools.md)

## Lab 1: Build Your First Agent

Put theory into practice. The lab provides hands-on exercises to extend the agent.

👉 **[Go to Lab 1](./lesson-1-fundamentals/docs/lab-1/README.md)**

## Goals

By the end of this lesson, you will understand:
*   How LLMs, tool calling, and MCP work together.
*   How to set up a local agentic AI environment.
*   The Observe-Validate-Evaluate testing methodology.
*   How to architect systems using AI as a partner.
