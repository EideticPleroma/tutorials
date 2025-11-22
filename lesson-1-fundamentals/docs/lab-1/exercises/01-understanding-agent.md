# Exercise 1: Understanding the Agent

**Goal**: Mental model mapping. You cannot build what you do not understand.

## Context
The file `src/agent/simple_agent.py` contains a "ReAct" (Reasoning + Acting) loop. It doesn't just answer; it thinks, acts, and observes.

## Tasks

### 1. Run with Verbose Logging
Run the agent and ask: "What is the weather in Paris?".
Observe the logs. You should see:
1.  **User Input**: "What is the weather in Paris?"
2.  **System Prompt**: The hidden instructions.
3.  **Tool Call**: `{"tool": "get_weather", "args": {"city": "Paris"}}`
4.  **Tool Output**: "15C, Cloudy"
5.  **Final Answer**: "The weather in Paris is 15C..."

### 2. Trace the Code
Open `src/agent/simple_agent.py`. Find the `chat()` method (line 49-100).
*   Where does the `messages` list get initialized? (Hint: Look in the `__init__` method)
*   Where is the `tool_registry` queried? (Hint: Look for `registry.get_schemas()` and `registry.get_tool()`)
*   How does the agent decide to make a second LLM call? (Hint: Look for the tool_calls check)

### 3. The Diagram
Sketch the flow you observed. Compare it with the flow description in [Tool Calling Architecture](../../tutorial-1/concepts/tool-calling-architecture.md).

## Checkpoint
*   [ ] I can explain why the agent loops twice for one question.

