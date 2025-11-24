# Tool Bridge: Connecting Tutorial 1 Tools to Tutorial 2 Agents

**Page 2.5 of 9** | [← Previous: Agent Specialization](./agent-specialization.md) | [Next: Agent Communication →](./agent-communication.md) | [↑ Reading Guide](../READING_GUIDE.md)

> **🎯 Why This Matters**
> 
> You built tools in Tutorial 1 and agents in Tutorial 2. But how do they connect?
> - ResearchAgent needs `search_files` - where does it come from?
> - How does `allowed_tools` actually filter the registry?
> - Why does `allowed_tools=["file_search"]` result in zero tools?
> 
> **The tool bridge is the connection layer** between Tutorial 1's tool registry and Tutorial 2's specialized agents. Understanding it prevents the #1 debugging issue in multi-agent systems: tool name mismatches.

> **🏗️ Building on Tutorial 1**
> 
> In Tutorial 1, you created tools using `@registry.register` decorator. All tools went into a global registry.
> 
> **Tutorial 2 doesn't create new tools - it filters existing ones:**
> - Tools still registered in Tutorial 1's registry (`src/agent/tool_registry.py`)
> - `WorkerAgent` adds `allowed_tools` parameter to filter the registry
> - Each specialized agent gets only the tools it needs
> - Same tool calling loop, just with filtered tool list
> 
> **The insight:** Multi-agent systems reuse single-agent infrastructure, not reimplement it.

## How the Tool Bridge Works

### The Architecture

```mermaid
graph TB
    subgraph "Tutorial 1: Tool Registration"
        T1[search_files in file_search.py]
        T2[read_file in read_file.py]
        T3[calculate in simple_agent.py]
        T4[get_weather in simple_agent.py]
        T5[list_directory in mcp_tool_bridge.py]
        
        T1 -->|@registry.register| REG[Global Tool Registry]
        T2 -->|@registry.register| REG
        T3 -->|@registry.register| REG
        T4 -->|@registry.register| REG
        T5 -->|@registry.register| REG
    end
    
    subgraph "Tutorial 2: Tool Filtering"
        REG -->|All tools| WB[WorkerAgent Base Class]
        WB -->|allowed_tools filter| RA[ResearchAgent]
        WB -->|allowed_tools filter| DA[DataAgent]
        WB -->|allowed_tools filter| WA[WriterAgent]
        
        RA -->|search_files, read_file| R_TOOLS[2 tools available]
        DA -->|calculate| D_TOOLS[1 tool available]
        WA -->|empty list| W_TOOLS[0 tools, LLM-only]
    end
    
    style REG fill:#4a90e2,stroke:#2e5c8a,color:#fff
    style WB fill:#50c878,stroke:#2d7a4a,color:#fff
    style RA fill:#f39c12,stroke:#a6680a,color:#fff
    style DA fill:#f39c12,stroke:#a6680a,color:#fff
    style WA fill:#f39c12,stroke:#a6680a,color:#fff
    
    classDef toolNode fill:#e8f4f8,stroke:#4a90e2,color:#000
    class T1,T2,T3,T4,T5 toolNode
```

### Step-by-Step: How a Tool Gets to an Agent

**1. Tool Registration (Tutorial 1)**

```python
# src/agent/tools/file_search.py
from src.agent.tool_registry import registry

@registry.register
def search_files(directory: str, pattern: str) -> str:
    """
    Search for files matching a pattern in a directory.
    
    Args:
        directory: The path to search in (e.g., "src/", "tests/")
        pattern: The file pattern to match (e.g., "*.py", "test_*.py")
    
    Returns:
        A string describing the results
    """
    # Implementation
    ...
```

**Key point:** The function name `search_files` becomes the tool name in the registry.

**2. Tool Available to All Agents (Tutorial 1)**

```python
# src/agent/simple_agent.py
class Agent:
    def chat(self, user_message: str) -> str:
        # Gets ALL tools from registry
        tools = registry.get_schemas()  # All 5 tools
        
        response = ollama.chat(
            model=config.model_name,
            messages=self.messages,
            tools=tools  # LLM sees all tools
        )
```

