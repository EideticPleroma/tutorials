# Setting Up LlamaIndex

[← Knowledge Integration](../concepts/knowledge-integration.md) | [Next: Debugging RAG →](./debugging-rag-systems.md) | [↑ Index](../INDEX.md)

This guide walks you through setting up LlamaIndex with Ollama for local RAG development.

---

## Prerequisites

Before starting, ensure you have:

- [ ] Python 3.11+ installed
- [ ] Ollama 0.4.0+ running with `llama3.1:8b`
- [ ] Completed Tutorial 2 (multi-agent foundations)
- [ ] At least 8GB RAM available

**Verify prerequisites:**
```bash
python --version    # Should show 3.11.x or higher
ollama --version    # Should show 0.4.x or higher
ollama list         # Should include llama3.1:8b
```

---

## Installation

### Core Packages

Install the essential LlamaIndex packages:

```bash
# Core LlamaIndex
pip install llama-index-core

# Ollama integration (for LLM)
pip install llama-index-llms-ollama

# Local embeddings (no API costs)
pip install llama-index-embeddings-huggingface

# File readers (PDF, markdown, code)
pip install llama-index-readers-file
```

### Optional: Persistent Storage

For saving your index to disk:

```bash
# ChromaDB for persistent vector storage
pip install llama-index-vector-stores-chroma chromadb
```

### All-in-One Install

Or install everything at once:

```bash
pip install llama-index-core \
            llama-index-llms-ollama \
            llama-index-embeddings-huggingface \
            llama-index-readers-file \
            llama-index-vector-stores-chroma \
            chromadb
```

### Verify Installation

```python
# Quick verification script
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

print("LlamaIndex imports successful!")

# Test Ollama connection
llm = Ollama(model="llama3.1:8b", request_timeout=60.0)
response = llm.complete("Say 'LlamaIndex is working!' and nothing else.")
print(f"LLM response: {response}")

# Test embeddings
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
embedding = embed_model.get_text_embedding("Test embedding")
print(f"Embedding dimensions: {len(embedding)}")

print("\nAll components working!")
```

---

## Configuration

### Settings Object

LlamaIndex uses a global `Settings` object for configuration:

```python
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Configure LLM (for generation)
Settings.llm = Ollama(
    model="llama3.1:8b",
    request_timeout=120.0,  # Longer timeout for complex queries
    temperature=0.1,        # Lower = more deterministic
)

# Configure embeddings (for retrieval)
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# Configure chunking
Settings.chunk_size = 512        # Tokens per chunk
Settings.chunk_overlap = 50      # Overlap between chunks
```

### Model Configuration Options

**LLM Options (Ollama):**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `model` | Required | Ollama model name |
| `request_timeout` | 30.0 | Timeout in seconds |
| `temperature` | 0.7 | Randomness (0-1) |
| `context_window` | 4096 | Max context tokens |
| `num_output` | 256 | Max output tokens |

**Embedding Options (HuggingFace):**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `model_name` | Required | HuggingFace model ID |
| `cache_folder` | None | Local cache directory |
| `device` | "cpu" | "cpu" or "cuda" |

### Recommended Configuration

```python
# For Tutorial 3 development
Settings.llm = Ollama(
    model="llama3.1:8b",
    request_timeout=120.0,
    temperature=0.1,
)

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

Settings.chunk_size = 512
Settings.chunk_overlap = 50
```

---

## First Index

Let's create your first searchable index.

### Loading Documents

```python
from llama_index.core import SimpleDirectoryReader

# Load all files from a directory
documents = SimpleDirectoryReader(
    input_dir="./sample_docs",
    recursive=True,  # Include subdirectories
    required_exts=[".py", ".md", ".txt"],  # Filter by extension
).load_data()

print(f"Loaded {len(documents)} documents")
for doc in documents[:3]:
    print(f"  - {doc.metadata.get('file_name', 'unknown')}")
```

### Creating VectorStoreIndex

```python
from llama_index.core import VectorStoreIndex

# Create index (this embeds all documents)
index = VectorStoreIndex.from_documents(
    documents,
    show_progress=True,  # Show progress bar
)

print("Index created successfully!")
```

### Querying

```python
# Create a query engine
query_engine = index.as_query_engine(
    similarity_top_k=5,  # Return top 5 matches
)

# Ask a question
response = query_engine.query("What does this codebase do?")
print(response)

# Get source nodes (for citations)
for node in response.source_nodes:
    print(f"\nSource: {node.metadata.get('file_name', 'unknown')}")
    print(f"Score: {node.score:.3f}")
    print(f"Content: {node.text[:200]}...")
```

---

## Persistence

Don't re-embed every time! Save and load your index.

### Saving Index

```python
# Save to disk
index.storage_context.persist(persist_dir="./storage")
print("Index saved to ./storage")
```

### Loading Index

```python
from llama_index.core import StorageContext, load_index_from_storage

# Load from disk
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
print("Index loaded from ./storage")

# Ready to query
query_engine = index.as_query_engine()
```

### Using ChromaDB for Persistence

For larger indexes, use ChromaDB:

```python
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext, VectorStoreIndex

# Create ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("tutorial_index")

# Create vector store
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Create index with ChromaDB
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    show_progress=True,
)

# ChromaDB automatically persists - no need to call persist()
print("Index created and persisted to ChromaDB")

# Later, load the index:
# Just recreate the vector store pointing to the same directory
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(vector_store)
```

