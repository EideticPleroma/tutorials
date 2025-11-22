import dataclasses
from typing import List, Dict, Any, Callable, Optional
import json

@dataclasses.dataclass
class TraceStep:
    role: str
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_outputs: Optional[List[Dict[str, Any]]] = None

@dataclasses.dataclass
class Trace:
    input_prompt: str
    steps: List[TraceStep]
    final_output: str
    error: Optional[str] = None

class TestCase:
    __test__ = False  # Tell pytest this is not a test class
    def __init__(
        self,
        name: str,
        prompt: str,
        expected_tool_calls: Optional[List[str]] = None,
        expected_content_keywords: Optional[List[str]] = None,
        evaluators: Optional[List[Callable[[Trace], float]]] = None
    ):
        self.name = name
        self.prompt = prompt
        self.expected_tool_calls = expected_tool_calls or []
        self.expected_content_keywords = expected_content_keywords or []
        self.evaluators = evaluators or []

class TestResult:
    __test__ = False  # Tell pytest this is not a test class
    def __init__(self, test_case: TestCase, trace: Trace):
        self.test_case = test_case
        self.trace = trace
        self.passed_validation = False
        self.evaluation_score = 0.0
        self.validation_errors: List[str] = []

class AgentTestRunner:
    def __init__(self, agent):
        self.agent = agent

    def run(self, test_case: TestCase) -> TestResult:
        print(f"Running Test: {test_case.name}")
        
        # 1. OBSERVE
        # We need to hook into the agent to capture the trace.
        # For this tutorial, we'll rely on the agent's internal message history
        # assuming the agent is reset before run.
        
        # Reset agent state if needed (basic implementation)
        self.agent.messages = [{"role": "system", "content": self.agent.messages[0]['content']}]
        
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
        steps = []
        for msg in messages:
            if msg['role'] == 'system': continue
            steps.append(TraceStep(
                role=msg['role'],
                content=msg.get('content', ''),
                tool_calls=msg.get('tool_calls'),
                # capturing tool output is harder with just message list unless we parse role='tool'
            ))
        
        final = messages[-1]['content'] if messages else ""
        return Trace(messages[1]['content'] if len(messages)>1 else "", steps, final)

    def _validate(self, result: TestResult):
        trace = result.trace
        case = result.test_case
        errors = []

        # Check tool calls
        called_tools = []
        for step in trace.steps:
            if step.tool_calls:
                for tc in step.tool_calls:
                    called_tools.append(tc['function']['name'])
        
        for expected in case.expected_tool_calls:
            if expected not in called_tools:
                errors.append(f"Expected tool '{expected}' was not called.")

        # Check keywords
        for keyword in case.expected_content_keywords:
            if keyword.lower() not in trace.final_output.lower():
                errors.append(f"Expected keyword '{keyword}' missing from output. Got: '{trace.final_output}'")

        result.validation_errors = errors
        result.passed_validation = len(errors) == 0

    def _evaluate(self, result: TestResult):
        # Run custom evaluators (e.g., LLM judge)
        scores = []
        for eval_func in result.test_case.evaluators:
            scores.append(eval_func(result.trace))
        
        if scores:
            result.evaluation_score = sum(scores) / len(scores)
        else:
            result.evaluation_score = 1.0 if result.passed_validation else 0.0

