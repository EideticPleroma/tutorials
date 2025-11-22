# Exercise 3: Prompt Engineering

**Goal**: Control the Agent's brain.

## Context
The system prompt in `src/agent/agent_config.py` is the Agent's operating system. It's defined as `config.system_prompt` (lines 9-12) and loaded by the Agent in its `__init__` method. We want to upgrade it to force "Chain of Thought" (CoT).

## Steps

### 1. The "Think First" Rule
Modify the `system_prompt` string in `src/agent/agent_config.py`.
Add a directive:
> "Before calling any tool, you must output a thought block explaining your reasoning: `Thought: I need to check X because Y.`"

### 2. Few-Shot Prompting
The best way to teach is by example. Add a section to the prompt:

```
Examples:

User: Find the error in app.py
Thought: I need to locate app.py and read it.
Tool: search_files(pattern="app.py")
...
```

### 3. Testing
Run the agent with a complex query: "What tools are available and how do they work?"
Does it explain its reasoning before acting?

### 4. Verify Changes
After modifying `agent_config.py`, restart your agent:
```bash
python -m src.agent.simple_agent
```

The agent will automatically use the updated system prompt.

## Reflection
Compare the agent's behavior from Exercise 1 and Exercise 3. The CoT agent should be more deliberate and explain its reasoning process.

