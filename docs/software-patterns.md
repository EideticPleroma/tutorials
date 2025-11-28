# Software Patterns in Agentic AI Tutorials

This appendix documents the design patterns, SOLID principles, and architectural patterns demonstrated throughout the tutorial series. Understanding these patterns helps you recognize reusable solutions and make better design decisions.

---

## Design Patterns

### Registry Pattern (Tutorial 1)

**Location:** `src/agent/tool_registry.py`

**What it is:** A global registry that tracks available tools. Tools register themselves, and consumers query the registry to discover what's available.

**Why it matters for agents:** Agents need to know what tools exist without hardcoding them. The registry allows dynamic tool discovery and extensibility.

**Code Example:**
```python
# Registration (in tool file)
from src.agent.tool_registry import registry

@registry.register
def search_files(directory: str, pattern: str) -> str:
    """Search for files matching a pattern."""
    # Implementation...

# Usage (in agent)
tools = registry.get_all_tools()  # Get all registered tools
schema = registry.get_schemas()    # Get JSON schemas for LLM
```

**Pattern Structure:**
```
┌─────────────────┐     registers     ┌──────────────┐
│  @registry.register  ───────────────>│   Registry   │
│  def my_tool()   │                   │  _tools: {}  │
└─────────────────┘                    └──────────────┘
                                              │
        ┌─────────────────────────────────────┘
        │ queries
        v
┌─────────────────┐
│     Agent       │
│  get_schemas()  │
└─────────────────┘
```

**When to use:**
- Plugin architectures where capabilities are added dynamically
- Decoupling registration from usage
- When consumers need to discover available services

**Real-world examples:**
- Flask route decorators (`@app.route`)
- pytest fixtures
- Django admin registration

---

### Strategy Pattern (Tutorial 2)

**Location:** Specialized agents (`src/multi_agent/specialized/`)

**What it is:** Define a family of algorithms (strategies), encapsulate each one, and make them interchangeable. The strategy can vary independently from clients using it.

**Why it matters for agents:** Different agents handle different types of tasks. The coordinator selects which "strategy" (agent) to use based on the task type.

**Code Example:**
```python
# Strategies (specialized agents)
class ResearchAgent(WorkerAgent):
    """Strategy for gathering information."""
    def execute(self, action, payload):
        # Research-specific logic
        
class DataAgent(WorkerAgent):
    """Strategy for data analysis."""
    def execute(self, action, payload):
        # Analysis-specific logic

# Context (coordinator selects strategy)
class Coordinator:
    def __init__(self):
        self.research = ResearchAgent()  # Strategy 1
        self.data = DataAgent()          # Strategy 2
        self.writer = WriterAgent()      # Strategy 3
    
    def handle_task(self, task_type, payload):
        if task_type == "research":
            return self.research.execute("gather", payload)
        elif task_type == "analyze":
            return self.data.execute("analyze", payload)
        # Coordinator selects appropriate strategy
```

**Pattern Structure:**
```
┌─────────────────┐
│   Coordinator   │──────────────────────────────────┐
│   (Context)     │                                  │
└────────┬────────┘                                  │
         │ selects strategy                          │
         v                                           v
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ ResearchAgent   │   │   DataAgent     │   │  WriterAgent    │
│  (Strategy 1)   │   │  (Strategy 2)   │   │  (Strategy 3)   │
└─────────────────┘   └─────────────────┘   └─────────────────┘
```

**When to use:**
- Multiple algorithms for the same task
- Need to switch behavior at runtime
- Want to isolate algorithm implementation details

---

### Template Method Pattern (Tutorial 2)

**Location:** `src/multi_agent/worker_base.py`

**What it is:** Define the skeleton of an algorithm in a base class, letting subclasses override specific steps without changing the structure.

**Why it matters for agents:** All workers follow the same basic flow (receive message, execute, return response), but each specialization implements execution differently.

