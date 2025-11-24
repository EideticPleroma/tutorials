# Challenge: Read File Tool

**Goal**: Extend the agent with file reading capabilities.

**Difficulty**: Intermediate | **Time**: 1-2 hours

## Context

You've successfully implemented `search_files` which helps the agent find files. Now let's give it the ability to actually read file contents. This is a common pattern in agentic AI: **search → read → analyze**.

## AI-Assisted Challenge Approach

> **AI Context for This Challenge**
> - `@.cursorrules` (always)
> - `@src/agent/tools/file_search.py` (your previous tool as reference)
> - `@lesson-1-fundamentals/tutorial-1/guides/agentic-practices.md` (tool design patterns)

**This is a challenge - you should figure it out with AI help, not just copy!**

**Recommended conversation flow (expect 3-5 AI exchanges):**

**Phase 1 - Design:**
```
@.cursorrules @lesson-1-fundamentals/tutorial-1/guides/agentic-practices.md

Challenge: Implement read_file tool.

Requirements: [paste requirements from below]

Based on agentic practices:
1. What error cases must I handle?
2. Should I return the raw content or formatted?
3. How do I detect binary files?
```

**Phase 2 - Implementation:**
```
@.cursorrules @src/agent/tools/file_search.py

Here's my read_file implementation:
[paste code]

Following the patterns from file_search:
1. Is my error handling correct (strings, not exceptions)?
2. Is my docstring LLM-friendly?
3. Did I miss any edge cases?
```

**Phase 3 - Testing:**
```
@.cursorrules @tests/test_framework.py

I need tests for read_file. Looking at my implementation:
[paste relevant parts]

How should I structure:
1. Unit tests for each error case?
2. E2E test for tool chaining (search → read)?
```

**Phase 4 - Refinement:**
```
@.cursorrules

Test results: [describe what's failing]
Agent behavior: [describe what happens]

What needs adjustment?
```

**Challenge Mindset:**
- ✅ Use previous exercises as patterns, not exact templates
- ✅ Iterate with AI - first draft won't be perfect
- ✅ Test each requirement individually
- ✅ Build on what you've learned, not from scratch

**Remember:** Expect 3-5 iterations to get this working well. That's how real development works!

## The Challenge

Implement a `read_file` tool that allows the agent to read and display the contents of text files.

## Requirements

### 1. Tool Signature

Create `src/agent/tools/read_file.py` with this function:

```python
def read_file(filename: str) -> str:
    """
    Read the contents of a text file.
    
    Args:
        filename: Path to the file to read (e.g., "data/notes.txt")
    
    Returns:
        String containing file contents or an error message
    
    Examples:
        read_file("data/notes.txt") -> "File contents: ..."
        read_file("missing.txt") -> "Error: File not found"
    """
```

### 2. Error Handling (Critical!)

Your tool MUST handle these cases gracefully:

**Missing Files**:
- If file doesn't exist, return: `"Error: File '{filename}' not found"`
- Don't raise exceptions - return error strings!

**Large Files**:
- Reject files larger than 10MB
- Return: `"Error: File too large (X.XMB, limit is 10MB)"`
- Use `os.path.getsize()` to check before reading

**Binary Files**:
- Catch `UnicodeDecodeError` when trying to read
- Return: `"Error: Cannot read binary file '{filename}'"`
- This prevents the agent from trying to read images, PDFs, etc.

### 3. Registration

Don't forget to:
1. Add `@registry.register` decorator
2. Import in `src/agent/tools/__init__.py`
3. Import in `src/agent/simple_agent.py` (with `# noqa: F401`)

## Testing Requirements

Create `tests/unit/test_read_file.py` with:

### Unit Tests (4 minimum)
1. **test_read_file_reads_existing_file**: Use `data/todos.txt`
2. **test_read_file_handles_missing_file**: Use a non-existent filename
3. **test_read_file_handles_large_file**: Create a temp file >10MB
4. **test_read_file_handles_binary_file**: Create a temp binary file

### E2E Tests (2 minimum)
1. **test_agent_uses_read_file_tool**: Agent reads a specific file
2. **test_agent_finds_and_reads_file**: Agent chains search → read

Example E2E test:

```python
def test_agent_uses_read_file_tool():
    agent = Agent()
    runner = AgentTestRunner(agent)
    
    case = TestCase(
        name="Read specific file",
        prompt="Read the file data/todos.txt",
        expected_tool_calls=["read_file"],
        expected_content_keywords=["TODO"]
    )
    
    result = runner.run(case)
    assert result.passed_validation
```

## Multi-Tool Orchestration

The real power comes when the agent can chain tools. Test this scenario:

**Prompt**: "Find files in data/ and tell me what's in notes.txt"

**Expected behavior**:
1. Agent calls `search_files("data/", "*")` → finds todos.txt, notes.txt, sample.py
2. Agent calls `read_file("data/notes.txt")` → reads the content
3. Agent responds with the actual content from notes.txt

