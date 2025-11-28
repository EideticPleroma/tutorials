# Exercise 4: The Complete Architect-Builder Workflow

| Duration | Difficulty | Prerequisites | Skills Practiced |
|----------|------------|---------------|------------------|
| ~120 min | Advanced | Exercise 3 complete | Architect-Builder pattern, O.V.E. for RAG, End-to-end workflows |

**Challenge Exercise**

## Objective

Build the complete Architect-Builder workflow where Llama plans, DeepSeek implements, and O.V.E. validates - creating a coding assistant for this project.

## Context

This is where everything comes together:
- **RAG** provides codebase knowledge
- **Architect (Llama)** plans changes using that knowledge
- **Builder (DeepSeek)** implements according to plan
- **O.V.E. Harness** validates the implementation
- **Iteration loop** handles failures

**The Complete Flow:**
```
User: "Add a greeting tool to the agent"
    ↓
Architect ──query──→ RAG: "How are tools registered?"
    ↓
Architect: Creates task plan with 2 tasks
    ↓
Builder ──query──→ RAG: "Show me tool examples"
    ↓
Builder: Implements Task 1
    ↓
O.V.E. Harness: Run tests → Pass/Fail
    ↓ (if fail, retry with error context)
Architect: Validate implementation
    ↓
Builder: Implements Task 2
    ↓
... continue until all tasks complete ...
    ↓
User: "Done! Created greet_user tool in simple_agent.py"
```

## Prerequisites

- [ ] Complete [Exercise 3: Multi-Model Coordination](./03-multi-model-coordination.md)
- [ ] Working RAG engine with project indexed
- [ ] Working Architect and Builder agents
- [ ] Read [Testing RAG with O.V.E.](../../tutorial-3/guides/testing-rag-ove.md)

## Code Scaffold

You'll create/update these files:
```
src/memory_rag/
├── ove_harness.py              # NEW: Testing harness
├── architect_builder.py        # NEW: Coordinator
└── ... (existing files)

tests/memory_rag/
└── test_architect_builder.py   # NEW: Integration tests
```

## Tasks

### Task 1: Implement Task Planning (Architect)

Enhance the Architect to create detailed, actionable task plans.

**Update `src/memory_rag/architect_agent.py`:**

**Requirements:**
- Plans should include acceptance criteria
- Plans should reference existing patterns from RAG
- Plans should be specific enough for Builder to implement

**AI Assistant Prompt:**
```
@.cursorrules @src/memory_rag/architect_agent.py

Enhance the Architect's plan() method:

1. Add better context gathering:
   - Query RAG for existing patterns
   - Query RAG for project conventions
   - Include .cursorrules content for coding standards

2. Improve plan structure:
   ```python
   {
       "request_summary": "What the user wants",
       "context_used": ["file1.py", "file2.md"],
       "tasks": [
           {
               "id": 1,
               "description": "Human-readable description",
               "file": "path/to/file.py",
               "spec": "Detailed specification",
               "acceptance_criteria": [
                   "Function has type hints",
                   "Function has docstring",
                   "Function is registered with @registry.register"
               ],
               "patterns_to_follow": "Based on search_codebase() in knowledge_tool.py"
           }
       ]
   }
   ```

3. Add plan validation:
   - Ensure all tasks have required fields
   - Ensure file paths are valid
   - Return helpful errors if planning fails
```

### Task 2: Implement Code Generation (Builder)

Enhance the Builder to generate production-quality code.

**Update `src/memory_rag/builder_agent.py`:**

**Requirements:**
- Follow patterns from RAG examples exactly
- Include proper imports
- Generate code that passes linting

**AI Assistant Prompt:**
```
@.cursorrules @src/memory_rag/builder_agent.py

Enhance the Builder's implement() method:

1. Better example retrieval:
   - Query for similar functions in the codebase
   - Query for import patterns
   - Query for docstring style

2. Structured output:
   ```python
   {
       "task_id": 1,
       "status": "complete",
       "imports": ["from x import y", ...],
       "code": "def function_name()...",
       "tests": "def test_function_name()...",
       "notes": "Implementation notes",
       "patterns_used": ["Based on existing_func in file.py"]
   }
   ```

3. Code quality checks:
   - Ensure type hints are present
   - Ensure docstring is present
   - Clean up markdown fences
   - Validate basic syntax (try to compile)
```

### Task 3: Add O.V.E. Testing Harness

Create a testing harness that validates Builder output.

**Create file:** `src/memory_rag/ove_harness.py`

