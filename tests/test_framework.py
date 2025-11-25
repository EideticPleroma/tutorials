"""
O.V.E. (Observe-Validate-Evaluate) testing framework for agentic AI.

This module implements the core testing methodology for Tutorial 1, providing
structured testing of agent behavior through three phases:

1. OBSERVE: Capture the agent's execution trace (tool calls, responses)
2. VALIDATE: Check deterministic outputs (did it call the right tools?)
3. EVALUATE: Check probabilistic outputs (is the answer good quality?)

The framework supports both unit tests (testing individual tools) and
end-to-end tests (testing the full agent loop with real LLM calls).

Classes:
    TraceStep: Single step in agent execution (message, tool calls)
    Trace: Complete execution trace from input to output
    TestCase: Test specification with expected behaviors
    TestResult: Test outcome with validation and evaluation results
    AgentTestRunner: Test executor that implements O.V.E. methodology

Example:
    from tests.test_framework import AgentTestRunner, TestCase

    runner = AgentTestRunner(agent)
    case = TestCase(
        name="Weather Check",
        prompt="What's the weather in Paris?",
        expected_tool_calls=["get_weather"],
        expected_content_keywords=["Paris"]
    )
    result = runner.run(case)
    assert result.passed_validation

See Also:
    - Tutorial 1 Lab 4: Testing Methodology
    - tests/unit/: Example unit tests
"""

import dataclasses
from typing import List, Dict, Any, Callable, Optional
import json


@dataclasses.dataclass
class TraceStep:
    """
    A single step in an agent's execution trace.

    Captures one message in the agent's conversation history, including
    any tool calls made and their outputs. Used for observing agent
    behavior during testing.

    Attributes:
        role: Message role ("system", "user", "assistant", "tool")
        content: Text content of the message
        tool_calls: List of tool calls made in this step (if any)
        tool_outputs: Results from tool executions (if any)

    Example:
        step = TraceStep(
            role="assistant",
            content="I'll calculate that for you",
            tool_calls=[{"function": {"name": "calculate", "arguments": {...}}}]
        )
    """

    role: str
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_outputs: Optional[List[Dict[str, Any]]] = None


@dataclasses.dataclass
class Trace:
    """
    Complete execution trace of an agent processing a user prompt.

    Contains all steps from the initial prompt through to the final output,
    enabling detailed analysis of agent behavior for testing and debugging.

    Attributes:
        input_prompt: The original user query
        steps: List of execution steps (messages, tool calls)
        final_output: The agent's final response to the user
        error: Error message if execution failed (None if successful)

    Example:
        trace = Trace(
            input_prompt="What's 5 + 3?",
            steps=[...],
            final_output="The result is 8"
        )
    """

    input_prompt: str
    steps: List[TraceStep]
    final_output: str
    error: Optional[str] = None


class TestCase:
    """
    Specification for an agent test case using the O.V.E. methodology.

    Defines what behavior to test (via prompt), what to validate
    (expected tool calls, keywords), and how to evaluate quality
    (custom evaluator functions).

    Attributes:
        name: Descriptive name for the test
        prompt: User input to send to the agent
        expected_tool_calls: List of tool names the agent should call (VALIDATE)
        expected_content_keywords: Keywords that should appear in output (EVALUATE)
        evaluators: Optional custom evaluation functions (EVALUATE)

    Example:
        test = TestCase(
            name="Weather lookup",
            prompt="What's the weather in Paris?",
            expected_tool_calls=["get_weather"],
            expected_content_keywords=["Paris", "Sunny"]
        )
    """

    __test__ = False  # Tell pytest this is not a test class

    def __init__(
        self,
        name: str,
        prompt: str,
        expected_tool_calls: Optional[List[str]] = None,
        expected_content_keywords: Optional[List[str]] = None,
        evaluators: Optional[List[Callable[[Trace], float]]] = None,
    ):
        """
        Create a new test case specification.

        Args:
            name: Descriptive name for the test (used in reports)
            prompt: The user message to send to the agent
            expected_tool_calls: List of tool names expected to be called
                                for validation (empty list = no tools expected)
            expected_content_keywords: Keywords that should appear in the
                                      agent's final output
            evaluators: Optional list of functions that take a Trace and
                       return a score (0.0-1.0) for custom evaluation

        Example:
            case = TestCase(
                name="Math calculation",
                prompt="What is 15 * 23?",
                expected_tool_calls=["calculate"],
                expected_content_keywords=["345"]
            )
        """
        self.name = name
        self.prompt = prompt
        self.expected_tool_calls = expected_tool_calls or []
        self.expected_content_keywords = expected_content_keywords or []
        self.evaluators = evaluators or []


