# Lab 2: Checklist

Track your progress through Lab 2: Building Multi-Agent Systems.

## Prerequisites ✅

Before starting the lab:
- [ ] Completed Tutorial 1: Fundamentals
- [ ] Read Tutorial 2 concepts (minimum Pages 1-4)
- [ ] Ollama is running (`curl localhost:11434` works)
- [ ] Python environment active
- [ ] Can import `from src.multi_agent import Coordinator`
- [ ] Reviewed [Lab 2 README](./README.md)

**Not ready?** See [Setup Guide](./setup-guide.md)

---

## Exercise 1: Build a Coordinator Agent (~90 min)

**Goal:** Implement coordinator that orchestrates worker agents

### Phase 1: Core Structure
- [ ] Read [Exercise 1](./exercises/01-coordinator-agent.md)
- [ ] Review `src/multi_agent/coordinator.py` scaffold
- [ ] Understand coordinator responsibilities
- [ ] Review coordinator patterns from [Page 8](../tutorial-2/architecture/coordinator-patterns.md)

### Phase 2: Implementation
- [ ] Implement `__init__()` - Initialize coordinator with workers
- [ ] Implement `delegate()` - Send tasks to worker agents
- [ ] Implement `execute_sequential()` - Execute research → data → writer
- [ ] Add error handling and retries
- [ ] Implement result aggregation

### Phase 3: Testing
- [ ] Run `test_coordinator_initialization()`
- [ ] Run `test_sequential_delegation()`
- [ ] Run `test_error_handling()`
- [ ] All coordinator tests pass

### Phase 4: Validation
- [ ] Coordinator can delegate to mock workers
- [ ] Sequential execution works (correct order)
- [ ] Error handling catches failures
- [ ] Logs show clear message flow

**Checkpoint:** Can your coordinator orchestrate three mock agents in sequence?

---

## Exercise 2: Create Specialized Agents (~90 min)

**Goal:** Build research, data, and writer agents

### Phase 1: Research Agent
- [ ] Read [Exercise 2](./exercises/02-specialized-agents.md)
- [ ] Review `src/multi_agent/specialized/research_agent.py` scaffold
- [ ] Implement `gather_info()` method
- [ ] Assign research tools (web_search, read_file)
- [ ] Write focused system prompt
- [ ] Test research agent independently
- [ ] Agent writes findings to shared state

### Phase 2: Data Agent
- [ ] Review `src/multi_agent/specialized/data_agent.py` scaffold
- [ ] Implement `analyze_trends()` method
- [ ] Assign analysis tools (calculate, analyze)
- [ ] Write focused system prompt
- [ ] Test data agent independently
- [ ] Agent reads from shared state, writes analysis

### Phase 3: Writer Agent
- [ ] Review `src/multi_agent/specialized/writer_agent.py` scaffold
- [ ] Implement `create_report()` method
- [ ] Assign writing tools (format_markdown)
- [ ] Write focused system prompt
- [ ] Test writer agent independently
- [ ] Agent synthesizes research + analysis

### Phase 4: Integration Testing
- [ ] Run research → data → writer with shared state
- [ ] Verify each agent uses only its assigned tools
- [ ] Check agents stay within specialization boundaries
- [ ] All specialized agent tests pass

**Checkpoint:** Can each agent execute its role independently and write to shared state?

---

## Exercise 3: Implement Agent Communication (~60 min)

**Goal:** Build message protocol for agent interactions

### Phase 1: Message Protocol
- [ ] Read [Exercise 3](./exercises/03-agent-communication.md)
- [ ] Review `src/multi_agent/message_protocol.py` scaffold
- [ ] Implement `Message` class with serialization
- [ ] Add message types: request, response, error
- [ ] Implement `to_json()` and `from_json()`
- [ ] Test message serialization

### Phase 2: Integration with Coordinator
- [ ] Update coordinator to use Message protocol
- [ ] Implement `send_message()` in coordinator
- [ ] Add message logging (trace IDs)
- [ ] Workers send responses using Message
- [ ] Test message flow end-to-end

