# Software Engineering Best Practices for Agentic AI

**Page 9 of 15** | [← Previous: Context Management](./context-management.md) | [Next: Agentic Code Practices →](./agentic-practices.md) | [↑ Reading Guide](../READING_GUIDE.md)

## Terminal Productivity

Agents live in the code, but you live in the terminal.

### Aliases
Create aliases for repetitive tasks to speed up your "human-in-the-loop" workflow.
```bash
# In .bashrc or setup script
alias agent="python3 src/agent/simple_agent.py"
alias test="pytest tests/"
alias lint="flake8 src/"
```

### History
Use `Ctrl+R` to search command history. Don't type the same long docker command twice.

## Git Workflow

AI can generate code fast, which means you can break things fast.

1.  **Micro-Commits**: Commit after every successful "featurelet" the agent generates.
    *   "Agent implemented calculate tool" -> Commit.
    *   "Agent added tests" -> Commit.
    *   This gives you save points to revert to if the agent goes off the rails.
2.  **Branch per Task**: Never let an agent work directly on `main`. Create a branch `feat/agent-weather-tool`.

## Code Review

You are the Lead Engineer; the Agent is the Junior Dev.
*   **Never copy-paste blindly**.
*   Read every line.
*   Ask: "Why did you import this?" "Is this variable name clear?"
*   If the code looks complex, ask the agent to "Simplify this" before accepting it.

## Observability

If the agent fails, you need to know *why*.
*   **Log Everything**: Inputs, system prompts, tool calls, raw outputs.
*   **Trace IDs**: If you have a complex chain, tag all logs with a unique request ID.

