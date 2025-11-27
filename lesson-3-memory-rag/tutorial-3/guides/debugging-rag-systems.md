# Debugging RAG Systems

[← Setting Up LlamaIndex](./setting-up-llamaindex.md) | [Next: Testing RAG with O.V.E. →](./testing-rag-ove.md) | [↑ Index](../INDEX.md)

RAG systems have multiple failure points. This guide helps you systematically debug issues when retrieval doesn't work as expected.

---

## The Retrieval Debugging Challenge

RAG failures are tricky because they can happen at any layer:

```
User Query: "How does the coordinator work?"
    ↓
Layer 1: Document Loading    → Did we load the right files?
    ↓
Layer 2: Chunking            → Are chunks meaningful units?
    ↓
Layer 3: Embedding           → Does similarity work correctly?
    ↓
Layer 4: Retrieval           → Are the right chunks returned?
    ↓
Layer 5: Generation          → Does the LLM use the context?
    ↓
Answer: "I don't know" or wrong answer
```

**The "Garbage In, Garbage Out" principle applies:** If early layers fail, later layers can't compensate.

---

## Debugging Layers

### Layer 1: Document Loading

**Question:** Did the documents load correctly?

**Symptoms:**
- Zero results for any query
- Missing files in index
- Truncated content

**Debug steps:**

```python
from llama_index.core import SimpleDirectoryReader

# Load documents
documents = SimpleDirectoryReader("./src").load_data()

# Check what was loaded
print(f"Loaded {len(documents)} documents")

for doc in documents:
    print(f"\nFile: {doc.metadata.get('file_path', 'unknown')}")
    print(f"Characters: {len(doc.text)}")
    print(f"Preview: {doc.text[:200]}...")
    
    # Check for common issues
    if len(doc.text) < 100:
        print("WARNING: Document seems too short")
    if doc.text.strip() == "":
        print("WARNING: Document is empty")
```

**Common fixes:**
- Check file extensions in `required_exts`
- Verify file permissions
- Check for encoding issues (UTF-8)

### Layer 2: Chunking

**Question:** Are chunks semantically meaningful?

**Symptoms:**
- Partial function definitions
- Split sentences
- Missing context

**Debug steps:**

```python
from llama_index.core.node_parser import SentenceSplitter

# Create parser with debug output
parser = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=50,
)

# Parse one document
nodes = parser.get_nodes_from_documents([documents[0]])

print(f"Document split into {len(nodes)} chunks")

for i, node in enumerate(nodes):
    print(f"\n--- Chunk {i} ---")
    print(f"Characters: {len(node.text)}")
    print(f"Start: {node.text[:100]}...")
    print(f"End: ...{node.text[-100:]}")
    
    # Check for issues
    if node.text.count("def ") > 3:
        print("WARNING: Multiple function definitions in one chunk")
    if node.text.endswith(("(", ",", ":")):
        print("WARNING: Chunk ends mid-statement")
```

**Common fixes:**
- Increase `chunk_size` for code (functions should stay together)
- Increase `chunk_overlap` to preserve context
- Use language-aware chunking for code

### Layer 3: Embedding

**Question:** Does similarity search work correctly?

**Symptoms:**
- Semantically similar content has low similarity
- Unrelated content has high similarity
- Inconsistent results

**Debug steps:**

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import numpy as np

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Test with known similar/dissimilar pairs
test_pairs = [
    ("coordinator delegates tasks", "manager assigns work"),  # Should be high
    ("coordinator delegates tasks", "python is a language"),  # Should be low
    ("def __init__(self):", "def __init__(self):"),          # Should be 1.0
]

for text1, text2 in test_pairs:
    emb1 = embed_model.get_text_embedding(text1)
    emb2 = embed_model.get_text_embedding(text2)
    sim = cosine_similarity(emb1, emb2)
    print(f"Similarity: {sim:.3f}")
    print(f"  '{text1[:40]}...'")
    print(f"  '{text2[:40]}...'")
    print()
```

**Common fixes:**
- Try different embedding models
- Normalize text before embedding
- Check for tokenization issues

### Layer 4: Retrieval

**Question:** Are the right chunks being retrieved?

**Symptoms:**
- Wrong chunks returned
- Relevant chunks ranked low
- Too few/many results

**Debug steps:**

```python
# Create query engine with verbose output
query_engine = index.as_query_engine(
    similarity_top_k=10,  # Get more results to see ranking
)

