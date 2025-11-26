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

## 2. Few-Shot Prompting for Tools

Models often struggle to call tools correctly on the first try. Giving them examples ("shots") helps immensely.

### One-Shot Example (In System Prompt)
```text
User: Calculate 2+2
Assistant: { "tool": "calculate", "args": { "op": "add", "a": 2, "b": 2 } }
```

## 3. Chain of Thought (CoT)

Encourage the model to "think" before acting. This drastically improves complex reasoning.

**Without CoT:**
User: "Who is the president of the country where the Eiffel Tower is?"
Agent: *Calls tool `get_president("Eiffel Tower")`* -> Fail.

**With CoT:**
System: "Think step-by-step."
Agent:
1. "The Eiffel Tower is in Paris."
2. "Paris is in France."
3. "I need to find the president of France."
4. *Calls tool `get_president("France")`* -> Success.

## 4. Iterative Refinement (No One-Shot Magic)

Don't expect a perfect result from a single prompt.
*   **Draft**: Ask for a rough plan.
*   **Critique**: Ask the agent to find flaws in its own plan.
*   **Execute**: Ask it to execute the improved plan.