**3. Tool Filtering (Tutorial 2)**

```python
# src/multi_agent/worker_base.py
class WorkerAgent(Agent):
    def __init__(self, name: str, shared_state: SharedState, allowed_tools: List[str]):
        super().__init__()  # Inherits from Tutorial 1's Agent
        self.name = name
        self.shared_state = shared_state
        self.allowed_tools = allowed_tools
        
        # FILTER: Only keep tools in allowed_tools list
        all_schemas = registry.get_schemas()
        self.available_tools = [
            schema for schema in all_schemas
            if schema['function']['name'] in allowed_tools
        ]
```

**4. Specialized Agent Uses Filtered Tools**

```python
# src/multi_agent/specialized/research_agent.py
class ResearchAgent(WorkerAgent):
    def __init__(self, shared_state: SharedState):
        super().__init__(
            name="research",
            shared_state=shared_state,
            allowed_tools=["search_files", "read_file"]  # Only these 2
        )
        # Now self.available_tools has only 2 schemas, not 5
```

**5. LLM Sees Only Filtered Tools**

```python
# When ResearchAgent calls self.chat()
response = ollama.chat(
    model=config.model_name,
    messages=self.messages,
    tools=self.available_tools  # Only search_files and read_file
)
```

## Tutorial 1 Tool Reference

### Complete Tool Inventory

| Tool Name | Registered In | Function Signature | Purpose | Tutorial 2 Usage |
|-----------|--------------|-------------------|---------|-----------------|
| `search_files` | `src/agent/tools/file_search.py` | `search_files(directory: str, pattern: str) -> str` | Search for files matching glob patterns in a directory | ResearchAgent |
| `read_file` | `src/agent/tools/read_file.py` | `read_file(filename: str) -> str` | Read and return the contents of a text file (max 10MB) | ResearchAgent |
| `calculate` | `src/agent/simple_agent.py` | `calculate(operation: str, a: float, b: float) -> float` | Perform basic arithmetic (add, subtract, multiply, divide) | DataAgent |
| `get_weather` | `src/agent/simple_agent.py` | `get_weather(city: str) -> str` | Mock weather API (returns fake data for demo) | (Not used) |
| `list_directory` | `src/agent/mcp_tool_bridge.py` | `list_directory(dir_path: str = ".") -> str` | List contents of a directory via MCP bridge | (Available but unused) |

### Validation Commands

**Check all registered tools:**
```bash
python -c "from src.agent.tool_registry import registry; print([t['function']['name'] for t in registry.get_schemas()])"
```

Expected output:
```
['calculate', 'get_weather', 'read_file', 'list_directory', 'search_files']
```

**Verify a specific tool exists:**
```python
from src.agent.tool_registry import registry

tool = registry.get_tool("search_files")
if tool:
    print("✓ search_files is registered")
else:
    print("✗ search_files NOT found - check spelling!")
```

**Inspect a tool's schema:**
```python
from src.agent.tool_registry import registry

schemas = registry.get_schemas()
for schema in schemas:
    if schema['function']['name'] == 'search_files':
        print(schema)
        # Shows: name, description, parameters
```

## Agent Tool Assignments

### ResearchAgent
```python
allowed_tools=["search_files", "read_file"]
```

**Purpose:**
- `search_files`: Find files in the project matching patterns
- `read_file`: Extract content from discovered files

**Example workflow:**
1. User asks: "What testing frameworks are used?"
2. Agent calls `search_files("tests/", "*.py")` → finds test files
3. Agent calls `read_file("tests/conftest.py")` → reads imports
4. Agent extracts "pytest" from imports
5. Returns findings with source citations

### DataAgent
```python
allowed_tools=["calculate"]
```

**Purpose:**
- `calculate`: Perform arithmetic on data from research findings

**Example workflow:**
1. Research found: "2022: 5 million units, 2023: 8 million units"
2. Agent calls `calculate("subtract", 8, 5)` → 3
3. Agent calls `calculate("divide", 3, 5)` → 0.6
4. Agent returns: "60% growth year-over-year"

