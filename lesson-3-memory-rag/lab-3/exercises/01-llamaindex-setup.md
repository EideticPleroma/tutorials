# Exercise 1: LlamaIndex Setup

| Duration | Difficulty | Prerequisites | Skills Practiced |
|----------|------------|---------------|------------------|
| ~60 min | Beginner | Ollama running, RAG concepts read | LlamaIndex setup, Document indexing, Basic queries |

## Objective

Set up LlamaIndex with Ollama and create your first searchable index from sample documents.

## Context

Before we can build RAG-powered agents, we need the foundation: a working LlamaIndex installation that can index documents and answer questions about them.

**What you'll accomplish:**
- Install and configure LlamaIndex packages
- Connect LlamaIndex to your local Ollama instance
- Create an index from sample documents
- Query the index and understand the results

```
Sample Documents
    ↓
LlamaIndex (embed + index)
    ↓
Query Engine
    ↓
"What is in these documents?"
```

## Prerequisites

- [ ] Python 3.11+ installed
- [ ] Ollama running with `llama3.1:8b` model
- [ ] Read [RAG Architecture](../../tutorial-3/concepts/rag-architecture.md)
- [ ] Read [Setting Up LlamaIndex](../../tutorial-3/guides/setting-up-llamaindex.md)

**Verify Ollama:**
```bash
ollama list
# Should show llama3.1:8b
```

## Tasks

### Task 1: Install Dependencies

Install the required LlamaIndex packages.

**Requirements:**
- Core LlamaIndex package
- Ollama LLM integration
- HuggingFace embeddings (local, free)
- File readers

**AI Assistant Prompt:**
```
@.cursorrules @lesson-3-memory-rag/tutorial-3/guides/setting-up-llamaindex.md

I need to install LlamaIndex with Ollama support for local RAG development.

Requirements:
- LlamaIndex core
- Ollama integration for LLM
- Local embeddings (HuggingFace bge-small)
- File readers for Python and markdown

Generate the pip install commands.
```

**Validation:**
```bash
# Should complete without errors
python -c "from llama_index.core import Settings; print('Core OK')"
python -c "from llama_index.llms.ollama import Ollama; print('Ollama OK')"
python -c "from llama_index.embeddings.huggingface import HuggingFaceEmbedding; print('Embeddings OK')"
```

### Task 2: Configure LlamaIndex with Ollama

Create the configuration file that connects LlamaIndex to Ollama.

**Create file:** `src/memory_rag/config.py`

**Requirements:**
- Configure `Settings.llm` to use Ollama with llama3.1:8b
- Configure `Settings.embed_model` to use bge-small-en-v1.5
- Set chunk_size to 512 and chunk_overlap to 50
- Add request timeout of 120 seconds for LLM

**AI Assistant Prompt:**
```
@.cursorrules @src/memory_rag/config.py

Create a LlamaIndex configuration module that:
1. Configures Settings.llm with Ollama (llama3.1:8b, 120s timeout, temperature 0.1)
2. Configures Settings.embed_model with HuggingFace bge-small-en-v1.5
3. Sets chunk_size=512 and chunk_overlap=50
4. Exports a configure() function that applies these settings

Include type hints and docstrings following project standards.
```

**Validation:**
```python
from src.memory_rag.config import configure
configure()

from llama_index.core import Settings
print(f"LLM: {Settings.llm.model}")
print(f"Embed model: {Settings.embed_model.model_name}")
print(f"Chunk size: {Settings.chunk_size}")
```

Expected output:
```
LLM: llama3.1:8b
Embed model: BAAI/bge-small-en-v1.5
Chunk size: 512
```

### Task 3: Create Your First Index

Create an index from sample documents.

**Step 1:** Create sample documents

Create a `data/sample_docs/` directory with some test files:

```
data/sample_docs/
├── about_rag.md
├── about_agents.md
└── sample_code.py
```

**Content for `about_rag.md`:**
```markdown
# About RAG

Retrieval-Augmented Generation (RAG) enhances LLM responses by retrieving 
relevant context from a knowledge base before generating answers.

## Key Components

1. **Document Loader**: Reads files into documents
2. **Chunker**: Splits documents into smaller pieces
3. **Embedder**: Converts text to vectors
4. **Vector Store**: Stores and searches embeddings
5. **Query Engine**: Orchestrates retrieval and generation
```

**Content for `about_agents.md`:**
```markdown
# About AI Agents

An AI agent is a system that uses an LLM to reason about tasks and take actions.

## Key Concepts

- **Tool Calling**: Agents can invoke external functions
- **Planning**: Breaking down complex tasks
- **Memory**: Remembering context across interactions
- **Coordination**: Multiple agents working together
```

**Content for `sample_code.py`:**
```python
"""Sample Python file for indexing test."""

def greet(name: str) -> str:
    """Greet a person by name.
    
    Args:
        name: The person's name
        
    Returns:
        A greeting string
    """
    return f"Hello, {name}!"

class Calculator:
    """A simple calculator class."""
    
    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        return a + b
```

**Step 2:** Create the indexing script

**Create file:** `scripts/create_sample_index.py`

**AI Assistant Prompt:**
```
@.cursorrules @src/memory_rag/config.py

Create a script that:
1. Imports and calls configure() from config.py
2. Loads documents from data/sample_docs/ using SimpleDirectoryReader
3. Creates a VectorStoreIndex from the documents
4. Saves the index to ./storage/sample_index/
5. Prints the number of documents loaded and indexed

Include proper error handling and progress output.
```