This demonstrates the agent's ability to break down complex tasks into multiple tool calls.

## Verification Checklist

- [ ] Tool is registered and imported correctly
- [ ] Agent can answer: "Read the file data/todos.txt"
- [ ] Agent handles: "Read the file nonexistent.txt" (shows error gracefully)
- [ ] All unit tests pass (4/4)
- [ ] All E2E tests pass (2/2)
- [ ] Agent can chain tools: "Find and read data/notes.txt"

## Tips

**Returning Descriptive Strings**:
Instead of just returning the raw content, add context:
```python
return f"File '{filename}' ({lines} lines, {file_size} bytes):\n\n{content}"
```

This helps the agent understand what it's seeing.

**Using Fixtures**:
For temp file tests, use pytest fixtures for automatic cleanup:
```python
@pytest.fixture
def temp_large_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"A" * (10 * 1024 * 1024 + 1))  # >10MB
        tmp_path = tmp.name
    yield tmp_path
    os.remove(tmp_path)
```

## Reflection Questions

After completing this challenge, consider:

1. **Why return error strings instead of raising exceptions?**
   - The agent can't catch Python exceptions
   - Error strings let the agent communicate errors to users naturally

2. **Why limit file size?**
   - LLMs have context limits
   - Reading huge files would overflow the context window
   - 10MB is reasonable for config files, logs, code

3. **How does tool chaining work?**
   - Agent sees tool outputs in its conversation history
   - It can use previous outputs to decide next actions
   - This enables complex multi-step workflows

## Success Criteria

You've completed the challenge when:
✅ All 6+ tests pass consistently (run 5 times)
✅ Agent successfully chains search → read operations
✅ Error cases are handled gracefully
✅ Agent provides helpful responses using file contents

## Common Issues for This Challenge

### File Not Found Errors
- **Check:** Paths are relative to project root
- **Check:** Using `os.path.join()` for cross-platform compatibility
- **Try:** Print the full path being accessed for debugging

### Binary File Detection
- **Approach 1:** Try to decode as UTF-8, catch `UnicodeDecodeError`
- **Approach 2:** Check for null bytes in first 8KB
- **Approach 3:** Use `mimetypes` module

### Large File Handling
- **Don't:** Load entire file into memory
- **Do:** Check `os.path.getsize()` first
- **Return:** Helpful error like "File too large (15MB). Max size: 10MB"

### Agent Doesn't Chain Tools
- **Check:** System prompt encourages tool chaining
- **Try:** Test with explicit query: "Search for Python files, then read todos.txt"
- **Debug:** Check message history - are both tool calls present?

---

## 💡 Stuck on This Challenge?

**Tool Implementation Help:**

```
@.cursorrules

Challenge Exercise: Implementing read_file tool.

I'm stuck on: [error handling / binary detection / large files / testing]

Current implementation:
[paste your read_file function]

Error I'm getting:
[paste error or describe issue]

According to agentic best practices, how should I handle this?
```

**Tool Chaining Issues:**

```
@.cursorrules

My agent can search OR read, but not chain search→read.

System prompt includes: [paste relevant part]

Test query: "Find Python files in tests/, then read test_framework.py"

Agent behavior: [describe what happens]

How do I encourage multi-step reasoning?
```

**Test Writing Help:**

```
@.cursorrules

Challenge: Writing tests for read_file tool.

Completed unit tests: [list which ones]
Stuck on: [E2E test / chained tools test / flakiness]

Test code attempt:
[paste test]

Following O.V.E. methodology, how should this test be structured?
```

**Debug Tool Chaining:**
```bash
# Enable debug mode to see both tool calls
# Add to simple_agent.py:
print(f"DEBUG: Tool call {i}: {tool_call['function']['name']}")

# Then test
python -m src.agent.simple_agent
```

**See Also:**
- [Agentic Code Practices](../../tutorial-1/guides/agentic-practices.md) - Tool design principles
- [Troubleshooting: Tool Errors](../troubleshooting.md#tool-registration-errors)
- [FAQ: Tool Chaining](../FAQ.md#q-can-i-force-the-agent-to-always-use-a-specific-tool)

---

## 🎉 **CHALLENGE COMPLETE!**

**Congratulations!** You've built a file-reading agent that can navigate and analyze codebases. This is a significant achievement! You've:

- ✅ Implemented multi-error handling (missing, large, binary files)
- ✅ Mastered tool chaining (search → read → analyze)
- ✅ Built a complete test suite (6+ tests with O.V.E. methodology)
- ✅ Created a production-ready tool with proper error handling

**You've gone from understanding agents to building sophisticated agentic tools. You're now equipped to build your own AI-powered systems!**

## Next Steps

Once you've mastered this challenge:
- Try implementing a `write_file` tool
- Add support for reading specific line ranges
- Implement a `grep` tool for content search
- Chain tools: search → read → analyze → summarize

