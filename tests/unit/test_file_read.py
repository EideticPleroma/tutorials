"""
Unit and E2E tests for read_file tool.
Demonstrates the O.V.E. (Observe, Validate, Evaluate) methodology.

Students: Complete these tests in Exercise 5 (Challenge).
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

    TODO: Students implement this test in Exercise 5 (Challenge)
    After implementing read_file:
    1. Remove the pytest.skip() line
    2. Run to verify your implementation
    """
    pytest.skip("Students implement read_file in Exercise 5, then complete this test")

    # TODO: Implement this test


def test_read_file_handles_missing_file():
    """
    Unit test: Verify read_file returns error for missing file.

    TODO: Students implement this test in Exercise 5 (Challenge)
    """
    pytest.skip("Students implement in Exercise 5")

    # TODO: Implement this test


def test_read_file_handles_large_file():
    """
    Unit test: Verify read_file rejects files over 10MB.

    Creates a temporary file larger than 10MB, attempts to read it using the tool,
    and asserts that the error message mentions 'too large'. Cleans up the temp file.

    TODO: Students implement this test in Exercise 5 (Challenge)
    Hints:
    - Use tempfile.NamedTemporaryFile to create a temp file
    - Write > 10MB of data (10 * 1024 * 1024 + 1 bytes)
    - Test that read_file returns an error mentioning "too large"
    - Clean up the temp file in a finally block
    """
    pytest.skip("Students implement in Exercise 5")

    # TODO: Implement this test


def test_read_file_handles_binary_file():
    """
    Unit test: Verify read_file rejects binary files.

    Creates a temporary binary file, attempts to read it using the tool,
    and asserts that the error message mentions 'binary'.

    TODO: Students implement this test in Exercise 5 (Challenge)
    """
    pytest.skip("Students implement in Exercise 5")

    # TODO: Implement this test


def test_read_file_reads_small_file():
    """
    Unit test example: Verifies read_file correctly reads a small, known text file.

    - Uses data/todos.txt, which has predictable contents.
    - Asserts the output does not include errors.
    - Checks that the filename, relevant contents, and line count appear in the result.

    Use this pattern as a reference for building additional file read tests.

    TODO: Students implement this test in Exercise 5 (Challenge)
    """
    pytest.skip("Students implement in Exercise 5")

    # TODO: Implement this test


# ============================================================================
# E2E Tests - Testing the Agent with the Tool
# ============================================================================


def test_agent_uses_read_file_tool():
    """
    E2E test: Confirm the agent calls the read_file tool when prompted.

    This test demonstrates VALIDATION (deterministic check) by ensuring:
    - The agent calls "read_file" when asked to read Python files in the tests/ directory.
    - The agent's response includes a relevant keyword from the file content.

    TODO: Students implement this test in Exercise 5 (Challenge)
    After implementing read_file and importing it:
    1. Remove the pytest.skip() line
    2. Run to verify the agent uses your tool
    """
    pytest.skip("Students implement in Exercise 5")

    # TODO: Implement this test


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

    TODO: Students implement this test in Exercise 5 (Challenge)
    This test requires both search_files AND read_file to be implemented.
    """
    pytest.skip("Students implement in Exercise 5")

    # TODO: Implement this test


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
