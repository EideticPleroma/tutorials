# Tutorial 2: Reading Guide & Documentation Order

This guide provides the recommended reading order for Tutorial 2: Multi-Agent Systems. Follow this sequence to build your understanding progressively.

## Reading Path Overview

The tutorial is organized into **4 phases** with **9 core documents**. Each phase builds on the previous one.

**Estimated Reading Time**: ~2.5 hours for all documentation
**Recommended Approach**: Read concepts first, then reference guides as you build in Lab 2.

---

## Prerequisites Check

Before starting Tutorial 2, ensure you've completed Tutorial 1:

- [ ] Completed [Tutorial 1: Fundamentals](../../../lesson-1-fundamentals/docs/tutorial-1/READING_GUIDE.md)
- [ ] Built a working single agent with custom tools
- [ ] Understand the 7-step tool calling loop
- [ ] Familiar with O.V.E. testing methodology
- [ ] Can debug agent behaviors using logs

**Not sure?** Review [Tutorial 1 Concepts](../../../lesson-1-fundamentals/docs/tutorial-1/concepts/tool-calling-architecture.md) before continuing.

---

## Phase 1: Core Concepts (Pages 1-4)

### Page 1: Multi-Agent Architecture (~15 min)
**📄 [Multi-Agent Architecture](./concepts/multi-agent-architecture.md)**
- What is a multi-agent system?
- When to use multiple agents vs. single agent
- Coordination patterns (coordinator-worker, peer-to-peer, hierarchical)
- Benefits and challenges
- **Why First**: Establishes when and why to use multi-agent

### Page 2: Agent Specialization (~15 min)
**📄 [Agent Specialization](./concepts/agent-specialization.md)**
- Specialist vs. generalist trade-offs
- Tool assignment strategies
- Prompt engineering for specialized behavior
- Example personas (research, data, writer)
- **Critical**: Learn how to design focused agents

### Page 3: Agent Communication (~15 min)
**📄 [Agent Communication](./concepts/agent-communication.md)**
- Message passing fundamentals
- JSON-based message protocol
- Request-response patterns
- Error handling in messaging
- **Important**: Understand how agents talk to each other

### Page 4: State Management (~10 min)
**📄 [State Management](./concepts/state-management.md)**
- Shared vs. isolated agent state
- File-based state implementation
- State consistency challenges
- When to use shared state vs. messages
- **Foundation**: Learn how agents share data

---

## Phase 2: Practical Guides (Pages 5-7)

### Page 5: Designing Agent Teams (~20 min)
**📄 [Designing Agent Teams](./guides/designing-agent-teams.md)**
- Systematic design process (6 steps)
- Task decomposition strategies
- Agent specification templates
- Workflow design patterns
- **Actionable**: Use this when planning your multi-agent system

### Page 6: Debugging Multi-Agent Systems (~15 min)
**📄 [Debugging Multi-Agent Systems](./guides/debugging-multi-agent.md)**
- Structured logging with trace IDs
- Message flow tracing
- Common failure modes (6+ types)
- Debugging checklist
- **Essential**: Learn to troubleshoot before you need it

### Page 7: Testing Multi-Agent Systems (~15 min)
**📄 [Testing Multi-Agent Systems](./guides/testing-multi-agent.md)**
- Extending O.V.E. for multi-agent
- Testing pyramid (unit, interaction, integration)
- Testing coordination logic
- Mocking strategies
- **Quality**: Build reliable multi-agent systems

---

## Phase 3: Architecture Patterns (Pages 8-9)

### Page 8: Coordinator Patterns (~20 min)
**📄 [Coordinator Patterns](./architecture/coordinator-patterns.md)**
- Sequential pipeline pattern
- Parallel execution pattern
- Conditional branching pattern
- Iterative refinement pattern
- Delegation and aggregation strategies
- **Advanced**: Master coordination techniques

### Page 9: Hierarchical vs. Peer-to-Peer (~15 min) ⚠️ OPTIONAL
**📄 [Hierarchical vs. Peer-to-Peer](./architecture/hierarchical-vs-peer.md)** 
- **Advanced Preview:** Beyond Tutorial 2 scope
- When to scale beyond coordinator-worker (10+ agents)
- Hierarchical multi-level coordination (Tutorial 3+)
- Peer-to-peer architectures (Tutorial 4)
- Comparison and trade-offs
- **Recommendation**: Skip for now, return after Lab 2

---

## Phase 4: Hands-On Practice

### Lab 2: Build Multi-Agent Systems (4-6 hours)
**📄 [Lab 2 README](../../lab-2/README.md)**
- Exercise 1: Build coordinator agent (~90 min)
- Exercise 2: Create specialized agents (~90 min)
- Exercise 3: Implement communication (~60 min)
- Exercise 4: Challenge workflow (~120 min, optional)
- **Action**: Apply everything you've learned

