# Context Management in AI IDEs

**Page 8 of 15** | [← Previous: Prompting Techniques](./prompting.md) | [Next: Engineering Best Practices →](./engineering.md) | [↑ Reading Guide](../READING_GUIDE.md)

Working with an AI IDE like Cursor requires managing the "Context Window"—the limited short-term memory of the LLM.

## The Context Bucket

Imagine a bucket that can hold ~100,000 words.
*   Every file you open adds to the bucket.
*   Every message in the chat adds to the bucket.
*   If the bucket overflows, the oldest information falls out (or the model gets confused).

## Best Practices

### 1. Be Selective with References
Don't add the entire repository to the context (`@Codebase`) unless you have a general question.
*   **Good**: `@src/agent/simple_agent.py` "How does this file handle errors?"
*   **Bad**: "Fix the bug in my app" (without referencing files).

### 2. Small, Focused Files
AI agents perform better with modular code.
*   Break 1000-line files into five 200-line files.
*   This allows you to feed *only* the relevant module to the agent, saving context tokens.

### 3. Reset Often
Conversations get "polluted" with old assumptions.
*   If you change tasks (e.g., from "debugging" to "writing tests"), start a **New Chat**.
*   This clears the context and prevents the agent from getting confused by previous unrelated instructions.

### 4. Use `.cursorrules`
The `.cursorrules` file is a "permanent" part of the context. Use it for high-level instructions that should *always* apply (coding style, testing requirements).

