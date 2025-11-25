"""
Python-to-Node.js bridge for MCP (Model Context Protocol) tools.

This module provides a bridge between Python agents and TypeScript/JavaScript
tools by spawning Node.js processes. It enables agents to use tools written
in other languages while maintaining a Python-native agent implementation.

The bridge implements two core tools:
- read_file: Read file contents from the filesystem
- list_directory: List files and directories

Architecture:
    Python Agent -> run_node_tool() -> Node.js process -> TypeScript tool -> Result

In production, consider:
- Using a persistent Node.js server instead of spawning processes
- Implementing proper error handling and timeouts
- Adding security validation for file paths

Example:
    from agent.mcp_tool_bridge import read_file, list_directory

    # These tools are automatically registered and available to agents
    contents = read_file("data/notes.txt")
    files = list_directory("data/")
"""

import subprocess
import os
import json
from typing import List
from .tool_registry import registry

# Path to the compiled JS tool
TOOLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS_TOOL_PATH = os.path.join(TOOLS_DIR, "tools", "dist", "index.js")

def run_node_tool(command: str, *args) -> str:
    """
    Execute a Node.js tool script with the given command and arguments.

    This helper function bridges Python to TypeScript MCP tools by spawning
    a Node.js process to execute the compiled JavaScript tool.

    Args:
        command: The tool command to execute (e.g., "read_file", "list_dir")
        *args: Variable arguments to pass to the Node.js tool

    Returns:
        The stdout output from the Node.js tool as a string, or an error
        message if execution fails

    Note:
        In production, consider using a persistent Node.js process or server
        instead of spawning a new process for each call.
    """
    try:
        # Check if node is installed
        # In a real app, we might use a persistent process/server
        full_args = ["node", JS_TOOL_PATH, command] + list(args)
        result = subprocess.run(
            full_args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"
    except Exception as e:
        return f"System Error: {str(e)}"

@registry.register
def read_file(file_path: str) -> str:
    """
    Read the contents of a file from the local filesystem.

    This tool uses a Node.js bridge to read files. It provides basic
    file reading capabilities for the agent.

    Args:
        file_path: Path to the file to read. Can be absolute or relative
                  to the current working directory

    Returns:
        The contents of the file as a string, or an error message if
        the file cannot be read

    Examples:
        read_file("data/notes.txt") -> "File contents..."
        read_file("missing.txt") -> "Error: File not found"

    Security:
        In production environments, strictly validate and sanitize file paths
        to prevent directory traversal attacks and unauthorized file access.
    """
    # Security: In a real agent, strictly validate paths here!
    return run_node_tool("read_file", file_path)

@registry.register
def list_directory(dir_path: str = ".") -> str:
    """
    List all files and subdirectories in a specified directory.

    This tool uses a Node.js bridge to list directory contents.
    Useful for exploring the filesystem structure.

    Args:
        dir_path: Path to the directory to list. Defaults to "." (current
                 directory). Can be absolute or relative

    Returns:
        A string listing the contents of the directory, or an error message
        if the directory cannot be accessed

    Examples:
        list_directory(".") -> "Files: file1.txt, file2.py, ..."
        list_directory("data/") -> "Files: notes.txt, todos.txt, ..."
        list_directory("invalid/") -> "Error: Directory not found"
    """
    return run_node_tool("list_dir", dir_path)

