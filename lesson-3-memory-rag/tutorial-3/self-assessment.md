# Self-Assessment Quiz - Tutorial 3

**Time:** 10 minutes | **Questions:** 20 | [Index](./INDEX.md) | [Reading Guide](./READING_GUIDE.md)

Test your understanding of Memory & RAG concepts before starting the lab exercises.

---

## Section 1: RAG Fundamentals (Questions 1-5)

**1. What does RAG stand for?**

<details>
<summary>Show Answer</summary>

**Retrieval-Augmented Generation**

RAG combines information retrieval with text generation. The system first retrieves relevant context from a knowledge base, then uses that context to generate informed responses.

</details>

**2. When should you use RAG instead of fine-tuning?**

<details>
<summary>Show Answer</summary>

**Use RAG when:**
- Knowledge changes frequently (RAG can update without retraining)
- You need source citations
- You have limited compute for training
- Knowledge is domain-specific but follows standard patterns

**Use fine-tuning when:**
- You need to change the model's behavior/style
- Knowledge is stable and can be baked in
- You have sufficient training data and compute

</details>

**3. What are the three phases of a RAG pipeline?**

<details>
<summary>Show Answer</summary>

1. **Ingestion**: Documents → Chunks → Embeddings → Vector Store
2. **Retrieval**: Query → Embedding → Similarity Search → Context
3. **Generation**: Context + Query → LLM → Response

</details>

**4. What is "chunking" and why does chunk size matter?**

<details>
<summary>Show Answer</summary>

**Chunking** is breaking documents into smaller pieces for indexing.

**Chunk size trade-offs:**
- **Too large**: Retrieval returns irrelevant content mixed with relevant
- **Too small**: Context is fragmented, loses coherence
- **Just right**: Captures complete thoughts while staying focused

Typical sizes: 256-1024 tokens with 10-20% overlap.

</details>

**5. What is the "Library Analogy" for RAG?**

<details>
<summary>Show Answer</summary>

RAG is like a **librarian who reads relevant books before answering your question**.

