# Exercise 2: Adding a Tool

**Goal**: Extend the Agent's capabilities.

## Context
An agent is only as smart as its tools. We will add a `search_files` tool that allows the agent to grep for code in your project.

## Steps

### 1. Create the Tool
Create `src/agent/tools/file_search.py`.
Implement a function `search_files(directory: str, pattern: str) -> str`.
*   Use `os.walk` or `glob`.
*   Return a **descriptive string** with the results (not a raw list!).
*   **Crucial**: Handle `FileNotFoundError` and return a friendly string like "Error: Directory not found".
*   **Agentic Best Practice**: Tools should return human-readable strings, not data structures. LLMs understand natural language better than raw lists.

### 2. Register the Tool
Import `registry` from `src.agent.tool_registry`.
Decorate your function with `@registry.register`.

```python
from src.agent.tool_registry import registry

@registry.register
def search_files(directory: str, pattern: str) -> str:
    """
    Search for files matching a pattern in a directory.
    
    Args:
        directory: The path to search in (e.g., "src/", "tests/")
        pattern: The file pattern to match (e.g., "*.py", "test_*.py")
    
    Returns:
        A string describing the results: list of files found, or an error message
    
    Examples:
        search_files("src/", "*.py") -> "Found 3 files: src/agent/simple_agent.py, ..."
        search_files("invalid/", "*.py") -> "Error: Directory not found"
    """
    # Your implementation here
    # Hint: Return descriptive strings like "Found 5 files: ..." or "Error: ..."
```

### 3. Make the Tool Importable
First, update `src/agent/tools/__init__.py` to import your tool:

```python
"""
Tools package for the agent.
Import tool modules here to ensure they get registered.
"""
from . import file_search

__all__ = ['file_search']
```

Then, in `src/agent/simple_agent.py`, add this import near the top (around line 8):

```python
from .tools import file_search  # noqa: F401
```

**Why this matters**: 
- The import triggers the `@registry.register` decorator, which adds your tool to the registry
- We use **relative imports** (`.tools`) since we're inside the `src.agent` package
- The `# noqa: F401` comment tells linters to ignore "unused import" warnings (this is a **side-effect import**)
- Without these imports, Python never loads the module, so the decorator never runs!

**Python Philosophy Note**: Every Python package directory should have an `__init__.py` file. This makes packages explicit and enables proper exports. See the [Package Structure Guide](../../tutorial-1/guides/package-structure.md) for details.

### 4. Verify
Run the agent and test with these queries:
1. "Find all python files in the tests directory."
2. "Find all files in the data directory."
3. "Search for text files in data/"

Expected behavior:
- Query 1: Should find test_framework.py, conftest.py, and any test files
- Query 2: Should find todos.txt, notes.txt, sample.py
- Query 3: Should find todos.txt and notes.txt (*.txt pattern)

The agent should call `search_files` and return descriptive results for each query

## Common Pitfalls
*   **Missing Docstring**: If you don't write a docstring, the Agent won't know how to use the tool.
*   **Wrong Type Hints**: The `tool_registry` uses type hints to build the JSON schema. Make sure they are correct.
*   **Returning Complex Types**: Return strings (natural language) instead of lists or dictionaries. Agents understand `"Found 3 files: ..."` better than `['file1', 'file2', 'file3']`.
*   **Raising Exceptions**: Return error strings like `"Error: Directory not found"` instead of raising exceptions. Let the agent handle the error gracefully.

