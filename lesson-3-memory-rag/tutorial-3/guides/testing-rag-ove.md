# Testing RAG with O.V.E. Methodology

[← Debugging RAG Systems](./debugging-rag-systems.md) | [↑ Index](../INDEX.md)

This guide extends the O.V.E. (Observe-Validate-Evaluate) methodology from Tutorials 1-2 to test RAG system quality.

---

## Why RAG Testing is Different

RAG introduces new testing challenges:

| Aspect | Agent Testing (T1-T2) | RAG Testing (T3) |
|--------|----------------------|------------------|
| **Inputs** | User query | User query + knowledge base |
| **Deterministic** | Tool calls | Retrieval results |
| **Probabilistic** | Response quality | Answer accuracy + retrieval quality |
| **Ground truth** | Expected tool sequence | Expected chunks + answer |

**Key insight:** RAG has TWO outputs to test:
1. **Retrieval** - Did we find the right chunks? (partially deterministic)
2. **Generation** - Did we produce the right answer? (probabilistic)

---

## O.V.E. Applied to RAG

### Observe: Capture Everything

For RAG, observation must capture both retrieval AND generation:

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class RAGObservation:
    """Complete observation of a RAG query."""
    
    # Input
    query: str
    timestamp: datetime
    
    # Retrieval phase
    retrieved_chunks: list[dict]  # {text, score, metadata}
    retrieval_time_ms: float
    
    # Generation phase
    response: str
    generation_time_ms: float
    
    # Context
    prompt_tokens: int
    response_tokens: int
    
    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "timestamp": self.timestamp.isoformat(),
            "retrieval": {
                "chunks": self.retrieved_chunks,
                "time_ms": self.retrieval_time_ms,
            },
            "generation": {
                "response": self.response,
                "time_ms": self.generation_time_ms,
            },
            "tokens": {
                "prompt": self.prompt_tokens,
                "response": self.response_tokens,
            },
        }
```

### Validate: Check Deterministic Aspects

Validation focuses on **retrieval quality** - the deterministic part:

```python
def validate_retrieval(
    observation: RAGObservation,
    expected_chunks: list[str],
    min_score: float = 0.7,
) -> dict:
    """
    Validate that retrieval returned expected chunks.
    
    Args:
        observation: The RAG observation to validate
        expected_chunks: File paths or content snippets that should be retrieved
        min_score: Minimum similarity score threshold
    
    Returns:
        Validation result with pass/fail and details
    """
    results = {
        "passed": True,
        "checks": [],
    }
    
    # Check 1: Did we retrieve anything?
    if not observation.retrieved_chunks:
        results["passed"] = False
        results["checks"].append({
            "name": "has_results",
            "passed": False,
            "message": "No chunks retrieved",
        })
        return results
    
    results["checks"].append({
        "name": "has_results",
        "passed": True,
        "message": f"Retrieved {len(observation.retrieved_chunks)} chunks",
    })
    
    # Check 2: Are scores above threshold?
    low_scores = [c for c in observation.retrieved_chunks if c["score"] < min_score]
    if low_scores:
        results["checks"].append({
            "name": "score_threshold",
            "passed": False,
            "message": f"{len(low_scores)} chunks below {min_score} threshold",
        })
    else:
        results["checks"].append({
            "name": "score_threshold",
            "passed": True,
            "message": f"All chunks above {min_score}",
        })
    
    # Check 3: Are expected chunks present?
    retrieved_content = [c["text"] for c in observation.retrieved_chunks]
    retrieved_files = [c["metadata"].get("file_path", "") for c in observation.retrieved_chunks]
    
    for expected in expected_chunks:
        found = any(
            expected in content or expected in file
            for content, file in zip(retrieved_content, retrieved_files)
        )
        if not found:
            results["passed"] = False
            results["checks"].append({
                "name": f"expected_chunk_{expected[:30]}",
                "passed": False,
                "message": f"Expected chunk not found: {expected}",
            })
        else:
            results["checks"].append({
                "name": f"expected_chunk_{expected[:30]}",
                "passed": True,
                "message": f"Found expected chunk: {expected}",
            })
    
    return results
