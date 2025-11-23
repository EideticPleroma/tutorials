# Lesson 1 - Fundamentals: Progress Tracker

**Page 16 of 16** | [← Previous: Visualization Tools](./tutorial-1/architecture/visualization-tools.md) | [↑ Reading Guide](./tutorial-1/READING_GUIDE.md)

Track your progress through the lab exercises and documentation reading.

## 📚 Documentation Reading

### Phase 1: Foundation
- [ ] Page 1: [README.md](./README.md)
- [ ] Page 2: [Software Engineering Evolution](./tutorial-1/concepts/software-engineering-evolution.md)

### Phase 2: Core Concepts
- [ ] Page 3: [LLM Fundamentals](./tutorial-1/concepts/llm-fundamentals.md)
- [ ] Page 4: [Tool Calling Architecture](./tutorial-1/concepts/tool-calling-architecture.md)
- [ ] Page 5: [MCP Introduction](./tutorial-1/concepts/mcp-intro.md)
- [ ] Page 5a: [Tech Stack Decisions](./tutorial-1/concepts/tech-stack-decisions.md) (Optional)
- [ ] Page 6: [Testing Agents](./tutorial-1/concepts/testing-agents.md)
- [ ] Page 6a: [Architecture in AI Era](./tutorial-1/concepts/architecture-in-ai-era.md)

### Phase 3: Implementation Guides
- [ ] Page 7: [Prompting Techniques](./tutorial-1/guides/prompting.md)
- [ ] Page 8: [Context Management](./tutorial-1/guides/context-management.md)
- [ ] Page 9: [Engineering Best Practices](./tutorial-1/guides/engineering.md)
- [ ] Page 10: [Agentic Code Practices](./tutorial-1/guides/agentic-practices.md)
- [ ] Page 10a: [Package Structure Guide](./tutorial-1/guides/package-structure.md) (Reference)

### Phase 4: Advanced Architecture (Optional)
- [ ] Page 13: [Architecture Evolution](./tutorial-1/architecture/evolution.md)
- [ ] Page 14: [LLM Driven Design](./tutorial-1/architecture/llm-driven-design.md)
- [ ] Page 15: [Visualization Tools](./tutorial-1/architecture/visualization-tools.md)

---

## 🛠️ Lab 1: Building Your First Agent

### Setup Phase
- [ ] Completed [Setup Guide](./lab-1/setup-guide.md)
- [ ] Ollama is running (`curl localhost:11434`)
- [ ] Python environment is active
- [ ] IDE configured (Cursor/VS Code/Continue/Copilot/Manual)
- [ ] Baseline test: `python -m src.agent.simple_agent` works

---

### Exercise 1: Understanding the Agent
**[Go to Exercise](./lab-1/exercises/01-understanding-agent.md)**

- [ ] Task 1: Ran agent with verbose logging
- [ ] Task 2: Traced the code - found `chat()` method
- [ ] Task 2: Located `messages` list initialization in `__init__`
- [ ] Task 2: Found `tool_registry` queries
- [ ] Task 2: Understood second LLM call decision logic
- [ ] Task 3: Sketched the flow diagram
- [ ] Task 3: Compared with Tool Calling Architecture doc
- [ ] **Checkpoint**: Can explain why agent loops twice ✅

**Key Learning**: 
- 

---

### Exercise 2: Adding a Tool
**[Go to Exercise](./lab-1/exercises/02-adding-tools.md)**

- [ ] Step 1: Created `src/agent/tools/file_search.py`
- [ ] Step 1: Implemented `search_files(directory, pattern)` function
- [ ] Step 1: Function returns descriptive strings (not data structures)
- [ ] Step 1: Added error handling with error strings (no exceptions)
- [ ] Step 2: Added `@registry.register` decorator
- [ ] Step 2: Wrote comprehensive docstring with examples
- [ ] Step 3: Updated `src/agent/tools/__init__.py`
- [ ] Step 3: Added import in `src/agent/simple_agent.py` (with `# noqa: F401`)
- [ ] Step 4: Verified with test query: "Find all python files in tests/"
- [ ] Step 4: Verified with test query: "Find all files in data/"
- [ ] Step 4: Verified with test query: "Search for text files in data/"
- [ ] **Victory Checkpoint**: Tool works! 🎉

**Key Learning**: 
- 

---

### Exercise 3: Prompt Engineering
**[Go to Exercise](./lab-1/exercises/03-prompt-engineering.md)**

