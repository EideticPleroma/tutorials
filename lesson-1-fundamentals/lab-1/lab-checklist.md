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
- [x] Located the `chat()` method in `simple_agent.py` (line 49-100).
- [x] Identified the `system_prompt` in `agent_config.py` (loaded in `__init__`).
- [x] Traced the tool execution flow (registry lookup and tool call).
- [x] Understood the ReAct loop and two-step LLM call pattern.

## 2. Adding a New Tool
**[Go to Exercise 2](./exercises/02-adding-tools.md)**
- [x] Created `src/agent/tools/file_search.py` with proper package structure.
- [x] Implemented `search_files(directory, pattern)` returning descriptive strings.
- [x] Added `@registry.register` decorator.
- [x] Added comprehensive docstring (Type hints, Args, Returns, Examples).
- [x] Imported the module in `simple_agent.py` to trigger registration.
- [x] **Validation**: Agent successfully uses search_files tool.

## 3. Prompt Engineering
**[Go to Exercise 3](./exercises/03-prompt-engineering.md)**
- [x] Modified `system_prompt` in `agent_config.py` for tool usage clarity.
- [x] Learned CoT must be compatible with structured tool calling.
- [x] Updated prompt to use natural language guidance (not text templates).
- [x] **Validation**: Agent correctly calls tools using structured API.

## 4. Testing & Validation
**[Go to Exercise 4](./exercises/04-testing-methodology.md)**
- [x] Created `tests/unit/test_file_search.py` with O.V.E. methodology.
- [x] Wrote 3 Unit Tests (all passing):
  - `test_file_search_finds_existing_files` ✅
  - `test_file_search_handles_invalid_directory` ✅
  - `test_file_search_returns_empty_for_no_matches` ✅
- [x] Wrote E2E Test using `AgentTestRunner` (passing):
  - `test_agent_uses_file_search_tool` ✅
- [x] **Evaluation**: Flakiness test passes 5/5 runs consistently! ✅
  - `test_agent_file_search_multiple_runs` - 100% reliable

## 5. Challenge (Optional)
**[Go to Challenge](./exercises/05-challenge-read-file.md)**
- [ ] Implemented `read_file` tool with comprehensive error handling.
- [ ] Handles: missing files, large files (>10MB), binary files.
- [ ] Created complete test suite (6+ tests).
- [ ] **Validation**: Agent successfully chains search_files → read_file tools.

