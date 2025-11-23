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
Open `src/agent/simple_agent.py`. Find the `chat()` method (around lines 51-102).
*   Where does the `messages` list get initialized? (Hint: Look in the `__init__` method around line 46)
*   Where is the `tool_registry` queried? (Hint: Look for `registry.get_schemas()` and `registry.get_tool()`)
*   How does the agent decide to make a second LLM call? (Hint: Look for the tool_calls check)

### 3. The Diagram
Sketch the flow you observed. Compare it with the flow description in [Tool Calling Architecture](../../tutorial-1/concepts/tool-calling-architecture.md).

**Visual Reference - Tool Calling Flow:**

```mermaid
sequenceDiagram
    participant User
    participant Agent
    participant LLM
    participant Tool
    
    User->>Agent: "What is the weather in Paris?"
    Agent->>Agent: Add to messages[]
    Agent->>LLM: messages + tool schemas
    LLM->>Agent: Response with tool_call
    Agent->>Agent: Parse tool_call
    Agent->>Tool: get_weather("Paris")
    Tool->>Agent: "The weather in Paris is Sunny, 25°C"
    Agent->>Agent: Add tool result to messages[]
    Agent->>LLM: messages (now with tool result)
    LLM->>Agent: Final response with answer
    Agent->>User: "The weather in Paris is Sunny, 25°C"
    
    Note over Agent,LLM: First LLM call: Decision
    Note over Agent,LLM: Second LLM call: Synthesis
```

**Key Insight:** The agent makes **two LLM calls**:
1. First call: LLM decides to use a tool and outputs structured JSON
2. Second call: LLM synthesizes the tool output into a natural language response

## Checkpoint
*   [ ] I can explain why the agent loops twice for one question.
*   [ ] I understand the flow: User → Agent → LLM (decide) → Tool → LLM (synthesize) → User

---

## 💡 Stuck on This Exercise?

**Ask Your AI Assistant** (include `.cursorrules` for context):

```
@.cursorrules

I'm working on Exercise 1 (Understanding the Agent).

I'm having trouble [understanding the flow / finding the code / tracing execution].

Specifically: [describe what's confusing]

Can you explain this according to the project's architecture?
```

**Or debug with the tool:**
```bash
python scripts/debug_agent.py --test "What is the weather in Paris?"
```

**See also:**
- [Tool Calling Architecture](../../tutorial-1/concepts/tool-calling-architecture.md) - The 7-step loop explained
- [Getting Unstuck Guide](../getting-unstuck.md) - Systematic debugging
- [FAQ](../FAQ.md#why-does-my-agent-make-two-llm-calls-for-one-question) - Why two LLM calls?