---

## Verification Steps

After setup, verify everything works:

### 1. Test LLM Connection

```python
from llama_index.llms.ollama import Ollama

llm = Ollama(model="llama3.1:8b")
response = llm.complete("What is 2 + 2?")
assert "4" in str(response), "LLM not responding correctly"
print("LLM: OK")
```

### 2. Test Embeddings

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
embedding = embed_model.get_text_embedding("test")
assert len(embedding) == 384, f"Expected 384 dimensions, got {len(embedding)}"
print("Embeddings: OK")
```

### 3. Test Index Creation

```python
from llama_index.core import Document, VectorStoreIndex

docs = [Document(text="This is a test document about RAG.")]
index = VectorStoreIndex.from_documents(docs)
assert index is not None, "Index creation failed"
print("Index: OK")
```

### 4. Test Query

```python
query_engine = index.as_query_engine()
response = query_engine.query("What is this about?")
assert "RAG" in str(response) or "test" in str(response), "Query not working"
print("Query: OK")
```

### 5. Full Verification Script

```python
"""Full LlamaIndex verification script."""

def verify_llamaindex():
    print("Verifying LlamaIndex setup...\n")
    
    # 1. Imports
    try:
        from llama_index.core import Settings, Document, VectorStoreIndex
        from llama_index.llms.ollama import Ollama
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding
        print("[OK] Imports successful")
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        return False
    
    # 2. Configure
    try:
        Settings.llm = Ollama(model="llama3.1:8b", request_timeout=60.0)
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )
        print("[OK] Configuration successful")
    except Exception as e:
        print(f"[FAIL] Configuration error: {e}")
        return False
    
    # 3. Test embedding
    try:
        embedding = Settings.embed_model.get_text_embedding("test")
        assert len(embedding) == 384
        print(f"[OK] Embeddings working (dim={len(embedding)})")
    except Exception as e:
        print(f"[FAIL] Embedding error: {e}")
        return False
    
    # 4. Test index
    try:
        docs = [
            Document(text="The coordinator delegates tasks to workers."),
            Document(text="RAG improves answer quality with retrieval."),
        ]
        index = VectorStoreIndex.from_documents(docs)
        print("[OK] Index creation successful")
    except Exception as e:
        print(f"[FAIL] Index error: {e}")
        return False
    
    # 5. Test query
    try:
        query_engine = index.as_query_engine()
        response = query_engine.query("What does the coordinator do?")
        assert "delegate" in str(response).lower() or "task" in str(response).lower()
        print(f"[OK] Query successful")
        print(f"    Response: {str(response)[:100]}...")
    except Exception as e:
        print(f"[FAIL] Query error: {e}")
        return False
    
    print("\n All verification checks passed!")
    return True

if __name__ == "__main__":
    verify_llamaindex()
```

---

## Common Setup Issues

### Issue: "Ollama connection refused"

**Symptom:** `ConnectionRefusedError` when creating Ollama LLM

**Solutions:**
1. Ensure Ollama is running: `ollama serve`
2. Check the port: Default is `http://localhost:11434`
3. Verify model is pulled: `ollama list`

```python
# Specify custom URL if needed
llm = Ollama(
    model="llama3.1:8b",
    base_url="http://localhost:11434"
)
```

### Issue: "HuggingFace model download fails"

**Symptom:** Timeout or connection error downloading embedding model

**Solutions:**
1. Check internet connection
2. Use a cached model:
```python
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    cache_folder="./models"  # Cache locally
)
```

### Issue: "Out of memory during indexing"

**Symptom:** Process killed or memory error with large document sets

**Solutions:**
1. Reduce batch size:
```python
Settings.embed_batch_size = 10  # Default is 100
```

2. Index in batches:
```python
# Split documents
batch_size = 100
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    if i == 0:
        index = VectorStoreIndex.from_documents(batch)
    else:
        index.insert_nodes(batch)
```

### Issue: "Query returns irrelevant results"

**Symptom:** Retrieved chunks don't match the query

**Solutions:**
1. Improve chunking:
```python
Settings.chunk_size = 256  # Smaller chunks
Settings.chunk_overlap = 50  # More overlap
```

2. Increase `top_k`:
```python
query_engine = index.as_query_engine(similarity_top_k=10)
```

3. Check embedding model matches content type (code vs. prose)

---

## Quick Start Summary

```python
"""Minimal LlamaIndex setup for Tutorial 3."""

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 1. Configure
Settings.llm = Ollama(model="llama3.1:8b", request_timeout=120.0)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# 2. Load documents
documents = SimpleDirectoryReader("./your_docs").load_data()

# 3. Create index
index = VectorStoreIndex.from_documents(documents, show_progress=True)

# 4. Save for later
index.storage_context.persist("./storage")

# 5. Query
query_engine = index.as_query_engine()
response = query_engine.query("Your question here")
print(response)
```

---

**Next:** [Debugging RAG Systems →](./debugging-rag-systems.md) - Learn to troubleshoot retrieval issues.

[← Knowledge Integration](../concepts/knowledge-integration.md) | [Next: Debugging RAG →](./debugging-rag-systems.md) | [↑ Index](../INDEX.md)

