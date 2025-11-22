# Exercise 3: Prompt Engineering

**Goal**: Control the Agent's brain.

## Context
The system prompt in `src/agent/agent_config.py` is the Agent's operating system. It's defined as `config.system_prompt` (lines 8-10) and loaded by the Agent in its `__init__` method. We want to upgrade it to improve the agent's reasoning and tool usage.

## Learning by Asking

Before diving in, learn from AI! Use these prompts with your AI assistant (like Claude, GPT, etc.):

**Understanding Prompts:**
```
"What is a system prompt in an LLM-based agent? How does it differ from user messages?"
```

**Chain of Thought:**
```
"Explain Chain of Thought (CoT) prompting. Show me examples of prompts with and without CoT."
```

**Tool Calling Prompts:**
```
"I'm building an agent that can call tools. What should I include in the system prompt to make it:
1. Always use tools when appropriate
2. Include the tool's output in its response to the user
3. Handle errors gracefully"
```

**Few-Shot Learning:**
```
"What is few-shot prompting? Show me an example of a system prompt that includes examples for a file search agent."
```

## Steps

### 1. Analyze the Current Prompt

First, look at the current system prompt in `src/agent/agent_config.py`:

```python
system_prompt: str = """You are a helpful AI assistant with access to tools.
When answering questions, use the available tools when needed.
Provide clear and accurate responses."""
```

**What's missing?**
- No guidance on WHEN to use tools
- No instruction on HOW to use tool outputs
- No examples of good behavior
- No reasoning/thinking guidance

### 2. Improve the Prompt

Using what you learned from asking the AI, modify the prompt to improve:

**A. Tool Usage Clarity**
- When should the agent use tools vs. answer directly?
- Should it explain WHY it's using a tool?

**B. Output Quality**
- How should it incorporate tool results?
- Should it include specific data from tool outputs?

**C. Error Handling**
- What should happen if a tool fails?
- How should errors be communicated to users?

**Experiment!** Try different approaches:
1. Add explicit instructions: "When you need to X, use tool Y"
2. Add examples: "User: Find Python files. You: [calls search_files]..."
3. Add reasoning: "Think step-by-step before using tools"

### 3. Test Your Changes

After modifying `agent_config.py`, restart your agent:
```bash
python -m src.agent.simple_agent
```

Test with these queries:
1. "What tools are available?" (Should NOT call tools)
2. "Find Python files in tests/" (Should call search_files)
3. "What did you find?" (Tests if it remembers context)

### 4. Iterate

Prompt engineering is iterative. If the agent:
- **Doesn't use tools**: Make instructions more explicit
- **Uses wrong tools**: Add examples of correct usage
- **Ignores tool outputs**: Add "IMPORTANT: Include tool data in response"
- **Is too verbose**: Add "Be concise"

## AI-Assisted Learning

Ask your AI assistant to review your prompt:

```
"Here's my system prompt for a tool-calling agent:

[paste your prompt]

What could be improved? What best practices am I missing?"
```

Or get specific help:

```
"My agent keeps ignoring the output from file_search. How should I phrase the system prompt to make it use the actual data returned?"
```

## Reflection Questions

After completing this exercise:

1. **Compare Behaviors**: How did the agent's responses change with your new prompt?
2. **What Worked**: Which instructions had the biggest impact?
3. **What Didn't**: Which instructions did the model ignore?
4. **Learning**: What did asking AI teach you about prompt engineering?

## Success Criteria

Your improved prompt should make the agent:
- ✅ Use tools appropriately (not too much, not too little)
- ✅ Include specific data from tool outputs in responses
- ✅ Explain its reasoning (at least briefly)
- ✅ Handle errors gracefully

