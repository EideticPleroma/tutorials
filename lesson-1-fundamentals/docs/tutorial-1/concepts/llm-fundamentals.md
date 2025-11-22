# LLM Fundamentals for Agentic AI

**Page 3 of 15** | [← Previous: Software Engineering Evolution](./software-engineering-evolution.md) | [Next: Tool Calling Architecture →](./tool-calling-architecture.md) | [↑ Reading Guide](../READING_GUIDE.md)

Understanding how Large Language Models (LLMs) work is crucial for building effective agents. This guide covers the basics relevant to agent development.

## What is an LLM?

At its core, an LLM is a probabilistic engine that predicts the next token in a sequence.

### The Inference Pipeline

1.  **Tokenization**: Text is broken down into smaller units called "tokens" (roughly 0.75 words).
2.  **Embedding**: Tokens are converted into high-dimensional vectors (lists of numbers) representing semantic meaning.
3.  **Attention**: The model looks at all tokens in the context window to understand relationships (e.g., "it" refers to "the cat").
4.  **Generation**: The model calculates the probability of every possible next token and selects one based on your settings.

## Key Parameters

### Context Window
The amount of text (tokens) the model can "remember" at once.
*   **Llama 3.1**: Support for large context windows (up to 128k tokens), allowing for passing large documentation or code files.
*   **Implication**: You must manage what goes into the context. Too much noise degrades performance.

### Temperature
Controls the randomness of the output.
*   **Low (0.0 - 0.2)**: Deterministic, focused. Best for code generation and tool calling.
*   **High (0.7 - 1.0)**: Creative, varied. Best for brainstorming or creative writing.

### System Prompts
The initial instruction given to the model that sets its persona and rules.
*   **Agentic AI**: This is where we define the agent's capabilities ("You are a research assistant...") and constraints ("Always use tools for...").

## Why Llama 3.1?

For this tutorial, we use Llama 3.1 because:
*   **Local**: Runs on your machine via Ollama (privacy, no cost).
*   **State-of-the-Art**: Matches GPT-4 class performance on many tasks.
*   **Tool Calling**: Fine-tuned specifically to understand and generate structured tool calls.

