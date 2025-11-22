# The Evolution of Software Engineering

**Page 2 of 15** | [← Previous: README](../../../README.md) | [Next: LLM Fundamentals →](./llm-fundamentals.md) | [↑ Reading Guide](../READING_GUIDE.md)

Agentic AI is not just a new tool; it's a new way of working. As we move from "writing code" to "orchestrating intelligence," our daily workflows are shifting.

## From Syntax to Semantics

*   **Old**: Memorizing syntax, standard libraries, and boilerplate.
*   **New**: Focusing on system architecture, data flow, and *intent*. The AI handles the syntax; you handle the logic and verification.

## The New Development Loop

1.  **Spec via Prompt**: You describe the intent to the IDE/Agent.
2.  **Generation**: The agent proposes code or changes.
3.  **Review & Refine**: You act as the Senior Engineer reviewing a Junior's code. You spot logical errors, security flaws, or architectural misalignments.
4.  **Iteration**: You don't rewrite; you *re-prompt* or tweak the context to guide the agent to the solution.

## Why Iteration > Perfection

In this new paradigm, trying to write the perfect prompt (One-Shot) is often less efficient than a quick interactive dialogue.
*   Start with a rough idea.
*   Let the agent generate a scaffold.
*   Critique it: "Make this more modular," "Handle this edge case."
*   This interactive "REPL for Code" is faster and often produces better results because the context builds up over time.

## Verification is King

As generation becomes cheap (near zero cost), **verification** becomes the most valuable skill.
*   You must be able to look at code and *know* if it's right without writing it yourself.
*   Testing frameworks (like the one we build in this tutorial) become your safety net, allowing you to trust the agent's output.

## The Agentic Tech Stack

*   **Python**: The lingua franca of AI.
*   **TypeScript/Node**: The glue of the web and now the standard for MCP.
*   **Local LLMs (Ollama)**: Development requires fast, free loops. Waiting for API calls or paying per token kills the flow.
*   **Vector DBs**: Long-term memory for agents (covered in later tutorials).

