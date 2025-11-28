# Lesson 2 - Multi-Agent Systems: Progress Tracker

**Page 10 of 10** | [← Previous: Hierarchical vs. Peer-to-Peer](./tutorial-2/architecture/hierarchical-vs-peer.md) | [↑ Reading Guide](./tutorial-2/READING_GUIDE.md)

Track your progress through the lab exercises and documentation reading.

## 📚 Documentation Reading

### Phase 1: Core Concepts
- [ ] Page 1: [Multi-Agent Architecture](./tutorial-2/concepts/multi-agent-architecture.md)
- [ ] Page 2: [Agent Specialization](./tutorial-2/concepts/agent-specialization.md)
- [ ] Page 3: [Agent Communication](./tutorial-2/concepts/agent-communication.md)
- [ ] Page 4: [State Management](./tutorial-2/concepts/state-management.md)

### Phase 2: Practical Guides
- [ ] Page 5: [Designing Agent Teams](./tutorial-2/guides/designing-agent-teams.md)
- [ ] Page 6: [Debugging Multi-Agent Systems](./tutorial-2/guides/debugging-multi-agent.md)
- [ ] Page 7: [Testing Multi-Agent Systems](./tutorial-2/guides/testing-multi-agent.md)

### Phase 3: Architecture Patterns
- [ ] Page 8: [Coordinator Patterns](./tutorial-2/architecture/coordinator-patterns.md)
- [ ] Page 9: [Hierarchical vs. Peer-to-Peer](./tutorial-2/architecture/hierarchical-vs-peer.md) (Optional)

### Additional Resources
- [ ] [Self-Assessment Quiz](./tutorial-2/self-assessment.md)
- [ ] [Case Studies](./tutorial-2/case-studies.md)

---

## 🛠️ Lab 2: Building Multi-Agent Systems

### Setup Phase
- [ ] Completed [Setup Guide](./lab-2/setup-guide.md)
- [ ] Ollama is running (`curl localhost:11434`)
- [ ] Python environment is active
- [ ] AI IDE configured (Cursor/VS Code/Continue/Cline/Copilot)
- [ ] Baseline test: `python -m pytest tests/ -v` works
- [ ] Read Tutorial 2 concepts (at minimum Pages 1-4)

---

### Exercise 0: Bridge - From Single to Multi-Agent (NEW)
**[Go to Exercise](./lab-2/exercises/00-bridge-refactoring.md)** | **Time**: ~45 minutes

> **Recommended for students coming from Tutorial 1.** This exercise bridges the gap between single-agent and multi-agent thinking.

- [ ] Step 1: Created GathererAgent with limited tools
- [ ] Step 2: Created ReporterAgent (LLM-only)
- [ ] Step 3: Wired two agents together
- [ ] Step 4: Reflected on the pattern
- [ ] **Checkpoint**: Understand why direct function calls don't scale

**Key Learning:**
- Responsibility splitting is the core multi-agent pattern
- Direct function calls work for 2 agents but not 5+

---

### Exercise 1A: Coordinator Basics
**[Go to Exercise](./lab-2/exercises/01a-coordinator-basics.md)** | **Time**: ~60 minutes

- [ ] Step 1: Initialized coordinator with mock agents
- [ ] Step 2: Implemented delegation with error handling
- [ ] Step 3: Implemented sequential workflow
- [ ] Step 4: Added basic retry logic
- [ ] Testing: Created `tests/multi_agent/test_coordinator_basics.py`
- [ ] **Checkpoint**: Coordinator orchestrates workers with direct calls

**Key Learning:**
- Coordinator orchestrates, workers execute
- Error handling at each delegation step

---

### Exercise 1B: Message Protocol
**[Go to Exercise](./lab-2/exercises/01b-message-protocol.md)** | **Time**: ~60 minutes

- [ ] Step 1: Implemented MessageType enum
- [ ] Step 2: Implemented Message class with all fields
- [ ] Step 3: Added JSON serialization (to_json/from_json)
- [ ] Step 4: Added helper methods (create_response/create_error)
- [ ] Step 5: Updated coordinator delegate() to use messages
- [ ] Step 6: Updated worker agents with execute_message()
- [ ] Testing: Created `tests/multi_agent/test_message_protocol.py`
- [ ] **Checkpoint**: Agents communicate via structured messages

