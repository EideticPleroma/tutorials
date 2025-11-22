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
- [ ] Docker is running (`docker ps` works)
- [ ] Ollama is running (`curl localhost:11434` works)
- [ ] Python environment is active (`source venv/bin/activate` or similar)
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

*   Check the [Troubleshooting Guide](./troubleshooting.md).
*   Review the [Reference Documentation](../tutorial-1/READING_GUIDE.md).
*   Ask the AI: "Explain this error trace in the context of a Python tool calling loop."

