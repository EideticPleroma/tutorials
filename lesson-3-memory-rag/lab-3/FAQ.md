# Frequently Asked Questions - Lab 3

Common questions about Memory & RAG in Tutorial 3.

---

## General Questions

### Why LlamaIndex over LangChain?

**LlamaIndex is more focused on RAG.**

| Aspect | LlamaIndex | LangChain |
|--------|------------|-----------|
| Focus | Data + RAG | Everything |
| Learning curve | Moderate | Steeper |
| RAG features | Comprehensive | Good |
| Abstraction | Right amount | More layers |
| Community | Active | Very active |

LlamaIndex was designed specifically for RAG use cases, making it a better fit for Tutorial 3. LangChain tries to do everything, which adds complexity we don't need.

### Why local embeddings instead of OpenAI?

**Cost, privacy, and educational value.**

1. **Cost**: Local embeddings are free. OpenAI charges per token.
2. **Privacy**: Your code never leaves your machine.
3. **Speed**: No network latency.
4. **Learning**: You understand what's happening locally.

`bge-small-en-v1.5` provides good quality (competitive with OpenAI on many benchmarks) while being free and fast.

### Why DeepSeek-Coder specifically?

**Best open-source code generation at reasonable size.**

| Model | Size | Code Quality | Speed |
|-------|------|--------------|-------|
| DeepSeek-Coder 6.7B | 4GB | Excellent | Fast |
| CodeLlama 7B | 4GB | Good | Fast |
| StarCoder 7B | 4GB | Good | Fast |
| Llama 3.1 8B | 5GB | Good | Medium |

DeepSeek-Coder was specifically trained on code and consistently produces cleaner, more correct implementations than general-purpose models.

### How much RAM do I need?

**12GB minimum, 16GB+ recommended.**

| Configuration | RAM Usage |
|---------------|-----------|
| Llama 3.1 only | ~8GB |
| + DeepSeek-Coder | ~6GB additional |
| + Embeddings | ~1GB |
| + Index in memory | ~1-2GB |

With 16GB, you can run both models with comfortable headroom. Ollama swaps models automatically if you're memory-constrained.

---

## RAG Questions

### Why doesn't my query find the right documents?

**Common causes:**

1. **Query phrasing**: Try different words
   - Instead of "tool calling", try "how the agent executes tools"
   
2. **Chunking issues**: Information split across chunks
   - Increase chunk size
   - Add more overlap
   
3. **Embedding mismatch**: Query and content semantically different
   - Check similarity scores
   - Try more specific queries
   
4. **Index not updated**: New files not indexed
   - Rebuild the index

### What chunk size should I use?

**It depends on content type:**

| Content | Chunk Size | Overlap | Reasoning |
|---------|------------|---------|-----------|
| Code | 1024-1500 | 100-200 | Keep functions together |
| Documentation | 512 | 50 | Sections are independent |
| Chat logs | 256 | 50 | Conversations are granular |

Start with the defaults and adjust based on retrieval quality.

### How do I know if retrieval is working well?

**Check these metrics:**

1. **Similarity scores**: Top result should be >0.7
2. **Relevant content**: Top chunks should contain the answer
3. **Ranking**: Most relevant chunk should be first

Use the debugging tools:
```python
results = engine.retrieve("your query", top_k=10)
for r in results:
    print(f"Score: {r.score:.3f} | File: {r.metadata['file_path']}")
```

### Can I use a different vector store?

**Yes! LlamaIndex supports many options:**

- **In-memory** (default): Simple, no persistence
- **ChromaDB**: Persistent, simple setup
- **Pinecone**: Cloud-hosted, production-ready
- **Weaviate**: Self-hosted or cloud
- **FAISS**: High performance, no persistence

For learning, ChromaDB is recommended. For production, consider Pinecone or Weaviate.

---

## Multi-Model Questions

### When does Llama vs. DeepSeek get used?

**Based on task type:**

| Task | Model | Why |
|------|-------|-----|
| Understanding user intent | Llama | Better at natural language |
| Creating plans | Llama | Better at reasoning |
| Writing code | DeepSeek | Optimized for code |
| Writing tests | DeepSeek | Tests are code |
| Explaining code | Llama | Better explanations |
| Validating implementations | Llama | Better at judgments |

### Can I use different models?

**Yes!** Update the config:

```python
# Use different models
ARCHITECT_MODEL = "mistral:7b"  # Or any Ollama model
BUILDER_MODEL = "codellama:7b"  # Or any code model
```

Just ensure the models are pulled in Ollama first.

### Why does model switching seem slow?

**Ollama swaps models in memory.**

