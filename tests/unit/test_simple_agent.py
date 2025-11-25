"""
Unit tests for the simple agent using O.V.E. methodology.

These tests verify the basic functionality of the Agent class from Tutorial 1,
demonstrating tool calling, message handling, and response generation.

Tests cover:
- Math tool usage (calculate)
- Weather tool usage (get_weather)
- No-tool scenarios (chitchat)

Each test uses the AgentTestRunner and TestCase classes to implement
the Observe-Validate-Evaluate testing approach.
"""

import pytest
from src.agent.simple_agent import Agent
from tests.test_framework import AgentTestRunner, TestCase


@pytest.fixture
def agent():
    """
    Pytest fixture providing a fresh Agent instance for each test.

    Returns:
        Agent: New agent instance with default configuration

    Example:
        def test_something(agent):
            response = agent.chat("Hello")
    """
    return Agent()


def test_math_tool(agent):
    """
    Test that agent correctly uses the calculate tool for math queries.

    VALIDATE: Agent calls the "calculate" tool
    EVALUATE: Agent's response includes the correct answer "8"

    This demonstrates the O.V.E. methodology on a deterministic tool.
    """
    runner = AgentTestRunner(agent)

    case = TestCase(
        name="Basic Addition",
        prompt="What is 5 plus 3?",
        expected_tool_calls=["calculate"],
        expected_content_keywords=["8"],
    )

    result = runner.run(case)

    assert result.passed_validation, f"Validation failed: {result.validation_errors}"


def test_weather_tool(agent):
    """
    Test that agent correctly uses the get_weather tool for weather queries.

    VALIDATE: Agent calls the "get_weather" tool
    EVALUATE: Agent's response includes both the city name and weather info

    This tests that the agent can route queries to the appropriate tool.
    """
    runner = AgentTestRunner(agent)

    case = TestCase(
        name="Weather Check",
        prompt="What's the weather in Paris?",
        expected_tool_calls=["get_weather"],
        expected_content_keywords=["Paris", "Sunny"],
    )

    result = runner.run(case)

    assert result.passed_validation, f"Validation failed: {result.validation_errors}"


def test_no_tool_needed(agent):
    """
    Test that agent doesn't call tools for simple conversation.

    VALIDATE: Agent makes NO tool calls (empty list)
    EVALUATE: Agent responds naturally to greeting

    This tests that the agent can distinguish between queries that need
    tools versus those that don't, avoiding unnecessary tool calls.
    """
    runner = AgentTestRunner(agent)

    case = TestCase(
        name="Chitchat",
        prompt="Hello, how are you?",
        expected_tool_calls=[],  # Should NOT call tools
        expected_content_keywords=[],
    )

    result = runner.run(case)

    assert result.passed_validation, f"Validation failed: {result.validation_errors}"