```

### Evaluate: Judge Probabilistic Aspects

Evaluation focuses on **answer quality** - requires human judgment or LLM-as-judge:

```python
def evaluate_answer(
    observation: RAGObservation,
    expected_contains: list[str],
    expected_not_contains: list[str] = None,
) -> dict:
    """
    Evaluate answer quality.
    
    Args:
        observation: The RAG observation to evaluate
        expected_contains: Keywords/phrases that should appear in answer
        expected_not_contains: Keywords/phrases that should NOT appear
    
    Returns:
        Evaluation result with score and details
    """
    results = {
        "score": 1.0,
        "checks": [],
    }
    
    response_lower = observation.response.lower()
    
    # Check for expected content
    for expected in expected_contains:
        if expected.lower() in response_lower:
            results["checks"].append({
                "name": f"contains_{expected[:20]}",
                "passed": True,
                "message": f"Response contains '{expected}'",
            })
        else:
            results["score"] -= 0.2
            results["checks"].append({
                "name": f"contains_{expected[:20]}",
                "passed": False,
                "message": f"Response missing '{expected}'",
            })
    
    # Check for unexpected content (hallucinations, etc.)
    if expected_not_contains:
        for unexpected in expected_not_contains:
            if unexpected.lower() in response_lower:
                results["score"] -= 0.3
                results["checks"].append({
                    "name": f"not_contains_{unexpected[:20]}",
                    "passed": False,
                    "message": f"Response incorrectly contains '{unexpected}'",
                })
    
    # Ensure score doesn't go negative
    results["score"] = max(0.0, results["score"])
    
    return results
```

---

## Retrieval Quality Metrics

### Precision@K

**Definition:** Of the K chunks retrieved, how many are relevant?

```
Precision@K = (Relevant chunks in top K) / K
```

```python
def precision_at_k(
    retrieved: list[str],
    relevant: set[str],
    k: int = 5,
) -> float:
    """
    Calculate Precision@K.
    
    Args:
        retrieved: List of retrieved chunk identifiers (in order)
        relevant: Set of relevant chunk identifiers
        k: Number of top results to consider
    
    Returns:
        Precision@K score (0.0 to 1.0)
    """
    top_k = retrieved[:k]
    relevant_in_top_k = sum(1 for chunk in top_k if chunk in relevant)
    return relevant_in_top_k / k

# Example
retrieved = ["chunk_1", "chunk_3", "chunk_7", "chunk_2", "chunk_5"]
relevant = {"chunk_1", "chunk_2", "chunk_4"}

p_at_5 = precision_at_k(retrieved, relevant, k=5)
print(f"Precision@5: {p_at_5:.2f}")  # 2/5 = 0.40
```

### Recall@K

**Definition:** Of all relevant chunks, how many did we find in top K?

```
Recall@K = (Relevant chunks in top K) / (Total relevant chunks)
```

```python
def recall_at_k(
    retrieved: list[str],
    relevant: set[str],
    k: int = 5,
) -> float:
    """
    Calculate Recall@K.
    
    Args:
        retrieved: List of retrieved chunk identifiers (in order)
        relevant: Set of relevant chunk identifiers
        k: Number of top results to consider
    
    Returns:
        Recall@K score (0.0 to 1.0)
    """
    if not relevant:
        return 1.0  # Edge case: no relevant chunks
    
    top_k = retrieved[:k]
    relevant_in_top_k = sum(1 for chunk in top_k if chunk in relevant)
    return relevant_in_top_k / len(relevant)

# Example
r_at_5 = recall_at_k(retrieved, relevant, k=5)
print(f"Recall@5: {r_at_5:.2f}")  # 2/3 = 0.67
```

### Mean Reciprocal Rank (MRR)

**Definition:** How high is the first relevant result ranked?

```
MRR = 1 / (rank of first relevant result)
```

```python
def mean_reciprocal_rank(
    retrieved: list[str],
    relevant: set[str],
) -> float:
    """
    Calculate Mean Reciprocal Rank.
    
    Args:
        retrieved: List of retrieved chunk identifiers (in order)
        relevant: Set of relevant chunk identifiers
    
    Returns:
        MRR score (0.0 to 1.0)
    """
    for i, chunk in enumerate(retrieved):
        if chunk in relevant:
            return 1.0 / (i + 1)
    return 0.0  # No relevant chunk found

# Example
mrr = mean_reciprocal_rank(retrieved, relevant)
print(f"MRR: {mrr:.2f}")  # First relevant at position 1 -> 1.0
```

---

## Building a RAG Test Suite

### Ground Truth Dataset

Create a dataset of queries with expected results:

```python
# tests/memory_rag/ground_truth.py