---

## Quick Reference: By Topic

### If you want to understand...
- **When to use multi-agent**: Page 1 (Multi-Agent Architecture)
- **How to design specialized agents**: Page 2 (Agent Specialization)
- **How agents communicate**: Page 3 (Agent Communication)
- **How to share state**: Page 4 (State Management)
- **How to design a system**: Page 5 (Designing Agent Teams)
- **How to debug issues**: Page 6 (Debugging Multi-Agent)
- **How to test thoroughly**: Page 7 (Testing Multi-Agent)
- **Advanced coordination**: Page 8 (Coordinator Patterns)
- **How to scale**: Page 9 (Hierarchical vs. Peer-to-Peer)

---

## Navigation

Each document includes:
- **Previous**: Link to the previous page in sequence
- **Next**: Link to the next page in sequence
- **Up**: Link back to this reading guide
- **Related**: Cross-references to Tutorial 1 when applicable

---

## Reading Strategies

### Strategy 1: Linear (Recommended for Most)
Read pages 1-9 in order. This builds knowledge systematically.

**Timeline:**
- Day 1: Read concepts (Pages 1-4, ~55 min)
- Day 2: Read guides (Pages 5-7, ~50 min)
- Day 3: Read architecture (Pages 8-9, ~35 min)
- Day 4-5: Complete Lab 2 (4-6 hours)

### Strategy 2: Concept-First
Read all concepts and architecture (Pages 1-4, 8-9) before guides. Good for those who want theory before practice.

### Strategy 3: Just-in-Time
Read concepts (Pages 1-4), start Lab 2, reference guides as needed. Good for hands-on learners.

### Strategy 4: Quick Start
1. Read Page 1 (Multi-Agent Architecture)
2. Read Page 5 (Designing Agent Teams)
3. Start Lab 2 Exercise 1
4. Reference other pages as questions arise

**Recommendation**: Use Strategy 1 for best retention and understanding.

---

## Comparison with Tutorial 1

| Aspect | Tutorial 1 | Tutorial 2 |
|--------|-----------|-----------|
| **Reading Time** | ~3 hours (16 pages) | ~2.5 hours (9 pages) |
| **Lab Time** | ~3-5 hours | ~4-6 hours |
| **Key Concepts** | Tool calling, O.V.E. testing | Coordination, specialization, communication |
| **Complexity** | Beginner | Intermediate |
| **Prerequisites** | Basic Python | Tutorial 1 completion |
| **Lab Style** | Step-by-step | AI-native scaffolds |

**Tutorial 2 assumes you're comfortable with:**
- Tool calling and agent loops
- Testing with O.V.E.
- Debugging single agents
- Using AI assistants effectively

---

## Document Status

- ✅ All core concepts documented
- ✅ All practical guides written
- ✅ Architecture patterns complete
- ✅ Lab exercises available
- ✅ Navigation links added
- ✅ Code examples included

---

## Learning Outcomes

By completing Tutorial 2, you will be able to:

**Core Competencies:**
- Design multi-agent architectures for complex tasks
- Create specialized agents with focused capabilities
- Implement message protocols for inter-agent communication
- Manage shared state across agents
- Debug multi-agent interactions effectively

**Practical Skills:**
- Build coordinator agents that orchestrate workers
- Implement research → analysis → writing pipelines
- Test multi-agent systems using extended O.V.E.
- Handle failures and retries in coordination logic
- Design agent teams systematically

**Advanced Understanding:**
- Know when to use multi-agent vs. single agent
- Understand coordination patterns and their trade-offs
- Recognize when to scale to hierarchical architectures
- Evaluate peer-to-peer vs. coordinator approaches

---

## What's Next?

After completing Tutorial 2:

1. **Immediate**: Build more complex multi-agent workflows
2. **Short-term**: Explore hierarchical patterns for larger systems (Tutorial 3 preview)
3. **Medium-term**: Add memory and RAG to your agents (Tutorial 3)
4. **Long-term**: Production deployment and monitoring (Tutorial 4)

---

## Getting Help

While reading:
- Use the [Index](./INDEX.md) for quick lookup
- Check [FAQ](../../lab-2/FAQ.md) for common questions
- Reference [Tutorial 1](../../../lesson-1-fundamentals/docs/tutorial-1/INDEX.md) for foundations

While building:
- See [Troubleshooting Guide](../../lab-2/troubleshooting.md)
- Use [Getting Unstuck Guide](../../lab-2/getting-unstuck.md)
- Include `@.cursorrules` when asking AI for help

---

**Ready to Start?** Begin with [Page 1: Multi-Agent Architecture](./concepts/multi-agent-architecture.md)

**Want to Build First?** Go to [Lab 2 README](../../lab-2/README.md)

**Need Overview?** See [Documentation Index](./INDEX.md)