### WriterAgent
```python
allowed_tools=[]  # Empty list - LLM only
```

**Purpose:**
- Pure text generation, no external tool calls needed
- Uses LLM's native capabilities for markdown formatting

**Why no tools?**
- Writing is a generative task, not a retrieval/computation task
- LLM already knows markdown syntax
- Keeps writer focused on synthesis, not data gathering

## Common Issues and Solutions

### Issue 1: Tool Name Mismatch

**Symptom:**
```python
research = ResearchAgent(shared_state)
print(len(research.available_tools))  # Prints 0 (expected 2)
```

**Cause:** Tool name in `allowed_tools` doesn't match registered name.

**Example:**
```python
# WRONG: Tool is registered as "search_files", not "file_search"
allowed_tools=["file_search", "read_file"]  # ❌ Typo!
```

**Solution:**
```python
# CORRECT: Match the function name exactly
allowed_tools=["search_files", "read_file"]  # ✅ Matches @registry.register def search_files(...)
```

**How to debug:**
```python
from src.agent.tool_registry import registry

# Check what you're asking for
requested = ["file_search", "read_file"]

# Check what's actually available
available = [t['function']['name'] for t in registry.get_schemas()]

# Find mismatches
for tool_name in requested:
    if tool_name not in available:
        print(f"❌ '{tool_name}' not in registry!")
        print(f"   Did you mean: {[t for t in available if 'file' in t.lower()]}")
```

Output:
```
❌ 'file_search' not in registry!
   Did you mean: ['search_files', 'read_file']
```

### Issue 2: Tool Not Registered

**Symptom:**
```python
allowed_tools=["web_search"]  # Doesn't exist yet
# Agent has zero tools
```

**Cause:** Tool hasn't been created in Tutorial 1 yet.

**Solution:** Add the tool to Tutorial 1 first:

```python
# src/agent/tools/web_search.py (new file)
from src.agent.tool_registry import registry

@registry.register
def web_search(query: str) -> str:
    """Search the web for information."""
    # Implementation
    ...

# THEN import it in simple_agent.py
from .tools import web_search  # noqa: F401
```

### Issue 3: Agent Has All Tools (Filter Not Working)

**Symptom:**
```python
research = ResearchAgent(shared_state)
print(len(research.available_tools))  # Prints 5 (expected 2)
```

**Cause:** `WorkerAgent` not properly filtering tools.

**Solution:** Check `worker_base.py` implementation:

```python
class WorkerAgent(Agent):
    def __init__(self, name, shared_state, allowed_tools):
        super().__init__()
        self.allowed_tools = allowed_tools
        
        # MUST filter tools here
        all_schemas = registry.get_schemas()
        self.available_tools = [
            schema for schema in all_schemas
            if schema['function']['name'] in allowed_tools
        ]
        
        # DON'T forget to override chat() to use self.available_tools!
```

### Issue 4: Forgot to Import Tool File

**Symptom:**
```python
# Tool file exists: src/agent/tools/file_search.py
# But registry doesn't see it
```

**Cause:** Tool file not imported in `simple_agent.py`.

**Solution:**
```python
# src/agent/simple_agent.py
from . import mcp_tool_bridge  # noqa: F401
from .tools import file_search  # noqa: F401  <-- MUST import
from .tools import read_file   # noqa: F401  <-- MUST import
```

**Why?** Python doesn't execute decorators until the module is imported. The `@registry.register` decorator only runs when you import the file.

## Best Practices

### 1. Verify Tool Names Before Using

**Before implementing an agent:**
```bash
# List all available tools
python -c "from src.agent.tool_registry import registry; [print(t['function']['name']) for t in registry.get_schemas()]"
```

**Copy exact names into allowed_tools:**
```python
# Don't guess - copy from the output above
allowed_tools=["search_files", "read_file"]  # ✅ Verified
```

### 2. Add Tool Validation in __init__

