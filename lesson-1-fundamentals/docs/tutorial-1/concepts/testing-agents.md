# Testing Agents: Observe, Validate, Evaluate

**Page 6 of 15** | [← Previous: MCP Introduction](./mcp-intro.md) | [Next: Prompting Techniques →](../guides/prompting.md) | [↑ Reading Guide](../READING_GUIDE.md)

Testing AI agents is fundamentally different from testing traditional software. Agents are non-deterministic (probabilistic), meaning they might solve the same problem in different ways each time.

## The Challenge

*   **Traditional Unit Test**: `assert add(2, 2) == 4` (Binary: Pass/Fail)
*   **Agent Test**: `agent.ask("Summarize this text")` (Output varies every time)

## The Methodology: O.V.E.

To test agents effectively, we use the **Observe, Validate, Evaluate** loop.

### 1. Observe
Capture not just the final answer, but the *process*.
*   What tools were called?
*   What arguments were used?
*   How many steps did it take?
*   What was the "thought process" (if using Chain of Thought)?

### 2. Validate (Deterministic Checks)
Check the things that *must* be true.
*   **Structure**: Did it return valid JSON?
*   **Tool Usage**: If asked to calculate `2+2`, did it call the `calculator` tool?
*   **Safety**: Did it avoid forbidden topics?

### 3. Evaluate (Probabilistic Checks)
Score the quality of the response.
*   **LLM-as-a-Judge**: Use a stronger model (or the same model) to grade the output.
    *   "On a scale of 1-5, how concise is this summary?"
    *   "Does this answer directly address the user's question?"
*   **Semantic Similarity**: Compare the vector embedding of the output against a "gold standard" answer.

## Test Harness

In this tutorial, we will build a simple test harness that:
1.  Runs the agent against a set of scenarios.
2.  Records the trace (inputs, tool calls, outputs).
3.  Runs assertions (validations) on the trace.
4.  Can be extended to run evaluations.