**Code Example:**
```python
# Template (base class)
class WorkerAgent(Agent):
    """Base class with template method."""
    
    def execute_message(self, request: Message) -> Message:
        """Template method - defines the algorithm skeleton."""
        # Step 1: Validate (common)
        self._validate_request(request)
        
        # Step 2: Execute (subclass overrides)
        result = self.execute(request.action, request.payload)
        
        # Step 3: Create response (common)
        return request.create_response(result)
    
    def execute(self, action: str, payload: dict) -> dict:
        """Hook method - subclasses override."""
        raise NotImplementedError

# Concrete implementations
class ResearchAgent(WorkerAgent):
    def execute(self, action, payload):
        """Research-specific execution."""
        if action == "gather_info":
            return self.gather_info(payload["query"])
        
class DataAgent(WorkerAgent):
    def execute(self, action, payload):
        """Data-specific execution."""
        if action == "analyze_trends":
            return self.analyze_trends(payload["findings"])
```

**Pattern Structure:**
```
┌───────────────────────────────────┐
│         WorkerAgent               │
│  ─────────────────────────────    │
│  execute_message()  [template]    │
│    ├─ _validate_request()         │
│    ├─ execute()  [abstract hook]  │
│    └─ create_response()           │
└──────────────┬────────────────────┘
               │ extends
      ┌────────┴────────┐
      v                 v
┌────────────┐   ┌────────────┐
│ Research   │   │   Data     │
│  Agent     │   │   Agent    │
│ execute()  │   │ execute()  │
└────────────┘   └────────────┘
```

**When to use:**
- Common algorithm structure with varying implementations
- Want to enforce a sequence of steps
- Sharing code between similar classes

---

### Command Pattern (Tutorial 2)

**Location:** `src/multi_agent/message_protocol.py`

**What it is:** Encapsulate a request as an object, allowing you to parameterize, queue, log, and undo operations.

**Why it matters for agents:** The Message class encapsulates requests to agents. This enables logging, replay, and async processing.

**Code Example:**
```python
# Command (Message)
@dataclass
class Message:
    """Encapsulates a request as an object."""
    from_agent: str
    to_agent: str
    message_type: MessageType
    action: str
    payload: Dict[str, Any]
    message_id: str  # Enables tracking
    trace_id: str    # Enables correlation
    
    def to_json(self) -> str:
        """Serialize for logging/queuing."""
        return json.dumps(self.__dict__)

# Invoker (Coordinator)
class Coordinator:
    def delegate(self, agent, action, payload):
        # Create command (message)
        request = Message(
            from_agent="coordinator",
            to_agent=agent.name,
            action=action,
            payload=payload
        )
        
        # Log command
        logger.info("Command: %s", request.to_json())
        
        # Execute command
        response = agent.execute_message(request)
        return response

# Receiver (Worker)
class WorkerAgent:
    def execute_message(self, request: Message):
        # Process command
        result = self.execute(request.action, request.payload)
        return request.create_response(result)
```

**Benefits:**
- **Logging**: Every command is recorded
- **Replay**: Commands can be re-executed
- **Queuing**: Commands can be stored and processed later
- **Undo**: With additional state, commands can be reversed

**When to use:**
- Need to log/audit operations
- Want to support undo/redo
- Implementing job queues
- Decoupling sender from receiver

---

### Factory Pattern (Implicit, Tutorial 2)

**Location:** Coordinator initialization

**What it is:** Define an interface for creating objects, letting subclasses or configuration decide which class to instantiate.

**Why it matters for agents:** The coordinator creates worker agents. In production, you might create different agents based on configuration or context.

**Code Example:**
```python
# Simple factory in coordinator
class Coordinator:
    def __init__(self, config: Optional[dict] = None):
        config = config or {}
        
        # Factory logic - create appropriate agents
        if config.get("use_mock", False):
            self.research = MockResearchAgent()
            self.data = MockDataAgent()
        else:
            self.research = ResearchAgent(shared_state)
            self.data = DataAgent(shared_state)

# More explicit factory
class AgentFactory:
    @staticmethod
    def create_agent(agent_type: str, shared_state) -> WorkerAgent:
        if agent_type == "research":
            return ResearchAgent(shared_state)
        elif agent_type == "data":
            return DataAgent(shared_state)
        elif agent_type == "writer":
            return WriterAgent(shared_state)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")

# Usage
factory = AgentFactory()
research = factory.create_agent("research", shared_state)
```

**When to use:**
- Object creation logic is complex
- Need to switch implementations (mock vs. real)
- Want to centralize creation for consistency

---

## SOLID Principles Demonstrated

### Single Responsibility Principle (SRP)

