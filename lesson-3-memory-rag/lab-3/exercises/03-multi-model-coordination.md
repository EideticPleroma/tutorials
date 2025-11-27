# Exercise 3: Multi-Model Coordination

**Duration**: ~90 minutes | **Difficulty**: Intermediate

## Objective

Set up DeepSeek-Coder and create a model router that directs tasks to the appropriate model (Llama for planning, DeepSeek for coding).

## Context

Different models excel at different tasks:
- **Llama 3.1**: General reasoning, planning, validation
- **DeepSeek-Coder**: Code generation, implementation

We'll build a system that uses both:
```
User Request
    ↓
Model Router ─┬─→ Llama (planning/reasoning)
              └─→ DeepSeek (code generation)
```

## Prerequisites

- [ ] Complete [Exercise 2: Embedding the Project](./02-embedding-the-project.md)
- [ ] Read [Multi-Model Orchestration](../../tutorial-3/concepts/multi-model-orchestration.md)
- [ ] Read [Architect-Builder Pattern](../../tutorial-3/architecture/architect-builder-pattern.md)

## Code Scaffold

You'll create these files:
```
src/memory_rag/
├── config.py              # Update with DeepSeek config
├── model_router.py        # NEW: Route to appropriate model
├── architect_agent.py     # NEW: Planning agent (Llama)
└── builder_agent.py       # NEW: Implementation agent (DeepSeek)
```

## Tasks

### Task 1: Install and Configure DeepSeek-Coder

Set up DeepSeek-Coder in Ollama.

**Install the model:**
```bash
# Pull DeepSeek-Coder (6.7B parameters, ~4GB download)
ollama pull deepseek-coder:6.7b

# Verify it's available
ollama list
# Should show:
# llama3.1:8b
# deepseek-coder:6.7b

# Quick test
ollama run deepseek-coder:6.7b "Write a Python function to reverse a string"
```

**Update `src/memory_rag/config.py`:**

**AI Assistant Prompt:**
```
@.cursorrules @src/memory_rag/config.py

Update the config module to support multiple models:

1. Add constants:
   ARCHITECT_MODEL = "llama3.1:8b"
   BUILDER_MODEL = "deepseek-coder:6.7b"

2. Add functions:
   def get_architect_llm() -> Ollama:
       """Get LLM configured for planning/reasoning tasks."""
       # Temperature 0.1 for consistent planning
       
   def get_builder_llm() -> Ollama:
       """Get LLM configured for code generation tasks."""
       # Temperature 0.2 for slightly more creative code

3. Keep existing configure() and configure_for_project() functions.
```

**Validation:**
```python
from src.memory_rag.config import get_architect_llm, get_builder_llm

architect = get_architect_llm()
builder = get_builder_llm()

print(f"Architect model: {architect.model}")
print(f"Builder model: {builder.model}")

# Quick test
print("\nArchitect response:")
print(architect.complete("Explain what a function does in one sentence."))

print("\nBuilder response:")
print(builder.complete("Write a Python function that adds two numbers."))
```

### Task 2: Create Model Router

Build a router that directs requests to the appropriate model.

**Create file:** `src/memory_rag/model_router.py`

**Requirements:**
- `ModelRouter` class that decides which model to use
- `route(task_type: str) -> Ollama`: Return appropriate LLM
- `classify_task(request: str) -> str`: Classify task type from natural language

**Task types:**
- `planning`: Break down requirements, create task lists → Llama
- `coding`: Write code, implement features → DeepSeek
- `reasoning`: Explain, analyze, validate → Llama
- `unknown`: Default to Llama

**AI Assistant Prompt:**
```
@.cursorrules @src/memory_rag/model_router.py @src/memory_rag/config.py

Create a ModelRouter class:

class ModelRouter:
    """Routes tasks to appropriate models."""
    
    # Task type to model mapping
    TASK_MODELS = {
        "planning": "architect",    # Llama
        "coding": "builder",        # DeepSeek
        "reasoning": "architect",   # Llama
        "explaining": "architect",  # Llama
        "implementing": "builder",  # DeepSeek
        "testing": "builder",       # DeepSeek (test code is code)
        "unknown": "architect",     # Default to Llama
    }
    
    def __init__(self):
        self.architect_llm = get_architect_llm()
        self.builder_llm = get_builder_llm()
    
    def route(self, task_type: str) -> Ollama:
        """Get the appropriate LLM for a task type."""
        # TODO: Return architect or builder based on task_type
    
    def classify_task(self, request: str) -> str:
        """Classify a natural language request into task type."""
        # TODO: Use simple keyword matching or LLM classification
        # Keywords for coding: "implement", "write", "code", "create function"
        # Keywords for planning: "plan", "break down", "design", "analyze"
    
    def process(self, request: str) -> str:
        """Classify and route a request, return response."""
        task_type = self.classify_task(request)
        llm = self.route(task_type)
        return llm.complete(request)

Include logging to show which model is handling each request.
```

