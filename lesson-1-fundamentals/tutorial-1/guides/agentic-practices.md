# Agentic Code Practices

**Page 13 of 16** | [← Previous: Engineering Best Practices](./engineering.md) | [Next: Package Structure Guide →](./package-structure.md) | [↑ Reading Guide](../READING_GUIDE.md)

Writing code *for* agents to use is different from writing code for humans.

## 1. Tool Design

Tools are the API for your agent.
*   **Descriptive Names**: `get_weather` is better than `weather`.
*   **Type Hints**: Essential. The agent uses these to understand what arguments to pass.
*   **Docstrings**: This is the "Prompt" for the tool. Be verbose.
    *   *Bad*: "Calculates stuff."
    *   *Good*: "Calculates the sum of two numbers. Returns an error if inputs are not numbers."

## 2. Robustness & Error Handling

Agents are clumsy. They will pass strings to integer fields. They will hallucinate file paths.
*   **Defensive Coding**: Your tools must handle bad inputs gracefully.
    *   Don't crash. Return a clear error string: `Error: File 'xyz' not found.`
    *   The agent can read this error and *correct itself* (e.g., try a different path).
*   **Retries**: If an agent fails a step, your system should allow it to retry with the error message as feedback.

## 3. Modularity

Keep tools small and atomic.
*   *Bad*: `manage_database()` (Too broad)
*   *Good*: `create_table()`, `insert_row()`, `query_data()`
*   Small tools allow the agent to compose complex workflows ("Plan -> Create Table -> Insert Data").

## 4. Determinism

Where possible, make tools deterministic.
*   If `get_time()` returns different seconds every time, it's hard to test.
*   Consider mocking time or external APIs during testing (see `tests/test_framework.py`).