**Requirements:**
- **Observe**: Capture code and test output
- **Validate**: Check deterministic aspects (syntax, imports, type hints)
- **Evaluate**: Run tests, check for expected behavior

**AI Assistant Prompt:**
```
@.cursorrules @src/memory_rag/ove_harness.py

Create the OVETestHarness class:

class OVETestHarness:
    """
    O.V.E. testing harness for validating Builder output.
    
    Observe: Capture code, tests, execution results
    Validate: Check syntax, imports, type hints
    Evaluate: Run tests, check functionality
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = project_root
    
    def observe(self, implementation: dict) -> dict:
        """Capture all artifacts from Builder."""
        return {
            "code": implementation["code"],
            "tests": implementation.get("tests", ""),
            "file": implementation["file"],
            "timestamp": datetime.now().isoformat(),
        }
    
    def validate(self, observation: dict) -> dict:
        """Check deterministic aspects."""
        results = {"passed": True, "checks": []}
        
        code = observation["code"]
        
        # Check 1: Syntax valid
        try:
            compile(code, "<string>", "exec")
            results["checks"].append({"name": "syntax", "passed": True})
        except SyntaxError as e:
            results["passed"] = False
            results["checks"].append({
                "name": "syntax",
                "passed": False,
                "error": str(e)
            })
        
        # Check 2: Has type hints (for functions)
        if "def " in code:
            has_hints = ": " in code.split("def ")[1].split(")")[0]
            results["checks"].append({
                "name": "type_hints",
                "passed": has_hints
            })
            if not has_hints:
                results["passed"] = False
        
        # Check 3: Has docstring
        has_docstring = '"""' in code or "'''" in code
        results["checks"].append({
            "name": "docstring",
            "passed": has_docstring
        })
        
        return results
    
    def evaluate(self, observation: dict, validation: dict) -> dict:
        """Run tests and evaluate functionality."""
        if not validation["passed"]:
            return {
                "passed": False,
                "reason": "Validation failed, skipping evaluation"
            }
        
        # Try to run the tests
        tests = observation.get("tests", "")
        if not tests:
            return {"passed": True, "reason": "No tests to run"}
        
        # TODO: Actually execute tests in sandbox
        # For now, just check test syntax
        try:
            compile(tests, "<string>", "exec")
            return {"passed": True, "reason": "Test syntax valid"}
        except SyntaxError as e:
            return {"passed": False, "reason": f"Test syntax error: {e}"}
    
    def run(self, implementation: dict) -> dict:
        """Run complete O.V.E. pipeline."""
        observation = self.observe(implementation)
        validation = self.validate(observation)
        evaluation = self.evaluate(observation, validation)
        
        return {
            "observation": observation,
            "validation": validation,
            "evaluation": evaluation,
            "overall_passed": validation["passed"] and evaluation["passed"]
        }

Add logging for each phase.
Include helper methods as needed.
```

### Task 4: Create Iteration Loop

Build the coordinator that handles retries and completion.

**Create file:** `src/memory_rag/architect_builder.py`

**Requirements:**
- Coordinate Architect and Builder
- Handle failures with retry (max 3 attempts)
- Collect results from all tasks
- Provide final summary

