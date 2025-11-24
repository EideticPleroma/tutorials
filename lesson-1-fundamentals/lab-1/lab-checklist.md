# Lab 1 Checklist

Use this checklist to track your progress through the lab.

## 0. Setup Phase
> **Need help?** Follow the [Detailed Setup Guide](./setup-guide.md).

- [ ] **Environment Check**: Run `./setup.sh` and ensure all checks pass.
- [ ] **LLM Check**: Run `ollama list` to confirm `llama3.1:8b` is available.
- [ ] **Baseline Run**: Run `python -m src.agent.simple_agent` and ask "What is the weather in Paris?".
- [ ] **Test Check**: Run `pytest tests/` to confirm the baseline system is green.

## 1. Understanding the Agent
**[Go to Exercise 1](./exercises/01-understanding-agent.md)**
- [ ] Located the `chat()` method in `simple_agent.py`.
- [ ] Identified the `system_prompt` in `agent_config.py`.
- [ ] Traced the tool execution flow (registry lookup and tool call).
- [ ] Understood the ReAct loop and two-step LLM call pattern.

## 2. Adding a New Tool
**[Go to Exercise 2](./exercises/02-adding-tools.md)**
- [ ] Created `src/agent/tools/file_search.py` with proper package structure.
- [ ] Implemented `search_files(directory, pattern)` returning descriptive strings.
- [ ] Added `@registry.register` decorator.
- [ ] Added comprehensive docstring (Type hints, Args, Returns, Examples).
- [ ] Imported the module in `simple_agent.py` to trigger registration.
- [ ] **Validation**: Agent successfully uses search_files tool.

## 3. Prompt Engineering
**[Go to Exercise 3](./exercises/03-prompt-engineering.md)**
- [ ] Modified `system_prompt` in `agent_config.py` for tool usage clarity.
- [ ] Learned CoT must be compatible with structured tool calling.
- [ ] Updated prompt to use natural language guidance (not text templates).
- [ ] **Validation**: Agent correctly calls tools using structured API.

## 4. Testing & Validation
**[Go to Exercise 4](./exercises/04-testing-methodology.md)**
- [ ] Created `tests/unit/test_file_search.py` with O.V.E. methodology.
- [ ] Wrote 3 Unit Tests (all passing).
- [ ] Wrote E2E Test using `AgentTestRunner` (passing).
- [ ] **Evaluation**: Flakiness test passes 5/5 runs consistently.

## 5. Challenge (Optional)
**[Go to Challenge](./exercises/05-challenge-read-file.md)**
- [ ] Implemented `read_file` tool with comprehensive error handling.
- [ ] Handles: missing files, large files (>10MB), binary files.
- [ ] Created complete test suite (6+ tests).
- [ ] **Validation**: Agent successfully chains search_files → read_file tools.

