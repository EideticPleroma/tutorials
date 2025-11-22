# Test Data Files

This directory contains sample files used for testing file operation tools in Lab 1.

## Files

### todos.txt
Sample TODO list for testing file reading capabilities. Contains a realistic project task list with both pending items and completed tasks.

**Used in**:
- Unit tests for `read_file` tool
- E2E tests verifying agent can read and interpret task lists
- Demonstrates handling of multi-line text files

### notes.txt
Simple project notes file for testing search and read operations. Contains brief project information in a natural format.

**Used in**:
- Testing file search with specific patterns
- Multi-tool orchestration (search → read)
- Demonstrates small file handling

### sample.py
Basic Python file for testing code file operations. Contains a simple function and main block.

**Used in**:
- Testing search for Python files (*.py pattern)
- Demonstrating agent's ability to read code files
- Future exercises on code analysis

## Purpose

These files are part of the Lab 1 exercises and provide consistent test data for:

1. **Unit Testing**: Validate that your tools (file_search, read_file) work correctly with known inputs
2. **E2E Testing**: Verify the agent's ability to find and read files in realistic scenarios
3. **O.V.E. Methodology**: Demonstrate Observe-Validate-Evaluate testing with predictable results
4. **Multi-Tool Orchestration**: Enable testing of tool chaining (search → read → analyze)

## Important Notes

⚠️ **Do not modify these files** - Tests depend on their specific content and structure. Any changes may cause test failures.

✅ **These files are committed to the repository** - Unlike student implementation files (which are gitignored), test data is shared to ensure consistency.

## Test Data Philosophy

In agentic AI development, having consistent test data is crucial because:
- LLM outputs are probabilistic, but tool inputs/outputs should be deterministic
- Shared test data enables reproducible test results across different environments
- Realistic data helps validate that tools work in production-like scenarios
- Small, focused files keep context windows manageable

If you need additional test files for your own experiments, create them in a separate directory (e.g., `data/experiments/`) to avoid conflicts with the lab exercises.