### Phase 3: Error Messages
- [ ] Implement error message handling
- [ ] Test timeout scenarios
- [ ] Test partial failure responses
- [ ] Verify error messages propagate correctly

### Phase 4: Validation
- [ ] All messages have required fields
- [ ] Request-response matching works
- [ ] Message logs are readable
- [ ] All communication tests pass

**Checkpoint:** Can you trace a complete user request through message logs?

---

## Exercise 4: Challenge - Research Workflow (~120 min, Optional)

**Goal:** Build end-to-end research → analyze → report workflow

### Phase 1: Workflow Design
- [ ] Read [Exercise 4](./exercises/04-challenge-workflow.md)
- [ ] Design agent team for research report
- [ ] Map dependencies and workflow
- [ ] Define success criteria

### Phase 2: Implementation
- [ ] Implement end-to-end coordinator flow
- [ ] Handle user query parsing
- [ ] Execute research phase
- [ ] Execute analysis phase
- [ ] Execute writing phase
- [ ] Return formatted report

### Phase 3: Advanced Features (Choose 1+)
- [ ] Parallel execution for independent tasks
- [ ] Quality gates between phases
- [ ] Iterative refinement (retry if quality low)
- [ ] Progress reporting to user

### Phase 4: Testing & Evaluation
- [ ] Write integration tests
- [ ] Test with real user queries
- [ ] Measure execution time
- [ ] Evaluate output quality
- [ ] All challenge tests pass

**Checkpoint:** Can your system generate a complete research report from a single user query?

---

## Completion Criteria 🎯

You've successfully completed Lab 2 when:

### Core Implementation
- [ ] Coordinator orchestrates multiple agents
- [ ] Three specialized agents work independently
- [ ] Message protocol handles all communication
- [ ] Shared state persists data correctly
- [ ] Error handling and retries work

### Testing
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Can trace workflows through logs
- [ ] Messages are well-formed

### End-to-End
- [ ] User query → Coordinator → Agents → Report works
- [ ] System completes in reasonable time (<2 min)
- [ ] Output quality is good (human-readable, accurate)

### Optional Challenge
- [ ] Completed Exercise 4 with advanced features
- [ ] System handles edge cases gracefully

---

## Time Tracking

Record your actual time spent:

| Exercise | Estimated | Actual | Notes |
|----------|-----------|--------|-------|
| Exercise 1: Coordinator | 90 min | ___ min | |
| Exercise 2: Specialized Agents | 90 min | ___ min | |
| Exercise 3: Communication | 60 min | ___ min | |
| Exercise 4: Challenge | 120 min | ___ min | Optional |
| **Total** | **4-6 hours** | **___ hours** | |

---

## Debugging Checklist

If stuck on an exercise:
1. [ ] Read the relevant tutorial page
2. [ ] Review the error message carefully
3. [ ] Check the [Troubleshooting Guide](./troubleshooting.md)
4. [ ] Try the AI assistant prompts provided
5. [ ] Use [Getting Unstuck Guide](./getting-unstuck.md)
6. [ ] Check [FAQ](./FAQ.md) for your specific issue

---

## Post-Lab Reflection

After completing Lab 2, consider:
- [ ] What was the hardest part?
- [ ] How did using AI assistance change your workflow?
- [ ] What would you do differently next time?
- [ ] What multi-agent systems could you build for real projects?

---

## Next Steps

After Lab 2:
1. **Experiment:** Build custom multi-agent workflows
2. **Optimize:** Try different coordination patterns
3. **Scale:** Add more agents or hierarchical coordination
4. **Share:** Post your work in the community
5. **Continue:** Start Tutorial 3 (Memory & RAG)

---

**Ready to start?** Go to [Exercise 1: Build a Coordinator Agent](./exercises/01-coordinator-agent.md)

**Need help?** See [Getting Unstuck Guide](./getting-unstuck.md)

**Track progress:** Check off tasks as you complete them!