**AI Assistant Prompt:**
```
@.cursorrules @src/memory_rag/architect_builder.py

Create the ArchitectBuilderCoordinator:

class ArchitectBuilderCoordinator:
    """
    Coordinates the Architect-Builder workflow.
    
    Flow:
    1. User request → Architect plans
    2. For each task: Builder implements → O.V.E. validates → Architect reviews
    3. Retry on failure (max 3 times)
    4. Return summary of completed work
    """
    
    MAX_RETRIES = 3
    
    def __init__(self, persist_dir: str = "./storage/project_index"):
        self.rag_engine = RAGEngine(persist_dir)
        self.rag_engine.load_index()
        self.architect = ArchitectAgent(self.rag_engine)
        self.builder = BuilderAgent(self.rag_engine)
        self.harness = OVETestHarness()
        self.logger = logging.getLogger(__name__)
    
    def process_request(self, request: str) -> dict:
        """Process a user request through the full workflow."""
        self.logger.info("Processing request: %s", request[:100])
        
        # 1. Architect creates plan
        plan = self.architect.plan(request)
        self.logger.info("Plan created with %d tasks", len(plan))
        
        results = []
        
        # 2. Process each task
        for task in plan:
            result = self._process_task(task)
            results.append(result)
            
            if not result["success"]:
                self.logger.warning("Task %d failed after retries", task["id"])
        
        # 3. Create summary
        return self._create_summary(request, plan, results)
    
    def _process_task(self, task: dict) -> dict:
        """Process a single task with retries."""
        for attempt in range(self.MAX_RETRIES):
            self.logger.info(
                "Task %d attempt %d/%d",
                task["id"], attempt + 1, self.MAX_RETRIES
            )
            
            # Builder implements
            implementation = self.builder.implement(task)
            
            # O.V.E. validates
            ove_result = self.harness.run(implementation)
            
            if ove_result["overall_passed"]:
                # Architect validates
                validation = self.architect.validate(task, implementation["code"])
                
                if validation.get("approved", False):
                    return {
                        "task_id": task["id"],
                        "success": True,
                        "implementation": implementation,
                        "attempts": attempt + 1
                    }
                else:
                    # Add architect feedback for retry
                    task["previous_feedback"] = validation.get("feedback", "")
            else:
                # Add O.V.E. errors for retry
                task["previous_errors"] = ove_result
            
            self.logger.info("Attempt %d failed, retrying...", attempt + 1)
        
        return {
            "task_id": task["id"],
            "success": False,
            "attempts": self.MAX_RETRIES,
            "last_error": task.get("previous_errors", task.get("previous_feedback"))
        }
    
    def _create_summary(self, request: str, plan: list, results: list) -> dict:
        """Create summary of completed work."""
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]
        
        return {
            "request": request,
            "total_tasks": len(plan),
            "successful_tasks": len(successful),
            "failed_tasks": len(failed),
            "results": results,
            "overall_success": len(failed) == 0
        }

Add comprehensive logging throughout.
Include type hints and docstrings.
```

### Task 5: End-to-End Test

Create integration tests for the full workflow.

**Create file:** `tests/memory_rag/test_architect_builder.py`

**Test scenarios:**
1. Simple request that should succeed
2. Request that requires retry
3. Request that fails validation

**AI Assistant Prompt:**
```
@.cursorrules @tests/memory_rag/test_architect_builder.py

Create integration tests:

import pytest
from src.memory_rag.architect_builder import ArchitectBuilderCoordinator

@pytest.fixture
def coordinator():
    """Create coordinator with loaded index."""
    coord = ArchitectBuilderCoordinator()
    return coord

class TestArchitectBuilderWorkflow:
    """Integration tests for Architect-Builder workflow."""
    
    @pytest.mark.slow
    def test_simple_request_succeeds(self, coordinator):
        """Test that a simple request completes successfully."""
        result = coordinator.process_request(
            "Add a function that returns the current timestamp"
        )
        
        assert result["total_tasks"] >= 1
        assert result["successful_tasks"] >= 1
        # May not be 100% success, but should have progress
    
    def test_plan_has_required_fields(self, coordinator):
        """Test that Architect creates valid plans."""
        plan = coordinator.architect.plan("Add a greeting function")
        
        assert isinstance(plan, list)
        assert len(plan) >= 1
        
        for task in plan:
            assert "id" in task
            assert "description" in task
            assert "file" in task
    
    def test_ove_catches_syntax_errors(self, coordinator):
        """Test that O.V.E. harness catches invalid code."""
        bad_implementation = {
            "code": "def broken( name",  # Syntax error
            "file": "test.py"
        }
        
        result = coordinator.harness.run(bad_implementation)
        
        assert not result["overall_passed"]
        assert not result["validation"]["passed"]
    
    def test_ove_validates_type_hints(self, coordinator):
        """Test that O.V.E. checks for type hints."""
        no_hints = {
            "code": '''def greet(name):
    """Greet someone."""
    return f"Hello, {name}"
''',
            "file": "test.py"
        }
        
        result = coordinator.harness.run(no_hints)
        
        # Should flag missing type hints
        type_check = next(
            c for c in result["validation"]["checks"]
            if c["name"] == "type_hints"
        )
        assert not type_check["passed"]

Use @pytest.mark.slow for tests that hit LLMs.
Include fixtures for common setup.
```

**Run tests:**
```bash
# Run all tests
python -m pytest tests/memory_rag/test_architect_builder.py -v

# Run only fast tests (skip LLM calls)
python -m pytest tests/memory_rag/test_architect_builder.py -v -m "not slow"
```

## Validation Checkpoints

