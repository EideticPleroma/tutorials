"""
Example workflows demonstrating agent capabilities.

This module provides example scenarios showing how the agent can be used
for different tasks like research assistance, code analysis, and data
processing. Each workflow demonstrates different tool combinations.

Workflows:
1. Research Assistant - Uses list_directory and read_file to explore data
2. Code Analyzer - Uses read_file to examine code files
3. Data Processor - Uses calculate for mathematical operations

Run this script to see the agent in action:
    python src/agent/examples.py

Note:
    These examples assume certain files exist in the data/ directory.
    The agent behavior depends on the configured LLM model.
"""

import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.simple_agent import Agent

def run_workflow(name, prompt):
    """
    Execute a single workflow example with the agent.

    Creates a fresh agent instance, sends the prompt, and displays
    the workflow name, prompt, and final response.

    Args:
        name: Descriptive name for the workflow (e.g., "Research Assistant")
        prompt: The user query to send to the agent

    Example:
        run_workflow(
            "Calculator",
            "What is 25 * 4?"
        )

    Output:
        Prints the workflow name, prompt, agent's response, and any
        tool calls made during execution.
    """
    print(f"\n=== Running Workflow: {name} ===")
    print(f"Prompt: {prompt}")
    agent = Agent()
    response = agent.chat(prompt)
    print(f"Final Response: {response}\n")

def main():
    """
    Run all example workflows demonstrating agent capabilities.

    Executes three workflows in sequence:
    1. Research Assistant: Explores data directory and reads files
    2. Code Analyzer: Examines Python code for bugs
    3. Data Processor: Performs calculations

    Each workflow demonstrates different tool usage patterns and
    shows how the agent chains tool calls to accomplish tasks.

    Usage:
        python src/agent/examples.py

    Requirements:
        - Ollama running locally with configured model
        - data/ directory with sample files (notes.txt, sample.py)
    """
    # 1. Research Assistant
    # Needs to list directory to find files, then read them.
    # Note: We need to ensure the agent knows where the files are.
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))
    
    run_workflow(
        "Research Assistant",
        f"Please list the files in {data_dir} and summarize the content of 'notes.txt'."
    )

    # 2. Code Analyzer
    run_workflow(
        "Code Analyzer",
        f"Read the file {os.path.join(data_dir, 'sample.py')} and tell me if there are any obvious bugs."
    )

    # 3. Data Processor
    run_workflow(
        "Data Processor",
        "Calculate 155 * 32 and tell me if the result is greater than 5000."
    )

if __name__ == "__main__":
    main()

