import subprocess
import os
import json
from typing import List
from .tool_registry import registry

# Path to the compiled JS tool
TOOLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS_TOOL_PATH = os.path.join(TOOLS_DIR, "tools", "dist", "index.js")

def run_node_tool(command: str, *args) -> str:
    """Helper to run the Node.js tool script."""
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
    file_path: path to the file
    """
    # Security: In a real agent, strictly validate paths here!
    return run_node_tool("read_file", file_path)

@registry.register
def list_directory(dir_path: str = ".") -> str:
    """
    List files in a directory.
    dir_path: path to the directory (default: current)
    """
    return run_node_tool("list_dir", dir_path)