# Query with source inspection
response = query_engine.query("How does delegation work?")

print("Query: How does delegation work?")
print(f"\nAnswer: {response}")
print("\n--- Retrieved Chunks (ranked by similarity) ---")

for i, node in enumerate(response.source_nodes):
    print(f"\n[{i+1}] Score: {node.score:.3f}")
    print(f"    File: {node.metadata.get('file_path', 'unknown')}")
    print(f"    Content: {node.text[:200]}...")
    
    # Flag potential issues
    if node.score < 0.5:
        print("    WARNING: Low similarity score")
    if "delegate" not in node.text.lower():
        print("    WARNING: Keyword 'delegate' not in chunk")
```

**Common fixes:**
- Adjust `similarity_top_k`
- Add metadata filters
- Improve query phrasing

### Layer 5: Generation

**Question:** Is the LLM using the retrieved context?

**Symptoms:**
- LLM ignores context
- Generic responses
- Hallucinated information

**Debug steps:**

```python
# Inspect the actual prompt sent to LLM
from llama_index.core import PromptTemplate

# Custom prompt that logs context usage
qa_prompt = PromptTemplate(
    """Context information is below.
---------------------
{context_str}
---------------------
Given the context information and not prior knowledge, answer the query.
If the context doesn't contain the answer, say "Not found in context."

Query: {query_str}
Answer: """
)

query_engine = index.as_query_engine(
    text_qa_template=qa_prompt,
)

# Test with context-dependent question
response = query_engine.query("What is the exact function name for delegation?")

print(f"Response: {response}")
print("\nDid the LLM use context?")
print("- If answer is specific: Yes")
print("- If answer is generic: Check context relevance")
print("- If 'Not found': Context doesn't have answer")
```

**Common fixes:**
- Improve prompt structure
- Put context BEFORE question
- Add explicit instructions to use context

---

## Debugging Tools

### LlamaIndex Callbacks

Enable detailed logging:

```python
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler

# Create debug handler
debug_handler = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager([debug_handler])

# Use in Settings
Settings.callback_manager = callback_manager

# Now all operations will be logged
index = VectorStoreIndex.from_documents(documents)
response = query_engine.query("test query")

# View event trace
print(debug_handler.get_event_time_info())
```

### Chunk Inspection Tool

```python
def inspect_chunks(index, query: str, top_k: int = 5):
    """Detailed inspection of retrieved chunks."""
    
    retriever = index.as_retriever(similarity_top_k=top_k)
    nodes = retriever.retrieve(query)
    
    print(f"Query: {query}")
    print(f"Retrieved {len(nodes)} chunks\n")
    
    for i, node in enumerate(nodes):
        print(f"{'='*60}")
        print(f"Chunk {i+1} of {len(nodes)}")
        print(f"{'='*60}")
        print(f"Score: {node.score:.4f}")
        print(f"File: {node.metadata.get('file_path', 'N/A')}")
        print(f"Lines: {node.metadata.get('start_line', '?')}-{node.metadata.get('end_line', '?')}")
        print(f"\nContent ({len(node.text)} chars):")
        print("-" * 40)
        print(node.text)
        print("-" * 40)
        print()
    
    return nodes

# Usage
chunks = inspect_chunks(index, "How does the coordinator delegate?")
```

### Similarity Score Analysis

```python
def analyze_scores(index, queries: list[str], top_k: int = 5):
    """Analyze similarity score distribution."""
    
    retriever = index.as_retriever(similarity_top_k=top_k)
    
    for query in queries:
        nodes = retriever.retrieve(query)
        scores = [n.score for n in nodes]
        
        print(f"\nQuery: {query}")
        print(f"  Max score: {max(scores):.3f}")
        print(f"  Min score: {min(scores):.3f}")
        print(f"  Mean score: {sum(scores)/len(scores):.3f}")
        print(f"  Score gap (1st-2nd): {scores[0]-scores[1]:.3f}" if len(scores) > 1 else "")
        
        # Flag issues
        if max(scores) < 0.5:
            print("  WARNING: All scores are low - query may not match indexed content")
        if scores[0] - scores[1] < 0.05:
            print("  WARNING: Small gap between top results - may be ambiguous")