class TestResult:
    """
    Result of running a test case through the O.V.E. methodology.

    Contains the execution trace, validation results (pass/fail),
    evaluation scores, and any errors encountered. Used to determine
    if the agent behaved correctly.

    Attributes:
        test_case: The original test case specification
        trace: The execution trace captured during the test
        passed_validation: True if all deterministic checks passed
        evaluation_score: Quality score from 0.0 to 1.0 (average of evaluators)
        validation_errors: List of validation failures (empty if passed)

    Example:
        result = TestResult(test_case, trace)
        # After validation and evaluation:
        if result.passed_validation and result.evaluation_score > 0.7:
            print("Test passed!")
    """

    __test__ = False  # Tell pytest this is not a test class

    def __init__(self, test_case: TestCase, trace: Trace):
        """
        Create a new test result container.

        Args:
            test_case: The test case that was executed
            trace: The execution trace captured during test run

        Note:
            passed_validation and evaluation_score are set to defaults and
            should be updated by the test runner's _validate() and _evaluate()
            methods.
        """
        self.test_case = test_case
        self.trace = trace
        self.passed_validation = False
        self.evaluation_score = 0.0
        self.validation_errors: List[str] = []


class AgentTestRunner:
    """
    Test runner that implements the O.V.E. (Observe-Validate-Evaluate) methodology.

    Executes test cases against an agent, captures execution traces, validates
    deterministic behavior, and evaluates probabilistic outputs. Core component
    of the Tutorial 1 testing framework.

    Attributes:
        agent: The agent instance to test

    Example:
        from agent.simple_agent import Agent
        from tests.test_framework import AgentTestRunner, TestCase

        agent = Agent()
        runner = AgentTestRunner(agent)

        test = TestCase(
            name="Addition",
            prompt="What is 5 + 3?",
            expected_tool_calls=["calculate"],
            expected_content_keywords=["8"]
        )

        result = runner.run(test)
        assert result.passed_validation
    """

    def __init__(self, agent):
        """
        Initialize test runner with an agent instance.

        Args:
            agent: The agent to test. Must have a chat() method and
                  messages attribute for trace extraction

        Example:
            agent = Agent()
            runner = AgentTestRunner(agent)
        """
        self.agent = agent

    def run(self, test_case: TestCase) -> TestResult:
        """
        Execute a test case using the O.V.E. methodology.

        Implements the three-phase testing approach:
        1. OBSERVE: Run the agent and capture execution trace
        2. VALIDATE: Check deterministic outputs (tool calls, structure)
        3. EVALUATE: Check probabilistic outputs (quality, correctness)

        Args:
            test_case: The test specification to execute

        Returns:
            TestResult containing trace, validation status, and evaluation scores

        Example:
            test = TestCase(name="Test", prompt="Hello", expected_tool_calls=[])
            result = runner.run(test)
            if result.passed_validation:
                print("Success!")
        """
        print(f"Running Test: {test_case.name}")

        # 1. OBSERVE
        # We need to hook into the agent to capture the trace.
        # For this tutorial, we'll rely on the agent's internal message history
        # assuming the agent is reset before run.

        # Reset agent state if needed (basic implementation)
        self.agent.messages = [
            {"role": "system", "content": self.agent.messages[0]["content"]}
        ]

        try:
            final_response = self.agent.chat(test_case.prompt)
            trace = self._extract_trace(self.agent.messages)
        except Exception as e:
            trace = Trace(test_case.prompt, [], "", str(e))

        result = TestResult(test_case, trace)

        # 2. VALIDATE (Deterministic)
        self._validate(result)

        # 3. EVALUATE (Probabilistic)
        self._evaluate(result)

        return result

    def _extract_trace(self, messages: List[Dict]) -> Trace:
        """
        Extract execution trace from agent's message history.

        Converts the agent's internal message list into a structured Trace
        object for analysis. Skips system messages and captures user input,
        assistant responses, and tool calls.

        Args:
            messages: The agent's message history (list of dicts with role/content)

        Returns:
            Trace object containing structured execution steps

        Note:
            This is a simplified trace extractor. Production implementations
            might capture more details like timestamps, token usage, etc.
        """
        steps = []
        for msg in messages:
            if msg["role"] == "system":
                continue
            steps.append(
                TraceStep(
                    role=msg["role"],
                    content=msg.get("content", ""),
                    tool_calls=msg.get("tool_calls"),
                    # capturing tool output is harder with just message list unless we parse role='tool'
                )
            )

        final = messages[-1]["content"] if messages else ""
        return Trace(messages[1]["content"] if len(messages) > 1 else "", steps, final)

    def _validate(self, result: TestResult):
        """
        VALIDATE phase: Check deterministic outputs.

        Verifies that the agent:
        - Called the expected tools
        - Included expected keywords in the final output

        These are deterministic checks that should pass consistently.
        Failures indicate bugs or incorrect agent behavior.

        Args:
            result: TestResult to validate (modifies in-place)

        Side Effects:
            - Sets result.validation_errors with any failures found
            - Sets result.passed_validation to True if all checks pass

        Example:
            If expected_tool_calls=["calculate"] but agent didn't call it,
            validation_errors will contain: "Expected tool 'calculate' was not called."
        """
        trace = result.trace
        case = result.test_case
        errors = []

        # Check tool calls
        called_tools = []
        for step in trace.steps:
            if step.tool_calls:
                for tc in step.tool_calls:
                    called_tools.append(tc["function"]["name"])

        for expected in case.expected_tool_calls:
            if expected not in called_tools:
                errors.append(f"Expected tool '{expected}' was not called.")

        # Check keywords
        for keyword in case.expected_content_keywords:
            if keyword.lower() not in trace.final_output.lower():
                errors.append(
                    f"Expected keyword '{keyword}' missing from output. Got: '{trace.final_output}'"
                )

        result.validation_errors = errors
        result.passed_validation = len(errors) == 0

    def _evaluate(self, result: TestResult):
        """
        EVALUATE phase: Check probabilistic outputs.

        Runs custom evaluator functions to assess the quality of the
        agent's output. Evaluators return scores from 0.0 (bad) to 1.0 (good).
        The final score is the average of all evaluator scores.

        If no custom evaluators are provided, defaults to 1.0 if validation
        passed, 0.0 otherwise.

        Args:
            result: TestResult to evaluate (modifies in-place)

        Side Effects:
            Sets result.evaluation_score to the average evaluator score

        Example:
            def check_politeness(trace: Trace) -> float:
                return 1.0 if "please" in trace.final_output.lower() else 0.5

            test = TestCase(..., evaluators=[check_politeness])
            # After run, result.evaluation_score will reflect politeness
        """
        # Run custom evaluators (e.g., LLM judge)
        scores = []
        for eval_func in result.test_case.evaluators:
            scores.append(eval_func(result.trace))

        if scores:
            result.evaluation_score = sum(scores) / len(scores)
        else:
            result.evaluation_score = 1.0 if result.passed_validation else 0.0
