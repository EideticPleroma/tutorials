# Tech Stack Decisions

This document explains why we chose specific technologies for Tutorial 1 and when to use alternatives.

## Core Technologies

### Llama 3.1 (via Ollama)

**Why Llama over GPT-4/Claude?**
*   **Local & Free**: Runs entirely on your machine. No API costs, no rate limits, no data leaving your machine.
*   **Fast Iteration**: No network latency. You can test prompts in seconds, not minutes.
*   **Privacy**: Your code, prompts, and data never leave your machine.
*   **State-of-the-Art**: Llama 3.1 matches GPT-4 class performance on many benchmarks.
*   **Tool Calling**: Fine-tuned specifically for structured tool calling, which is critical for agents.

**When to use alternatives:**
*   **GPT-4**: If you need the absolute best reasoning for complex tasks (but accept API costs).
*   **Claude**: If you need very long context windows (200k+ tokens) for analyzing entire codebases.

### Ollama

**Why Ollama?**
*   **Simple API**: Just `ollama.chat()` - no complex SDK setup.
*   **Model Management**: Easy to pull, switch, and manage models (`ollama pull llama3.1:8b`).
*   **Cross-Platform**: Works on Windows (WSL2), Mac, Linux.
*   **Active Development**: Well-maintained with regular updates.

**Alternatives:**
*   **vLLM**: If you need higher throughput for production.
*   **Direct HuggingFace**: If you want more control over model loading.

### Python (for Agent)

**Why Python?**
*   **AI Ecosystem**: `ollama`, `pydantic`, `pytest` - everything you need is a `pip install` away.
*   **Rapid Prototyping**: Fast to write, easy to debug.
*   **Type Hints**: Critical for tool calling (agents read type hints to understand function signatures).
*   **Industry Standard**: Most agent frameworks are Python-first.

**When to use alternatives:**
*   **TypeScript/Node**: If you're building a web-based agent or need tight MCP integration (we use it for tools).
*   **Rust**: If you need extreme performance (overkill for Tutorial 1).

### TypeScript (for Tools/MCP)

**Why TypeScript for MCP tools?**
*   **MCP Ecosystem**: The official MCP SDKs are TypeScript-first.
*   **Type Safety**: Catches errors at compile time (important when bridging to Python).
*   **Node.js Integration**: Easy to call from Python via subprocess.

**Note**: In Tutorial 1, we use a simple subprocess bridge. In later tutorials, you'll see more sophisticated MCP client patterns.

### Cursor IDE

**Why Cursor?**
*   **AI-First**: Built from the ground up for AI-assisted development.
*   **Context Management**: Better than VS Code + Copilot at managing large codebases.
*   **MCP Native**: Can consume MCP servers directly (we'll explore this in later tutorials).

**Alternatives:**
*   **VS Code + GitHub Copilot**: Works, but context management is less sophisticated.
*   **JetBrains IDEs**: Great for Java/Kotlin, but AI integration is newer.

## Development Tools

### Docker (Optional)

**Why Optional?**
*   Tutorial 1 focuses on fundamentals. Docker adds complexity.
*   Local Ollama is simpler for learning.
*   We provide `docker-compose.yml` for those who want containerization.

**When to use:**
*   **Production**: Consistent environments across dev/staging/prod.
*   **Team Collaboration**: Ensures everyone has the same setup.
*   **Isolation**: If you want to keep Ollama separate from your system.

### WSL2 (Windows)

**Why WSL2?**
*   **Linux Tools**: Most AI tooling assumes Linux/Mac.
*   **Docker Integration**: Docker Desktop works better with WSL2.
*   **Terminal Experience**: Better shell experience than PowerShell for development.

**Alternatives:**
*   **Native Windows**: Possible but requires more configuration.
*   **Dual Boot Linux**: Overkill for this tutorial.

## Testing Framework

### Custom Framework (vs pytest alone)

**Why Custom?**
*   **O.V.E. Methodology**: Traditional pytest doesn't understand "Observe-Validate-Evaluate".
*   **Trace Capture**: We need to capture the entire agent interaction, not just final outputs.
*   **Educational**: Building it teaches you how agent testing works.

**Note**: We still use pytest as the test runner. Our framework is a pytest plugin.

## Future Considerations

As you progress to Tutorial 2+, you'll encounter:
*   **Vector Databases** (Chroma, Pinecone): For long-term memory.
*   **LangChain/LlamaIndex**: Frameworks that abstract away tool calling (we avoid in Tutorial 1 to learn fundamentals).
*   **Production LLM APIs**: When you need reliability and scale.

---

**Key Principle**: Tutorial 1 uses minimal abstractions to teach fundamentals. Later tutorials will introduce frameworks that make development faster but hide complexity.

