# Tech Stack Decisions

**Shared Reference** | [Tutorial 1](../lesson-1-fundamentals/tutorial-1/INDEX.md) | [Tutorial 2](../lesson-2-multi-agent/tutorial-2/INDEX.md) | [Main README](../README.md)

This document explains the technology choices for the Agentic AI tutorial series and when to use alternatives.

## Core Technologies

### Llama 3.3 (via Ollama)

**Why Llama over GPT-4o/Claude 3.5?**
*   **Local & Free**: Runs entirely on your machine. No API costs, no rate limits, no data leaving your machine.
*   **Fast Iteration**: No network latency. You can test prompts in seconds, not minutes.
*   **Privacy**: Your code, prompts, and data never leave your machine.
*   **State-of-the-Art**: Llama 3.3 (Dec 2024) matches GPT-4o performance on many benchmarks.
*   **Tool Calling**: Llama 3.3 has enhanced structured output capabilities, critical for reliable agent behavior.

**Context Window**: 128k tokens standard across all sizes (8B, 70B models).

**When to use alternatives:**
*   **GPT-4o**: Multimodal capabilities (vision, audio) and fastest response times in production.
*   **Claude 3.5 Sonnet**: Best for code generation and long-context reasoning (200k tokens).
*   **Gemini 2.0 Flash**: Fastest inference, multimodal support, excellent for production deployments.

### Ollama

**Why Ollama?**
*   **Simple API**: Just `ollama.chat()` - no complex SDK setup.
*   **Model Management**: Easy to pull, switch, and manage models (`ollama pull llama3.3:8b`).
*   **Cross-Platform**: Works on Windows (WSL2), Mac, Linux.
*   **Active Development**: Well-maintained with regular updates.
*   **Multi-Agent Ready**: Handles concurrent requests well for Tutorial 2's multi-agent patterns.

**Multi-Agent Considerations:**
*   Ollama can serve multiple agents simultaneously (coordinator + workers)
*   Resource usage scales with number of active agents (RAM, CPU)
*   For Tutorial 2: 16GB RAM recommended when running 3+ agents concurrently
*   Consider GPU acceleration (optional) if running many parallel agent conversations

**Alternatives:**
*   **vLLM**: If you need higher throughput for production.
*   **Direct HuggingFace**: If you want more control over model loading.

### Modern AI Capabilities (2025)

**Structured Outputs**:
Modern LLMs (GPT-4o, Claude 3.5, Llama 3.3) now support **native JSON schema enforcement**:
*   **Traditional**: Send tool schemas, hope LLM returns valid JSON, catch parsing errors
*   **Modern (2025)**: Use `.with_structured_output(schema)` - LLM guarantees JSON compliance
*   **Tutorial Approach**: We teach the traditional approach (works with ANY model, educational value)
*   **Production**: Use structured outputs for reliability and faster iteration

**Prompt Caching**:
Major cost optimization for 2025:
*   **Ollama 0.4+**: Automatic system prompt caching (faster multi-turn conversations)
*   **Claude 3.5 & GPT-4o**: Explicit prompt caching (90% cost reduction for repeated prompts)
*   **Multi-Agent Benefit**: Coordinator + workers share cached context
*   **Tutorial 2**: We leverage Ollama's automatic caching; advanced strategies in Tutorial 4

**Multimodal Capabilities**:
Beyond this tutorial's scope, but important context:
*   **GPT-4o**: Vision, audio, structured JSON in single model
*   **Gemini 2.0**: Real-time video, native tool calling
*   **Claude 3.5**: PDF understanding, code execution
*   **Tutorial Focus**: Text-based fundamentals that transfer to any model

## Version Requirements (2025)

**Python**: 3.11+ required
*   Type hints improvements critical for agent development
*   Better error messages for debugging
*   Performance improvements (10-25% faster than 3.10)
*   Python 3.10 approaching end-of-life (Oct 2026)

**TypeScript**: 5.3+ (for MCP tools)
*   Required for modern MCP SDK features
*   Better inference for tool schemas
*   Improved type safety for agent-tool bridges

**Node.js**: 20 LTS (current as of 2025)
*   Required for MCP server hosting
*   Node 18 moves to maintenance mode in 2025
*   Better performance and security

**Ollama**: 0.4.0+ (Nov 2024+)
*   Context caching support (faster multi-turn conversations)
*   Improved GPU utilization
*   Enhanced structured output mode
*   Multiple model loading

**Verification Commands**:
```bash
python --version    # Should show 3.11.x or higher
node --version      # Should show 20.x.x
ollama --version    # Should show 0.4.x or higher
```

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

### Tutorial 2: Multi-Agent Systems

Tutorial 2 builds on this foundation by introducing multi-agent coordination while maintaining the same core stack:

**Core Stack (Unchanged):**
*   **Ollama + Llama 3.3**: Still local-first for fast iteration
*   **Python**: Remains the primary language for agent logic
*   **TypeScript**: Continues for MCP tool development

**New Considerations:**
*   **Message Passing**: Inter-agent communication patterns (no external message queue needed for Tutorial 2)
*   **Shared State**: Simple shared memory or file-based state (lightweight, educational)
*   **Coordinator Patterns**: One coordinator agent managing multiple specialized agents
*   **Testing Multi-Agent**: Extended O.V.E. methodology for testing agent interactions

**Production Performance Note (2025)**:
*   **Prompt Caching**: Ollama 0.4+ caches system prompts automatically
*   **Multi-Agent Benefit**: Coordinator + workers share cached context (significant speedup)
*   **Cost Savings**: Claude 3.5 and GPT-4o also support prompt caching (90% cost reduction for repeated prompts)
*   **Tutorial 2 Scope**: We use Ollama's automatic caching; advanced caching strategies in Tutorial 4

**What We Still Avoid:**
*   **Heavy Frameworks**: No LangChain/CrewAI - we continue building fundamentals from scratch
*   **External Dependencies**: No Redis, RabbitMQ, or complex infrastructure
*   **Vector Databases**: Deferred to Tutorial 3 (Memory & RAG)

**Why This Approach:**
Tutorial 2 focuses on understanding multi-agent coordination patterns without introducing production infrastructure complexity. You'll learn how agents communicate, specialize, and collaborate using the same lightweight stack you mastered in Tutorial 1.

### Beyond Tutorial 2

As you progress further, you'll encounter:
*   **Tutorial 3+**: Vector databases (Chroma, Pinecone) for long-term memory and RAG
*   **Production Patterns**: Message queues, distributed systems, monitoring
*   **Advanced Frameworks**: When and how to adopt LangChain, LlamaIndex, or CrewAI
*   **Cloud LLM APIs**: GPT-4o, Claude 3.5 Sonnet for production deployments requiring reliability at scale

---

**Key Principle**: Tutorials 1-2 use minimal abstractions to teach fundamentals. Later tutorials will introduce frameworks and infrastructure that make development faster but hide complexity. Master the basics first, then adopt tools that accelerate your work.

