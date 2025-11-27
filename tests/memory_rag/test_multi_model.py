"""
Tests for multi-model coordination.

Tests the ModelRouter, ArchitectAgent, and BuilderAgent components.
"""

import pytest

# TODO: Import after implementation
# from src.memory_rag.model_router import ModelRouter
# from src.memory_rag.architect_agent import ArchitectAgent
# from src.memory_rag.builder_agent import BuilderAgent
# from src.memory_rag.rag_engine import RAGEngine


class TestModelRouter:
    """Test ModelRouter task classification and routing."""
    
    def test_router_initialization(self):
        """Test that router initializes correctly."""
        # TODO: Implement
        # router = ModelRouter()
        # assert router.architect_llm is not None
        # assert router.builder_llm is not None
        pass
    
    @pytest.mark.parametrize("request,expected_type", [
        ("Write a function to sort a list", "coding"),
        ("Implement the delegate method", "coding"),
        ("Create a class for handling messages", "coding"),
        ("Explain how RAG works", "reasoning"),
        ("What is the coordinator pattern?", "reasoning"),
        ("Break down this feature into tasks", "planning"),
        ("Design the architecture for...", "planning"),
    ])
    def test_classify_task(self, request, expected_type):
        """Test task classification for various requests."""
        # TODO: Implement
        # router = ModelRouter()
        # task_type = router.classify_task(request)
        # assert task_type == expected_type
        pass
    
    def test_route_returns_correct_llm(self):
        """Test that routing returns the correct LLM."""
        # TODO: Implement
        # router = ModelRouter()
        # 
        # coding_llm = router.route("coding")
        # assert coding_llm.model == "deepseek-coder:6.7b"
        # 
        # planning_llm = router.route("planning")
        # assert planning_llm.model == "llama3.1:8b"
        pass
    
    def test_unknown_task_defaults_to_architect(self):
        """Test that unknown task types default to Architect."""
        # TODO: Implement
        # router = ModelRouter()
        # task_type = router.classify_task("do something random")
        # assert task_type == "unknown"
        # 
        # llm = router.route("unknown")
        # assert llm.model == "llama3.1:8b"
        pass


class TestArchitectAgent:
    """Test ArchitectAgent planning and validation."""
    
    @pytest.fixture
    def architect(self):
        """Fixture providing ArchitectAgent."""
        # TODO: Implement fixture
        # rag_engine = RAGEngine()
        # rag_engine.load_index()
        # return ArchitectAgent(rag_engine)
        pytest.skip("ArchitectAgent not implemented yet")
    
    def test_plan_returns_list(self, architect):
        """Test that plan() returns a list of tasks."""
        plan = architect.plan("Add a greeting function")
        
        assert isinstance(plan, list)
        assert len(plan) >= 1
    
    def test_plan_task_has_required_fields(self, architect):
        """Test that each task has required fields."""
        plan = architect.plan("Add a greeting function")
        
        for task in plan:
            assert "id" in task
            assert "description" in task
            assert "file" in task
            assert "spec" in task
    
    def test_plan_references_existing_files(self, architect):
        """Test that plan references real files in the project."""
        plan = architect.plan("Add logging to the agent")
        
        for task in plan:
            file_path = task.get("file", "")
            # Should reference actual project files
            assert file_path.endswith(".py"), f"Expected Python file, got: {file_path}"
    
    def test_validate_approves_good_code(self, architect):
        """Test that validation approves well-formed code."""
        task = {
            "id": 1,
            "description": "Add greeting function",
            "spec": "Function that takes name and returns greeting",
            "acceptance_criteria": ["Has type hints", "Has docstring"],
        }
        
        good_code = '''
def greet(name: str) -> str:
    """Greet a person by name.
    
    Args:
        name: The person's name.
    
    Returns:
        A greeting string.
    """
    return f"Hello, {name}!"
'''
        
        result = architect.validate(task, good_code)
        assert result["approved"] is True
    
    def test_validate_rejects_code_missing_requirements(self, architect):
        """Test that validation rejects code missing requirements."""
        task = {
            "id": 1,
            "description": "Add greeting function",
            "spec": "Function that takes name and returns greeting",
            "acceptance_criteria": ["Has type hints", "Has docstring"],
        }
        
        bad_code = '''
def greet(name):
    return f"Hello, {name}!"
'''
        
        result = architect.validate(task, bad_code)
        assert result["approved"] is False
        assert len(result.get("issues", [])) > 0