GROUND_TRUTH = [
    {
        "query": "What is the 7-step tool calling loop?",
        "expected_chunks": [
            "tool-calling-architecture.md",
            "simple_agent.py",
        ],
        "expected_answer_contains": [
            "parse",
            "execute",
            "loop",
        ],
        "expected_answer_not_contains": [
            "I don't know",
            "not sure",
        ],
    },
    {
        "query": "How does the coordinator delegate tasks?",
        "expected_chunks": [
            "coordinator.py",
            "message_protocol.py",
        ],
        "expected_answer_contains": [
            "delegate",
            "worker",
            "message",
        ],
    },
    {
        "query": "What testing methodology does this project use?",
        "expected_chunks": [
            "testing-agents.md",
            "test_",  # Any test file
        ],
        "expected_answer_contains": [
            "O.V.E",
            "observe",
            "validate",
            "evaluate",
        ],
    },
]
```

### Query Variants

Test with different phrasings:

```python
QUERY_VARIANTS = {
    "delegation": [
        "How does the coordinator delegate tasks?",
        "What is the delegation mechanism?",
        "How are tasks assigned to workers?",
        "Explain the task distribution process",
    ],
    "tool_calling": [
        "What is the 7-step tool calling loop?",
        "How does tool execution work?",
        "Explain the agent tool calling process",
        "What happens when the agent calls a tool?",
    ],
}
```

---

## Test Patterns

### Unit Test: Retrieval Quality

```python
# tests/memory_rag/test_retrieval_quality.py

import pytest
from src.memory_rag.rag_engine import RAGEngine
from .ground_truth import GROUND_TRUTH

@pytest.fixture
def rag_engine():
    """Create RAG engine with indexed codebase."""
    engine = RAGEngine()
    engine.load_index("./storage")
    return engine

class TestRetrievalQuality:
    """Test that retrieval returns expected chunks."""
    
    @pytest.mark.parametrize("test_case", GROUND_TRUTH)
    def test_retrieves_expected_chunks(self, rag_engine, test_case):
        """Validate that expected chunks are retrieved."""
        # Retrieve
        results = rag_engine.retrieve(
            test_case["query"],
            top_k=10,
        )
        
        # Get file paths from results
        retrieved_files = [r.metadata.get("file_path", "") for r in results]
        
        # Check each expected chunk is present
        for expected in test_case["expected_chunks"]:
            found = any(expected in f for f in retrieved_files)
            assert found, f"Expected chunk '{expected}' not found in retrieval"
    
    def test_similarity_scores_above_threshold(self, rag_engine):
        """Validate that top results have reasonable scores."""
        results = rag_engine.retrieve("How does the agent work?", top_k=5)
        
        # Top result should have high confidence
        assert results[0].score > 0.7, "Top result score too low"
        
        # All results should be above minimum
        for result in results:
            assert result.score > 0.5, f"Result score {result.score} below minimum"
```

### Integration Test: Full Pipeline

```python
class TestRAGPipeline:
    """Test the full RAG pipeline end-to-end."""
    
    @pytest.mark.parametrize("test_case", GROUND_TRUTH)
    def test_end_to_end_answer_quality(self, rag_engine, test_case):
        """Test that full pipeline produces correct answers."""
        # Query
        response = rag_engine.query(test_case["query"])
        
        # Check answer contains expected content
        response_lower = response.lower()
        for expected in test_case.get("expected_answer_contains", []):
            assert expected.lower() in response_lower, \
                f"Response missing expected content: '{expected}'"
        
        # Check answer doesn't contain unexpected content
        for unexpected in test_case.get("expected_answer_not_contains", []):
            assert unexpected.lower() not in response_lower, \
                f"Response contains unexpected content: '{unexpected}'"
```

### Regression Test: Retrieval Stability

```python
class TestRetrievalRegression:
    """Ensure changes don't break retrieval quality."""
    
    def test_retrieval_baseline(self, rag_engine):
        """Check retrieval matches baseline metrics."""
        # Run all ground truth queries
        precision_scores = []
        recall_scores = []
        
        for test_case in GROUND_TRUTH:
            results = rag_engine.retrieve(test_case["query"], top_k=5)
            retrieved = [r.metadata.get("file_path", "") for r in results]
            relevant = set(test_case["expected_chunks"])
            
            precision_scores.append(precision_at_k(retrieved, relevant, k=5))
            recall_scores.append(recall_at_k(retrieved, relevant, k=5))
        
        avg_precision = sum(precision_scores) / len(precision_scores)
        avg_recall = sum(recall_scores) / len(recall_scores)
        
        # Assert against baseline (update as you improve)
        assert avg_precision >= 0.6, f"Precision dropped: {avg_precision:.2f}"
        assert avg_recall >= 0.7, f"Recall dropped: {avg_recall:.2f}"
