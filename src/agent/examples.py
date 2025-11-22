import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.simple_agent import Agent

def run_workflow(name, prompt):
    print(f"\n=== Running Workflow: {name} ===")
    print(f"Prompt: {prompt}")
    agent = Agent()
    response = agent.chat(prompt)
    print(f"Final Response: {response}\n")

def main():
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

