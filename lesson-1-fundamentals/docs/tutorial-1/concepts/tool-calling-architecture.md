# Tool Calling Architecture

**Page 4 of 15** | [← Previous: LLM Fundamentals](./llm-fundamentals.md) | [Next: MCP Introduction →](./mcp-intro.md) | [↑ Reading Guide](../READING_GUIDE.md)

"Tool calling" (or function calling) is the capability that turns a chatbot into an agent. It allows the LLM to interact with the outside world.

## The Loop

Tool calling is not magic; it's a structured dialogue loop:

1.  **User Request**: "What is the weather in London?"
2.  **Schema Injection**: The system sends the prompt *plus* a list of available tools (function definitions) to the LLM.
    ```json
    [
      {
        "name": "get_weather",
        "description": "Get current weather",
        "parameters": { "type": "object", "properties": { "city": { "type": "string" } } }
      }
    ]
    ```
3.  **LLM Decision**: The LLM recognizes it cannot answer from training data but *can* answer using a tool.
4.  **Structured Output**: Instead of text, the LLM outputs a specific JSON structure requesting a tool execution:
    ```json
    { "tool": "get_weather", "args": { "city": "London" } }
    ```
5.  **System Execution**: Your code intercepts this JSON, pauses the LLM, executes the actual Python/JS function, and gets the result ("15°C, Cloudy").
6.  **Feedback**: The system feeds the result back to the LLM as a new message.
7.  **Final Response**: The LLM uses the tool output to answer the user: "The weather in London is currently 15°C and cloudy."

## Why is this "Agentic"?

*   **Reasoning**: The model *decided* to use a tool.
*   **Multi-step**: The model can call tool A, get a result, realize it needs tool B, and continue until the task is done.
*   **Action**: The model is not just observing; it is acting (reading files, making API calls).

## Challenges

*   **Hallucination**: The model might try to call a tool that doesn't exist or invent parameters.
*   **Loops**: The model might get stuck calling the same tool repeatedly.
*   **Error Handling**: If a tool fails, the agent needs to know how to recover (e.g., try a different search query).