**Validation:**
```python
from src.memory_rag.model_router import ModelRouter

router = ModelRouter()

# Test routing
print("Testing task classification...")

tests = [
    ("Explain how RAG works", "reasoning"),
    ("Write a function to parse JSON", "coding"),
    ("Break down this feature into tasks", "planning"),
    ("Implement error handling", "coding"),
]

for request, expected in tests:
    task_type = router.classify_task(request)
    print(f"'{request[:40]}...' -> {task_type} (expected: {expected})")
```

### Task 3: Implement Architect Agent

Create the Architect agent that plans and validates.

**Create file:** `src/memory_rag/architect_agent.py`

**Requirements:**
- Uses Llama 3.1 for reasoning
- Has access to RAG for context
- `plan(request: str) -> list[dict]`: Break down into tasks
- `validate(task: dict, code: str) -> dict`: Check implementation

**AI Assistant Prompt:**
```
@.cursorrules @src/memory_rag/architect_agent.py @src/memory_rag/rag_engine.py

Create the ArchitectAgent class:

class ArchitectAgent:
    """
    Architect agent that plans code changes using Llama 3.1.
    
    Responsibilities:
    - Understand user requirements
    - Query RAG for existing patterns
    - Create detailed task plans
    - Validate implementations
    """
    
    SYSTEM_PROMPT = '''You are an Architect agent that plans code changes.
    
    When planning:
    1. Understand what the user wants
    2. Search for existing patterns (you have search_codebase tool)
    3. Break down into specific, implementable tasks
    4. Each task should have: description, file to modify, specification
    
    Output plans as JSON:
    {"tasks": [{"id": 1, "description": "...", "file": "...", "spec": "..."}]}
    '''
    
    def __init__(self, rag_engine: RAGEngine):
        self.llm = get_architect_llm()
        self.rag_engine = rag_engine
    
    def plan(self, request: str) -> list[dict]:
        """Create a task plan from user request."""
        # 1. Query RAG for context
        context = self.rag_engine.retrieve(request, top_k=5)
        
        # 2. Generate plan
        prompt = f"""
        {self.SYSTEM_PROMPT}
        
        Context from codebase:
        {self._format_context(context)}
        
        User request: {request}
        
        Create a detailed task plan:
        """
        
        response = self.llm.complete(prompt)
        return self._parse_plan(response)
    
    def validate(self, task: dict, code: str) -> dict:
        """Validate that code meets task requirements."""
        prompt = f"""
        Task: {task['description']}
        Specification: {task.get('spec', 'N/A')}
        
        Implementation:
        ```python
        {code}
        ```
        
        Does this implementation meet the requirements?
        Respond with JSON: {{"approved": true/false, "feedback": "..."}}
        """
        
        response = self.llm.complete(prompt)
        return self._parse_validation(response)

Include helper methods for formatting and parsing.
Add comprehensive logging.
```

### Task 4: Implement Builder Agent

Create the Builder agent that implements code.

**Create file:** `src/memory_rag/builder_agent.py`

**Requirements:**
- Uses DeepSeek-Coder for code generation
- Has access to RAG for examples
- `implement(task: dict) -> dict`: Generate code for a task
- Follow codebase conventions (type hints, docstrings)

**AI Assistant Prompt:**
```
@.cursorrules @src/memory_rag/builder_agent.py @src/memory_rag/rag_engine.py

Create the BuilderAgent class:

class BuilderAgent:
    """
    Builder agent that implements code using DeepSeek-Coder.
    
    Responsibilities:
    - Receive task specifications from Architect
    - Query RAG for code examples
    - Generate clean, well-documented code
    - Follow codebase conventions
    """
    
    SYSTEM_PROMPT = '''You are a Builder agent that implements code.
    
    Code standards for this project:
    - Type hints on all functions
    - Google-style docstrings
    - Logging with lazy % formatting (logger.info("msg %s", var))
    - Follow patterns from the codebase
    
    Output only the code, no explanations.
    '''
    
    def __init__(self, rag_engine: RAGEngine):
        self.llm = get_builder_llm()
        self.rag_engine = rag_engine
    
    def implement(self, task: dict) -> dict:
        """Implement a task according to specification."""
        # 1. Get code examples from RAG
        examples = self.rag_engine.retrieve(
            f"code example: {task['spec']}",
            top_k=3
        )
        
        # 2. Generate implementation
        prompt = f"""
        {self.SYSTEM_PROMPT}
        
        Examples from codebase:
        {self._format_examples(examples)}
        
        Task: {task['description']}
        File: {task['file']}
        Specification: {task['spec']}
        
        Generate the implementation:
        """
        
        code = self.llm.complete(prompt)
        
        return {
            "task_id": task['id'],
            "status": "complete",
            "code": self._clean_code(code),
            "file": task['file'],
        }

Include helper methods for formatting examples and cleaning code output.
Add logging for each step.
```

### Task 5: Test Model Handoff

Verify that the Architect and Builder work together.

