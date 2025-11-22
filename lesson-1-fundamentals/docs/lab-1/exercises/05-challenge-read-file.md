# Challenge: Read File Tool

**Goal**: Extend the agent with file reading capabilities.

**Difficulty**: Intermediate | **Time**: 1-2 hours

## Context

You've successfully implemented `search_files` which helps the agent find files. Now let's give it the ability to actually read file contents. This is a common pattern in agentic AI: **search → read → analyze**.

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

