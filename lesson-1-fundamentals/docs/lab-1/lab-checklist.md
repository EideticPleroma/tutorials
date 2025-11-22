# Lab 1 Checklist

Use this checklist to track your progress through the lab.

## 0. Setup Phase
> **Need help?** Follow the [Detailed Setup Guide](./setup-guide.md).

- [x] **Environment Check**: Run `./setup.sh` and ensure all checks pass.
- [x] **LLM Check**: Run `ollama list` to confirm `llama3.1` (or similar) is available.
- [x] **Baseline Run**: Run `python -m src.agent.simple_agent` and ask "What is the time?".
- [x] **Test Check**: Run `pytest tests/` to confirm the baseline system is green.

## 1. Understanding the Agent
**[Go to Exercise 1](./exercises/01-understanding-agent.md)**
- [ ] Located the `chat()` method in `simple_agent.py` (line 49-100).
- [ ] Identified the `system_prompt` in `agent_config.py` (loaded in `__init__`).
- [ ] Traced the tool execution flow (registry lookup and tool call).
- [ ] Drawn (on paper or tool) the sequence of a "Get Weather" request.

## 2. Adding a New Tool
**[Go to Exercise 2](./exercises/02-adding-tools.md)**
- [ ] Created `src/agent/tools/file_search.py` (or added to existing file).
- [ ] Implemented `search_files(directory, pattern)`.
- [ ] Added `@registry.register` decorator.
- [ ] Added comprehensive docstring (Type hints, Description, Example).
- [ ] Imported the module in `simple_agent.py` to trigger registration.
- [ ] **Validation**: Agent can answer "Find all python files in src/".

## 3. Prompt Engineering
**[Go to Exercise 3](./exercises/03-prompt-engineering.md)**
- [ ] Modified `system_prompt` in `agent_config.py` to encourage Chain of Thought.
- [ ] Added a "Few-Shot" example for tool usage.
- [ ] Restarted the agent to load the updated prompt.
- [ ] **Validation**: Agent explains *why* it is taking an action before executing it.

## 4. Testing & Validation
**[Go to Exercise 4](./exercises/04-testing-methodology.md)**
- [ ] Created `tests/test_file_search.py`.
- [ ] Wrote a Unit Test for the `search_files` function directly.
- [ ] Wrote an E2E Test using `AgentTestRunner` to verify the agent calls the tool.
- [ ] **Evaluation**: Test suite passes 3 times in a row (checking for flakiness).

## 5. Challenge (Optional)
- [ ] Implement a `read_file` tool to allow the agent to read content.
- [ ] Ask the agent: "Find the file with 'Todo' in it and tell me what the todos are."
- [ ] Handle the error if the file is too large or binary.

