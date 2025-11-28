# Glossary

A comprehensive reference of terms used throughout the Agentic AI Tutorial Series. Terms are organized alphabetically with definitions, the tutorial where they're introduced, and links to detailed explanations.

---

## A

### Agent
A system that uses an LLM to reason about tasks and take actions. Unlike a simple chatbot that only generates text, an agent can call tools, make decisions, and execute multi-step workflows.

**Introduced:** Tutorial 1  
**See:** [LLM Fundamentals](../lesson-1-fundamentals/tutorial-1/concepts/llm-fundamentals.md)

### Agent Loop
The iterative cycle an agent follows: receive input, think, optionally call tools, think again, respond. Also called the "7-step loop" in Tutorial 1.

**Introduced:** Tutorial 1  
**See:** [Tool Calling Architecture](../lesson-1-fundamentals/tutorial-1/concepts/tool-calling-architecture.md)

### Agentic AI
AI systems capable of autonomous reasoning and action. Characterized by: tool use, planning, memory, and goal-directed behavior. Distinguished from conversational AI (just chat) or predictive AI (just outputs).

**Introduced:** Tutorial 1  
**See:** [Software Engineering Evolution](../lesson-1-fundamentals/tutorial-1/concepts/software-engineering-evolution.md)

### Allowed Tools
The subset of available tools that a specific agent can use. Part of agent specialization - each agent only has access to tools relevant to its job.

**Introduced:** Tutorial 2  
**See:** [Agent Specialization](../lesson-2-multi-agent/tutorial-2/concepts/agent-specialization.md)

---

## C

### Chunking
The process of splitting documents into smaller pieces for embedding and retrieval. Chunk size affects retrieval quality - too small loses context, too large adds noise.

**Introduced:** Tutorial 3  
**See:** [RAG Architecture](../lesson-3-memory-rag/tutorial-3/concepts/rag-architecture.md)

### Context Window
The maximum amount of text (measured in tokens) that an LLM can process at once. Includes system prompt, conversation history, tool results, and user input.

**Introduced:** Tutorial 1  
**See:** [LLM Fundamentals](../lesson-1-fundamentals/tutorial-1/concepts/llm-fundamentals.md)

### Coordinator
An agent that orchestrates other agents without executing tasks itself. The coordinator receives requests, decomposes them, delegates to workers, and aggregates results.

**Introduced:** Tutorial 2  
**See:** [Multi-Agent Architecture](../lesson-2-multi-agent/tutorial-2/concepts/multi-agent-architecture.md)

### Coordinator-Worker Pattern
An architectural pattern where a central coordinator manages multiple specialized workers. The coordinator handles orchestration; workers handle execution.

**Introduced:** Tutorial 2  
**See:** [Coordinator Patterns](../lesson-2-multi-agent/tutorial-2/architecture/coordinator-patterns.md)

---

## D

### Delegation
The act of a coordinator assigning a task to a worker agent. In Tutorial 2, delegation uses the message protocol for structured communication.

**Introduced:** Tutorial 2  
**See:** [Exercise 1A: Coordinator Basics](../lesson-2-multi-agent/lab-2/exercises/01a-coordinator-basics.md)

### Docstring
Documentation string in Python code. For tools, docstrings are critical because the LLM reads them to understand how to use the tool.

**Introduced:** Tutorial 1  
**See:** [Agentic Code Practices](../lesson-1-fundamentals/tutorial-1/guides/agentic-practices.md)

---

## E

### Embedding
A numerical vector representation of text that captures semantic meaning. Similar texts have similar embeddings. Used for semantic search in RAG systems.

**Introduced:** Tutorial 3  
**See:** [Embeddings & Vector Stores](../lesson-3-memory-rag/tutorial-3/concepts/embeddings-vector-stores.md)

### Evaluation (in O.V.E.)
Assessing probabilistic, qualitative outputs from agents. Unlike validation, evaluation involves judgment about quality, relevance, and appropriateness. May require human review or LLM-as-judge.

**Introduced:** Tutorial 1  
**See:** [Testing Agents](../lesson-1-fundamentals/tutorial-1/concepts/testing-agents.md)

---

## F

### Function Calling
See: **Tool Calling**. These terms are used interchangeably. "Function calling" is the OpenAI terminology; "tool calling" is more common in agent frameworks.

---

## G

### Gatherer Agent
In the bridge exercise, an agent specialized in finding and collecting information using search and read tools. Does not analyze or summarize.

**Introduced:** Tutorial 2 (Exercise 0)  
**See:** [Exercise 0: Bridge](../lesson-2-multi-agent/lab-2/exercises/00-bridge-refactoring.md)

---

## I

### In Reply To
A field in the Message class that links a response to its original request. Enables tracking request-response pairs within a trace.

**Introduced:** Tutorial 2  
**See:** [Exercise 1B: Message Protocol](../lesson-2-multi-agent/lab-2/exercises/01b-message-protocol.md)

---

## K

### Knowledge Tool
A tool that queries the RAG engine to retrieve relevant information from indexed documents. Gives agents access to custom knowledge bases.