**"A class should have only one reason to change."**

**Tutorial 1 Examples:**
- Each tool does ONE thing:
  - `search_files()`: Find files matching pattern
  - `read_file()`: Read file contents
  - `calculate()`: Perform calculations
- Tools don't overlap responsibilities

**Tutorial 2 Examples:**
- Each agent has ONE job:
  - **ResearchAgent**: Gather information (NOT analyze or write)
  - **DataAgent**: Analyze data (NOT gather or write)
  - **WriterAgent**: Create reports (NOT gather or analyze)
- **Coordinator**: Orchestrate (NOT execute tasks itself)

**Code Evidence:**
```python
# ResearchAgent system prompt enforces SRP
"""You are a Research Agent. Your ONLY job is gathering information.

What you DO:
- Search for files
- Extract facts
- Cite sources

What you DO NOT do:
- Analyze data (Data Agent does that)
- Write reports (Writer Agent does that)
"""
```

**Benefits:**
- Easier to test (one thing to verify)
- Easier to change (minimal impact)
- Clearer code (obvious purpose)

---

### Open/Closed Principle (OCP)

**"Software entities should be open for extension but closed for modification."**

**Tutorial 1 Examples:**
- Tool registry is open for extension (add new tools)
- Don't modify registry code to add tools
- Use `@registry.register` decorator