**Key Learning:**
- Message protocol enables traceability and debugging
- trace_id groups related messages
- in_reply_to links responses to requests

---

### (Legacy) Exercise 1: Build a Coordinator Agent
**[Go to Exercise](./lab-2/exercises/01-coordinator-agent.md)** | **Time**: ~90 minutes

> **Note:** This exercise has been split into 1A and 1B above. If you completed this original exercise, skip to Exercise 2.

- [x] Step 1: Reviewed coordinator architecture and patterns
- [x] Step 2: Implemented coordinator initialization
- [x] Step 3: Created delegation logic for sequential execution
- [x] Step 4: Added error handling with retries
- [x] Step 5: Implemented message tracking
- [x] Step 6: Added result aggregation logic
- [x] Testing: Created `tests/multi_agent/test_coordinator.py`
- [x] Testing: Validated delegation to workers
- [x] Testing: Verified error handling
- [x] Testing: Confirmed message flow
- [x] **Checkpoint**: Coordinator orchestrates workers successfully ✅

**Key Learning**: 
- Coordinator orchestrates worker agents through message protocol with REQUEST/RESPONSE/ERROR types
- Retry logic with exponential backoff (1s, 2s, 4s) handles transient failures gracefully
- Custom exceptions (CoordinatorError, AgentDelegationError, WorkflowError) provide clear error hierarchy
- Sequential workflow validation at each step prevents cascading errors
- Structured JSON logging and file output enable debugging multi-agent interactions
- Trace IDs connect messages across the workflow for end-to-end tracking 

---

### Exercise 2: Create Specialized Agents
**[Go to Exercise](./lab-2/exercises/02-specialized-agents.md)** | **Time**: ~90 minutes

- [x] Step 1: Reviewed agent specialization principles
- [x] Step 2: Created Research Agent scaffold
- [x] Step 2: Implemented research tools and prompt
- [x] Step 2: Tested research agent independently
- [x] Step 3: Created Data Agent scaffold
- [x] Step 3: Implemented data analysis tools and prompt
- [x] Step 3: Tested data agent independently
- [x] Step 4: Created Writer Agent scaffold
- [x] Step 4: Implemented writing tools and prompt
- [x] Step 4: Tested writer agent independently
- [x] Testing: Created `tests/multi_agent/test_specialized_agents.py`
- [x] Testing: Validated specialization boundaries
- [x] Testing: Verified tool assignments
- [x] **Checkpoint**: All three agents work independently ✅

**Test Results**: 9/9 tests passing in `test_specialized_agents.py`

**Overall Test Summary**:
```bash
python -m pytest tests/multi_agent/ -v
# Result: 17 passed, 4 skipped in ~35s
# - Coordinator: 4/5 passed (1 skipped - requires Ollama)
# - Message Protocol: 4/4 passed
# - Specialized Agents: 9/9 passed
# - Integration: 0/3 passed (3 skipped - Exercise 4)
```

**Key Learning**: 
- Agent specialization enforced through focused system prompts and filtered tool access
- Research Agent: Uses `search_files` and `read_file` tools to gather information with citations
- Data Agent: Uses `calculate` tool to extract metrics and identify quantitative trends
- Writer Agent: LLM-only (no tools), synthesizes research and analysis into structured markdown reports
- Shared state enables sequential workflows: Research → Data → Writer
- Tool filtering in WorkerAgent ensures agents can only use their allowed_tools
- Structured parsing of LLM responses extracts findings, metrics, and insights for next agent
- Direct markdown generation in WriterAgent provides deterministic output for reliable testing 

---

### Exercise 3: Review Agent Communication
**[Go to Exercise](./lab-2/exercises/03-agent-communication.md)** | **Time**: ~60 minutes

**Note**: Message protocol was implemented in Exercises 1-2. This exercise focuses on review and validation.

