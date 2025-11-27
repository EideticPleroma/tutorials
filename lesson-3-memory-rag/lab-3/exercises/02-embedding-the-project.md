# Exercise 2: Embedding the Tutorial Project

**Duration**: ~90 minutes | **Difficulty**: Intermediate

## Objective

Index the entire tutorial codebase and documentation, creating a knowledge base that agents can query to understand their own implementation.

## Context

"Teaching the agent about itself" - by indexing our codebase, we enable agents to:
- Answer questions about their own implementation
- Find relevant code patterns when implementing new features
- Understand project conventions and architecture

**What you'll build:**
```
src/agent/           ─┐
src/multi_agent/      │
lesson-1-fundamentals/├─→ [RAG Index] ─→ "How does the coordinator work?"
lesson-2-multi-agent/ │                  "What is the 7-step loop?"
tests/               ─┘
```

## Prerequisites

- [ ] Complete [Exercise 1: LlamaIndex Setup](./01-llamaindex-setup.md)
- [ ] Read [Embeddings & Vector Stores](../../tutorial-3/concepts/embeddings-vector-stores.md)
- [ ] Read [Debugging RAG Systems](../../tutorial-3/guides/debugging-rag-systems.md)

## Code Scaffold

You'll create/modify these files:
```
src/memory_rag/
├── __init__.py
├── config.py              # From Exercise 1
├── document_loaders.py    # NEW: Custom loaders
├── rag_engine.py          # NEW: Main RAG interface
└── knowledge_tool.py      # NEW: Tool for agents
```

## Tasks

### Task 1: Create Document Loaders for Code + Docs

Create custom document loaders that handle both Python code and Markdown documentation appropriately.

**Create file:** `src/memory_rag/document_loaders.py`

**Requirements:**
- `load_code_files()`: Load .py files from src/ and tests/
- `load_documentation()`: Load .md files from lesson-1/, lesson-2/, lesson-3/
- Add metadata: file_path, file_type, category (code/docs/test)
- Exclude: __pycache__, .git, .env, .agent_state, .agent_logs

**AI Assistant Prompt:**
```
@.cursorrules @src/memory_rag/document_loaders.py

Create a document loading module with:

1. load_code_files(base_path: str) -> list[Document]
   - Load all .py files from src/ and tests/
   - Add metadata: file_path, file_type="python", category="code" or "test"
   - Exclude __pycache__, .pyc files

2. load_documentation(base_path: str) -> list[Document]  
   - Load all .md files from lesson-*/ directories
   - Add metadata: file_path, file_type="markdown", category="docs"
   - Extract tutorial number from path (lesson-1 -> tutorial=1)

3. load_all_project_files(base_path: str) -> list[Document]
   - Combine code and documentation
   - Print summary of what was loaded

Include proper type hints and Google-style docstrings.
Use SimpleDirectoryReader from llama_index.core.
```

**Validation:**
```python
from src.memory_rag.document_loaders import load_all_project_files

docs = load_all_project_files(".")
print(f"Total documents: {len(docs)}")

# Check metadata
code_docs = [d for d in docs if d.metadata.get("file_type") == "python"]
md_docs = [d for d in docs if d.metadata.get("file_type") == "markdown"]
print(f"Code files: {len(code_docs)}")
print(f"Documentation files: {len(md_docs)}")
```

### Task 2: Configure Chunking Strategy

Set up appropriate chunking for code vs. documentation.

**Considerations:**
- Code: Keep functions together (larger chunks)
- Documentation: Respect section boundaries
- Both: Sufficient overlap to maintain context

**Update `src/memory_rag/config.py`:**

**AI Assistant Prompt:**
```
@.cursorrules @src/memory_rag/config.py

Update the config module to include chunking configuration:

1. Add code chunking settings:
   - chunk_size=1024 for code (keep functions together)
   - chunk_overlap=100

2. Add documentation chunking settings:
   - chunk_size=512 for docs
   - chunk_overlap=50

3. Create a get_node_parser(file_type: str) function that returns
   the appropriate SentenceSplitter based on file type.

4. Add a configure_for_project() function that sets optimal 
   settings for indexing this tutorial project.
```

### Task 3: Build the Project Index

Create the RAG engine that indexes the project.

