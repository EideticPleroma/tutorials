# Lab 3 Checklist

Track your progress through Lab 3: Memory & RAG.

## Setup

- [ ] Python 3.11+ installed
- [ ] Ollama running
- [ ] llama3.1:8b model pulled
- [ ] deepseek-coder:6.7b model pulled
- [ ] LlamaIndex packages installed
- [ ] Verification script passes

## Exercise 1: LlamaIndex Setup

- [ ] Task 1: Install dependencies
  - [ ] llama-index-core installed
  - [ ] llama-index-llms-ollama installed
  - [ ] llama-index-embeddings-huggingface installed
  - [ ] Imports work without errors

- [ ] Task 2: Configure LlamaIndex
  - [ ] Created `src/memory_rag/config.py`
  - [ ] Settings.llm configured with Ollama
  - [ ] Settings.embed_model configured with bge-small
  - [ ] Configuration verified

- [ ] Task 3: Create first index
  - [ ] Sample documents created
  - [ ] Index built successfully
  - [ ] Index saved to `./storage/sample_index/`

- [ ] Task 4: Query the index
  - [ ] Query script created
  - [ ] "What is RAG?" returns relevant answer
  - [ ] Source nodes displayed

- [ ] **Exercise 1 Complete** ✅

## Exercise 2: Embedding the Project

- [ ] Task 1: Document loaders
  - [ ] Created `src/memory_rag/document_loaders.py`
  - [ ] `load_code_files()` works
  - [ ] `load_documentation()` works
  - [ ] `load_all_project_files()` works
  - [ ] Metadata includes file_path, file_type, category

- [ ] Task 2: Chunking strategy
  - [ ] Code chunk size configured (1024)
  - [ ] Documentation chunk size configured (512)
  - [ ] Overlap configured

- [ ] Task 3: Build project index
  - [ ] Created `src/memory_rag/rag_engine.py`
  - [ ] RAGEngine class implemented
  - [ ] Project indexed successfully
  - [ ] Index persisted

- [ ] Task 4: Knowledge tool
  - [ ] Created `src/memory_rag/knowledge_tool.py`
  - [ ] `search_codebase()` tool registered
  - [ ] Tool returns formatted results

- [ ] Task 5: Test retrieval quality
  - [ ] Ground truth queries defined
  - [ ] "7-step loop" retrieves tool-calling-architecture.md
  - [ ] "coordinator delegate" retrieves coordinator.py
  - [ ] Tests pass

- [ ] **Exercise 2 Complete** ✅

## Exercise 3: Multi-Model Coordination

- [ ] Task 1: DeepSeek setup
  - [ ] deepseek-coder:6.7b pulled
  - [ ] Model verified working
  - [ ] Config updated with both models

- [ ] Task 2: Model router
  - [ ] Created `src/memory_rag/model_router.py`
  - [ ] ModelRouter class implemented
  - [ ] `classify_task()` works
  - [ ] `route()` returns correct LLM

- [ ] Task 3: Architect agent
  - [ ] Created `src/memory_rag/architect_agent.py`
  - [ ] `plan()` method implemented
  - [ ] Plans include tasks with descriptions and files
  - [ ] `validate()` method implemented

- [ ] Task 4: Builder agent
  - [ ] Created `src/memory_rag/builder_agent.py`
  - [ ] `implement()` method implemented
  - [ ] Code output is clean (no markdown)
  - [ ] Code includes type hints

- [ ] Task 5: Test handoff
  - [ ] Router tests pass
  - [ ] Architect creates valid plans
  - [ ] Builder generates valid code
  - [ ] Architect validates correctly

- [ ] **Exercise 3 Complete** ✅

## Exercise 4: Architect-Builder Workflow

- [ ] Task 1: Enhanced Architect
  - [ ] Plan includes acceptance criteria
  - [ ] Plan references RAG context
  - [ ] Plan validation added

- [ ] Task 2: Enhanced Builder
  - [ ] Better example retrieval
  - [ ] Structured output
  - [ ] Code quality checks

- [ ] Task 3: O.V.E. harness
  - [ ] Created `src/memory_rag/ove_harness.py`
  - [ ] `observe()` captures artifacts
  - [ ] `validate()` checks syntax, type hints, docstrings
  - [ ] `evaluate()` runs tests
  - [ ] `run()` executes full pipeline

- [ ] Task 4: Iteration loop
  - [ ] Created `src/memory_rag/architect_builder.py`
  - [ ] `process_request()` implemented
  - [ ] Retry logic works (max 3 attempts)
  - [ ] Summary created correctly

- [ ] Task 5: End-to-end tests
  - [ ] Created `tests/memory_rag/test_architect_builder.py`
  - [ ] Simple request test
  - [ ] O.V.E. catches syntax errors
  - [ ] Type hint check works

- [ ] **Exercise 4 Complete** ✅

## Final Verification

- [ ] All tests pass: `python -m pytest tests/memory_rag/ -v`
- [ ] Code follows project conventions (type hints, docstrings)
- [ ] No hardcoded paths
- [ ] Logging implemented throughout
- [ ] RAG queries return relevant results

## 🎉 Lab 3 Complete!

**Total Time Spent:** ________ hours

**Notes:**
```
[Your notes here]
```

**Challenges encountered:**
```
[What was difficult?]
```

**Key learnings:**
```
[What did you learn?]
```

