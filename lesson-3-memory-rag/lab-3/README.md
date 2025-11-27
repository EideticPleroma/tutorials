# Lab 3: Memory & RAG

Build RAG-powered agents using LlamaIndex and multi-model orchestration.

## What You'll Build

A complete **Architect-Builder** coding assistant that:
- Indexes your codebase with LlamaIndex
- Uses Llama 3.1 for planning and validation
- Uses DeepSeek-Coder for code generation
- Validates implementations with O.V.E. methodology

```
User: "Add a greeting tool"
         ↓
   [RAG: Query codebase]
         ↓
Architect (Llama): Create task plan
         ↓
Builder (DeepSeek): Implement code
         ↓
   [O.V.E.: Validate]
         ↓
Result: Working greeting tool
```

## Prerequisites

Before starting Lab 3, ensure you have:

- [ ] **Completed Tutorial 2** - You need multi-agent foundations
- [ ] **Python 3.11+** - Required for LlamaIndex
- [ ] **Ollama running** with `llama3.1:8b`
- [ ] **Read the concepts** - At minimum:
  - [RAG Architecture](../tutorial-3/concepts/rag-architecture.md)
  - [Multi-Model Orchestration](../tutorial-3/concepts/multi-model-orchestration.md)

**Verify prerequisites:**
```bash
python --version    # 3.11+
ollama list         # llama3.1:8b should be present
```

## Time Commitment

| Exercise | Duration | Difficulty |
|----------|----------|------------|
| Exercise 1: LlamaIndex Setup | ~60 min | Beginner |
| Exercise 2: Embedding the Project | ~90 min | Intermediate |
| Exercise 3: Multi-Model Coordination | ~90 min | Intermediate |
| Exercise 4: Architect-Builder Workflow | ~120 min | Advanced |

**Total: 6-8 hours** (can be split across multiple sessions)

## Exercise Overview

### Exercise 1: LlamaIndex Setup
Set up LlamaIndex with Ollama and create your first searchable index.
- Install LlamaIndex packages
- Configure with local LLM and embeddings
- Create and query a sample index

### Exercise 2: Embedding the Project
Index the entire tutorial codebase and documentation.
- Create document loaders for code and docs
- Build a project-wide knowledge base
- Test retrieval quality with ground truth queries

### Exercise 3: Multi-Model Coordination
Set up DeepSeek-Coder and create a model router.
- Install and configure DeepSeek-Coder
- Build Architect (Llama) and Builder (DeepSeek) agents
- Test model handoff and coordination

### Exercise 4: Architect-Builder Workflow (Challenge)
Build the complete workflow with O.V.E. testing.
- Create the iteration loop with retry logic
- Implement O.V.E. testing harness for generated code
- Run end-to-end tests

## Getting Started

1. **Start with the setup guide:**
   ```bash
   # Follow the setup guide first
   cat lesson-3-memory-rag/lab-3/setup-guide.md
   ```

2. **Begin Exercise 1:**
   ```bash
   # Open the first exercise
   code lesson-3-memory-rag/lab-3/exercises/01-llamaindex-setup.md
   ```

3. **Track your progress:**
   - Use the [Lab Checklist](./lab-checklist.md)
   - Update [progress.md](../progress.md) as you complete sections

## Getting Help

- **Stuck?** See [Getting Unstuck](./getting-unstuck.md)
- **Errors?** Check [Troubleshooting](./troubleshooting.md)
- **Questions?** Read [FAQ](./FAQ.md)
- **Need concepts?** Return to [Tutorial 3 Index](../tutorial-3/INDEX.md)

## Project Structure After Lab 3

```
src/memory_rag/
├── __init__.py
├── config.py              # LlamaIndex + multi-model config
├── document_loaders.py    # Code + docs loaders
├── rag_engine.py          # Main RAG interface
├── knowledge_tool.py      # search_codebase() tool
├── model_router.py        # Route to Llama or DeepSeek
├── architect_agent.py     # Planning agent (Llama)
├── builder_agent.py       # Implementation agent (DeepSeek)
├── architect_builder.py   # Coordinator
└── ove_harness.py         # Testing harness

tests/memory_rag/
├── test_rag_engine.py
├── test_retrieval_quality.py
├── test_multi_model.py
└── test_architect_builder.py
```

## Key Concepts Summary

| Concept | What It Is | Where Used |
|---------|------------|------------|
| **RAG** | Retrieval-Augmented Generation | All exercises |
| **Embeddings** | Text as vectors | Exercise 1-2 |
| **Vector Store** | Searchable embedding database | Exercise 1-2 |
| **Multi-Model** | Different LLMs for different tasks | Exercise 3-4 |
| **Architect-Builder** | Plan → Implement pattern | Exercise 3-4 |
| **O.V.E.** | Observe-Validate-Evaluate testing | Exercise 4 |

## Learning Outcomes

After completing Lab 3, you will be able to:

1. **Set up LlamaIndex** with local LLMs and embeddings
2. **Index codebases** with appropriate chunking strategies
3. **Query knowledge bases** and evaluate retrieval quality
4. **Orchestrate multiple models** for different tasks
5. **Build Architect-Builder workflows** with retry logic
6. **Test RAG systems** using O.V.E. methodology

## Tips for Success

1. **Complete exercises in order** - Each builds on the previous
2. **Test incrementally** - Verify each component before moving on
3. **Read the logs** - Multi-component systems need good observability
4. **Use the AI prompts** - They're designed to generate working code
5. **Don't skip the concepts** - Understanding "why" helps with debugging

---

**Ready to start?** Go to [Exercise 1: LlamaIndex Setup](./exercises/01-llamaindex-setup.md)

**Need setup help?** See [Setup Guide](./setup-guide.md)

