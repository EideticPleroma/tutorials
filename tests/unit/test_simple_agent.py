import pytest
from src.agent.simple_agent import Agent
from tests.test_framework import AgentTestRunner, TestCase

@pytest.fixture
def agent():
    return Agent()

def test_math_tool(agent):
    runner = AgentTestRunner(agent)
    
    case = TestCase(
        name="Basic Addition",
        prompt="What is 5 plus 3?",
        expected_tool_calls=["calculate"],
        expected_content_keywords=["8"]
    )
    
    result = runner.run(case)
    
    assert result.passed_validation, f"Validation failed: {result.validation_errors}"

def test_weather_tool(agent):
    runner = AgentTestRunner(agent)
    
    case = TestCase(
        name="Weather Check",
        prompt="What's the weather in Paris?",
        expected_tool_calls=["get_weather"],
        expected_content_keywords=["Paris", "Sunny"]
    )
    
    result = runner.run(case)
    
    assert result.passed_validation, f"Validation failed: {result.validation_errors}"

def test_no_tool_needed(agent):
    runner = AgentTestRunner(agent)
    
    case = TestCase(
        name="Chitchat",
        prompt="Hello, how are you?",
        expected_tool_calls=[], # Should NOT call tools
        expected_content_keywords=[]
    )
    
    result = runner.run(case)
    
    assert result.passed_validation, f"Validation failed: {result.validation_errors}"

