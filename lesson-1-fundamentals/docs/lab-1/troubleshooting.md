# Troubleshooting Lab 1

## Common Issues

### 1. Agent Loops Forever
*   **Symptom**: The agent keeps calling the same tool or saying "I need to think" without acting.
*   **Cause**: The LLM output didn't match the expected JSON schema, so the system sent it back as "Invalid JSON", causing the LLM to retry endlessly.
*   **Fix**: Check your System Prompt. Ensure you explicitly force JSON format. Check `simple_agent.py` loop logic.

### 2. Tool Not Found
*   **Symptom**: `KeyError: 'search_files'`
*   **Cause**: You forgot to import the tool file in `simple_agent.py`. The decorator `@register_tool` only runs when the module is imported.
*   **Fix**: Add `import src.agent.tools.file_search` to the top of `simple_agent.py`.

### 3. "Connection Refused" (Ollama)
*   **Symptom**: `httpx.ConnectError`
*   **Cause**: Ollama is not running.
*   **Fix**: Run `ollama serve` in a separate terminal or ensure the Docker container is up.

### 4. Tests Fail Randomly (Flakiness)
*   **Symptom**: Test passes 4 times, fails the 5th.
*   **Cause**: LLMs are probabilistic.
*   **Fix**:
    *   Lower the `temperature` in `agent_config.py` (try 0.1 or 0.0).
    *   Make the System Prompt more strict.
    *   Use fuzzy matching in tests (e.g., `assert "15" in answer` instead of `assert answer == "15C"`).

### 5. Import Errors after Rename
*   **Symptom**: `ModuleNotFoundError: No module named 'tutorial-1'`
*   **Cause**: We renamed the project to `lesson-1-fundamentals` but some code/tests might still reference the old name.
*   **Fix**: Grep for `tutorial-1` and replace with `lesson-1-fundamentals` or relative imports.

### 6. Tools Directory Missing
*   **Symptom**: `ModuleNotFoundError: No module named 'src.agent.tools'`
*   **Cause**: You skipped creating the tools directory in Exercise 2.
*   **Fix**: Run `mkdir -p src/agent/tools` and `touch src/agent/tools/__init__.py`.

