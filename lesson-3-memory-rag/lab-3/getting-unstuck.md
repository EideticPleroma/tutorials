# Getting Unstuck - Lab 3

Hints and guidance when you're stuck on Lab 3 exercises.

---

## Before Asking for Help

1. **Read the error message** - What does it actually say?
2. **Check the logs** - Is there more context?
3. **Verify prerequisites** - Did earlier steps work?
4. **Try a simpler case** - Does a minimal example work?

---

## Exercise 1 Hints

### Task 1: Install Dependencies

**Stuck on imports?**

Check you installed the right packages:
```bash
# These are the correct package names
pip install llama-index-core
pip install llama-index-llms-ollama
pip install llama-index-embeddings-huggingface

# NOT these (common mistakes)
# pip install llama-index  # Old package
# pip install llamaindex   # Wrong name
```

### Task 2: Configure LlamaIndex

**Settings not taking effect?**

Make sure you call configure() before using LlamaIndex:
```python
from src.memory_rag.config import configure
configure()  # Must be called first!

# Now use LlamaIndex
from llama_index.core import VectorStoreIndex
```

**Ollama connection failing?**

```python
# Check Ollama is running
import requests
try:
    r = requests.get("http://localhost:11434/api/tags")
    print("Ollama is running")
except:
    print("Start Ollama with: ollama serve")
```

### Task 3: Create First Index

**No documents loaded?**

Check your paths:
```python
from llama_index.core import SimpleDirectoryReader
import os

# Verify path exists
path = "./data/sample_docs"
print(f"Path exists: {os.path.exists(path)}")
print(f"Contents: {os.listdir(path) if os.path.exists(path) else 'N/A'}")

# Load with verbose output
docs = SimpleDirectoryReader(path).load_data()
print(f"Loaded {len(docs)} documents")
for d in docs:
    print(f"  - {d.metadata.get('file_name')}: {len(d.text)} chars")
```

### Task 4: Query the Index

**Query returns nothing relevant?**

Verify the index has content:
```python
# Check what's in the index
print(f"Documents in index: {len(index.docstore.docs)}")

# Try a very generic query
results = index.as_retriever(similarity_top_k=10).retrieve("the")
print(f"Generic query found: {len(results)} results")
```

---

## Exercise 2 Hints

### Task 1: Document Loaders

**Files not being found?**

Debug your paths:
```python
import os
from pathlib import Path

# Check project structure
for root, dirs, files in os.walk(".", topdown=True):
    # Skip hidden and cache directories
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
    
    py_files = [f for f in files if f.endswith('.py')]
    md_files = [f for f in files if f.endswith('.md')]
    
    if py_files or md_files:
        print(f"{root}: {len(py_files)} .py, {len(md_files)} .md")
```

**Metadata not being added?**

Check your loader returns Documents with metadata:
```python
def load_code_files(base_path: str) -> list:
    from llama_index.core import SimpleDirectoryReader
    
    reader = SimpleDirectoryReader(
        input_dir=f"{base_path}/src",
        recursive=True,
        required_exts=[".py"],
    )
    
    docs = reader.load_data()
    
    # Add custom metadata
    for doc in docs:
        doc.metadata["file_type"] = "python"
        doc.metadata["category"] = "code"
    
    return docs
```

### Task 3: Build Project Index

**RAGEngine not working?**

Test each method individually:
```python
engine = RAGEngine()

# Test build
try:
    engine.build_index(".")
    print("Build: OK")
except Exception as e:
    print(f"Build failed: {e}")

# Test load
try:
    engine.load_index()
    print("Load: OK")
except Exception as e:
    print(f"Load failed: {e}")

# Test query
try:
    result = engine.query("test")
    print(f"Query: OK ({len(result)} chars)")
except Exception as e:
    print(f"Query failed: {e}")
```

### Task 5: Test Retrieval Quality

**Expected files not in results?**

Debug with verbose output:
```python
query = "What is the 7-step tool calling loop?"
results = engine.retrieve(query, top_k=10)

print(f"Query: {query}\n")
print("Results:")
for i, r in enumerate(results):
    file_path = r["metadata"].get("file_path", "unknown")
    score = r["score"]
    preview = r["text"][:100].replace("\n", " ")
    print(f"  {i+1}. [{score:.3f}] {file_path}")
    print(f"      {preview}...")
```

---

## Exercise 3 Hints

### Task 1: DeepSeek Setup

**Model not found?**

```bash
# Pull the model (takes a few minutes)
ollama pull deepseek-coder:6.7b

# Verify it's there
ollama list | grep deepseek

# Test it works
ollama run deepseek-coder:6.7b "def hello():"
```

**Model very slow?**

First inference loads the model (~30 seconds). Subsequent calls are faster.

### Task 2: Model Router

**Classification not working?**

Start with simple keyword matching:
```python
def classify_task(self, request: str) -> str:
    request_lower = request.lower()
    
    # Coding keywords
    if any(kw in request_lower for kw in ["implement", "write", "code", "function", "def "]):
        return "coding"
    
    # Planning keywords
    if any(kw in request_lower for kw in ["plan", "break down", "design", "analyze"]):
        return "planning"
    
    # Reasoning keywords
    if any(kw in request_lower for kw in ["explain", "why", "how does", "what is"]):
        return "reasoning"
    
    return "unknown"
```

### Task 3: Architect Agent

**Plan output not valid JSON?**