**Create file:** `src/memory_rag/rag_engine.py`

**Requirements:**
- `RAGEngine` class with methods:
  - `__init__(persist_dir: str)`: Initialize with storage location
  - `build_index(base_path: str)`: Index project files
  - `load_index()`: Load existing index
  - `query(question: str, top_k: int) -> str`: Query the index
  - `retrieve(question: str, top_k: int) -> list`: Get raw chunks

**AI Assistant Prompt:**
```
@.cursorrules @src/memory_rag/rag_engine.py @src/memory_rag/document_loaders.py

Create the RAGEngine class:

class RAGEngine:
    """Main interface for RAG operations on the tutorial codebase."""
    
    def __init__(self, persist_dir: str = "./storage/project_index"):
        """Initialize RAG engine with storage location."""
        # TODO: Store persist_dir, initialize index to None
    
    def build_index(self, base_path: str = ".") -> None:
        """Build index from project files."""
        # TODO: 
        # 1. Call configure_for_project()
        # 2. Load documents using load_all_project_files()
        # 3. Create VectorStoreIndex
        # 4. Persist to self.persist_dir
        # 5. Store index in self.index
    
    def load_index(self) -> None:
        """Load existing index from storage."""
        # TODO: Load from persist_dir using StorageContext
    
    def query(self, question: str, top_k: int = 5) -> str:
        """Query the index and return response."""
        # TODO: Create query engine, return response as string
    
    def retrieve(self, question: str, top_k: int = 5) -> list[dict]:
        """Retrieve chunks without generation."""
        # TODO: Use index.as_retriever(), return list of
        # {"text": ..., "score": ..., "metadata": ...}

Include logging for all operations.
Handle case where index doesn't exist (raise helpful error).
```

**Build the index:**
```python
from src.memory_rag.rag_engine import RAGEngine

engine = RAGEngine()
engine.build_index(".")  # Index current project
```

### Task 4: Implement Knowledge Query Tool

Create a tool that agents can use to query the knowledge base.

**Create file:** `src/memory_rag/knowledge_tool.py`

**Requirements:**
- `search_codebase(query: str) -> str` function decorated with `@registry.register`
- Google-style docstring (agents read this!)
- Return formatted results with file paths and content previews
- Handle errors gracefully

**AI Assistant Prompt:**
```
@.cursorrules @src/memory_rag/knowledge_tool.py @src/agent/tool_registry.py

Create a knowledge tool that agents can use:

from src.agent.tool_registry import registry
from src.memory_rag.rag_engine import RAGEngine

# Global engine instance (lazy loaded)
_engine = None

def get_engine() -> RAGEngine:
    """Get or create the RAG engine singleton."""
    global _engine
    if _engine is None:
        _engine = RAGEngine()
        _engine.load_index()
    return _engine

@registry.register
def search_codebase(query: str) -> str:
    """
    Search the tutorial codebase for relevant code and documentation.
    
    Use this tool when you need to:
    - Find how something is implemented in this project
    - Look up existing patterns or conventions
    - Understand how components work together
    
    Args:
        query: Natural language description of what to find.
               Examples: "How does the coordinator delegate tasks?"
                        "What is the message protocol format?"
                        "Show me examples of tool registration"
    
    Returns:
        Formatted search results including:
        - Relevant code snippets
        - Documentation excerpts
        - File paths for reference
        
        If nothing relevant is found, returns a message saying so.
    """
    # TODO: Implement using RAGEngine.retrieve()
    # Format results nicely for the agent to read
```

### Task 5: Test Retrieval Quality

Verify that the index returns correct results for known questions.

**Create test file:** `tests/memory_rag/test_retrieval_quality.py`

**Ground truth queries:**

| Query | Expected Source | Expected Content |
|-------|-----------------|------------------|
| "What is the 7-step tool calling loop?" | tool-calling-architecture.md | parse, execute, format |
| "How does the coordinator delegate?" | coordinator.py | delegate, worker, message |
| "What is the O.V.E. testing methodology?" | testing-agents.md | observe, validate, evaluate |
| "How do I register a tool?" | tool_registry.py or simple_agent.py | @registry.register |