### Test Complete Workflow:
```python
from src.memory_rag.architect_builder import ArchitectBuilderCoordinator

coordinator = ArchitectBuilderCoordinator()

# Process a request
result = coordinator.process_request(
    "Add a tool that returns the current date and time"
)

print(f"Total tasks: {result['total_tasks']}")
print(f"Successful: {result['successful_tasks']}")
print(f"Failed: {result['failed_tasks']}")
print(f"Overall success: {result['overall_success']}")

# Inspect a successful task
if result['results']:
    first = result['results'][0]
    if first['success']:
        print(f"\nGenerated code:")
        print(first['implementation']['code'])
```

### Test O.V.E. Harness:
```python
from src.memory_rag.ove_harness import OVETestHarness

harness = OVETestHarness()

# Test good code
good_code = {
    "code": '''def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"
''',
    "file": "test.py"
}

result = harness.run(good_code)
assert result["overall_passed"], "Good code should pass"

# Test bad code (no type hints)
bad_code = {
    "code": '''def greet(name):
    return f"Hello, {name}!"
''',
    "file": "test.py"
}

result = harness.run(bad_code)
# May pass syntax but should flag missing type hints
```

## Challenge Extensions

Completed the main workflow? Try these extensions:

### Extension 1: Add Code Review Step

Add a step where Architect reviews Builder's code for quality issues beyond validation:

```python
def review(self, implementation: dict) -> dict:
    """Review code for style, efficiency, and best practices."""
    # Query RAG for project conventions
    # Check against .cursorrules
    # Return improvement suggestions
```

### Extension 2: Implement Parallel Builders

For independent tasks, run multiple Builders in parallel:

```python
import asyncio

async def _process_tasks_parallel(self, tasks: list) -> list:
    """Process independent tasks in parallel."""
    async_tasks = [
        self._process_task_async(task) 
        for task in tasks
    ]
    return await asyncio.gather(*async_tasks)
```

### Extension 3: Add Memory of Past Implementations

Store successful implementations for future reference:

```python
def _store_successful_implementation(self, task: dict, impl: dict):
    """Add successful implementation to RAG index for future reference."""
    # Create document from implementation
    # Add to index
    # Future similar tasks can reference this
```

## Checkpoint Questions

1. **Why do we limit retries to 3 attempts?**
   <details>
   <summary>Answer</summary>
   Diminishing returns - if code doesn't work after 3 tries with feedback, the specification is likely ambiguous or the task is too complex. Better to fail and ask for clarification than loop forever.
   </details>

2. **What's the difference between O.V.E. validation and Architect validation?**
   <details>
   <summary>Answer</summary>
   O.V.E. checks mechanical aspects (syntax, type hints, tests pass). Architect checks semantic aspects (does this actually solve the problem? does it match the specification?).
   </details>

3. **How would you handle a task that requires modifying multiple files?**
   <details>
   <summary>Answer</summary>
   Split into subtasks (one per file) in the Architect's plan. Process sequentially so later tasks can see earlier changes. Or implement file-level transactions with rollback on failure.
   </details>

## Common Issues

### Issue: "Workflow times out"

**Solution:** Add timeout handling:
```python
from func_timeout import func_timeout, FunctionTimedOut

try:
    implementation = func_timeout(60, self.builder.implement, args=(task,))
except FunctionTimedOut:
    return {"success": False, "error": "Builder timed out"}
```

### Issue: "Architect doesn't use RAG context"

**Solution:** Make context usage explicit:
```python
prompt += """
IMPORTANT: You MUST reference specific files from the context above.
DO NOT make up file paths or function names.
"""
```

### Issue: "Builder ignores project conventions"

**Solution:** Include .cursorrules in Builder's context:
```python
with open(".cursorrules") as f:
    rules = f.read()
prompt += f"\nProject rules:\n{rules}\n"
```

## Wrap-Up

Congratulations! You've built a complete Architect-Builder coding assistant that:

- Uses RAG to understand the codebase
- Employs Llama for planning and validation
- Uses DeepSeek for code generation
- Validates with O.V.E. methodology
- Handles failures with intelligent retries

**What you've learned:**
1. RAG provides contextual knowledge to agents
2. Different models excel at different tasks
3. O.V.E. extends to testing generated code
4. Iteration loops handle imperfect generations

**Next steps:**
- Try the Challenge Extensions
- Apply this pattern to your own projects
- Explore advanced RAG techniques (reranking, hybrid search)
- Move to Tutorial 4: Production Patterns

---

## 💡 Final Tips

**Start small:** Test with simple requests before complex ones.

**Read the logs:** Multi-component systems need comprehensive logging.

**Iterate on prompts:** Fine-tune Architect and Builder prompts based on failures.

**Trust O.V.E.:** Let the harness catch errors rather than hoping for perfect generation.