**Create test file:** `tests/memory_rag/test_multi_model.py`

**AI Assistant Prompt:**
```
@.cursorrules @tests/memory_rag/test_multi_model.py

Create tests for multi-model coordination:

1. test_router_classifies_correctly():
   - Test that coding requests go to DeepSeek
   - Test that planning requests go to Llama

2. test_architect_creates_plan():
   - Give Architect a simple request
   - Verify plan has expected structure (list of tasks with id, description, file)

3. test_builder_generates_code():
   - Give Builder a simple task
   - Verify output contains valid Python code

4. test_architect_validates_code():
   - Give Architect task + implementation
   - Verify validation result has approved and feedback

5. test_end_to_end_handoff():
   - User request -> Architect plan -> Builder implement -> Architect validate
   - Verify the full flow works

Use pytest fixtures for RAG engine, Architect, and Builder.
Mark slow tests with @pytest.mark.slow
```

**Run tests:**
```bash
python -m pytest tests/memory_rag/test_multi_model.py -v
```

## Validation Checkpoints

### Test Router Classification:
```python
router = ModelRouter()

# These should route to DeepSeek
assert router.classify_task("Write a function to sort a list") == "coding"
assert router.classify_task("Implement the delegate method") == "coding"

# These should route to Llama
assert router.classify_task("Explain how RAG works") == "reasoning"
assert router.classify_task("Break down this feature") == "planning"
```

### Test Architect Planning:
```python
architect = ArchitectAgent(rag_engine)
plan = architect.plan("Add a greeting tool to the agent")

assert isinstance(plan, list)
assert len(plan) >= 1
assert "description" in plan[0]
assert "file" in plan[0]
```

### Test Builder Implementation:
```python
builder = BuilderAgent(rag_engine)
task = {
    "id": 1,
    "description": "Add a greet function",
    "file": "src/agent/simple_agent.py",
    "spec": "Function that takes a name and returns greeting string"
}
result = builder.implement(task)

assert "def " in result["code"]  # Contains function definition
assert "greet" in result["code"].lower()  # Function name present
```

## Message Protocol Extensions

Update your message protocol to support the new message types:

```python
# src/multi_agent/message_protocol.py

class MessageType(Enum):
    # Existing
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"
    
    # New for Tutorial 3
    TASK_PLAN = "task_plan"
    CODE_RESULT = "code_result"
    TEST_RESULT = "test_result"
    VALIDATION = "validation"
```

## Checkpoint Questions

1. **Why use DeepSeek for coding instead of Llama?**
   <details>
   <summary>Answer</summary>
   DeepSeek-Coder is specifically trained on code, producing cleaner implementations with better syntax. Llama is better at reasoning but produces more verbose, explanation-heavy code.
   </details>

2. **How does the Architect use RAG differently than the Builder?**
   <details>
   <summary>Answer</summary>
   Architect queries for patterns and architecture ("How is X implemented?"). Builder queries for specific code examples ("Show me function that does X"). Different intents, same RAG system.
   </details>

3. **What happens if DeepSeek produces code that doesn't compile?**
   <details>
   <summary>Answer</summary>
   The Architect validates and provides feedback. The Builder can retry with the error context. This is the retry loop in the Architect-Builder pattern.
   </details>

## Common Issues

### Issue: "DeepSeek model not found"

**Solution:**
```bash
ollama pull deepseek-coder:6.7b
ollama list  # Verify it's there
```

### Issue: "DeepSeek produces markdown-wrapped code"

**Solution:** Strip markdown fences in Builder:
```python
def _clean_code(self, code: str) -> str:
    """Remove markdown code fences."""
    code = code.strip()
    if code.startswith("```"):
        lines = code.split("\n")
        lines = lines[1:]  # Remove opening fence
        if lines[-1].startswith("```"):
            lines = lines[:-1]  # Remove closing fence
        code = "\n".join(lines)
    return code
```

### Issue: "Architect plan is not valid JSON"

**Solution:** Make JSON instruction more explicit:
```python
prompt += "\nRespond ONLY with valid JSON, no other text."
```

Or use structured output:
```python
import json

def _parse_plan(self, response: str) -> list[dict]:
    # Find JSON in response
    try:
        # Try to parse directly
        return json.loads(response)["tasks"]
    except:
        # Find JSON block in text
        start = response.find("[")
        end = response.rfind("]") + 1
        if start >= 0 and end > start:
            return json.loads(response[start:end])
    return []
```

## Next Steps

You have Architect and Builder working! Now let's put it all together.

👉 **Continue to [Exercise 4: Architect-Builder Workflow](./04-architect-builder-workflow.md)**

---

## 💡 Tips

**Test models individually:** Make sure each model responds correctly before testing coordination.

**Check model availability:** Ensure both models are pulled and Ollama is running.

**Use appropriate temperatures:** Low (0.1) for planning, slightly higher (0.2) for code.

**Log everything:** You'll need logs to debug multi-model issues.