**AI Assistant Prompt:**
```
@.cursorrules @tests/memory_rag/test_retrieval_quality.py

Create retrieval quality tests:

1. GROUND_TRUTH list with test cases (query, expected_files, expected_content)

2. test_retrieves_expected_files(): 
   - For each ground truth query, verify expected files appear in results

3. test_similarity_scores_above_threshold():
   - Verify top result has score > 0.7

4. test_content_contains_expected_terms():
   - Verify retrieved content contains expected keywords

Use pytest parametrize for ground truth tests.
Include a fixture that loads the RAG engine.
```

**Run tests:**
```bash
python -m pytest tests/memory_rag/test_retrieval_quality.py -v
```

## Validation Checkpoints

Test your implementation with these queries:

**Query 1: "What is the 7-step tool calling loop?"**
```python
result = engine.query("What is the 7-step tool calling loop?")
print(result)
# Should mention: parse, execute, format, and reference tool-calling-architecture
```

**Query 2: "How does the coordinator delegate tasks?"**
```python
result = engine.query("How does the coordinator delegate tasks?")
print(result)
# Should mention: Message, worker, delegate method
```

**Query 3: "Show me the Agent class initialization"**
```python
results = engine.retrieve("Agent class __init__ method", top_k=3)
for r in results:
    print(f"File: {r['metadata']['file_path']}, Score: {r['score']:.3f}")
# Should find simple_agent.py or worker_base.py
```

## O.V.E. Testing Focus

This exercise emphasizes **retrieval quality testing**:

**Ground Truth Dataset:**
```python
GROUND_TRUTH = [
    {
        "query": "What is the 7-step tool calling loop?",
        "expected_files": ["tool-calling-architecture.md"],
        "expected_content": ["parse", "execute", "format"],
    },
    {
        "query": "How does the coordinator delegate tasks?",
        "expected_files": ["coordinator.py"],
        "expected_content": ["delegate", "message", "worker"],
    },
    # Add more...
]
```

**Validation Phase:** Check that expected files appear in top-k results.

**Evaluation Phase:** Check that answer quality is good (content contains expected terms).

## Checkpoint Questions

1. **Why do we use different chunk sizes for code vs. documentation?**
   <details>
   <summary>Answer</summary>
   Code needs larger chunks to keep functions intact. Documentation can use smaller chunks since sections are more independent.
   </details>

2. **What metadata do we add to documents and why?**
   <details>
   <summary>Answer</summary>
   file_path (for citations), file_type (for filtering), category (code/docs/test for different treatment). Metadata enables filtering and provides context.
   </details>

3. **How would you debug if queries about code return documentation instead?**
   <details>
   <summary>Answer</summary>
   - Check similarity scores for both
   - Try adding metadata filter: `filter={"file_type": "python"}`
   - Inspect the query embedding to see if it's closer to prose or code
   - Adjust chunk sizes or try code-specific embedding model
   </details>

## Common Issues

### Issue: "Index is empty"

**Check:** Did documents load correctly?
```python
docs = load_all_project_files(".")
print(f"Loaded {len(docs)} documents")
for d in docs[:5]:
    print(f"  {d.metadata.get('file_path')}: {len(d.text)} chars")
```

### Issue: "Retrieval returns irrelevant results"

**Solutions:**
1. Reduce chunk_size for more precise matching
2. Increase top_k and filter by score threshold
3. Add metadata filters for code vs. docs

### Issue: "Code functions are split across chunks"

**Solution:** Increase code chunk size:
```python
Settings.chunk_size = 1500  # For code
Settings.chunk_overlap = 200
```

### Issue: "Index takes too long to build"

**Solution:** Index in batches or reduce scope:
```python
# Index just src/ first
docs = load_code_files("./src")
```

## Next Steps

Your agents can now query the codebase! Next, we'll add DeepSeek-Coder for implementation.

👉 **Continue to [Exercise 3: Multi-Model Coordination](./03-multi-model-coordination.md)**

---

## 💡 Tips

**Start with code:** Index src/ first, verify it works, then add docs.

**Check your queries:** If results are poor, try rephrasing. "coordinator delegate" vs "how does delegation work" may yield different results.

**Use metadata:** Filter by file_type when you know you need code or docs.

**Inspect chunks:** Use `retrieve()` to see raw chunks before `query()`.

