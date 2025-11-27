# Troubleshooting Guide - Lab 3

Solutions for common errors in Tutorial 3: Memory & RAG.

---

## LlamaIndex Errors

### ImportError: No module named 'llama_index'

**Cause:** Wrong package name or not installed.

**Solution:**
```bash
# Install the correct packages (note the dashes, not underscores)
pip install llama-index-core
pip install llama-index-llms-ollama
pip install llama-index-embeddings-huggingface
```

### ImportError: cannot import name 'X' from 'llama_index'

**Cause:** LlamaIndex restructured packages in v0.10+.

**Solution:** Use new import paths:
```python
# Old (v0.9 and earlier)
from llama_index import VectorStoreIndex

# New (v0.10+)
from llama_index.core import VectorStoreIndex
```

Common import mappings:
```python
# Core classes
from llama_index.core import Settings, VectorStoreIndex, Document
from llama_index.core import SimpleDirectoryReader, StorageContext

# LLMs
from llama_index.llms.ollama import Ollama

# Embeddings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
```

### ValueError: Could not load model

**Cause:** Embedding model not downloaded or wrong name.

**Solution:**
```python
# Use exact model name
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",  # Exact HuggingFace ID
    cache_folder="./models"  # Cache locally
)
```

### TimeoutError during indexing

**Cause:** Embedding or LLM call taking too long.

**Solution:**
```python
# Increase timeout
Settings.llm = Ollama(
    model="llama3.1:8b",
    request_timeout=300.0  # 5 minutes
)

# Reduce batch size
Settings.embed_batch_size = 10  # Default is 100
```

---

## Ollama Errors

### ConnectionRefusedError: [Errno 111] Connection refused

**Cause:** Ollama service not running.

**Solution:**
```bash
# Start Ollama
ollama serve

# Or check if it's running
curl http://localhost:11434/api/tags
```

### Error: model 'X' not found

**Cause:** Model not pulled or wrong name.

**Solution:**
```bash
# Pull the model
ollama pull llama3.1:8b
ollama pull deepseek-coder:6.7b

# List available models
ollama list
```

### CUDA out of memory

**Cause:** GPU memory exhausted.

**Solution:**
```bash
# Force CPU inference
OLLAMA_HOST=0.0.0.0 ollama serve

# Or reduce context in code
Settings.llm = Ollama(
    model="llama3.1:8b",
    context_window=4096  # Smaller context
)
```

### Model switching is very slow

**Cause:** Ollama swapping models in memory.

**Solution:**
```bash
# Keep models loaded (needs more RAM)
# In Ollama settings or environment
OLLAMA_NUM_PARALLEL=2

# Or batch similar tasks
# Run all Llama tasks, then all DeepSeek tasks
```

---

## Embedding Errors

### RuntimeError: CUDA error: device-side assert

**Cause:** GPU issue with embeddings.

**Solution:**
```python
# Force CPU
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    device="cpu"  # Force CPU
)
```

### Embeddings are all zeros or NaN

**Cause:** Model not loaded correctly.

**Solution:**
```python
# Verify embedding works
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
test = embed_model.get_text_embedding("test")
print(f"Dimension: {len(test)}")
print(f"First 5: {test[:5]}")
print(f"Any NaN: {any(x != x for x in test)}")  # NaN != NaN
```

### Dimension mismatch error

**Cause:** Mixed embedding models in same index.

**Solution:**
```python
# Delete old index and rebuild with consistent model
import shutil
shutil.rmtree("./storage/project_index")

# Ensure same model for all embeddings
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)
```

---

## Retrieval Quality Issues

### Query returns no results

**Causes and solutions:**

1. **Index is empty:**
   ```python
   # Check index size
   print(f"Index has {len(index.docstore.docs)} documents")
   ```

2. **Similarity threshold too high:**
   ```python
   # Lower threshold or remove it
   query_engine = index.as_query_engine(
       similarity_top_k=10,  # Get more results
   )
   ```

3. **Query doesn't match content:**
   ```python
   # Try more generic query
   results = engine.retrieve("python")  # Very generic
   print(f"Found {len(results)} results")
   ```

### Query returns wrong documents

**Causes and solutions:**

1. **Chunks too large:**
   ```python
   Settings.chunk_size = 256  # Smaller chunks
   # Rebuild index
   ```

2. **Wrong embedding model for content type:**
   ```python
   # For code, consider code-specific embeddings
   # Or add metadata filters
   results = retriever.retrieve(
       query,
       filters={"file_type": "python"}
   )
   ```

3. **Query ambiguous:**
   ```python
   # Be more specific
   # Instead of: "how does it work"
   # Use: "how does the coordinator delegate tasks to workers"
   ```

### Scores are all very low (<0.5)

**Causes and solutions:**

1. **Content not in index:**
   ```python
   # Verify content exists
   for doc in index.docstore.docs.values():
       if "keyword" in doc.text:
           print("Found!")
   ```

2. **Embedding model mismatch:**
   ```python
   # Ensure query uses same model as indexing
   # Check Settings.embed_model
   ```

3. **Content is code, query is natural language:**
   ```python
   # Try code-like query
   # Instead of: "how to greet users"
   # Use: "def greet" or "greeting function"
   ```

---

## Multi-Model Issues

### Router always picks same model

**Cause:** Classification not working.

