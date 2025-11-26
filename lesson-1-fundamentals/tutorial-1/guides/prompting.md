# Prompting Techniques for Agentic AI

**Page 10 of 16** | [← Previous: Visualization Tools](../architecture/visualization-tools.md) | [Next: Context Management →](./context-management.md) | [↑ Reading Guide](../READING_GUIDE.md)

Prompting an agent is different from prompting a chatbot. You are not just asking for text; you are programming behavior with natural language.

## 1. System Prompts: The Agent's "OS"

The system prompt is the most critical component. It defines:
*   **Persona**: "You are a senior data scientist..."
*   **Capabilities**: "You have access to a SQL database and a Python repl..."
*   **Constraints**: "Never delete data. Always ask for confirmation before modifying tables."
*   **Format**: "Output your reasoning step-by-step before calling a tool."

### Example (Good)
```text
You are a coding assistant.
Your goal is to help the user write clean, tested Python code.
RULES:
1. Always write tests before implementation (TDD).
2. Use the 'read_file' tool to understand the existing codebase before suggesting changes.
3. If you are unsure, ask clarifying questions.
```

## 2. Core Techniques

### Few-Shot Prompting
Models often struggle to call tools correctly on the first try. Giving them examples ("shots") helps immensely.

**One-Shot Example (In System Prompt):**
```text
User: Calculate 2+2
Assistant: { "tool": "calculate", "args": { "op": "add", "a": 2, "b": 2 } }
```

### Chain of Thought (CoT)
Encourage the model to "think" before acting. This drastically improves complex reasoning.

**Without CoT:**
> User: "Who is the president of the country where the Eiffel Tower is?"
> Agent: *Calls tool `get_president("Eiffel Tower")`* -> **Fail.**

**With CoT:**
> System: "Think step-by-step."
> Agent:
> 1. "The Eiffel Tower is in Paris."
> 2. "Paris is in France."
> 3. "I need to find the president of France."
> 4. *Calls tool `get_president("France")`* -> **Success.**

## 3. Advanced Prompting Overview

As you progress to more complex agents, you will encounter advanced patterns. These are covered in depth in **Lesson 3 and 4**, but here is a high-level overview of what's possible:

### 🚀 ReAct (Reason + Act)
A specialized loop where the agent explicitly writes: **Thought**, **Action**, **Observation**.
*   *Thought*: I need to check the file size.
*   *Action*: `get_file_size('data.csv')`
*   *Observation*: 400MB.
*   *Thought*: That is too big to read into memory. I will use pandas chunking.

### 🌳 Tree of Thoughts (ToT)
Asking the agent to generate multiple possible solutions ("branches"), evaluate each one self-critically, and then pursue the most promising path.
*   *Used for*: Complex architectural decisions or debugging hard bugs.

### 🛡️ Constitutional AI
Giving the agent a "Constitution" (a set of high-level principles like "Be harmless", "Respect privacy") and asking it to critique its own output against these principles before showing it to the user.

## 4. Iterative Refinement (No One-Shot Magic)

Don't expect a perfect result from a single prompt.
*   **Draft**: Ask for a rough plan.
*   **Critique**: Ask the agent to find flaws in its own plan.
*   **Execute**: Ask it to execute the improved plan.