**Introduced:** Tutorial 3  
**See:** [Knowledge Integration](../lesson-3-memory-rag/tutorial-3/concepts/knowledge-integration.md)

---

## L

### LlamaIndex
A Python framework for building RAG applications. Provides tools for document loading, chunking, embedding, indexing, and querying.

**Introduced:** Tutorial 3  
**See:** [Exercise 1: LlamaIndex Setup](../lesson-3-memory-rag/lab-3/exercises/01-llamaindex-setup.md)

### LLM (Large Language Model)
A neural network trained on vast text data to generate human-like text. The "brain" of an agent - provides reasoning and language capabilities.

**Introduced:** Tutorial 1  
**See:** [LLM Fundamentals](../lesson-1-fundamentals/tutorial-1/concepts/llm-fundamentals.md)

---

## M

### MCP (Model Context Protocol)
A standardized protocol for tools to communicate with LLMs. Enables interoperability between different tool providers and LLM frameworks.

**Introduced:** Tutorial 1  
**See:** [MCP Introduction](../lesson-1-fundamentals/tutorial-1/concepts/mcp-intro.md)

### Message
A structured object for agent communication. Contains metadata (message_id, timestamp, trace_id), routing (from_agent, to_agent), and content (action, payload).

**Introduced:** Tutorial 2  
**See:** [Agent Communication](../lesson-2-multi-agent/tutorial-2/concepts/agent-communication.md)

### Message Protocol
The system of structured messages used for agent-to-agent communication. Includes message types (REQUEST, RESPONSE, ERROR) and required fields.

**Introduced:** Tutorial 2  
**See:** [Exercise 1B: Message Protocol](../lesson-2-multi-agent/lab-2/exercises/01b-message-protocol.md)

### Message Type
Classification of messages: REQUEST (asking for work), RESPONSE (returning results), ERROR (something went wrong).

**Introduced:** Tutorial 2  
**See:** [Exercise 1B: Message Protocol](../lesson-2-multi-agent/lab-2/exercises/01b-message-protocol.md)

### Multi-Agent System
A system with multiple specialized agents working together, coordinated by a central coordinator or peer-to-peer protocols.

**Introduced:** Tutorial 2  
**See:** [Multi-Agent Architecture](../lesson-2-multi-agent/tutorial-2/concepts/multi-agent-architecture.md)

---

## O

### Observe (in O.V.E.)
The first step of testing: run the agent and collect outputs. Capture everything: tool calls, intermediate results, final response.

**Introduced:** Tutorial 1  
**See:** [Testing Agents](../lesson-1-fundamentals/tutorial-1/concepts/testing-agents.md)

### Ollama
A local LLM runtime that lets you run models like Llama on your own machine. Used in the tutorials for free, private, fast iteration.

**Introduced:** Tutorial 1  
**See:** [Tech Stack](./tech-stack.md)

### O.V.E. (Observe-Validate-Evaluate)
The testing methodology for agentic systems. Observe outputs, Validate deterministic aspects, Evaluate probabilistic aspects.

**Introduced:** Tutorial 1  
**See:** [Testing Agents](../lesson-1-fundamentals/tutorial-1/concepts/testing-agents.md)

---

## P

### Payload
The data content of a message or tool call. Contains the actual information being passed (query parameters, results, etc.).

**Introduced:** Tutorial 2  
**See:** [Agent Communication](../lesson-2-multi-agent/tutorial-2/concepts/agent-communication.md)

### Prompt Engineering
The practice of crafting effective prompts to guide LLM behavior. Includes system prompts, few-shot examples, and structured instructions.

**Introduced:** Tutorial 1  
**See:** [Prompting Techniques](../lesson-1-fundamentals/tutorial-1/guides/prompting.md)

---

## R

### RAG (Retrieval-Augmented Generation)
A technique that enhances LLM responses by retrieving relevant information from a knowledge base before generating. Combines search with generation.

**Introduced:** Tutorial 3  
**See:** [RAG Architecture](../lesson-3-memory-rag/tutorial-3/concepts/rag-architecture.md)

### Registry Pattern
A design pattern where components register themselves in a central registry. Used for tool registration in Tutorial 1.