**Run the script:**
```bash
python scripts/create_sample_index.py
```

**Expected output:**
```
Configuring LlamaIndex...
Loading documents from data/sample_docs/...
Loaded 3 documents
Creating index...
Index created with 3 documents
Saving to ./storage/sample_index/...
Done!
```

### Task 4: Query the Index

Create a query script and test retrieval.

**Create file:** `scripts/query_sample_index.py`

**AI Assistant Prompt:**
```
@.cursorrules @src/memory_rag/config.py

Create a query script that:
1. Configures LlamaIndex settings
2. Loads the index from ./storage/sample_index/
3. Creates a query engine with similarity_top_k=3
4. Takes a query from command line argument or uses default
5. Prints the response and source nodes (file, score, preview)

Include error handling for missing index.
```

**Test queries:**
```bash
# Query about RAG
python scripts/query_sample_index.py "What is RAG?"

# Query about agents
python scripts/query_sample_index.py "What can AI agents do?"

# Query about code
python scripts/query_sample_index.py "How do I greet someone in the code?"
```

**Expected output for "What is RAG?":**
```
Query: What is RAG?

Response: RAG (Retrieval-Augmented Generation) enhances LLM responses by 
retrieving relevant context from a knowledge base before generating answers.
The key components include document loaders, chunkers, embedders, vector 
stores, and query engines.

Sources:
[1] about_rag.md (score: 0.89)
    Preview: # About RAG\n\nRetrieval-Augmented Generation (RAG) enhances...
[2] about_agents.md (score: 0.52)
    Preview: # About AI Agents\n\nAn AI agent is a system...
```

## Validation Checkpoints

After completing all tasks, verify:

- [ ] All imports work without errors
- [ ] Configuration shows correct LLM and embed model
- [ ] Index is created in `./storage/sample_index/`
- [ ] Queries return relevant results with sources
- [ ] RAG query gets highest score for about_rag.md

**Full verification script:**
```python
"""Verify Exercise 1 completion."""

def verify_exercise_1():
    print("Verifying Exercise 1...\n")
    
    # 1. Check imports
    try:
        from llama_index.core import Settings, VectorStoreIndex
        from llama_index.llms.ollama import Ollama
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding
        print("[OK] All imports successful")
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        return False
    
    # 2. Check configuration
    try:
        from src.memory_rag.config import configure
        configure()
        assert Settings.llm is not None
        assert Settings.embed_model is not None
        print("[OK] Configuration successful")
    except Exception as e:
        print(f"[FAIL] Configuration error: {e}")
        return False
    
    # 3. Check index exists
    import os
    if os.path.exists("./storage/sample_index"):
        print("[OK] Index directory exists")
    else:
        print("[FAIL] Index not found at ./storage/sample_index")
        return False
    
    # 4. Check query works
    try:
        from llama_index.core import StorageContext, load_index_from_storage
        storage_context = StorageContext.from_defaults(
            persist_dir="./storage/sample_index"
        )
        index = load_index_from_storage(storage_context)
        query_engine = index.as_query_engine()
        response = query_engine.query("What is RAG?")
        assert "retrieval" in str(response).lower() or "rag" in str(response).lower()
        print("[OK] Query returns relevant response")
    except Exception as e:
        print(f"[FAIL] Query error: {e}")
        return False
    
    print("\n All Exercise 1 checks passed!")
    return True

if __name__ == "__main__":
    verify_exercise_1()
```

## Checkpoint Questions

Before moving to Exercise 2, verify you understand:

1. **What does `Settings.llm` control?**
   <details>
   <summary>Answer</summary>
   The LLM used for generating responses in query engines. We set it to Ollama with llama3.1:8b for local inference.
   </details>

2. **What does `Settings.embed_model` control?**
   <details>
   <summary>Answer</summary>
   The model used to convert text into vectors (embeddings). We use bge-small-en-v1.5 for free, local embeddings.
   </details>

3. **Why do we persist the index?**
   <details>
   <summary>Answer</summary>
   To avoid re-computing embeddings every time we start the application. Embedding can be slow for large document sets.
   </details>

4. **What does `similarity_top_k` control?**
   <details>
   <summary>Answer</summary>
   The number of most similar chunks to retrieve for each query. Higher values provide more context but may include irrelevant results.
   </details>

## Common Issues

### Issue: "Ollama connection refused"

**Solution:** Ensure Ollama is running:
```bash
ollama serve
```

### Issue: "Model not found"

**Solution:** Pull the required model:
```bash
ollama pull llama3.1:8b
```

### Issue: "Embedding model download slow"

**Solution:** The first run downloads the model (~130MB). Subsequent runs use cache:
```python
HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    cache_folder="./models"  # Cache locally
)
```

### Issue: "Out of memory"

**Solution:** Reduce batch size:
```python
Settings.embed_batch_size = 10  # Default is 100
```

## Next Steps

You've set up the foundation! Now let's index something more substantial.

👉 **Continue to [Exercise 2: Embedding the Project](./02-embedding-the-project.md)**

You'll index the entire tutorial codebase and documentation.

---

## 💡 Tips

**Start simple:** Make sure basic indexing works before adding complexity.

**Check Ollama:** Most issues are Ollama connectivity. Verify it's running.

**Use show_progress:** Add `show_progress=True` to index creation to see progress.

**Inspect documents:** Print loaded documents to verify content before indexing.