Make the prompt more explicit:
```python
prompt = """Create a task plan. 

IMPORTANT: Output ONLY valid JSON, nothing else. No explanation, no markdown.

Format:
{"tasks": [{"id": 1, "description": "...", "file": "...", "spec": "..."}]}

Request: {request}

JSON output:"""
```

### Task 4: Builder Agent

**Code has markdown fences?**

Clean the output:
```python
def _clean_code(self, code: str) -> str:
    code = code.strip()
    
    # Remove markdown fences
    if code.startswith("```"):
        lines = code.split("\n")
        # Skip first line (```python or similar)
        lines = lines[1:]
        # Remove trailing fence
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        code = "\n".join(lines)
    
    return code.strip()
```

### Task 5: Test Model Handoff

**Architect and Builder not communicating?**

Test each independently first:
```python
# Test Architect alone
plan = architect.plan("Add a greeting function")
print(f"Plan: {plan}")

# Test Builder alone with hardcoded task
task = {
    "id": 1,
    "description": "Add greeting function",
    "file": "test.py",
    "spec": "Function that takes name and returns greeting"
}
result = builder.implement(task)
print(f"Code: {result['code']}")
```

---

## Exercise 4 Hints

### Task 3: O.V.E. Harness

**Validation passing bad code?**

Add more checks:
```python
def validate(self, observation: dict) -> dict:
    results = {"passed": True, "checks": []}
    code = observation["code"]
    
    # 1. Syntax
    try:
        compile(code, "<string>", "exec")
        results["checks"].append({"name": "syntax", "passed": True})
    except SyntaxError as e:
        results["passed"] = False
        results["checks"].append({"name": "syntax", "passed": False, "error": str(e)})
        return results  # Can't check more if syntax fails
    
    # 2. Has function definition
    if "def " not in code:
        results["passed"] = False
        results["checks"].append({"name": "has_function", "passed": False})
    
    # 3. Has type hints (if has function)
    if "def " in code:
        # Simple check: look for ": " in function signature
        func_line = code.split("def ")[1].split("\n")[0]
        has_hints = ": " in func_line.split(")")[0] or "-> " in func_line
        results["checks"].append({"name": "type_hints", "passed": has_hints})
        if not has_hints:
            results["passed"] = False
    
    # 4. Has docstring
    has_docstring = '"""' in code or "'''" in code
    results["checks"].append({"name": "docstring", "passed": has_docstring})
    
    return results
```

### Task 4: Iteration Loop

**Retry loop not working?**

Add detailed logging:
```python
def _process_task(self, task: dict) -> dict:
    for attempt in range(self.MAX_RETRIES):
        self.logger.info("="*50)
        self.logger.info(f"Task {task['id']}, Attempt {attempt + 1}")
        
        # Builder implements
        impl = self.builder.implement(task)
        self.logger.info(f"Builder output: {len(impl['code'])} chars")
        
        # O.V.E. validates
        ove = self.harness.run(impl)
        self.logger.info(f"O.V.E. result: {ove}")
        
        if ove["overall_passed"]:
            self.logger.info("O.V.E. passed!")
            # Continue to architect validation...
        else:
            self.logger.info(f"O.V.E. failed: {ove['validation']}")
            # Add error context for retry
            task["previous_errors"] = ove
```

### Task 5: End-to-End Test

**Full workflow failing?**

Test each step in isolation:
```python
# Step 1: Test RAG
results = coordinator.rag_engine.retrieve("test query")
assert len(results) > 0, "RAG not returning results"

# Step 2: Test Architect
plan = coordinator.architect.plan("Simple task")
assert len(plan) > 0, "Architect not creating plans"

# Step 3: Test Builder
task = {"id": 1, "description": "test", "file": "test.py", "spec": "test"}
impl = coordinator.builder.implement(task)
assert "code" in impl, "Builder not returning code"

# Step 4: Test O.V.E.
ove = coordinator.harness.run(impl)
print(f"O.V.E. result: {ove}")

# Step 5: Full workflow
result = coordinator.process_request("Add a simple function")
print(f"Full result: {result}")
```

---

## General Debugging Tips

### Enable Verbose Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or for specific modules
logging.getLogger("src.memory_rag").setLevel(logging.DEBUG)
```

### Use Print Debugging

When logging isn't enough:
```python
def process_request(self, request: str) -> dict:
    print(f"[DEBUG] Starting request: {request}")
    
    plan = self.architect.plan(request)
    print(f"[DEBUG] Plan: {plan}")
    
    for task in plan:
        print(f"[DEBUG] Processing task: {task['id']}")
        result = self._process_task(task)
        print(f"[DEBUG] Task result: {result}")
    
    # ...
```

### Isolate the Problem

Create minimal test cases:
```python
# Don't test everything at once
# Test ONE thing

# BAD: Test full workflow
result = coordinator.process_request("Complex request")

# GOOD: Test one component
plan = architect.plan("Simple request")
print(plan)  # Does this work?
```

---

## Still Stuck?

1. **Re-read the exercise** - Did you miss a requirement?
2. **Check troubleshooting** - Is there a known issue?
3. **Check FAQ** - Has someone asked this before?
4. **Simplify** - Can you make a minimal example that fails?
5. **Ask with context** - Include error messages and what you tried

**When asking for help, include:**
- What you're trying to do
- What you expected to happen
- What actually happened
- The full error message
- What you've already tried

