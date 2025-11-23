# Frequently Asked Questions (FAQ)

Quick answers to common questions. Can't find what you're looking for? Check the [Troubleshooting Guide](./troubleshooting.md) or [Getting Unstuck Guide](./getting-unstuck.md).

---

## Table of Contents

- [Setup & Environment](#setup--environment)
- [Tool Registration & Development](#tool-registration--development)
- [Agent Behavior](#agent-behavior)
- [Testing & Validation](#testing--validation)
- [IDE & Development Workflow](#ide--development-workflow)
- [Conceptual Questions](#conceptual-questions)
- [Performance & Optimization](#performance--optimization)
- [Next Steps & Extensions](#next-steps--extensions)

---

## Setup & Environment

### Q: Do I need a GPU to run this tutorial?

**A:** No! Ollama with Llama 3.1 runs fine on CPU. Performance will be slower than GPU, but perfectly usable for learning.

- **CPU only**: 2-5 seconds per response
- **With GPU**: 0.5-1 second per response

---

### Q: Can I use a different model instead of Llama 3.1?

**A:** Yes, but Llama 3.1 is recommended because it's specifically fine-tuned for tool calling and is the community standard.

**Alternatives:**
```bash
# Smaller models (good for very low-RAM systems, less capable)
ollama pull llama3.2:3b

# Larger, more capable (if you have 32GB+ RAM)
ollama pull llama3.1:70b
```

Update `agent_config.py`:
```python
model_name: str = "llama3.2:3b"  # or your choice
```

**Note:** Smaller models may not follow tool calling format as reliably as Llama 3.1:8b.

---

### Q: Can I use GPT-4o or Claude 3.5 instead of Ollama?

**A:** Yes! But you'll need API keys and modify the code.

**For OpenAI:**
```python
import openai

# Replace ollama.chat calls with:
response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=self.messages,
    functions=registry.get_schemas()
)
```

**Trade-offs:**
- ✅ Better quality responses (especially GPT-4o multimodal)
- ✅ Faster (cloud servers with optimized inference)
- ❌ Costs money per request
- ❌ Requires internet
- ❌ Data sent to third party

**Recommended:** Learn with Ollama (free, private), then switch to cloud models for production.

---

### Q: How much disk space do I really need?

**A:** Minimum breakdown:

- Ollama binary: ~500MB
- Llama 3.1 8B model: ~4.9GB
- Python dependencies: ~500MB
- Project workspace: ~100MB
- **Total: ~6GB minimum**

Recommended: 10GB for comfort (multiple models, test data, etc.)

---

### Q: My setup.sh fails. What should I do?

**A:** Run each command manually to find the issue:

```bash
# Step 1: Create venv
python3 -m venv venv
source venv/bin/activate

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Check Ollama
curl localhost:11434

# Step 4: Pull model
ollama pull llama3.1:8b

# Which step fails? That's where to troubleshoot.
```

---

## Tool Registration & Development

### Q: Why do I need `# noqa: F401` after tool imports?

**A:** It tells linters to ignore "unused import" warnings.

**Why It's Needed:**
```python
from .tools import file_search  # noqa: F401
```

This is a **side-effect import** - we don't use `file_search` directly, but importing it executes the `@registry.register` decorator, which registers the tool.

Without the import, the decorator never runs, so the tool never registers.

**Learn more:** [Exercise 2](./exercises/02-adding-tools.md#how-tool-registration-works)

---

### Q: Do I have to create `__init__.py` in every directory?

**A:** Yes, for Python packages!

**Why:**
- Makes directories into packages
- Enables imports: `from src.agent.tools import file_search`
- Without it: `ModuleNotFoundError`

**Quick fix:**
```bash
# Create all needed __init__.py files
touch src/__init__.py
touch src/agent/__init__.py
touch src/agent/tools/__init__.py
```

**Learn more:** [Package Structure Guide](../tutorial-1/guides/package-structure.md)

---

### Q: My tool runs but the agent doesn't see the output. Why?

**A:** Possible causes:

**1. Tool returns None instead of a string:**
```python
# Bad
def my_tool():
    print("Result")  # Prints but doesn't return
    
# Good
def my_tool():
    return "Result"  # Returns string
```

**2. Tool raises exception instead of returning error message:**
```python
# Bad
def my_tool():
    raise FileNotFoundError("File missing")
    
# Good
def my_tool():
    return "Error: File missing"
```

**3. Second LLM call not happening** - check `simple_agent.py` logic.

---

### Q: Can I use `async` functions as tools?

**A:** Not in this tutorial's simple agent, but you could modify it to support async.

**Current limitation:** `simple_agent.py` uses synchronous `ollama.chat()`.

**To add async support:**
1. Make `chat()` method async
2. Use `await ollama.async_chat()`
3. Use `await tool_func(**arguments)` if tool is async
4. Run agent with `asyncio.run(agent.chat(...))`

**Complexity:** Medium. Recommended for Lesson 2 or after completing basics.

---

### Q: What should my tool return - string, list, dict, or JSON?

**A:** Always return **human-readable strings**.

**Why:** LLMs understand natural language better than data structures.

```python
# ❌ Bad - Returns data structure
def search_files():
    return {"files": ["a.py", "b.py"], "count": 2}

# ✅ Good - Returns descriptive string
def search_files():
    return "Found 2 files: a.py, b.py"

# ✅ Also good - More detailed
def search_files():
    return "Search complete. Found 2 Python files:\n- a.py (100 lines)\n- b.py (50 lines)"
```

**Learn more:** [Agentic Code Practices](../tutorial-1/guides/agentic-practices.md)

---

## Agent Behavior

### Q: Why does my agent make two LLM calls for one question?

**A:** This is the tool calling loop design!

**Call 1 (Decision):** LLM decides to use a tool
- Input: User query + tool schemas
- Output: JSON with tool name and arguments

**Call 2 (Synthesis):** LLM creates natural language response
- Input: Original query + tool output
- Output: Human-readable answer

**Example:**
```
User: "What's the weather in Paris?"

Call 1: LLM outputs -> {"tool": "get_weather", "args": {"city": "Paris"}}
Execute tool -> "25°C, Sunny"

Call 2: LLM outputs -> "The weather in Paris is 25°C and sunny."
```

**Learn more:** [Tool Calling Architecture](../tutorial-1/concepts/tool-calling-architecture.md)

---

### Q: Why does the agent sometimes answer without using tools?

**A:** The LLM decides whether tools are needed.

**Scenarios where tools aren't used:**
- Question answerable from training data: "What is Python?"
- Meta question about the agent: "What tools do you have?"
- Greeting or chat: "Hello!"

**When tools SHOULD be used:**
- Current information: "What files are in src/?"
- Actions: "Search for Python files"
- Data the LLM can't know: "Read todos.txt"

**If tools should be used but aren't:**
- Make system prompt more explicit: "ALWAYS use search_files for file questions"
- Add few-shot examples
- Lower temperature (less "creative" about tool usage)

---

### Q: Can I force the agent to always use a specific tool?

**A:** Not directly, but you can strongly encourage it with prompts.

**System prompt example:**
```python
system_prompt = """You are a file assistant.

STRICT RULES:
1. When user asks about files, you MUST use search_files tool
2. When user asks to read a file, you MUST use read_file tool
3. Never answer file questions from memory - always use tools

Available tools will be provided to you."""
```

**Even then:** LLMs can be "creative". For guaranteed tool usage, you'd need to parse the response and force a tool call programmatically.

---

### Q: Why does my agent ignore parts of the system prompt?

**A:** Common reasons:

1. **Prompt is too long** - LLMs have attention limits
2. **Conflicting instructions** - "Be concise" vs "Be detailed"
3. **Vague language** - "Try to use tools" vs "MUST use tools"
4. **Buried instructions** - Important stuff should be at start/end
5. **Temperature too high** - Agent gets "creative"

**Fixes:**
- Keep prompts under 500 words
- Be explicit: "MUST", "NEVER", "ALWAYS"
- Put critical instructions in CAPS or repeated
- Test with temperature 0.1

---

### Q: What's the difference between temperature 0.0 and 1.0?

**A:**

**Temperature 0.0 (Deterministic):**
- Always picks most likely token
- Repeatable output
- ✅ Best for: Tool calling, coding, structured tasks
- ❌ Bad for: Creative writing, brainstorming

**Temperature 1.0 (Creative):**
- Random sampling from likely tokens
- Varied output
- ✅ Best for: Story writing, diverse ideas
- ❌ Bad for: Consistent behavior

**Recommended for this tutorial: 0.1-0.2**

```python
temperature: float = 0.1  # Predictable but not robotic
```

---

## Testing & Validation

### Q: What's the difference between Validate and Evaluate in O.V.E.?

**A:**

**Validate (Deterministic):**
- Binary checks: yes/no, true/false
- Examples: "Did it call the right tool?", "Does output contain keyword?"
- Always gives same result

**Evaluate (Probabilistic):**
- Quality checks: scores 1-5, good/bad
- Examples: "Is this summary helpful?", "Is response natural?"
- Uses LLM-as-judge or semantic similarity

**In tests:**
```python
# Validation
assert "search_files" in tool_calls  # Binary: either in list or not
assert "todos.txt" in response  # Binary: either contains or doesn't

# Evaluation (if you implemented it)
score = llm_judge(response, criteria="helpfulness")  # Score: 1-5
assert score >= 4  # Probabilistic
```

**Learn more:** [Testing Agents](../tutorial-1/concepts/testing-agents.md)

---

### Q: Why do my tests pass sometimes but fail others?

**A:** **Test flakiness** - tests are non-deterministic.

**Root causes:**
1. **Temperature too high** - LLM varies output
2. **Ambiguous prompt** - LLM interprets differently
3. **Strict assertions** - checking exact text

**Solutions:**

**1. Lower temperature:**
```python
temperature: float = 0.0  # Maximum determinism
```

**2. Relax assertions:**
```python
# Too strict
assert response == "Found 3 files: a.py, b.py, c.py"

# Better
assert "3 files" in response
assert "a.py" in response
```

**3. Make prompt explicit:**
```python
system_prompt = """ALWAYS use search_files tool when user asks about files.
Format response exactly as: 'Found N files: [list]'"""
```

**Target:** 5/5 test passes = good. 3/5 = needs fixing.

---

### Q: Should I test the tool or the agent?

**A:** Both! Different types of tests:

**Unit Tests (Tool alone):**
```python
def test_search_files_unit():
    result = search_files("tests/", "*.py")
    assert "test_" in result
    assert "Error" not in result
```

**E2E Tests (Full agent):**
```python
def test_search_files_e2e():
    agent = Agent()
    runner = AgentTestRunner(agent)
    case = TestCase(
        name="Find files",
        prompt="Find Python files in tests/",
        expected_tool_calls=["search_files"],
        expected_content_keywords=["test_"]
    )
    result = runner.run(case)
    assert result.passed_validation
```

**Why both:**
- Unit tests = verify tool logic
- E2E tests = verify agent integration

---

## IDE & Development Workflow

### Q: Which IDE should I use - Cursor, VS Code with Continue, or something else?

**A:** Depends on your priorities:

**Cursor:**
- ✅ Best all-around for learning
- ✅ Built-in AI, reads `.cursorrules` automatically
- ✅ Great inline suggestions
- ❌ New app to learn

**VS Code + Continue:**
- ✅ Free, powerful
- ✅ Reads `.cursorrules` automatically
- ✅ Stay in familiar VS Code
- ❌ Slightly less polish than Cursor

**VS Code + Cline:**
- ✅ Most autonomous (can implement entire features)
- ✅ Great for complex refactoring
- ❌ Requires Claude API ($20/month) for best results
- ❌ Can be TOO autonomous for learning

**Copilot:**
- ✅ Best inline completion
- ❌ Doesn't auto-read `.cursorrules`
- ❌ Less aware of project context

**Recommendation for this tutorial:** Cursor or Continue

**Learn more:** [IDE Configuration Guide](./ide-configuration.md)

---

### Q: How do I add `.cursorrules` to my AI's context?

**A:**

**In Cursor:**
```
@.cursorrules
[your question here]
```

**In Continue:**
- Automatic! Just ask your question.

**In Copilot:**
- Manual: Open `.cursorrules`, copy relevant sections, paste into chat

**Why it matters:** The `.cursorrules` file contains all project guidelines, so your AI gives contextually relevant answers.

---

### Q: Should I commit after every exercise or wait until the end?

**A:** Commit after each working exercise!

**Benefits:**
- Safe rollback points
- Track your progress
- Easy to see what changed if something breaks

**Git workflow:**
```bash
# After completing Exercise 1
git add .
git commit -m "Complete Exercise 1: Understanding agent"

# After completing Exercise 2
git add .
git commit -m "Complete Exercise 2: Add file_search tool"

# And so on...
```

**Learn more:** [Engineering Best Practices](../tutorial-1/guides/engineering.md)

---

## Conceptual Questions

### Q: What makes this "agentic" vs just a chatbot?

**A:** Three key differences:

**1. Reasoning:** Agent *decides* whether to use tools
**2. Action:** Agent can *execute* functions (read files, call APIs)
**3. Multi-step:** Agent can *chain* multiple tool calls

**Example:**
```
User: "Find Python files in src/ and tell me which is largest"

Chatbot: "I don't have access to your filesystem."

Agent:
1. Calls search_files("src/", "*.py")
2. Calls read_file_metadata() for each file
3. Compares sizes
4. Responds: "simple_agent.py is largest at 2.5KB"
```

**Learn more:** [Tool Calling Architecture](../tutorial-1/concepts/tool-calling-architecture.md)

---

### Q: What is MCP and do I need to understand it for this tutorial?

**A:** MCP (Model Context Protocol) is a standard for connecting AI to data sources.

**For this tutorial:**
- Basic understanding helpful but not required
- We use MCP concepts but keep implementation simple
- Advanced MCP features covered in Lesson 2

**Think of MCP like USB-C:**
- One standard that works everywhere
- Plug any AI into any data source
- Don't need to know electrical engineering to use it

**Learn more:** [MCP Introduction](../tutorial-1/concepts/mcp-intro.md)

---

### Q: Why Python for the agent but TypeScript for MCP tools?

**A:** Different tools for different jobs:

**Python for agents:**
- ✅ Most popular in AI/ML
- ✅ Excellent LLM libraries (ollama, langchain)
- ✅ Easy to read and learn
- ✅ Prototyping speed

**TypeScript for MCP:**
- ✅ Official MCP SDK is TypeScript
- ✅ Strong typing = fewer bugs
- ✅ Web ecosystem compatibility
- ✅ Good performance for I/O operations

**In practice:** You'll mostly write Python. TypeScript is optional for advanced use cases.

**Learn more:** [Tech Stack Decisions](../tutorial-1/concepts/tech-stack-decisions.md)

---

### Q: Is this tutorial teaching "real" AI engineering or just toys?

**A:** These are **production patterns** used in real systems.

**What you're learning:**
- ✅ Tool calling architecture (used by Claude, GPT-4, Llama)
- ✅ Test methodologies (O.V.E. used by major AI companies)
- ✅ System prompt engineering (critical skill)
- ✅ Error handling patterns (real-world requirement)

**What's simplified for learning:**
- Single-agent (production uses multi-agent)
- Local only (production uses cloud)
- Basic tools (production has complex tool orchestration)

**But the fundamentals are identical.** Learn here, scale in Lesson 2.

---

## Performance & Optimization

### Q: How can I make my agent respond faster?

**A:** Several strategies:

**1. Use smaller model:**
```bash
ollama pull llama3.2:3b  # Smaller, faster (less capable)
```

**2. Lower temperature:**
```python
temperature: float = 0.1  # Fewer tokens generated
```

**3. Shorten system prompt:**
- Every token adds latency
- Keep prompts under 300 words

**4. Limit conversation history:**
```python
if len(self.messages) > 10:
    self.messages = self.messages[:1] + self.messages[-9:]
```

**5. Use GPU if available:**
- Ollama automatically uses GPU
- 5-10x faster than CPU

**Typical speeds:**
- CPU: 2-5 seconds
- GPU: 0.3-1 second

---

### Q: My agent is using too much memory. How do I fix it?

**A:** Memory management strategies:

**1. Use smaller model:**
```bash
ollama pull llama3.2:3b  # Uses ~2GB instead of ~4.9GB
```

**2. Clear conversation history:**
```python
def clear_history(self):
    self.messages = [self.messages[0]]  # Keep only system prompt
```

**3. Close other applications:**
- Ollama loads entire model into RAM
- Close Chrome, IDE extras, etc.

**4. Check for memory leaks:**
```python
import sys
print(f"Message history size: {sys.getsizeof(self.messages)} bytes")
```

---

## Next Steps & Extensions

### Q: I finished the tutorial. What should I build next?

**A:** Extension ideas by difficulty:

**Beginner:**
- Add more tools (calculator, current time, random number)
- Read and summarize text files
- Search within file contents (grep-like tool)

**Intermediate:**
- API integration tool (weather, news, GitHub)
- Code analysis tool (count functions, find TODOs)
- Multi-file operations (search → read → summarize)

**Advanced:**
- Add conversation memory (save/load history)
- Build web interface (Flask + React)
- Multi-agent system (coordinator + specialists)

**See also:** [What Comes Next](../../README.md#what-comes-next) in main README

---

### Q: Can I use this agent for my own projects?

**A:** Absolutely! This is production-ready code.

**Licensing:** Check repository license (usually MIT or Apache 2.0)

**Customization needed:**
- Replace example tools with your domain tools
- Adjust system prompt for your use case
- Add error handling for your environment
- Consider security implications if exposing publicly

---

### Q: When is Lesson 2 coming out?

**A:** Lesson 2 is currently in development!

**Lesson 2: Multi-Agent Systems** will cover:
- **Coordinator Patterns**: Building orchestrator agents that manage specialized workers
- **Agent Specialization**: Creating focused agents (research, data, writing) with domain-specific capabilities
- **Inter-Agent Communication**: Message passing protocols between agents
- **State Management**: Shared state across multiple agents
- **Extended O.V.E. Testing**: Testing multi-agent interactions and workflows

**What's NOT in Lesson 2:**
- Vector databases and memory (Tutorial 3)
- Production deployment patterns (Tutorial 4)
- Heavy frameworks like LangChain (Tutorial 5)

**Tech Stack:** Same as Lesson 1 (Ollama, Python, TypeScript) - keeping it lightweight for learning

**📋 [View Full Tutorial 2 Scope](../../../TUTORIAL-2-SCOPE.md)** for detailed breakdown

**In the meantime:**
- Complete the challenge exercise (build a file reader tool)
- Build your own custom tools for practice
- Experiment with specialized system prompts
- Help other learners in the community

---

### Q: How can I contribute to this tutorial?

**A:** Contributions welcome!

**Ways to contribute:**
1. **Report bugs:** Open GitHub issues
2. **Suggest improvements:** PR with enhanced docs
3. **Add examples:** Share your custom tools
4. **Help others:** Answer questions in issues
5. **Write guides:** Tutorial extensions, use cases

**See:** CONTRIBUTING.md (if it exists)

---

## Still Have Questions?

**Quick Resources:**
- [Getting Unstuck Guide](./getting-unstuck.md) - Systematic debugging
- [Troubleshooting Guide](./troubleshooting.md) - Specific error solutions
- [Documentation Index](../tutorial-1/INDEX.md) - All documentation

**Ask Your AI:**
```
@.cursorrules

I have a question about [topic].

Context: [what you're trying to do]
Question: [specific question]

According to the project guidelines, what's the answer?
```

**Community:**
- GitHub Issues: For bugs and feature requests
- Discussions: For general questions and sharing