When you switch from Llama to DeepSeek:
1. Llama gets unloaded (or cached)
2. DeepSeek gets loaded
3. First request is slow

**Mitigations:**
- Keep both models in memory (needs 14GB+ RAM)
- Batch similar tasks together
- Accept the latency for now

### How do I handle model disagreements?

**The Architect is the authority.**

If Builder's code doesn't meet Architect's requirements:
1. Architect provides feedback
2. Builder retries with that feedback
3. After 3 tries, fail the task

The Architect-Builder pattern intentionally gives Architect final say on quality.

---

## Testing Questions

### What's the difference between Validate and Evaluate in O.V.E.?

**Validate is deterministic, Evaluate is probabilistic.**

| Phase | What It Checks | Can Be Automated? |
|-------|----------------|-------------------|
| **Validate** | Syntax correct? Type hints present? | Yes, 100% |
| **Evaluate** | Is the answer good? Does it meet requirements? | Partially |

Validation catches mechanical errors. Evaluation judges quality.

### How do I test RAG retrieval quality?

**Create ground truth queries:**

```python
GROUND_TRUTH = [
    {
        "query": "What is the 7-step loop?",
        "expected_files": ["tool-calling-architecture.md"],
        "expected_content": ["parse", "execute"],
    },
]

def test_retrieval():
    for case in GROUND_TRUTH:
        results = engine.retrieve(case["query"])
        files = [r.metadata["file_path"] for r in results]
        assert any(exp in f for f in files for exp in case["expected_files"])
```

### Should I test LLM outputs?

**Test structure, not exact content.**

```python
# Good: Test structure
def test_plan_has_tasks():
    plan = architect.plan("Add a tool")
    assert isinstance(plan, list)
    assert len(plan) >= 1
    assert "description" in plan[0]

# Bad: Test exact content (will be flaky)
def test_plan_content():
    plan = architect.plan("Add a tool")
    assert plan[0]["description"] == "Create tool function"  # Too specific!
```

---

## Debugging Questions

### My index is empty after building

**Check document loading:**

```python
docs = load_all_project_files(".")
print(f"Loaded {len(docs)} documents")

if len(docs) == 0:
    # Check paths, extensions, exclusions
    print("Check: Are files in the expected location?")
    print("Check: Are file extensions included?")
```

### Queries return nothing relevant

**Debug in layers:**

```python
# Layer 1: Is the content indexed?
results = engine.retrieve("def ", top_k=100)  # Generic query
print(f"Found {len(results)} code chunks")

# Layer 2: Is similarity working?
results = engine.retrieve("coordinator", top_k=5)
for r in results:
    print(f"{r.score:.3f}: {r.metadata['file_path']}")

# Layer 3: Is your query too specific?
# Try broader terms
```

### Builder produces invalid Python

**Common causes:**

1. **Markdown fences**: Builder wraps code in ```python
   ```python
   def clean_code(code):
       if code.startswith("```"):
           lines = code.split("\n")[1:-1]
           code = "\n".join(lines)
       return code
   ```

2. **Incomplete output**: Builder got cut off
   - Increase max_tokens
   - Simplify the task

3. **Wrong model**: Accidentally using Llama for code
   - Check model routing

### Tests pass locally but fail in CI

**Common causes:**

1. **Model not available**: Ollama not running in CI
   - Mock LLM calls for CI
   - Or set up Ollama in CI

2. **Index not built**: Storage directory missing
   - Build index as part of CI setup
   - Or use fixtures

3. **Timing issues**: First model load is slow
   - Increase test timeouts
   - Warm up models before tests

---

## Performance Questions

### Indexing is very slow

**Solutions:**

1. **Reduce scope**: Index only what you need
2. **Batch processing**: Use `embed_batch_size`
3. **Skip re-indexing**: Check if files changed first
4. **Use persistence**: Don't rebuild every time

### Queries are slow

**Solutions:**

1. **Reduce top_k**: Retrieve fewer chunks
2. **Add filters**: Use metadata to narrow search
3. **Use faster index**: HNSW is faster than flat
4. **Cache queries**: Store frequent query results

### Memory usage keeps growing

**Solutions:**

1. **Limit index size**: Only index what's needed
2. **Use persistence**: ChromaDB instead of in-memory
3. **Clear cache**: `torch.cuda.empty_cache()` if using GPU
4. **Restart Ollama**: Models accumulate cache

---

## Still Have Questions?

1. Check [Troubleshooting](./troubleshooting.md) for specific errors
2. Check [Getting Unstuck](./getting-unstuck.md) for exercise help
3. Review [Tutorial 3 Concepts](../tutorial-3/INDEX.md) for theory
4. Ask your AI assistant with context from `.cursorrules`