- [x] Step 1: Reviewed message protocol specification
- [x] Step 2: Implemented Message class with all required fields
- [x] Step 3: Added message validation
- [x] Step 4: Implemented message routing in coordinator
- [x] Step 5: Added trace ID tracking for workflows
- [x] Step 6: Implemented request-response patterns
- [x] Step 7: Added error message handling
- [x] Testing: Created `tests/multi_agent/test_message_protocol.py`
- [x] Testing: Validated message structure
- [x] Testing: Verified trace ID continuity
- [x] Testing: Confirmed error propagation
- [x] Integration: Tested coordinator → worker → coordinator flow
- [x] **Checkpoint**: Agents communicate reliably ✅

**Test Results**: 4/4 tests passing in `test_message_protocol.py`
- test_message_creation ✅
- test_message_serialization ✅  
- test_response_message_links_to_request ✅
- test_error_message_format ✅

**Key Learning**: 
- Message protocol provides structured communication with traceability (message_id, timestamp, trace_id)
- MessageType enum defines three message types: REQUEST, RESPONSE, ERROR
- Coordinator uses Message protocol in delegate() method for all agent communication
- WorkerAgent.execute_message() wraps execute() with message protocol handling
- Trace IDs connect related messages across entire workflow for debugging
- JSON serialization enables logging and reconstruction of message flows
- in_reply_to field links responses back to original requests
- Error messages use ERROR type with error details in payload
- Message protocol was built early (Exercise 1) because coordinator delegation requires it 

---

### Exercise 4: Challenge - Research Workflow (Optional)
**[Go to Exercise](./lab-2/exercises/04-challenge-workflow.md)** | **Time**: ~120 minutes

- [ ] Step 1: Designed end-to-end workflow
- [ ] Step 2: Implemented user query parsing
- [ ] Step 3: Created sequential pipeline (research → data → writer)
- [ ] Step 4: Added parallel execution optimization (advanced)
- [ ] Step 5: Implemented shared state management
- [ ] Step 6: Added comprehensive error handling
- [ ] Step 7: Created final report formatting
- [ ] Testing: Created `tests/multi_agent/test_workflow.py`
- [ ] Testing: End-to-end test with sample query
- [ ] Testing: Validated state persistence
- [ ] Testing: Tested failure recovery
- [ ] Testing: Ran flakiness check (5 runs)
- [ ] Testing: Achieved 5/5 passes consistently
- [ ] Verification: Full workflow completes in 60-90 seconds
- [ ] **CHALLENGE COMPLETE!** 🏆

**Test Results**: 
- Unit tests: ___/3 agents passing
- Integration tests: ___/2 passing
- End-to-end workflow: ___/1 passing
- Flakiness: ___/5 runs successful

**Key Learning**: 
- 

---

## 📝 Notes & Insights

### Technical Insights
*Record key technical learnings about multi-agent systems*


### Challenges Faced
*What multi-agent problems did you encounter and how did you solve them?*


### Questions for Further Exploration
*What do you want to learn more about?*


---

## 🎯 Completion Status

**Documentation**: Review recommended pages as needed
**Lab Exercises**: 2/3 completed (2/4 with challenge)
**Test Results**: 13/13 tests passing (4 coordinator + 9 specialized agents + 4 message protocol - 4 integration pending)
**Overall Progress**: 67%

**Estimated Time Spent**: ~3-4 hours

**Ready for Tutorial 3?** □ Yes □ Not yet

**What to expect in Tutorial 3:**
- Memory systems and long-term context
- Vector databases and RAG
- Semantic search and retrieval
- Advanced state management

---

## 🚀 Next Steps

After completing Lesson 2:
- [ ] Review all key learnings about multi-agent systems
- [ ] Document personal insights above
- [ ] Build your own multi-agent workflow
- [ ] Explore hierarchical patterns for larger systems
- [ ] Share your multi-agent system with the community

---

## 🔍 Self-Assessment

Before marking Tutorial 2 complete:
- [ ] Can explain when to use multi-agent vs. single agent
- [ ] Can design specialized agents with clear boundaries
- [ ] Can implement message protocols for agent communication
- [ ] Can debug multi-agent interactions using trace IDs
- [ ] Can test multi-agent systems using extended O.V.E.
- [ ] Can handle failures and retries in coordination logic

---

**Last Updated**: November 24, 2025
**Current Focus**: Exercise 2 Complete ✅ - Exercise 3 (Message Protocol Review) and Exercise 4 (Challenge Workflow) Remaining