**Solution:**
```python
# Debug classification
router = ModelRouter()

test_queries = [
    "Write a function",
    "Explain this code",
    "Plan the implementation",
]

for q in test_queries:
    task_type = router.classify_task(q)
    print(f"'{q}' -> {task_type}")
```

### DeepSeek produces markdown-wrapped code

**Cause:** Model trained to output markdown.

**Solution:**
```python
def clean_code(code: str) -> str:
    """Remove markdown code fences."""
    code = code.strip()
    if code.startswith("```"):
        lines = code.split("\n")
        # Remove first line (```python)
        lines = lines[1:]
        # Remove last line if it's ```)
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        code = "\n".join(lines)
    return code
```

### Architect plan is not valid JSON

**Cause:** LLM adds extra text around JSON.

**Solution:**
```python
import json
import re

def parse_plan(response: str) -> list:
    """Extract JSON from LLM response."""
    # Try direct parse
    try:
        return json.loads(response)["tasks"]
    except:
        pass
    
    # Find JSON in response
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())["tasks"]
        except:
            pass
    
    # Find JSON array
    array_match = re.search(r'\[.*\]', response, re.DOTALL)
    if array_match:
        try:
            return json.loads(array_match.group())
        except:
            pass
    
    return []
```

### Model produces incomplete output

**Cause:** Max tokens too low.

**Solution:**
```python
Settings.llm = Ollama(
    model="llama3.1:8b",
    num_predict=2048,  # Max output tokens
)
```

---

## O.V.E. Harness Issues

### Syntax validation passes but code doesn't run

**Cause:** `compile()` only checks syntax, not imports or runtime.

**Solution:**
```python
def validate_imports(code: str) -> dict:
    """Check that imports are valid."""
    import_lines = [l for l in code.split("\n") if l.startswith("import") or l.startswith("from")]
    
    results = {"passed": True, "issues": []}
    
    for line in import_lines:
        try:
            exec(line)
        except ImportError as e:
            results["passed"] = False
            results["issues"].append(f"Invalid import: {line}")
    
    return results
```

### Tests never run in evaluate phase

**Cause:** Test execution not implemented.

**Solution:**
```python
import subprocess
import tempfile

def run_tests(test_code: str) -> dict:
    """Actually execute tests in sandbox."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        f.flush()
        
        result = subprocess.run(
            ['python', '-m', 'pytest', f.name, '-v'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "passed": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
```

### Type hint check gives false negatives

**Cause:** Complex type hints not detected.

**Solution:**
```python
import ast

def has_type_hints(code: str) -> bool:
    """Check for type hints using AST."""
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check return annotation
                if node.returns is not None:
                    return True
                # Check argument annotations
                for arg in node.args.args:
                    if arg.annotation is not None:
                        return True
        return False
    except:
        return False
```

---

## Storage/Persistence Issues

### Index not found after restart

**Cause:** Index wasn't persisted.

**Solution:**
```python
# Save index
index.storage_context.persist(persist_dir="./storage/project_index")

# Load index
from llama_index.core import StorageContext, load_index_from_storage

storage_context = StorageContext.from_defaults(persist_dir="./storage/project_index")
index = load_index_from_storage(storage_context)
```

### ChromaDB "collection already exists"

**Cause:** Trying to create existing collection.

**Solution:**
```python
# Use get_or_create instead of create
collection = client.get_or_create_collection("my_collection")
```

### Permission denied on storage directory

**Cause:** File permissions.

**Solution:**
```bash
# Fix permissions
chmod -R 755 ./storage

# Or use different directory
mkdir -p ~/.cache/tutorial_index
```

---

## Quick Diagnostic Script

Run this to diagnose common issues:

```python
"""Lab 3 diagnostic script."""

def diagnose():
    issues = []
    
    # 1. Check imports
    try:
        from llama_index.core import Settings
        from llama_index.llms.ollama import Ollama
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding
        print("[OK] LlamaIndex imports")
    except ImportError as e:
        issues.append(f"Import error: {e}")
        print(f"[FAIL] LlamaIndex imports: {e}")
    
    # 2. Check Ollama connection
    try:
        import requests
        r = requests.get("http://localhost:11434/api/tags")
        models = [m["name"] for m in r.json()["models"]]
        print(f"[OK] Ollama running, models: {models}")
        
        if "llama3.1:8b" not in str(models):
            issues.append("llama3.1:8b not found")
        if "deepseek-coder" not in str(models):
            issues.append("deepseek-coder not found")
    except Exception as e:
        issues.append(f"Ollama connection: {e}")
        print(f"[FAIL] Ollama: {e}")
    
    # 3. Check embedding model
    try:
        embed = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        vec = embed.get_text_embedding("test")
        print(f"[OK] Embeddings working ({len(vec)} dims)")
    except Exception as e:
        issues.append(f"Embeddings: {e}")
        print(f"[FAIL] Embeddings: {e}")
    
    # 4. Check storage
    import os
    if os.path.exists("./storage"):
        contents = os.listdir("./storage")
        print(f"[OK] Storage directory exists: {contents}")
    else:
        print("[INFO] Storage directory doesn't exist yet")
    
    # Summary
    print("\n" + "="*50)
    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("All checks passed!")
    
    return len(issues) == 0

if __name__ == "__main__":
    diagnose()
```

---

## Still Stuck?

1. Check [FAQ](./FAQ.md) for conceptual questions
2. Check [Getting Unstuck](./getting-unstuck.md) for exercise hints
3. Review your logs for specific error messages
4. Ask your AI assistant with full error context