Instead of relying only on what they remember (the LLM's training), they:
1. Search the library catalog (vector store)
2. Find relevant sections (retrieval)
3. Read those sections (context injection)
4. Then answer your question (generation)

</details>

---

## Section 2: Embeddings & Vector Stores (Questions 6-10)

**6. What is an embedding?**

<details>
<summary>Show Answer</summary>

An **embedding** is a numerical representation of text as a vector (list of numbers).

The key property: **semantically similar text has similar embeddings**.

Example: "happy" and "joyful" will have similar vectors, while "happy" and "motorcycle" will be distant.

</details>

**7. How does cosine similarity work?**

<details>
<summary>Show Answer</summary>

**Cosine similarity** measures the angle between two vectors:
- **1.0**: Identical direction (most similar)
- **0.0**: Perpendicular (unrelated)
- **-1.0**: Opposite direction (most dissimilar)

It's preferred over Euclidean distance because it focuses on direction (meaning) rather than magnitude (length).

</details>

**8. What is a vector store?**

<details>
<summary>Show Answer</summary>

A **vector store** is a database optimized for storing and searching embeddings.

Key operations:
- Store vectors with metadata
- Find k-nearest neighbors (similarity search)
- Filter by metadata

Examples: ChromaDB, Pinecone, Weaviate, FAISS

</details>

**9. Why do we use local embeddings (like bge-small) instead of OpenAI embeddings?**

<details>
<summary>Show Answer</summary>

**Local embeddings advantages:**
- **Free**: No API costs
- **Private**: Data never leaves your machine
- **Fast**: No network latency
- **Offline**: Works without internet

**Trade-off:** Slightly lower quality than GPT-4 embeddings, but good enough for most use cases.

</details>

**10. What is ChromaDB and why use it for Tutorial 3?**

<details>
<summary>Show Answer</summary>

**ChromaDB** is an open-source vector database that:
- Runs locally (no server setup)
- Persists to disk
- Integrates well with LlamaIndex
- Handles metadata filtering

**Why for Tutorial 3:** Simple setup, free, good for learning. Production might use Pinecone or Weaviate for scale.

</details>

---

## Section 3: Multi-Model Orchestration (Questions 11-15)

**11. What is the Architect-Builder pattern?**

<details>
<summary>Show Answer</summary>

A multi-model workflow where:
- **Architect (Llama 3.1)**: Plans, reasons, coordinates, validates
- **Builder (DeepSeek-Coder)**: Implements code, executes tasks

Like construction: architect designs the blueprint, builder constructs it.

</details>

**12. Why use different models for different tasks?**

<details>
<summary>Show Answer</summary>

**Reasons:**
1. **Specialization**: DeepSeek-Coder is better at code than general Llama
2. **Cost optimization**: Use cheaper models for simpler tasks
3. **Capability matching**: Right tool for the right job

**Example:** Use Llama for planning and reasoning, DeepSeek for implementation.

</details>

**13. What are the three multi-model orchestration patterns?**

<details>
<summary>Show Answer</summary>

1. **Sequential Handoff**: Model A plans → Model B implements (Architect-Builder)
2. **Parallel Consultation**: Ask both models, compare/merge results
3. **Router Pattern**: Decide which model to use based on task type

Tutorial 3 focuses on Sequential Handoff (Architect-Builder).

</details>

**14. How does the Architect-Builder pattern extend the coordinator-worker pattern from Tutorial 2?**

<details>
<summary>Show Answer</summary>

**Tutorial 2:** Coordinator (Llama) → Workers (Llama, Llama, Llama)
- Same model, different specializations via prompts

**Tutorial 3:** Coordinator/Architect (Llama) → Builder (DeepSeek)
- Different models, different capabilities
- Model as "super-specialized worker"

The message protocol extends to include TASK_PLAN, CODE_RESULT, TEST_RESULT types.

</details>

**15. What are DeepSeek-Coder's strengths and limitations?**

<details>
<summary>Show Answer</summary>

**Strengths:**
- Excellent code generation
- Good at following specifications
- Fast inference
- Free via Ollama

**Limitations:**
- Less general reasoning than Llama
- Can struggle with ambiguous requirements
- May not explain code well

**Solution:** Use Llama to clarify requirements, DeepSeek to implement.

</details>

---

## Section 4: Testing & Integration (Questions 16-20)

**16. How does O.V.E. apply to RAG testing?**

<details>
<summary>Show Answer</summary>

**Observe:** Capture both retrieval results AND generation output

**Validate (Deterministic):**
- Did retrieval return expected chunks?
- Are similarity scores above threshold?
- Is chunk ranking correct?

**Evaluate (Probabilistic):**
- Is the final answer accurate?
- Did the LLM use the context appropriately?

</details>

**17. What is Precision@K in RAG testing?**

<details>
<summary>Show Answer</summary>

**Precision@K** = (Relevant chunks in top K) / K

Example: If you retrieve 5 chunks and 3 are relevant:
Precision@5 = 3/5 = 0.6 (60%)

Measures: How many retrieved chunks are actually useful?

</details>

**18. What is Recall@K in RAG testing?**

<details>
<summary>Show Answer</summary>

**Recall@K** = (Relevant chunks in top K) / (Total relevant chunks)

Example: If there are 4 relevant chunks total and you retrieve 3 in top 5:
Recall@5 = 3/4 = 0.75 (75%)

Measures: How many of the relevant chunks did we find?

</details>

**19. What is "RAG as a Tool" vs "RAG as Memory"?**

<details>
<summary>Show Answer</summary>

**RAG as a Tool:**
- Agent explicitly calls `search_knowledge(query)` 
- Agent decides when to search
- More control, but agent must know to search

**RAG as Memory:**
- Context is automatically injected into every prompt
- Agent doesn't know it's using RAG
- Simpler but may add irrelevant context

Tutorial 3 uses the Tool pattern for more control.

</details>

**20. What should a ground truth dataset for RAG testing contain?**

<details>
<summary>Show Answer</summary>

**Ground truth dataset:**
1. **Questions**: Sample queries users might ask
2. **Expected chunks**: Which document chunks should be retrieved
3. **Expected answers**: What the final response should contain

Example:
```python
{
    "question": "What is the 7-step tool calling loop?",
    "expected_chunks": ["tool-calling-architecture.md:lines 45-89"],
    "expected_answer_contains": ["parse", "execute", "format", "loop"]
}
```

</details>

---

## Score Your Results

| Score | Assessment | Recommendation |
|-------|------------|----------------|
| 18-20 | Ready for Lab 3 | Start [Exercise 1](../lab-3/exercises/01-llamaindex-setup.md) |
| 14-17 | Mostly ready | Review weak areas, then start lab |
| 10-13 | Need review | Re-read [Concepts](./concepts/rag-architecture.md) |
| <10 | Not ready | Complete [Tutorial 2](../../lesson-2-multi-agent/tutorial-2/INDEX.md) first |

---

**Ready to build?** Start with [Lab 3 README](../lab-3/README.md).

**Need to review?** Go to [Reading Guide](./READING_GUIDE.md).

