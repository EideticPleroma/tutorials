# Documentation Index - Tutorial 2

Quick reference to all documentation in Tutorial 2: Multi-Agent Systems.

## By Reading Order

1. **[README (Tutorial 2 Overview)](../../../README.md#tutorial-2-multi-agent-systems)** - What you'll build
2. **[Multi-Agent Architecture](./concepts/multi-agent-architecture.md)** - When and why to use multiple agents
3. **[Agent Specialization](./concepts/agent-specialization.md)** - Designing focused agents
4. **[Agent Communication](./concepts/agent-communication.md)** - Message passing and protocols
5. **[State Management](./concepts/state-management.md)** - Shared state across agents
6. **[Designing Agent Teams](./guides/designing-agent-teams.md)** - Systematic design process
7. **[Debugging Multi-Agent Systems](./guides/debugging-multi-agent.md)** - Troubleshooting strategies
8. **[Testing Multi-Agent Systems](./guides/testing-multi-agent.md)** - Extending O.V.E. methodology
9. **[Coordinator Patterns](./architecture/coordinator-patterns.md)** - Orchestration strategies
10. **[Hierarchical vs. Peer-to-Peer](./architecture/hierarchical-vs-peer.md)** - Alternative architectures

## By Category

### Concepts (Foundation)
- [Multi-Agent Architecture](./concepts/multi-agent-architecture.md) - The "what" and "when"
- [Agent Specialization](./concepts/agent-specialization.md) - Specialist vs. generalist
- [Agent Communication](./concepts/agent-communication.md) - Message protocols
- [State Management](./concepts/state-management.md) - Shared data patterns

### Guides (Practical)
- [Designing Agent Teams](./guides/designing-agent-teams.md) - Design methodology
- [Debugging Multi-Agent Systems](./guides/debugging-multi-agent.md) - Troubleshooting
- [Testing Multi-Agent Systems](./guides/testing-multi-agent.md) - Quality assurance

### Architecture (Advanced)
- [Coordinator Patterns](./architecture/coordinator-patterns.md) - Orchestration techniques
- [Hierarchical vs. Peer-to-Peer](./architecture/hierarchical-vs-peer.md) - Scaling strategies

### Lab Materials
- [Lab 2 README](../../lab-2/README.md) - Lab overview
- [Exercise 1: Coordinator Agent](../../lab-2/exercises/01-coordinator-agent.md)
- [Exercise 2: Specialized Agents](../../lab-2/exercises/02-specialized-agents.md)
- [Exercise 3: Agent Communication](../../lab-2/exercises/03-agent-communication.md)
- [Exercise 4: Challenge Workflow](../../lab-2/exercises/04-challenge-workflow.md)

### Reference
- [Self-Assessment Quiz](./SELF_ASSESSMENT.md) - Test your readiness (10 min, 20 questions)
- [Reading Guide](./READING_GUIDE.md) - Start here for reading order
- [Lab Checklist](../../lab-2/lab-checklist.md) - Track your progress
- [Testing Setup Guide](../../lab-2/testing-setup.md) - pytest fixtures and patterns
- [FAQ](../../lab-2/FAQ.md) - Frequently asked questions
- [Troubleshooting](../../lab-2/troubleshooting.md) - Common errors

### Supplementary Guides
- [Performance Profiling](./guides/performance-profiling.md) - Measure and optimize multi-agent systems
- [Refactoring Guide](./guides/refactoring-single-to-multi.md) - Migrate from single to multi-agent
- [Case Studies](./CASE_STUDIES.md) - Real-world multi-agent applications

## Quick Lookup

**I want to understand...**
- When to use multiple agents → [Multi-Agent Architecture](./concepts/multi-agent-architecture.md)
- How to design specialized agents → [Agent Specialization](./concepts/agent-specialization.md)
- How agents communicate → [Agent Communication](./concepts/agent-communication.md)
- How to share state → [State Management](./concepts/state-management.md)
- How to design agent teams → [Designing Agent Teams](./guides/designing-agent-teams.md)
- How to debug multi-agent → [Debugging Guide](./guides/debugging-multi-agent.md)
- How to test multi-agent → [Testing Guide](./guides/testing-multi-agent.md)
- Coordination patterns → [Coordinator Patterns](./architecture/coordinator-patterns.md)
- Scaling architectures → [Hierarchical vs. Peer-to-Peer](./architecture/hierarchical-vs-peer.md)

**I need to...**
- Get started → [Reading Guide](./READING_GUIDE.md)
- Start the lab → [Lab 2 README](../../lab-2/README.md)
- Track progress → [Lab Checklist](../../lab-2/lab-checklist.md)
- Fix an error → [Troubleshooting Guide](../../lab-2/troubleshooting.md)
- Ask a question → [FAQ](../../lab-2/FAQ.md)

## Prerequisites

**Before starting Tutorial 2:**
- ✅ Complete [Tutorial 1: Fundamentals](../../../lesson-1-fundamentals/docs/tutorial-1/INDEX.md)
- ✅ Understand tool calling and the 7-step loop
- ✅ Familiar with O.V.E. testing methodology
- ✅ Have working agent from Lab 1

**Not sure if you're ready?** 
- Take the [Tutorial 2 Self-Assessment Quiz](./SELF_ASSESSMENT.md) (10 min, 20 questions)
- Or review [Tutorial 1 concepts](../../../lesson-1-fundamentals/docs/tutorial-1/READING_GUIDE.md)

## Reading Time Estimates

- **Concepts (Pages 2-5):** ~55 minutes
- **Guides (Pages 6-8):** ~50 minutes
- **Architecture (Pages 9-10):** ~35 minutes
- **Total Reading:** ~2.5 hours

## Lab Time Estimates

- **Exercise 1:** ~90 minutes (Build coordinator)
- **Exercise 2:** ~90 minutes (Create specialized agents)
- **Exercise 3:** ~60 minutes (Implement communication)
- **Exercise 4:** ~120 minutes (Challenge - optional)
- **Total Lab:** 4-6 hours

## What's Different from Tutorial 1?

| Aspect | Tutorial 1 | Tutorial 2 |
|--------|-----------|-----------|
| **Focus** | Single agent with tools | Multiple coordinated agents |
| **Complexity** | Linear execution | Parallel and sequential workflows |
| **State** | Conversation history | Shared state management |
| **Communication** | User ↔ Agent | Agent ↔ Agent + User ↔ Coordinator |
| **Testing** | Single agent O.V.E. | Multi-agent O.V.E. + integration |
| **Debugging** | Linear trace | Message flow tracing |
| **Lab Style** | Step-by-step guidance | AI-native scaffolds |

## What's Next After Tutorial 2?

After mastering multi-agent systems:

- **Tutorial 3:** Memory systems and RAG (vector databases, long-term memory)
- **Tutorial 4:** Production patterns (monitoring, deployment, scaling)
- **Tutorial 5:** Advanced frameworks (when to adopt LangChain, CrewAI)

## Navigation

Each document includes:
- **Previous/Next:** Navigate sequentially through content
- **Up:** Return to Reading Guide or Index
- **Related:** Links to relevant concepts

---

**Start Learning:** Go to [Reading Guide](./READING_GUIDE.md) for recommended reading order.

**Start Building:** Go to [Lab 2 README](../../lab-2/README.md) to begin exercises.