class TestBuilderAgent:
    """Test BuilderAgent code generation."""
    
    @pytest.fixture
    def builder(self):
        """Fixture providing BuilderAgent."""
        # TODO: Implement fixture
        # rag_engine = RAGEngine()
        # rag_engine.load_index()
        # return BuilderAgent(rag_engine)
        pytest.skip("BuilderAgent not implemented yet")
    
    def test_implement_returns_dict(self, builder):
        """Test that implement() returns a dict with expected keys."""
        task = {
            "id": 1,
            "description": "Add greeting function",
            "file": "src/agent/simple_agent.py",
            "spec": "Function that takes name and returns greeting",
        }
        
        result = builder.implement(task)
        
        assert isinstance(result, dict)
        assert "task_id" in result
        assert "status" in result
        assert "code" in result
    
    def test_implement_produces_valid_python(self, builder):
        """Test that generated code is valid Python."""
        task = {
            "id": 1,
            "description": "Add greeting function",
            "file": "test.py",
            "spec": "Simple function that returns a string",
        }
        
        result = builder.implement(task)
        code = result["code"]
        
        # Should compile without errors
        try:
            compile(code, "<string>", "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated code has syntax error: {e}")
    
    def test_implement_follows_conventions(self, builder):
        """Test that generated code follows project conventions."""
        task = {
            "id": 1,
            "description": "Add greeting function",
            "file": "test.py",
            "spec": "Function with proper type hints and docstring",
            "acceptance_criteria": ["Has type hints", "Has docstring"],
        }
        
        result = builder.implement(task)
        code = result["code"]
        
        # Check for type hints (basic check)
        assert "->" in code or ": str" in code or ": int" in code, (
            "Generated code should have type hints"
        )
    
    def test_implement_with_retry_context(self, builder):
        """Test that builder uses previous error context."""
        task = {
            "id": 1,
            "description": "Add greeting function",
            "file": "test.py",
            "spec": "Function that takes name",
            "previous_errors": "Missing type hints",
        }
        
        result = builder.implement(task)
        # Implementation should try to fix the error
        # Just verify it runs without error
        assert result["status"] == "complete"


class TestModelHandoff:
    """Test the handoff between Architect and Builder."""
    
    @pytest.fixture
    def architect_and_builder(self):
        """Fixture providing both agents."""
        # TODO: Implement fixture
        pytest.skip("Agents not implemented yet")
    
    @pytest.mark.slow
    def test_architect_plan_to_builder_implement(self, architect_and_builder):
        """Test that Architect's plan can be implemented by Builder."""
        architect, builder = architect_and_builder
        
        # Architect creates plan
        plan = architect.plan("Add a simple utility function")
        assert len(plan) >= 1
        
        # Builder implements each task
        for task in plan:
            result = builder.implement(task)
            assert result["status"] == "complete"
            assert len(result["code"]) > 0
    
    @pytest.mark.slow
    def test_builder_output_passes_architect_validation(self, architect_and_builder):
        """Test that Builder's output passes Architect validation."""
        architect, builder = architect_and_builder
        
        task = {
            "id": 1,
            "description": "Add greeting function",
            "file": "test.py",
            "spec": "Function that takes name string, returns greeting",
            "acceptance_criteria": [
                "Function named greet",
                "Takes name parameter",
                "Returns greeting string",
            ],
        }
        
        # Builder implements
        result = builder.implement(task)
        
        # Architect validates
        validation = architect.validate(task, result["code"])
        
        # May not always pass, but should have meaningful feedback
        assert "approved" in validation
        assert "feedback" in validation

