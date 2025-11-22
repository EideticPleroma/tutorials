# Exercise 4: Testing Methodology

**Goal**: Trust but Verify.

## Context
We use the O.V.E. (Observe, Validate, Evaluate) methodology.
*   **Observe**: Run the agent.
*   **Validate**: Check the structure (Did it return JSON? Did it call a tool?).
*   **Evaluate**: Check the quality (Did it answer the user's intent?).

**Note**: This exercise uses the test data files in `data/` (todos.txt, notes.txt, sample.py). These are provided in the repository for consistent testing.

## Steps

### 1. Create a Test File
Create `tests/unit/test_file_search.py`.

### 2. Unit Test (The Tool)
Test the Python function `search_files` in isolation.
*   Mock the filesystem (or use a temporary directory fixture).
*   Assert it finds the files it should.
*   Assert it returns an error string for invalid directories (don't raise Exceptions!).

### 3. E2E Test (The Agent)
Use the `AgentTestRunner` from `tests/test_framework.py`.

```python
from src.agent.simple_agent import Agent
from tests.test_framework import AgentTestRunner, TestCase

def test_agent_finds_files():
    agent = Agent()
    runner = AgentTestRunner(agent)
    
    case = TestCase(
        name="Find Python Files",
        prompt="Find python files in tests/",
        expected_tool_calls=["search_files"],
        expected_content_keywords=["test_framework.py"]
    )
    
    result = runner.run(case)
    
    assert result.passed_validation, f"Validation failed: {result.validation_errors}"
```

### 4. Flakiness Check
Run the test 5 times.
```bash
for i in {1..5}; do pytest tests/unit/test_file_search.py; done
```
If it fails once, your prompt might be ambiguous. Refine the prompt (Exercise 3) until it passes 5/5.