```

---

## Automating RAG Tests

### pytest Fixtures for RAG

```python
# tests/conftest.py

import pytest
from src.memory_rag.rag_engine import RAGEngine

@pytest.fixture(scope="session")
def rag_engine():
    """
    Session-scoped RAG engine fixture.
    Loads index once for all tests.
    """
    engine = RAGEngine()
    engine.load_index("./storage")
    yield engine
    # Cleanup if needed

@pytest.fixture
def mock_rag_engine():
    """
    Mock RAG engine for unit tests that don't need real retrieval.
    """
    class MockRAGEngine:
        def retrieve(self, query, top_k=5):
            return [
                MockResult(
                    text="Mock chunk about coordination",
                    score=0.9,
                    metadata={"file_path": "coordinator.py"}
                )
            ]
        
        def query(self, query):
            return "Mock response about the codebase"
    
    return MockRAGEngine()
```

### Mock vs. Real Index

| Approach | Use When | Pros | Cons |
|----------|----------|------|------|
| **Real Index** | Integration tests | Accurate results | Slow, requires setup |
| **Mock Index** | Unit tests | Fast, isolated | Doesn't test real retrieval |
| **Fixture Index** | CI/CD | Reproducible | Needs sample data |

```python
# Real index for integration
@pytest.mark.integration
def test_with_real_index(rag_engine):
    response = rag_engine.query("How does delegation work?")
    assert "delegate" in response.lower()

# Mock for unit tests
def test_with_mock(mock_rag_engine):
    response = mock_rag_engine.query("anything")
    assert response == "Mock response about the codebase"
```

---

## Example Test Cases

### Test: Retrieval finds code examples

```python
def test_retrieval_finds_code_for_implementation_query():
    """When asking how to implement something, should return code."""
    results = rag_engine.retrieve("Show me how to register a tool")
    
    # Should find Python files with tool registration
    python_results = [r for r in results if r.metadata.get("file_path", "").endswith(".py")]
    assert len(python_results) >= 1, "Should find at least one Python file"
    
    # Should contain registration code
    code_content = " ".join(r.text for r in python_results)
    assert "@registry.register" in code_content or "def register" in code_content
```

### Test: Documentation queries return docs

```python
def test_retrieval_finds_docs_for_concept_query():
    """When asking about concepts, should return documentation."""
    results = rag_engine.retrieve("What is the O.V.E. testing methodology?")
    
    # Should find markdown/docs files
    doc_results = [r for r in results if ".md" in r.metadata.get("file_path", "")]
    assert len(doc_results) >= 1, "Should find at least one documentation file"
```

### Test: Answer uses retrieved context

```python
def test_answer_cites_sources():
    """Answer should reference retrieved sources."""
    query = "How does the message protocol work?"
    response = rag_engine.query(query)
    
    # Response should mention specific files or concepts from retrieval
    assert any(keyword in response.lower() for keyword in [
        "message",
        "protocol",
        "message_protocol.py",
    ])
```

---

## Running Tests

```bash
# Run all RAG tests
python -m pytest tests/memory_rag/ -v

# Run only retrieval quality tests
python -m pytest tests/memory_rag/test_retrieval_quality.py -v

# Run with coverage
python -m pytest tests/memory_rag/ --cov=src/memory_rag --cov-report=html

# Run integration tests only
python -m pytest tests/memory_rag/ -m integration -v
```

---

## Quick Reference

### O.V.E. for RAG Summary

| Phase | What to Test | Metrics |
|-------|--------------|---------|
| **Observe** | Capture retrieval + generation | RAGObservation dataclass |
| **Validate** | Check retrieval correctness | Precision@K, Recall@K, MRR |
| **Evaluate** | Judge answer quality | Contains expected, LLM-as-judge |

### Test Priority

1. **High:** Expected chunks retrieved (core functionality)
2. **High:** Answer contains expected content
3. **Medium:** Similarity scores above threshold
4. **Medium:** No hallucinations in answer
5. **Low:** Performance metrics (latency)

---

**You're ready for Lab 3!** Go to [Lab 3 README](../../lab-3/README.md) to start building.

[← Debugging RAG Systems](./debugging-rag-systems.md) | [↑ Index](../INDEX.md)