- [ ] Learning: Asked AI "What is a system prompt?"
- [ ] Learning: Asked AI "Explain Chain of Thought prompting"
- [ ] Learning: Asked AI about tool usage in system prompts
- [ ] Learning: Asked AI about few-shot prompting
- [ ] Step 1: Analyzed current prompt in `agent_config.py`
- [ ] Step 1: Identified what's missing
- [ ] Step 2: Modified prompt for tool usage clarity
- [ ] Step 2: Modified prompt for output quality
- [ ] Step 2: Modified prompt for error handling
- [ ] Step 3: Tested with "What tools are available?"
- [ ] Step 3: Tested with "Find Python files in tests/"
- [ ] Step 3: Tested with "What did you find?"
- [ ] Step 4: Iterated based on agent behavior
- [ ] Reflection: Documented what worked and what didn't
- [ ] **Victory Checkpoint**: Agent behavior improved! 🎉

**Key Learning**: 
- 

---

### Exercise 4: Testing Methodology
**[Go to Exercise](./lab-1/exercises/04-testing-methodology.md)**

- [ ] Step 1: Created `tests/unit/test_file_search.py`
- [ ] Step 2: Wrote unit test for existing files
- [ ] Step 2: Wrote unit test for invalid directory
- [ ] Step 2: Wrote unit test for no matches
- [ ] Step 3: Wrote E2E test using `AgentTestRunner`
- [ ] Step 3: Test validates tool calls
- [ ] Step 3: Test validates content keywords
- [ ] Step 4: Ran flakiness check (5 runs)
- [ ] Step 4: Achieved 5/5 passes consistently
- [ ] **Victory Checkpoint**: Tests pass reliably! 🎉

**Test Results**: 
- Unit tests: ___/3 passing
- E2E tests: ___/1 passing
- Flakiness: ___/5 runs successful

**Key Learning**: 
- 

---

### Exercise 5: Challenge - Read File (Optional)
**[Go to Exercise](./lab-1/exercises/05-challenge-read-file.md)**

- [ ] Step 1: Created `src/agent/tools/read_file.py`
- [ ] Step 1: Implemented `read_file(filename)` function
- [ ] Step 2: Error handling for missing files
- [ ] Step 2: Error handling for large files (>10MB)
- [ ] Step 2: Error handling for binary files
- [ ] Step 3: Added `@registry.register` decorator
- [ ] Step 3: Updated `tools/__init__.py`
- [ ] Step 3: Added import in `simple_agent.py`
- [ ] Testing: Created `tests/unit/test_read_file.py`
- [ ] Testing: Wrote test for existing file
- [ ] Testing: Wrote test for missing file
- [ ] Testing: Wrote test for large file
- [ ] Testing: Wrote test for binary file
- [ ] Testing: Wrote E2E test for single file read
- [ ] Testing: Wrote E2E test for chained search→read
- [ ] Verification: All 6+ tests pass consistently
- [ ] Verification: Agent chains tools successfully
- [ ] **CHALLENGE COMPLETE!** 🏆

**Test Results**: 
- Unit tests: ___/4 passing
- E2E tests: ___/2 passing
- Flakiness: ___/5 runs successful

**Key Learning**: 
- 

---

## 📝 Notes & Insights

### Technical Insights
*Record key technical learnings here*


### Challenges Faced
*What problems did you encounter and how did you solve them?*


### Questions for Further Exploration
*What do you want to learn more about?*


---

## 🎯 Completion Status

**Documentation**: ___/15 pages read
**Lab Exercises**: ___/4 completed (___/5 with challenge)
**Overall Progress**: ___%

**Estimated Time Spent**: ___ hours

**Ready for Lesson 2?** □ Yes □ Not yet

**What to expect in Lesson 2:**
- Multi-agent coordinator-worker patterns
- Agent specialization and communication
- Extended testing for multi-agent systems
- **📋 [View Tutorial 2 Scope](../../TUTORIAL-2-SCOPE.md)**

---

## 🚀 Next Steps

After completing Lesson 1:
- [ ] Review all key learnings
- [ ] Document personal insights above
- [ ] Set up repository for your own agent project
- [ ] Review [Tutorial 2 Scope](../../TUTORIAL-2-SCOPE.md) to prepare for multi-agent systems

---

**Last Updated**: _________________
**Current Focus**: _________________