**Introduced:** Tutorial 1  
**See:** [Software Patterns](./software-patterns.md#registry-pattern-tutorial-1)

### Reporter Agent
In the bridge exercise, an agent specialized in summarizing gathered information. Uses LLM only (no tools).

**Introduced:** Tutorial 2 (Exercise 0)  
**See:** [Exercise 0: Bridge](../lesson-2-multi-agent/lab-2/exercises/00-bridge-refactoring.md)

### Retry Logic
Mechanism to automatically retry failed operations. In Tutorial 2, delegation includes exponential backoff retries (1s, 2s, 4s delays).

**Introduced:** Tutorial 2  
**See:** [Exercise 1A: Coordinator Basics](../lesson-2-multi-agent/lab-2/exercises/01a-coordinator-basics.md)

---

## S

### Semantic Search
Search based on meaning rather than exact keyword matching. Uses embeddings to find similar content even with different wording.

**Introduced:** Tutorial 3  
**See:** [Embeddings & Vector Stores](../lesson-3-memory-rag/tutorial-3/concepts/embeddings-vector-stores.md)

### Shared State
A storage mechanism for data that needs to persist across agents. In Tutorial 2, implemented as file-based JSON storage.

**Introduced:** Tutorial 2  
**See:** [State Management](../lesson-2-multi-agent/tutorial-2/concepts/state-management.md)

### Specialization
The practice of giving each agent a focused job with limited tools. Prevents agent confusion and enables expertise.

**Introduced:** Tutorial 2  
**See:** [Agent Specialization](../lesson-2-multi-agent/tutorial-2/concepts/agent-specialization.md)

### System Prompt
Initial instructions given to an LLM that define its persona, capabilities, and behavior. The "operating system" for the agent.

**Introduced:** Tutorial 1  
**See:** [Prompting Techniques](../lesson-1-fundamentals/tutorial-1/guides/prompting.md)

---

## T

### Temperature
An LLM parameter controlling randomness. Lower (0.0-0.3) = more deterministic; Higher (0.7-1.0) = more creative/varied.

**Introduced:** Tutorial 1  
**See:** [LLM Fundamentals](../lesson-1-fundamentals/tutorial-1/concepts/llm-fundamentals.md)

### Token
The basic unit of text for LLMs. Roughly 4 characters or 0.75 words in English. Used to measure context window size and cost.

**Introduced:** Tutorial 1  
**See:** [LLM Fundamentals](../lesson-1-fundamentals/tutorial-1/concepts/llm-fundamentals.md)

### Tool
A function that an agent can call to interact with the world. Examples: search_files, read_file, calculate. Tools extend agent capabilities beyond text generation.

**Introduced:** Tutorial 1  
**See:** [Tool Calling Architecture](../lesson-1-fundamentals/tutorial-1/concepts/tool-calling-architecture.md)

### Tool Calling
The capability that allows LLMs to invoke external functions. The LLM outputs a structured request; the system executes it and returns results.

**Introduced:** Tutorial 1  
**See:** [Tool Calling Architecture](../lesson-1-fundamentals/tutorial-1/concepts/tool-calling-architecture.md)

### Tool Registry
A central registry that tracks available tools. Tools register via decorator; agents query to discover capabilities.

**Introduced:** Tutorial 1  
**See:** [Exercise 2: Adding Tools](../lesson-1-fundamentals/lab-1/exercises/02-adding-tools.md)

### Trace ID
A unique identifier that groups all messages in a single workflow. Enables end-to-end debugging: "Show me everything in trace-abc-123".

**Introduced:** Tutorial 2  
**See:** [Exercise 1B: Message Protocol](../lesson-2-multi-agent/lab-2/exercises/01b-message-protocol.md)

---

## V

### Validate (in O.V.E.)
Testing deterministic aspects of agent behavior: Did the right tool get called? Was the message format correct? Are required fields present?

**Introduced:** Tutorial 1  
**See:** [Testing Agents](../lesson-1-fundamentals/tutorial-1/concepts/testing-agents.md)

### Vector Database
A database optimized for storing and searching embeddings. Enables fast similarity search for RAG systems.

**Introduced:** Tutorial 3  
**See:** [Embeddings & Vector Stores](../lesson-3-memory-rag/tutorial-3/concepts/embeddings-vector-stores.md)

---

## W

### Worker Agent
An agent that executes specific tasks under coordinator direction. Has specialized tools and focused responsibilities. Does not orchestrate other agents.

**Introduced:** Tutorial 2  
**See:** [Multi-Agent Architecture](../lesson-2-multi-agent/tutorial-2/concepts/multi-agent-architecture.md)

### WorkerAgent Base Class
The parent class for all specialized workers. Inherits from Tutorial 1's Agent class, adding tool filtering and message handling.

**Introduced:** Tutorial 2  
**See:** [Agent Specialization](../lesson-2-multi-agent/tutorial-2/concepts/agent-specialization.md)

---

## Quick Reference by Tutorial

### Tutorial 1 Terms
Agent, Agent Loop, Agentic AI, Context Window, Docstring, LLM, MCP, Ollama, O.V.E., Prompt Engineering, Registry Pattern, System Prompt, Temperature, Token, Tool, Tool Calling, Tool Registry

### Tutorial 2 Terms
Allowed Tools, Coordinator, Coordinator-Worker Pattern, Delegation, Gatherer Agent, In Reply To, Message, Message Protocol, Message Type, Multi-Agent System, Payload, Reporter Agent, Retry Logic, Shared State, Specialization, Trace ID, Worker Agent, WorkerAgent Base Class

### Tutorial 3 Terms
Chunking, Embedding, Knowledge Tool, LlamaIndex, RAG, Semantic Search, Vector Database

---

**Navigation:** [README](../README.md) | [Software Patterns](./software-patterns.md) | [Tech Stack](./tech-stack.md)