# Test queries
analyze_scores(index, [
    "How does the coordinator delegate tasks?",
    "What is the message protocol?",
    "xyzzy nonsense query",
])
```

---

## Common RAG Failures

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| No results for any query | Documents not indexed | Check document loading |
| All results have low scores | Query doesn't match content | Rephrase query, check embeddings |
| Wrong chunks retrieved | Chunking too large | Reduce chunk size |
| Relevant info split across chunks | Chunking too small | Increase chunk size |
| LLM ignores context | Prompt structure | Put context before question |
| LLM halluccinates | No relevant chunks | Add similarity threshold |
| Slow queries | Index too large | Add metadata filters |
| Inconsistent results | Temperature too high | Lower LLM temperature |

---

## Logging Best Practices

### Structured Logging for RAG

```python
import logging
import json
from datetime import datetime

# Configure structured logger
logger = logging.getLogger("rag")
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(".agent_logs/rag_debug.jsonl")
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)

def log_retrieval(query: str, results: list, duration_ms: float):
    """Log retrieval for debugging."""
    logger.info(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "event": "retrieval",
        "query": query,
        "num_results": len(results),
        "top_score": results[0].score if results else None,
        "duration_ms": duration_ms,
        "result_files": [r.metadata.get("file_path") for r in results[:3]],
    }))

def log_generation(query: str, context_tokens: int, response: str, duration_ms: float):
    """Log generation for debugging."""
    logger.info(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "event": "generation",
        "query": query,
        "context_tokens": context_tokens,
        "response_length": len(response),
        "duration_ms": duration_ms,
    }))
```

### Reading Debug Logs

```bash
# View retrieval events
cat .agent_logs/rag_debug.jsonl | jq 'select(.event == "retrieval")'

# Find slow queries
cat .agent_logs/rag_debug.jsonl | jq 'select(.duration_ms > 1000)'

# Find low-confidence retrievals
cat .agent_logs/rag_debug.jsonl | jq 'select(.top_score < 0.5)'
```

---

## Visual Debugging

### Embedding Space Visualization

For complex debugging, visualize your embedding space:

```python
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

def visualize_embeddings(index, sample_queries: list[str]):
    """Visualize chunk embeddings with query positions."""
    
    # Get all embeddings from index (simplified)
    # In practice, you'd extract these from the vector store
    
    # For demonstration, embed sample content
    sample_texts = [
        "coordinator delegates tasks",
        "worker executes actions",
        "message protocol defines format",
        "RAG retrieves context",
    ] + sample_queries
    
    embeddings = [
        Settings.embed_model.get_text_embedding(t) 
        for t in sample_texts
    ]
    
    # Reduce to 2D
    tsne = TSNE(n_components=2, random_state=42, perplexity=3)
    coords = tsne.fit_transform(np.array(embeddings))
    
    # Plot
    plt.figure(figsize=(10, 8))
    
    # Document chunks (blue)
    n_docs = len(sample_texts) - len(sample_queries)
    plt.scatter(coords[:n_docs, 0], coords[:n_docs, 1], 
                c='blue', label='Chunks', s=100)
    
    # Queries (red)
    plt.scatter(coords[n_docs:, 0], coords[n_docs:, 1], 
                c='red', label='Queries', s=100, marker='x')
    
    # Labels
    for i, text in enumerate(sample_texts):
        plt.annotate(text[:20] + "...", coords[i], fontsize=8)
    
    plt.legend()
    plt.title("Embedding Space Visualization")
    plt.savefig("embedding_space.png")
    print("Saved to embedding_space.png")

# Usage
visualize_embeddings(index, ["how does delegation work?"])
```

---

## Debugging Checklist

When RAG isn't working, work through this checklist:

- [ ] **Documents loaded?** Check count and content
- [ ] **Chunks reasonable?** Inspect size and boundaries
- [ ] **Embeddings working?** Test known similar/dissimilar pairs
- [ ] **Retrieval correct?** Check top-k scores and content
- [ ] **LLM using context?** Verify prompt structure
- [ ] **Logs showing issues?** Check for errors and warnings

---

**Next:** [Testing RAG with O.V.E. →](./testing-rag-ove.md) - Learn to systematically test retrieval quality.

[← Setting Up LlamaIndex](./setting-up-llamaindex.md) | [Next: Testing RAG with O.V.E. →](./testing-rag-ove.md) | [↑ Index](../INDEX.md)

