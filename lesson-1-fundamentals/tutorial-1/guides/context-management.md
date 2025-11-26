# Context Management in AI-Assisted Development

**Page 11 of 16** | [← Previous: Prompting Techniques](./prompting.md) | [Next: Engineering Best Practices →](./engineering.md) | [↑ Reading Guide](../READING_GUIDE.md)

Working with AI is all about managing the "Context Window"—the AI's short-term memory.

## 🎒 Analogy 1: The Backpack

Imagine you are hiking with an AI assistant. The AI has a backpack (the context window).
*   **Capacity**: It can only hold ~100,000 tokens (~50 items).
*   **Weight**: The heavier the pack, the slower the AI walks (latency increases).
*   **Spillover**: If you stuff too much in, the old stuff at the bottom falls out (the AI forgets early instructions).

**Your Job**: Be a minimalist packer. Don't pack the entire library; pack only the map (current file) and the compass (project rules).

## 🧠 Analogy 2: The Goldfish Memory

LLMs have "Goldfish Memory." They don't remember your project from yesterday. They only know what is in the *current chat thread*.
*   **New Chat = Clean Slate**.
*   **Long Chat = Polluted Water**. As the chat gets long, it fills with old code, failed attempts, and noise. The AI gets confused.

---

## Best Practices

### 1. Be Selective with References (`@`)
Don't dump the whole codebase.
*   ✅ **Good**: `@simple_agent.py` "Fix the bug in `chat()`"
*   ❌ **Bad**: `@Codebase` "Fix the bug" (Too noisy, AI might look in `tests/` or `docs/`)

### 2. Keep Files Small (The "200-Line Rule")
AI struggles with massive files.
*   **Big File**: You have to feed the AI 2000 lines just to change 1 function.
*   **Small File**: You feed 50 lines. The AI focuses better and responds faster.
*   *Agentic Code should be modular by default.*

### 3. The "Bankrupt" Reset
When the AI starts looping or suggesting code you already deleted:
**Declare Bankruptcy.**
1. Close the chat.
2. Open a new chat.
3. Re-state the *current* goal.

### 4. The "Permanent" Context (`.cursorrules`)
Some things should *always* be in the backpack.
Use `.cursorrules` (or `.vscode/settings.json` prompts) for:
*   Coding Style (PEP 8)
*   Architectural Constraints ("Always use O.V.E. testing")
*   Project Layout

---

## Summary Checklist
*   [ ] Am I referencing only relevant files?
*   [ ] Is my chat thread older than 1 hour? (If yes, reset)
*   [ ] Did I check `.cursorrules` is active?
