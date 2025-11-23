"""
Unit and E2E tests for read_file tool.
Demonstrates the O.V.E. (Observe, Validate, Evaluate) methodology.
"""

import pytest
import os
import tempfile
from src.agent.simple_agent import Agent
from tests.test_framework import AgentTestRunner, TestCase
from src.agent.tools.read_file import read_file


# ============================================================================
# Unit Tests - Testing the Tool Directly
# ============================================================================


def test_read_file_reads_existing_file():
    """
    Unit test: Verify read_file reads a file that exists.
    """
    result = read_file("data/todos.txt")
    print(f"\n🔍 Result: {result}")
    assert "Error" not in result
    assert "todos.txt" in result
    assert "TODO" in result


def test_read_file_handles_missing_file():
    """
    Unit test: Verify read_file returns error for missing file.
    """
    result = read_file("nonexistent.txt")
    print(f"\n🔍 Result: {result}")
    assert "Error: File" in result
    assert "not found" in result


def test_read_file_handles_large_file():
    """
    Unit test: Verify read_file rejects files over 10MB.

    Creates a temporary file larger than 10MB, attempts to read it using the tool,
    and asserts that the error message mentions 'too large'. Cleans up the temp file.

    Returns:
        None
    """
    # Create a temporary large file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_filename = tmp.name
        tmp.seek(0)
        # Write slightly over 10MB (10 * 1024 * 1024 bytes + 1)
        tmp.write(b"A" * (10 * 1024 * 1024 + 1))
    try:
        result = read_file(tmp_filename)
        print(f"\n🧪 Large file read result: {result}")
        assert (
            "too large" in result.lower() or "file size" in result.lower()
        ), "Should mention file size limit"
    finally:
        os.remove(tmp_filename)


def test_read_file_handles_binary_file():
    """
    Unit test: Verify read_file rejects binary files.

    Creates a temporary binary file, attempts to read it using the tool,
    and asserts that the error message mentions 'binary'.

    Returns:
        None
    """
    # Create a temporary binary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_filename = tmp.name
        # Write non-UTF8 (binary) content
        tmp.write(b"\x00\xff\x10\x80ThisIsNotText\x00\xfe\xfd")
    try:
        result = read_file(tmp_filename)
        print(f"\n🧪 Binary file read result: {result}")
        assert "binary" in result.lower(), "Should mention cannot read binary files"
    finally:
        os.remove(tmp_filename)


def test_read_file_reads_small_file():
    """
    Unit test example: Verifies read_file correctly reads a small, known text file.

    - Uses data/todos.txt, which has predictable contents.
    - Asserts the output does not include errors.
    - Checks that the filename, relevant contents, and line count appear in the result.

    Use this pattern as a reference for building additional file read tests.
    """
    # Setup: Use a known file (data/todos.txt has known content)
    result = read_file("data/todos.txt")

    # Validate
    assert "Error" not in result, f"Unexpected error: {result}"
    assert "todos.txt" in result, "Should mention filename"
    assert "TODO" in result, "todos.txt should contain TODO items"
    assert "13 lines" in result, "Should show line count"

    print(f"\n📄 Read result: {result[:100]}...")  # Show first 100 charss


# ============================================================================
# E2E Tests - Testing the Agent with the Tool
# ============================================================================


def test_agent_uses_read_file_tool():
    """
    E2E test: Confirm the agent calls the read_file tool when prompted.

    This test demonstrates VALIDATION (deterministic check) by ensuring:
    - The agent calls "read_file" when asked to read Python files in the tests/ directory.
    - The agent's response includes a relevant keyword from the file content.
    """
    # Create and configure the agent for E2E testing
    agent = Agent()

    # Set up the agent test runner
    runner = AgentTestRunner(agent)

    # Define the test scenario and validation criteria
    case = TestCase(
        name="Read specific file",
        prompt="Read the file data/todos.txt",  # ← More specific!
        expected_tool_calls=["read_file"],
        expected_content_keywords=["TODO"],  # ← Content we know is there
    )

    # Execute the test case
    result = runner.run(case)

    # Assert validation passed (tool was called correctly)
    assert result.passed_validation


def test_agent_finds_and_reads_file():
    """
    E2E test: Ensure the agent can first use the search_files tool to locate files, then use the read_file tool to read a specific file.

    This is meant as a compound action test for multi-tool use:
    - Use prompt: "Find files in data/ and tell me what's in notes.txt"
    - The agent should:
        1. Call search_files (to find files in data/)
        2. Call read_file (to read notes.txt)
    - expected_tool_calls: ["search_files", "read_file"]
    - expected_content_keywords: Should match content from notes.txt

    This scenario demonstrates the agent's ability to chain tool invocations and verify appropriate outputs from both steps.

    """
    agent = Agent()
    runner = AgentTestRunner(agent)

    case = TestCase(
        name="Find and read file",
        prompt="Use search_files to find files in data/, then use read_file to read notes.txt",
        expected_tool_calls=["search_files", "read_file"],
        expected_content_keywords=["note"],
    )

    result = runner.run(case)
    if not result.passed_validation:
        print(f"Validation errors: {result.validation_errors}")
    assert result.passed_validation


# ============================================================================
# Helper: Create Test Files
# ============================================================================


@pytest.fixture
def temp_text_file():
    """
    Fixture to create a temporary text file for testing.
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("This is a test file.\nLine 2\nLine 3\n")
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


@pytest.fixture
def temp_binary_file():
    """
    Fixture to create a temporary binary file for testing.
    """
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".bin") as f:
        f.write(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09")  # Binary data
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


# ============================================================================
# Notes for Students
# ============================================================================
"""
Testing the read_file Tool:

Unit Tests Focus:
1. Happy path: Read a known file successfully
2. Error cases: Missing file, binary file
3. Edge cases: Large files (optional)

E2E Tests Focus:
1. Agent can use read_file when prompted
2. Agent can chain tools: search → read
3. Agent incorporates file contents into response

Key Testing Patterns:
- Use fixtures for temp files (cleanup automatic)
- Test with real files when possible (tests/conftest.py)
- Check both success and error paths
- Verify error messages are descriptive

Challenge Scenario:
"Find the file with 'Todo' in it and tell me what the todos are."

Expected Flow:
1. Agent calls search_files("data/", "*")
2. Agent sees results include files
3. Agent calls read_file("data/notes.txt")
4. Agent reads content and finds "Todo" items
5. Agent lists the todos to user
"""