**Tutorial 2 Examples:**
- `WorkerAgent` base class is closed (don't modify it)
- Create new agent types by extending it (open for extension)
- Message protocol is extensible (add new message types)

**Code Evidence:**
```python
# Extension without modification
class CustomAgent(WorkerAgent):
    """Extend WorkerAgent, don't modify it."""
    
    def __init__(self, shared_state):
        super().__init__(
            name="custom",
            shared_state=shared_state,
            allowed_tools=["my_custom_tool"]
        )
    
    def execute(self, action, payload):
        # Custom behavior
        pass
```

**Benefits:**
- Add features without breaking existing code
- Stable core, flexible extensions
- Reduced regression risk

---

### Liskov Substitution Principle (LSP)

**"Subtypes must be substitutable for their base types."**

**Tutorial 2 Examples:**
- All workers inherit from `WorkerAgent`
- Coordinator treats all workers the same
- Any `WorkerAgent` subclass can be delegated to

**Code Evidence:**
```python
# Coordinator doesn't care which specific worker
def delegate(self, agent: WorkerAgent, action: str, payload: dict):
    """Works with ANY WorkerAgent subclass."""
    request = Message(...)
    response = agent.execute_message(request)  # Polymorphism
    return response.payload

# All these work identically:
coordinator.delegate(ResearchAgent(), "gather", {...})
coordinator.delegate(DataAgent(), "analyze", {...})
coordinator.delegate(WriterAgent(), "write", {...})
coordinator.delegate(CustomAgent(), "custom", {...})
```

**Benefits:**
- Polymorphic behavior
- Easy to add new agent types
- Coordinator code never changes

---

### Interface Segregation Principle (ISP)

**"Clients should not be forced to depend on interfaces they don't use."**

**Tutorial 2 Examples:**
- Tool filtering: Each agent only has tools it needs
- ResearchAgent: `["search_files", "read_file"]`
- DataAgent: `["calculate"]`
- WriterAgent: `[]` (no tools needed)

**Code Evidence:**
```python
class ResearchAgent(WorkerAgent):
    def __init__(self, shared_state):
        super().__init__(
            name="research",
            shared_state=shared_state,
            allowed_tools=["search_files", "read_file"]  # Only what it needs
        )
        # Agent doesn't have calculate tool - doesn't need it

class WriterAgent(WorkerAgent):
    def __init__(self, shared_state):
        super().__init__(
            name="writer",
            shared_state=shared_state,
            allowed_tools=[]  # No tools - LLM only
        )
```

**Benefits:**
- Agents aren't confused by irrelevant tools
- Clear boundaries
- Reduced coupling

---

### Dependency Inversion Principle (DIP)

**"Depend on abstractions, not concretions."**

**Tutorial 2 Examples:**
- Coordinator depends on `WorkerAgent` abstraction, not concrete agents
- Agents depend on `Message` protocol, not direct function signatures
- Shared state provides abstraction over storage

**Code Evidence:**
```python
# Coordinator depends on abstraction
class Coordinator:
    def __init__(self):
        # These could be any WorkerAgent implementation
        self.research: WorkerAgent = ResearchAgent(state)
        self.data: WorkerAgent = DataAgent(state)
    
    def delegate(self, agent: WorkerAgent, ...):  # Abstract type
        # Doesn't know or care about concrete type
        response = agent.execute_message(request)

# Easy to substitute for testing
coordinator = Coordinator()
coordinator.research = MockResearchAgent()  # Swap implementation
```

**Benefits:**
- Easy to mock for testing
- Swap implementations without changing code
- Loose coupling

---

## Architectural Patterns

### Coordinator-Worker Pattern

**Location:** Core architecture of Tutorial 2

**What it is:** A central coordinator receives requests, decomposes them into tasks, and delegates to specialized workers. Workers execute tasks and return results.

**Why it matters:** Separates orchestration logic from execution logic. Coordinator makes decisions; workers have capabilities.

**Structure:**
```
                    ┌──────────────────┐
                    │   User Request   │
                    └────────┬─────────┘
                             │
                             v
                    ┌──────────────────┐
                    │   Coordinator    │
                    │  (orchestrates)  │
                    └────────┬─────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          v                  v                  v
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │ Research │      │   Data   │      │  Writer  │
    │  Worker  │      │  Worker  │      │  Worker  │
    └──────────┘      └──────────┘      └──────────┘
```

**Responsibilities:**

| Coordinator | Workers |
|-------------|---------|
| Receives user requests | Execute specific tasks |
| Decomposes into subtasks | Have specialized tools |
| Selects which worker to call | Don't know about each other |
| Handles errors and retries | Return results |
| Aggregates results | Focus on one job |

**When to use:**
- Complex tasks requiring multiple capabilities
- Need clear separation of concerns
- Want to scale workers independently
- Need centralized error handling

---

### Message-Driven Architecture

**Location:** Message protocol in Tutorial 2

**What it is:** Components communicate through structured messages rather than direct method calls. Messages are self-describing and can be logged, queued, and replayed.

**Benefits:**
- **Traceability**: Follow requests through the system
- **Debugging**: Log all messages as JSON
- **Async potential**: Messages can be queued
- **Loose coupling**: Sender doesn't need to know receiver details

**Implementation:**
```python
# Instead of direct call:
result = agent.execute(action, payload)

# Use message:
request = Message(
    from_agent="coordinator",
    to_agent=agent.name,
    action=action,
    payload=payload,
    trace_id="trace-123"
)
response = agent.execute_message(request)
```

---

## Quick Reference

| Pattern | Tutorial | Location | Purpose |
|---------|----------|----------|---------|
| Registry | 1 | `tool_registry.py` | Dynamic tool discovery |
| Strategy | 2 | Specialized agents | Select algorithm at runtime |
| Template Method | 2 | `WorkerAgent` | Common structure, varying steps |
| Command | 2 | `Message` class | Encapsulate requests |
| Factory | 2 | Coordinator init | Create appropriate agents |
| Coordinator-Worker | 2 | Architecture | Orchestration + execution |
| Message-Driven | 2 | Message protocol | Structured communication |

| SOLID Principle | Where Demonstrated |
|-----------------|-------------------|
| Single Responsibility | One tool = one function; one agent = one job |
| Open/Closed | Extend WorkerAgent, don't modify |
| Liskov Substitution | Any WorkerAgent works with coordinator |
| Interface Segregation | Tool filtering per agent |
| Dependency Inversion | Depend on WorkerAgent, not concrete types |

---

## Further Reading

- **Design Patterns**: "Design Patterns: Elements of Reusable Object-Oriented Software" (Gang of Four)
- **SOLID**: "Clean Architecture" by Robert C. Martin
- **Multi-Agent Systems**: "Programming Multi-Agent Systems" by Bordini et al.
- **Message-Driven Architecture**: "Enterprise Integration Patterns" by Hohpe & Woolf

---

**Navigation:** [README](../README.md) | [Tutorial 1](../lesson-1-fundamentals/tutorial-1/READING_GUIDE.md) | [Tutorial 2](../lesson-2-multi-agent/tutorial-2/READING_GUIDE.md) | [Glossary](./glossary.md)

