# Documentation Index - Tutorial 3

Quick reference to all documentation in Tutorial 3: Memory & RAG.

## By Reading Order

1. **[README (Tutorial 3 Overview)](../../README.md#tutorial-3-memory--rag)** - What you'll build
2. **[RAG Architecture](./concepts/rag-architecture.md)** - What is RAG and when to use it
3. **[Embeddings & Vector Stores](./concepts/embeddings-vector-stores.md)** - How knowledge is stored and retrieved
4. **[Multi-Model Orchestration](./concepts/multi-model-orchestration.md)** - Using different LLMs for different tasks
5. **[Knowledge Integration](./concepts/knowledge-integration.md)** - Connecting RAG to your agents
6. **[Setting Up LlamaIndex](./guides/setting-up-llamaindex.md)** - Installation and configuration
7. **[Debugging RAG Systems](./guides/debugging-rag-systems.md)** - Troubleshooting retrieval issues
8. **[Testing RAG with O.V.E.](./guides/testing-rag-ove.md)** - Quality assurance for RAG
9. **[RAG Pipeline Architecture](./architecture/rag-pipeline.md)** - Component deep dive
10. **[Architect-Builder Pattern](./architecture/architect-builder-pattern.md)** - Multi-model workflow design

## By Category

### Concepts (Foundation)
- [RAG Architecture](./concepts/rag-architecture.md) - The "what" and "when" of RAG
- [Embeddings & Vector Stores](./concepts/embeddings-vector-stores.md) - How similarity search works
- [Multi-Model Orchestration](./concepts/multi-model-orchestration.md) - Right model for the right task
- [Knowledge Integration](./concepts/knowledge-integration.md) - RAG meets agents

### Guides (Practical)
- [Setting Up LlamaIndex](./guides/setting-up-llamaindex.md) - Get started with RAG
- [Debugging RAG Systems](./guides/debugging-rag-systems.md) - Fix retrieval problems
- [Testing RAG with O.V.E.](./guides/testing-rag-ove.md) - Measure retrieval quality

### Architecture (Advanced)
- [RAG Pipeline Architecture](./architecture/rag-pipeline.md) - Full pipeline breakdown
- [Architect-Builder Pattern](./architecture/architect-builder-pattern.md) - Llama + DeepSeek workflow

### Lab Materials
- [Lab 3 README](../lab-3/README.md) - Lab overview
- [Exercise 1: LlamaIndex Setup](../lab-3/exercises/01-llamaindex-setup.md)
- [Exercise 2: Embedding the Project](../lab-3/exercises/02-embedding-the-project.md)
- [Exercise 3: Multi-Model Coordination](../lab-3/exercises/03-multi-model-coordination.md)
- [Exercise 4: Architect-Builder Workflow](../lab-3/exercises/04-architect-builder-workflow.md)

### Reference
- [Self-Assessment Quiz](./self-assessment.md) - Test your readiness (10 min, 20 questions)
- [Reading Guide](./READING_GUIDE.md) - Start here for reading order
- [Lab Checklist](../lab-3/lab-checklist.md) - Track your progress
- [Setup Guide](../lab-3/setup-guide.md) - Environment setup for Lab 3
- [FAQ](../lab-3/FAQ.md) - Frequently asked questions
- [Getting Unstuck](../lab-3/getting-unstuck.md) - When you're blocked
- [Troubleshooting](../lab-3/troubleshooting.md) - Common errors

### Shared Reference
- [Tech Stack Decisions](../../docs/tech-stack.md) - Technology choices and alternatives

## Quick Lookup

**I want to understand...**
- What RAG is and when to use it → [RAG Architecture](./concepts/rag-architecture.md)
- How embeddings work → [Embeddings & Vector Stores](./concepts/embeddings-vector-stores.md)
- How to use multiple models together → [Multi-Model Orchestration](./concepts/multi-model-orchestration.md)
- How to connect RAG to agents → [Knowledge Integration](./concepts/knowledge-integration.md)
- The Architect-Builder pattern → [Architect-Builder Pattern](./architecture/architect-builder-pattern.md)
- How to test RAG quality → [Testing RAG with O.V.E.](./guides/testing-rag-ove.md)

**I need to...**
- Get started → [Reading Guide](./READING_GUIDE.md)
- Start the lab → [Lab 3 README](../lab-3/README.md)
- Track progress → [Lab Checklist](../lab-3/lab-checklist.md)
- Fix an error → [Troubleshooting Guide](../lab-3/troubleshooting.md)
- Ask a question → [FAQ](../lab-3/FAQ.md)

## Prerequisites

**Before starting Tutorial 3:**
- ✅ Complete [Tutorial 1: Fundamentals](../../lesson-1-fundamentals/tutorial-1/INDEX.md)
- ✅ Complete [Tutorial 2: Multi-Agent Systems](../../lesson-2-multi-agent/tutorial-2/INDEX.md)
- ✅ Understand coordinator-worker pattern
- ✅ Familiar with O.V.E. testing methodology
- ✅ Have working multi-agent system from Lab 2

**Not sure if you're ready?** 
- Take the [Tutorial 3 Self-Assessment Quiz](./self-assessment.md) (10 min, 20 questions)
- Or review [Tutorial 2 concepts](../../lesson-2-multi-agent/tutorial-2/READING_GUIDE.md)

## Reading Time Estimates

- **Concepts (Pages 1-4):** ~60 minutes
- **Guides (Pages 5-7):** ~45 minutes
- **Architecture (Pages 8-9):** ~40 minutes
- **Total Reading:** ~2.5 hours

## Lab Time Estimates

- **Exercise 1:** ~60 minutes (LlamaIndex setup)
- **Exercise 2:** ~90 minutes (Embed the project)
- **Exercise 3:** ~90 minutes (Multi-model coordination)
- **Exercise 4:** ~120 minutes (Challenge - Architect-Builder)
- **Total Lab:** 6-8 hours

## What's Different from Tutorial 2?

| Aspect | Tutorial 2 | Tutorial 3 |
|--------|-----------|-----------|
| **Focus** | Multi-agent coordination | Knowledge retrieval + multi-model |
| **New Concepts** | Message protocol, shared state | RAG, embeddings, vector stores |
| **Models** | Single model (Llama) | Multiple models (Llama + DeepSeek) |
| **Data** | In-memory state | Persistent vector storage |
| **Testing Focus** | Agent interactions | Retrieval quality |
| **Framework** | Built from scratch | LlamaIndex for RAG |
| **Analogy** | Manager + Team | Librarian + Architect + Builder |

## What's Next After Tutorial 3?

After mastering memory and RAG:

- **Tutorial 4:** Production patterns (monitoring, deployment, scaling)
- **Tutorial 5:** Advanced frameworks (when to adopt CrewAI, LangGraph)
- **Tutorial 6:** Real-world applications (building complete AI products)

## Navigation

Each document includes:
- **Previous/Next:** Navigate sequentially through content
- **Up:** Return to Reading Guide or Index
- **Related:** Links to relevant concepts

---

**Start Learning:** Go to [Reading Guide](./READING_GUIDE.md) for recommended reading order.

**Start Building:** Go to [Lab 3 README](../lab-3/README.md) to begin exercises.

