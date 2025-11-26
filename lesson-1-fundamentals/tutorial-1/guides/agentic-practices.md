# Agentic Code Practices

**Page 13 of 16** | [← Previous: Engineering Best Practices](./engineering.md) | [Next: Package Structure Guide →](./package-structure.md) | [↑ Reading Guide](../READING_GUIDE.md)

Writing code *for* agents to use is different from writing code for humans.

## 1. Tool Design

Tools are the API for your agent.
*   **Descriptive Names**: `get_weather` is better than `weather`.
*   **Type Hints**: Essential. The agent uses these to understand what arguments to pass.

### Docstrings: The "Prompt" for Your Tool
Your Python docstring is literally read by the LLM. If it's vague, the agent will fail.

**We enforce Google-Style Docstrings because they are highly structured.**

**Example:**
```python
def search_files(directory: str, pattern: str) -> list[str]:
    """
    Recursively search for files matching a pattern.

    Args:
        directory (str): The root path to start searching from.
                         Example: "src/agent"
        pattern (str): Glob pattern to match.
                       Example: "*.py"

    Returns:
        list[str]: A list of absolute file paths found.
                   Returns empty list if no matches.
    """
    # ... implementation
```

**Why this matters:**
1.  **Args Section**: Tells the agent *exactly* what format to generate (e.g., "glob pattern" vs "regex").
2.  **Returns Section**: Tells the agent what to expect back, so it can plan its next step ("I will receive a list of paths...").

## 2. Robustness & Error Handling

Agents are clumsy. They will pass strings to integer fields. They will hallucinate file paths.
*   **Defensive Coding**: Your tools must handle bad inputs gracefully.
    *   **Don't Raise Exceptions**: Catch them and return a string!
    *   *Bad*: `raise FileNotFoundError()` -> Crash.
    *   *Good*: `return "Error: File not found. Please check the path."` -> Agent reads error, tries again.

## 3. Modularity

Keep tools small and atomic.
*   *Bad*: `manage_database()` (Too broad)
*   *Good*: `create_table()`, `insert_row()`, `query_data()`
*   Small tools allow the agent to compose complex workflows ("Plan -> Create Table -> Insert Data").

## 4. Determinism

Where possible, make tools deterministic.
*   If `get_time()` returns different seconds every time, it's hard to test.
*   Consider mocking time or external APIs during testing (see `tests/test_framework.py`).
