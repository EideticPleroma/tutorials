# Setup Guide - Lab 3

This guide helps you set up the environment for Lab 3: Memory & RAG.

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **RAM** | 12GB | 16GB+ |
| **Storage** | 10GB free | 20GB free |
| **Python** | 3.11 | 3.11+ |
| **Ollama** | 0.4.0 | Latest |

**Why more RAM?** Lab 3 runs two models (Llama + DeepSeek) and stores embeddings.

## Python Dependencies

### Core Installation

```bash
# From project root
cd /mnt/d/Projects/tutorials

# Install LlamaIndex core packages
pip install llama-index-core \
            llama-index-llms-ollama \
            llama-index-embeddings-huggingface \
            llama-index-readers-file

# Optional: Persistent vector storage
pip install llama-index-vector-stores-chroma chromadb
```

### All-in-One

Or install everything with one command:

```bash
pip install llama-index-core \
            llama-index-llms-ollama \
            llama-index-embeddings-huggingface \
            llama-index-readers-file \
            llama-index-vector-stores-chroma \
            chromadb \
            sentence-transformers
```

### Update requirements.txt

Add to your project's `requirements.txt`:

```
# Tutorial 3: Memory & RAG
llama-index-core
llama-index-llms-ollama
llama-index-embeddings-huggingface
llama-index-readers-file
llama-index-vector-stores-chroma
chromadb
sentence-transformers
```

## Ollama Models

### Required Models

```bash
# Llama 3.1 for reasoning (you should already have this)
ollama pull llama3.1:8b

# DeepSeek-Coder for code generation (NEW for Lab 3)
ollama pull deepseek-coder:6.7b
```

### Model Sizes

| Model | Download | RAM Usage |
|-------|----------|-----------|
| llama3.1:8b | ~4.7GB | ~8GB |
| deepseek-coder:6.7b | ~4GB | ~6GB |

**Note:** When running both models, you may need to wait for model swapping. Ollama manages memory automatically.

### Verify Models

```bash
# List all models
ollama list

# Expected output:
# NAME                    ID              SIZE    MODIFIED
# llama3.1:8b            ...             4.7 GB  ...
# deepseek-coder:6.7b    ...             4.0 GB  ...

# Test Llama
ollama run llama3.1:8b "Say hello"

# Test DeepSeek
ollama run deepseek-coder:6.7b "Write a Python hello world"
```

## LlamaIndex Packages

Here's what each package does:

| Package | Purpose |
|---------|---------|
| `llama-index-core` | Core abstractions (Document, Index, etc.) |
| `llama-index-llms-ollama` | Connect LlamaIndex to Ollama |
| `llama-index-embeddings-huggingface` | Local embedding models |
| `llama-index-readers-file` | Load PDF, markdown, code files |
| `llama-index-vector-stores-chroma` | ChromaDB integration |
| `chromadb` | Vector database for persistence |

## ChromaDB (Optional)

ChromaDB provides persistent vector storage. Without it, your index is lost when the process ends.

### In-Memory (Development)
```python
# No persistence - good for testing
from llama_index.core import VectorStoreIndex
index = VectorStoreIndex.from_documents(docs)
```

### Persistent (Production)
```python
# Saved to disk - survives restarts
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("my_index")
vector_store = ChromaVectorStore(chroma_collection=collection)
```

## Verification Commands

Run these to verify your setup:

```bash
# 1. Check Python version
python --version
# Expected: Python 3.11.x or higher

# 2. Check Ollama
ollama --version
# Expected: 0.4.x or higher

# 3. Check models
ollama list
# Expected: llama3.1:8b and deepseek-coder:6.7b

# 4. Check LlamaIndex imports
python -c "from llama_index.core import Settings; print('Core OK')"
python -c "from llama_index.llms.ollama import Ollama; print('Ollama OK')"
python -c "from llama_index.embeddings.huggingface import HuggingFaceEmbedding; print('Embeddings OK')"

# 5. Test embedding model download (first run downloads ~130MB)
python -c "
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
embed = HuggingFaceEmbedding(model_name='BAAI/bge-small-en-v1.5')
result = embed.get_text_embedding('test')
print(f'Embedding OK: {len(result)} dimensions')
"
```

## Quick Start

Once setup is verified, create your first index:

```python
"""Quick start script for Lab 3."""

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Configure
Settings.llm = Ollama(model="llama3.1:8b", request_timeout=120.0)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Create a test file
with open("test_doc.txt", "w") as f:
    f.write("RAG stands for Retrieval-Augmented Generation. It improves LLM responses by retrieving relevant context first.")

# Load and index
docs = SimpleDirectoryReader(input_files=["test_doc.txt"]).load_data()
index = VectorStoreIndex.from_documents(docs)

# Query
engine = index.as_query_engine()
response = engine.query("What is RAG?")
print(response)

# Cleanup
import os
os.remove("test_doc.txt")
```

## Directory Structure

After setup, create the Lab 3 directories:

```bash
mkdir -p src/memory_rag
mkdir -p tests/memory_rag
mkdir -p storage
mkdir -p data/sample_docs

touch src/memory_rag/__init__.py
```

Expected structure:
```
src/
├── agent/           # Tutorial 1
├── multi_agent/     # Tutorial 2
└── memory_rag/      # Tutorial 3 (NEW)
    └── __init__.py

tests/
├── unit/            # Tutorial 1
├── multi_agent/     # Tutorial 2
└── memory_rag/      # Tutorial 3 (NEW)

storage/             # Index storage
data/
└── sample_docs/     # Test documents
```

## Common Setup Issues

### Issue: "ModuleNotFoundError: llama_index"

**Solution:** Install with correct package names:
```bash
pip install llama-index-core  # NOT llama-index
```

### Issue: "Ollama connection refused"

**Solution:** Start Ollama:
```bash
ollama serve
```

### Issue: "Model not found"

**Solution:** Pull the model:
```bash
ollama pull llama3.1:8b
ollama pull deepseek-coder:6.7b
```

### Issue: "Out of memory"

**Solutions:**
1. Close other applications
2. Use smaller embedding batch size:
   ```python
   Settings.embed_batch_size = 10
   ```
3. Index documents in smaller batches

### Issue: "Embedding model download fails"

**Solution:** Use a local cache:
```python
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    cache_folder="./models"
)
```

## Next Steps

Setup complete? Start the lab:

👉 **[Exercise 1: LlamaIndex Setup](./exercises/01-llamaindex-setup.md)**