```python
class ResearchAgent(WorkerAgent):
    def __init__(self, shared_state: SharedState):
        super().__init__(
            name="research",
            shared_state=shared_state,
            allowed_tools=["search_files", "read_file"]
        )
        
        # OPTIONAL: Validate tools are available (helpful for debugging)
        if len(self.available_tools) == 0:
            raise ValueError(
                f"ResearchAgent has no tools! "
                f"Check that allowed_tools={self.allowed_tools} "
                f"match registry names."
            )
```

### 3. Document Tool Dependencies

```python
class ResearchAgent(WorkerAgent):
    """
    Research specialist agent for information gathering.
    
    Required Tools (from Tutorial 1):
    - search_files: src/agent/tools/file_search.py
    - read_file: src/agent/tools/read_file.py
    
    Verify tools exist:
        python -c "from src.agent.tool_registry import registry; assert registry.get_tool('search_files')"
    """
```

### 4. Use Type Hints for Tool Names

```python
from typing import List, Literal

ToolName = Literal["search_files", "read_file", "calculate", "get_weather", "list_directory"]

class WorkerAgent(Agent):
    def __init__(self, name: str, shared_state: SharedState, allowed_tools: List[ToolName]):
        # Type checker will catch typos!
        ...
```

## Adding New Tools for Tutorial 2

If you need a tool that doesn't exist yet:

**Step 1: Add to Tutorial 1's tool registry**
```python
# src/agent/tools/sentiment_analysis.py (new file)
from src.agent.tool_registry import registry

@registry.register
def analyze_sentiment(text: str) -> str:
    """
    Analyze the sentiment of text.
    
    Args:
        text: Text to analyze
    
    Returns:
        Sentiment: "positive", "negative", or "neutral"
    """
    # Implementation
    return "positive"
```

**Step 2: Import in simple_agent.py**
```python
# src/agent/simple_agent.py
from .tools import sentiment_analysis  # noqa: F401
```

**Step 3: Use in Tutorial 2 agent**
```python
class SentimentAgent(WorkerAgent):
    def __init__(self, shared_state):
        super().__init__(
            name="sentiment",
            shared_state=shared_state,
            allowed_tools=["analyze_sentiment"]  # Now available!
        )
```

**Step 4: Verify**
```bash
python -c "from src.agent.tool_registry import registry; print('analyze_sentiment' in [t['function']['name'] for t in registry.get_schemas()])"
# Should print: True
```

## Quick Reference Card

### Tool Name Cheat Sheet
```
✅ search_files    (NOT file_search)
✅ read_file       (correct)
✅ calculate       (correct)
✅ get_weather     (correct)
✅ list_directory  (correct)
```

### Debug Checklist
- [ ] Tool file exists in `src/agent/tools/`
- [ ] Tool has `@registry.register` decorator
- [ ] Tool file imported in `simple_agent.py`
- [ ] Tool name in `allowed_tools` matches function name exactly
- [ ] `WorkerAgent.__init__()` filters tools correctly
- [ ] Agent's `available_tools` list is not empty

### Validation One-Liner
```bash
python -c "from src.agent.tool_registry import registry; from src.multi_agent.specialized import ResearchAgent; from src.multi_agent import SharedState; r = ResearchAgent(SharedState()); print(f'ResearchAgent has {len(r.available_tools)} tools:', [t['function']['name'] for t in r.available_tools])"
```

Expected output:
```
ResearchAgent has 2 tools: ['search_files', 'read_file']
```

---

**Next Steps:**
- **Understand:** [Agent Communication](./agent-communication.md) - How agents send messages
- **Practice:** [Lab 2 Exercise 2](../../lab-2/exercises/02-specialized-agents.md) - Build specialized agents
- **Debug:** [Troubleshooting Guide](../../lab-2/troubleshooting.md) - Tool name mismatches

**Related Concepts:**
- [Agent Specialization](./agent-specialization.md) - Why and how to specialize agents
- [Tutorial 1: Tool Calling](../../../lesson-1-fundamentals/tutorial-1/concepts/tool-calling-architecture.md) - Foundation of tool system

---

**Navigation:** [← Previous: Agent Specialization](./agent-specialization.md) | [Next: Agent Communication →](./agent-communication.md) | [↑ Reading Guide](../READING_GUIDE.md)

