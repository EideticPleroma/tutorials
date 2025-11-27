# Reading Guide - Tutorial 3: Memory & RAG

**Start Here** | [Index](./INDEX.md) | [Lab 3](../lab-3/README.md)

This guide helps you navigate Tutorial 3 materials efficiently based on your goals and available time.

## How to Use This Guide

Tutorial 3 introduces **Retrieval-Augmented Generation (RAG)** and **multi-model orchestration**. The materials are organized into:

1. **Concepts** - Foundational knowledge (read first)
2. **Guides** - Practical how-to instructions
3. **Architecture** - Deep dives into system design
4. **Lab Exercises** - Hands-on implementation

**Reading approach:** Read concepts before starting labs. Guides can be read as needed during lab work.

## Core Path (Essential Reading)

**Time: ~2 hours** | For learners who want to understand the fundamentals before building.

### Week 1: RAG Foundations

| Order | Document | Time | Key Takeaway |
|-------|----------|------|--------------|
| 1 | [RAG Architecture](./concepts/rag-architecture.md) | 20 min | What RAG is and when to use it |
| 2 | [Embeddings & Vector Stores](./concepts/embeddings-vector-stores.md) | 15 min | How similarity search works |
| 3 | [Setting Up LlamaIndex](./guides/setting-up-llamaindex.md) | 15 min | Installation and configuration |
| 4 | **Exercise 1** | 60 min | LlamaIndex working locally |
| 5 | **Exercise 2** | 90 min | Project codebase indexed |

### Week 2: Multi-Model & Integration

| Order | Document | Time | Key Takeaway |
|-------|----------|------|--------------|
| 6 | [Multi-Model Orchestration](./concepts/multi-model-orchestration.md) | 15 min | Architect-Builder pattern |
| 7 | [Knowledge Integration](./concepts/knowledge-integration.md) | 15 min | RAG meets agents |
| 8 | [Testing RAG with O.V.E.](./guides/testing-rag-ove.md) | 15 min | Measure retrieval quality |
| 9 | **Exercise 3** | 90 min | Llama + DeepSeek working |
| 10 | **Exercise 4** | 120 min | Complete Architect-Builder workflow |

## Extended Path (Deep Dive)

**Time: ~4 hours** | For learners who want comprehensive understanding.

Add these to the core path:

| Document | Time | When to Read |
|----------|------|--------------|
| [Debugging RAG Systems](./guides/debugging-rag-systems.md) | 20 min | Before Exercise 2 |
| [RAG Pipeline Architecture](./architecture/rag-pipeline.md) | 25 min | After Exercise 2 |
| [Architect-Builder Pattern](./architecture/architect-builder-pattern.md) | 20 min | Before Exercise 4 |
| [Self-Assessment](./self-assessment.md) | 10 min | After all concepts |

## Quick Reference: Document Purposes

### Concepts (The "Why")
- **RAG Architecture** - Understand the problem RAG solves and when to use it
- **Embeddings & Vector Stores** - Learn how text becomes searchable numbers
- **Multi-Model Orchestration** - Why use different models for different tasks
- **Knowledge Integration** - How RAG enhances agent capabilities

### Guides (The "How")
- **Setting Up LlamaIndex** - Step-by-step installation and first index
- **Debugging RAG Systems** - Diagnose retrieval problems layer by layer
- **Testing RAG with O.V.E.** - Measure and improve retrieval quality

### Architecture (The "What")
- **RAG Pipeline Architecture** - Detailed component breakdown
- **Architect-Builder Pattern** - Complete multi-model workflow design

## Suggested Schedule

### Two-Week Pace (Recommended)

**Week 1: RAG Foundations**
- Day 1-2: Read concepts 1-2, complete Exercise 1
- Day 3-5: Complete Exercise 2, read debugging guide

**Week 2: Multi-Model Workflow**
- Day 1-2: Read concepts 3-4, complete Exercise 3
- Day 3-5: Read architecture docs, complete Exercise 4

### One-Week Intensive

**Days 1-2:** All concepts + Exercise 1
**Days 3-4:** Exercise 2 + guides
**Days 5-7:** Exercises 3-4 + architecture

### Weekend Sprint

**Saturday:** Concepts + Exercises 1-2
**Sunday:** Exercises 3-4

## Learning Objectives by Section

### After Concepts
You should be able to:
- [ ] Explain what RAG is and when to use it vs. fine-tuning
- [ ] Describe how embeddings represent text as vectors
- [ ] Explain why multi-model orchestration improves results
- [ ] Draw the Architect-Builder workflow

### After Guides
You should be able to:
- [ ] Set up LlamaIndex with Ollama from scratch
- [ ] Debug retrieval issues systematically
- [ ] Write O.V.E. tests for RAG systems

### After Architecture
You should be able to:
- [ ] Identify all components in a RAG pipeline
- [ ] Design an Architect-Builder system
- [ ] Extend the message protocol for multi-model workflows

### After Lab
You should be able to:
- [ ] Index any codebase with LlamaIndex
- [ ] Query the index and get relevant context
- [ ] Orchestrate Llama and DeepSeek for coding tasks
- [ ] Test retrieval quality with ground truth datasets

## Prerequisites Check

Before starting, ensure you can answer:

1. **From Tutorial 1:**
   - What is the 7-step tool calling loop?
   - How do you test agents with O.V.E.?

2. **From Tutorial 2:**
   - What is the coordinator-worker pattern?
   - How do agents communicate via messages?
   - What is shared state?

**Can't answer these?** Review:
- [Tutorial 1 Reading Guide](../../lesson-1-fundamentals/tutorial-1/READING_GUIDE.md)
- [Tutorial 2 Reading Guide](../../lesson-2-multi-agent/tutorial-2/READING_GUIDE.md)

## Key Analogies in Tutorial 3

These analogies will help concepts click:

| Concept | Analogy | Key Insight |
|---------|---------|-------------|
| RAG | Librarian | Reads relevant books before answering |
| Embeddings | GPS Coordinates | Text as location in meaning-space |
| Vector Store | Library Catalog | Find books by topic similarity |
| Chunking | Bookmarking | Balance precision vs. context |
| Architect-Builder | Construction | Architect designs, builder constructs |

## Navigation

- **Previous Tutorial:** [Tutorial 2 Reading Guide](../../lesson-2-multi-agent/tutorial-2/READING_GUIDE.md)
- **This Tutorial:** [Index](./INDEX.md)
- **Next:** [RAG Architecture](./concepts/rag-architecture.md) (Page 1 of 4)

---

**Ready to start?** Begin with [RAG Architecture](./concepts/rag-architecture.md) to understand what you're building.

