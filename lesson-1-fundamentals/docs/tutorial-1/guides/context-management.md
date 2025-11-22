# Context Management in AI-Assisted Development

**Page 8 of 16** | [← Previous: Prompting Techniques](./prompting.md) | [Next: Engineering Best Practices →](./engineering.md) | [↑ Reading Guide](../READING_GUIDE.md)

Working with AI-capable IDEs (Cursor, VS Code + Continue, etc.) requires managing the "Context Window"—the limited short-term memory of the LLM.

## The Context Bucket

Imagine a bucket that can hold ~100,000 words (varies by model).
*   Every file you reference adds to the bucket.
*   Every message in the chat adds to the bucket.
*   If the bucket overflows, the oldest information falls out (or the model gets confused).

**Context Window Sizes:**
- **Llama 3.1**: Up to 128k tokens (~96,000 words)
- **GPT-4**: 8k-128k tokens depending on version
- **Claude 3**: Up to 200k tokens (~150,000 words)

## Best Practices (IDE-Agnostic)

### 1. Be Selective with References

Don't add the entire repository to the context unless you have a general question.

**Cursor/Continue:**
*   **Good**: `@src/agent/simple_agent.py` "How does this file handle errors?"
*   **Bad**: `@Codebase` "Fix the bug in my app" (too broad, floods context)

**GitHub Copilot:**
*   **Good**: Open only the files you're working on
*   **Bad**: Having 20+ files open simultaneously

**Manual/CLI:**
*   **Good**: `cat src/agent/simple_agent.py` then ask specific questions
*   **Bad**: Pasting entire codebases into chat

### 2. Small, Focused Files
AI agents perform better with modular code.
*   Break 1000-line files into five 200-line files.
*   This allows you to feed *only* the relevant module to the agent, saving context tokens.
*   **Benefits**: Faster AI responses, more accurate suggestions, easier to understand

### 3. Reset Often
Conversations get "polluted" with old assumptions and irrelevant history.

**When to reset:**
*   Switching tasks (e.g., from "debugging" to "writing tests")
*   After completing a major feature
*   When AI responses become less relevant
*   When you notice AI referring to old, changed code

**How to reset:**
- **Cursor**: Start a "New Chat" (Cmd/Ctrl+L, then click "+")
- **Continue**: Click the new conversation button in sidebar
- **Copilot**: Restart the chat session
- **Manual**: Simply start a new conversation with your AI tool

### 4. Use Configuration Files

Different IDEs support different configuration methods:

**`.cursorrules` (Cursor/Continue):**
```text
# This file is a "permanent" part of the context
# Use it for high-level instructions that should ALWAYS apply

- Follow PEP 8 style guide
- Write docstrings for all tools (agents read them!)
- Return human-readable strings from tools, not exceptions
- Test using O.V.E. methodology
```

**`.vscode/settings.json` (VS Code + Extensions):**
```json
{
  "continue.contextProviders": ["file", "code"],
  "github.copilot.enable": {
    "*": true,
    "python": true
  }
}
```

**Project README** (Manual/Any IDE):
Keep a clear README.md with coding standards that you can reference in AI conversations.

## IDE-Specific Tips

### Cursor
- Use `@Codebase` for architectural questions: "What's the overall structure?"
- Use `@filename` for specific file questions
- Create multiple chats for different tasks
- Review suggested changes before accepting

### VS Code + Continue
- Continue auto-detects open files in context
- Use `@file` to explicitly reference files
- Configure multiple AI providers in settings
- Supports both local (Ollama) and cloud models

### VS Code + GitHub Copilot  
- Copilot learns from your open files and recent edits
- Use `Cmd/Ctrl+I` for chat, Tab for inline suggestions
- Be aware: Your code is sent to GitHub's cloud
- Works best with well-named functions and clear comments

### Manual Consultation
- Copy only relevant code snippets, not entire files
- Provide clear context: "I'm building an agent that..."
- Ask specific questions: "How should I handle errors in this tool?"
- Keep track of conversation history yourself

## Context Management Strategies

### Strategy 1: Layered Context (Recommended)
1. **Always available**: System prompt, `.cursorrules`, core documentation
2. **Task-specific**: Only files related to current work
3. **Temporary**: Recent conversation history

### Strategy 2: File-by-File
Work on one file at a time, only referencing related files when needed. Best for focused refactoring.

### Strategy 3: Breadth-First
Start with `@Codebase` questions to understand architecture, then narrow down to specific files. Best for learning a new codebase.

## Common Context Issues

**Problem**: "AI suggests code from files I changed 10 minutes ago"
**Solution**: Start a new chat or explicitly mention recent changes

**Problem**: "AI is too slow to respond"
**Solution**: Reduce context by closing unnecessary files, using specific file references

**Problem**: "AI suggests wrong patterns"  
**Solution**: Check `.cursorrules` or add explicit instructions in current chat

**Problem**: "AI forgot what we were working on"
**Solution**: Context window overflow—summarize progress and start new chat with summary

