# Python Package Structure Guide

**Page 14 of 16** | [← Previous: Agentic Code Practices](./agentic-practices.md) | [Next: Lab 1 →](../../lab-1/README.md) | [↑ Reading Guide](../READING_GUIDE.md)

---

## The Python Philosophy: Explicit is Better Than Implicit

Python's package system is built on a simple principle from the Zen of Python:

> **Explicit is better than implicit.**

This guide explains how to structure Python packages properly for agentic AI development.

---

## What is a Python Package?

A **package** is a directory containing Python modules (`.py` files) AND an `__init__.py` file.

```
my_package/
├── __init__.py      ← Makes this a package
├── module1.py
└── module2.py
```

Without `__init__.py`, Python 3.3+ treats it as a **namespace package**, but this is implicit and not recommended for explicit packages.

---

## Our Project Structure

```
src/
├── __init__.py                    ← Makes src a package
├── agent/
│   ├── __init__.py                ← Makes agent a package
│   ├── agent_config.py
│   ├── simple_agent.py
│   ├── tool_registry.py
│   ├── mcp_tool_bridge.py
│   └── tools/
│       ├── __init__.py            ← Makes tools a package
│       └── file_search.py
├── config/
└── tools/                         ← TypeScript MCP tools (separate)
```

---

## Why `__init__.py` Matters

### 1. Explicit Package Boundaries
```python
# ✅ With __init__.py - clear package structure
from src.agent import Agent

# ❌ Without __init__.py - implicit namespace (works but unclear)
from src.agent.simple_agent import Agent
```

### 2. Package-Level Exports
The `__init__.py` file controls what gets exported:

```python
# src/agent/__init__.py
from .simple_agent import Agent
from .tool_registry import registry

__all__ = ['Agent', 'registry']
```

Now users can import cleanly:
```python
from src.agent import Agent, registry  # Clean!
```

Instead of:
```python
from src.agent.simple_agent import Agent  # Exposes internal structure
from src.agent.tool_registry import registry
```

### 3. Better IDE Support
IDEs use `__init__.py` to understand package structure:
- ✅ Autocomplete works better
- ✅ Import suggestions are cleaner
- ✅ Refactoring tools work correctly

### 4. Package Documentation
```python
"""
Agent implementation for Lesson 1 - Fundamentals.

This module implements a local tool-calling agent using:
- Ollama (local LLM inference)
- Tool Registry pattern for extensibility
- MCP (Model Context Protocol) bridge for TypeScript tools
"""
```

---

## Side-Effect Imports

Sometimes you import modules for their **side effects** (not to use them directly):

```python
# src/agent/simple_agent.py
from .tools import file_search  # noqa: F401
```

**Why?**
- The import triggers `@registry.register` decorator
- The tool gets registered when the module loads
- We don't directly reference `file_search` in the code

**The `# noqa: F401` comment**:
- Tells linters to ignore "unused import" warnings
- Documents that this is intentional
- Common pattern in Python for side-effect imports

---

## Best Practices for Agentic AI Projects

### 1. Every Package Has `__init__.py`
Even if it's minimal:
```python
"""Package docstring."""
```

### 2. Use Relative Imports Within Packages
```python
# ✅ Good - relative import
from .tool_registry import registry

# ❌ Avoid - absolute import (couples to project structure)
from src.agent.tool_registry import registry
```

### 3. Export Public API in `__init__.py`
```python
from .simple_agent import Agent
from .tool_registry import registry

__all__ = ['Agent', 'registry']
```

### 4. Document Side-Effect Imports
```python
from .tools import file_search  # noqa: F401 - registers tool via decorator
```

---

## Common Pitfalls

### Pitfall 1: Circular Imports
```python
# module_a.py
from .module_b import something  # ❌ Circular!

# module_b.py
from .module_a import something_else  # ❌ Circular!
```

**Solution**: Restructure or use late imports (inside functions).

### Pitfall 2: Forgetting `__init__.py` in Tool Directories
```python
# ❌ Tools won't be importable
src/agent/tools/
└── file_search.py

# ✅ Tools are properly packaged
src/agent/tools/
├── __init__.py
└── file_search.py
```

### Pitfall 3: Over-Exporting in `__init__.py`
```python
# ❌ Don't export everything
from .internal_helper import helper1, helper2, helper3

# ✅ Only export public API
from .simple_agent import Agent
__all__ = ['Agent']
```

---

## Testing Package Structure

Verify your package structure works:

```bash
# From project root
python -c "from src.agent import Agent; print('✅ Import works!')"
python -c "from src.agent import registry; print('✅ Registry accessible!')"
```

---

## Summary

| Principle | Why It Matters |
|-----------|----------------|
| **Explicit `__init__.py`** | Clear package boundaries, better tooling |
| **Package-level exports** | Clean public API, hide implementation details |
| **Relative imports** | Refactoring-friendly, decoupled from project structure |
| **Document side-effects** | `# noqa: F401` for decorator registration imports |

Following these practices makes your agentic AI codebase:
- ✅ More maintainable
- ✅ Better for AI-assisted development
- ✅ Easier to understand and extend

---

**Page 14 of 16** | [← Previous: Agentic Code Practices](./agentic-practices.md) | [Next: Lab 1 →](../../lab-1/README.md) | [↑ Reading Guide](../READING_GUIDE.md)

