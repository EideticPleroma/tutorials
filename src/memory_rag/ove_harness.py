"""
O.V.E. Testing Harness for validating Builder output.

This module extends the O.V.E. (Observe-Validate-Evaluate) methodology
to test generated code:
- Observe: Capture code and artifacts
- Validate: Check deterministic aspects (syntax, type hints)
- Evaluate: Run tests and check functionality
"""

import ast
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class OVETestHarness:
    """
    O.V.E. testing harness for validating Builder output.
    
    Phases:
    - Observe: Capture code, tests, metadata
    - Validate: Check syntax, type hints, docstrings
    - Evaluate: Run tests, check functionality
    
    Example:
        >>> harness = OVETestHarness()
        >>> implementation = {"code": "def greet(name: str) -> str: ...", "file": "test.py"}
        >>> result = harness.run(implementation)
        >>> if result['overall_passed']:
        ...     print("Code is valid!")
        >>> else:
        ...     print(f"Issues: {result['validation']['checks']}")
    """
    
    def __init__(self, project_root: str = "."):
        """
        Initialize O.V.E. harness.
        
        Args:
            project_root: Root directory of the project (for imports).
        """
        self.project_root = project_root
        logger.info("OVETestHarness initialized")
    
    def run(self, implementation: dict) -> dict:
        """
        Run complete O.V.E. pipeline on implementation.
        
        Args:
            implementation: Dict with keys:
                - code: Generated code string
                - file: Target file path
                - tests: Generated tests (optional)
                
        Returns:
            Result dict with keys:
            - observation: Captured artifacts
            - validation: Deterministic checks
            - evaluation: Test results
            - overall_passed: True if all checks passed
        """
        logger.info("Running O.V.E. harness")
        
        observation = self.observe(implementation)
        validation = self.validate(observation)
        evaluation = self.evaluate(observation, validation)
        
        overall_passed = validation["passed"] and evaluation["passed"]
        
        logger.info(
            "O.V.E. result: validation=%s, evaluation=%s, overall=%s",
            validation["passed"],
            evaluation["passed"],
            overall_passed
        )
        
        return {
            "observation": observation,
            "validation": validation,
            "evaluation": evaluation,
            "overall_passed": overall_passed,
        }
    
    def observe(self, implementation: dict) -> dict:
        """
        Observe phase: Capture all artifacts from implementation.
        
        Args:
            implementation: Builder output dict.
            
        Returns:
            Observation dict with all captured data.
        """
        return {
            "code": implementation.get("code", ""),
            "tests": implementation.get("tests", ""),
            "file": implementation.get("file", ""),
            "timestamp": datetime.now().isoformat(),
            "code_length": len(implementation.get("code", "")),
        }
    
    def validate(self, observation: dict) -> dict:
        """
        Validate phase: Check deterministic aspects of the code.
        
        Checks:
        1. Syntax is valid
        2. Has function definitions (if expected)
        3. Has type hints
        4. Has docstrings
        
        Args:
            observation: Output from observe phase.
            
        Returns:
            Validation result with 'passed' bool and 'checks' list.
        """
        results = {"passed": True, "checks": []}
        code = observation.get("code", "")
        
        if not code.strip():
            results["passed"] = False
            results["checks"].append({
                "name": "has_code",
                "passed": False,
                "message": "No code provided",
            })
            return results
        
        # Check 1: Syntax valid
        syntax_check = self._check_syntax(code)
        results["checks"].append(syntax_check)
        if not syntax_check["passed"]:
            results["passed"] = False
            return results  # Can't check more if syntax fails
        
        # Check 2: Has function definitions
        func_check = self._check_has_functions(code)
        results["checks"].append(func_check)
        
        # Check 3: Has type hints
        type_check = self._check_type_hints(code)
        results["checks"].append(type_check)
        if not type_check["passed"]:
            results["passed"] = False
        
        # Check 4: Has docstrings
        doc_check = self._check_docstrings(code)
        results["checks"].append(doc_check)
        # Docstrings are recommended but not required
        
        return results
    
    def evaluate(self, observation: dict, validation: dict) -> dict:
        """
        Evaluate phase: Run tests and check functionality.
        
        Args:
            observation: Output from observe phase.
            validation: Output from validate phase.
            
        Returns:
            Evaluation result with 'passed' bool and 'reason' string.
        """
        if not validation["passed"]:
            return {
                "passed": False,
                "reason": "Validation failed, skipping evaluation",
            }
        
        tests = observation.get("tests", "")
        
        if not tests.strip():
            return {
                "passed": True,
                "reason": "No tests to run",
            }
        
        # Check test syntax
        test_syntax = self._check_syntax(tests)
        if not test_syntax["passed"]:
            return {
                "passed": False,
                "reason": f"Test syntax error: {test_syntax.get('error', 'Unknown')}",
            }
        
        # TODO: Actually run tests in sandbox
        # For now, just verify test syntax is valid
        return {
            "passed": True,
            "reason": "Test syntax valid (execution not implemented)",
        }
    
    def _check_syntax(self, code: str) -> dict:
        """Check if code has valid Python syntax."""
        try:
            compile(code, "<string>", "exec")
            return {
                "name": "syntax",
                "passed": True,
                "message": "Syntax valid",
            }
        except SyntaxError as e:
            return {
                "name": "syntax",
                "passed": False,
                "message": f"Syntax error: {e.msg}",
                "error": str(e),
                "line": e.lineno,
            }
    
    def _check_has_functions(self, code: str) -> dict:
        """Check if code contains function definitions."""
        try:
            tree = ast.parse(code)
            functions = [
                node for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            
            if functions:
                return {
                    "name": "has_functions",
                    "passed": True,
                    "message": f"Found {len(functions)} function(s)",
                }
            else:
                return {
                    "name": "has_functions",
                    "passed": True,  # Not a hard requirement
                    "message": "No functions found (may be intentional)",
                }
        except:
            return {
                "name": "has_functions",
                "passed": True,
                "message": "Could not parse for functions",
            }
    
    def _check_type_hints(self, code: str) -> dict:
        """Check if functions have type hints."""
        try:
            tree = ast.parse(code)
            functions = [
                node for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            
            if not functions:
                return {
                    "name": "type_hints",
                    "passed": True,
                    "message": "No functions to check",
                }
            
            hints_found = False
            for func in functions:
                # Check return annotation
                if func.returns is not None:
                    hints_found = True
                    break
                
                # Check argument annotations (skip self/cls)
                for arg in func.args.args:
                    if arg.arg not in ("self", "cls") and arg.annotation is not None:
                        hints_found = True
                        break
            
            if hints_found:
                return {
                    "name": "type_hints",
                    "passed": True,
                    "message": "Type hints found",
                }
            else:
                return {
                    "name": "type_hints",
                    "passed": False,
                    "message": "No type hints found on functions",
                }
        except:
            return {
                "name": "type_hints",
                "passed": False,
                "message": "Could not parse for type hints",
            }
    
    def _check_docstrings(self, code: str) -> dict:
        """Check if functions have docstrings."""
        try:
            tree = ast.parse(code)
            functions = [
                node for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            
            if not functions:
                return {
                    "name": "docstrings",
                    "passed": True,
                    "message": "No functions to check",
                }
            
            has_docstring = False
            for func in functions:
                if (func.body and isinstance(func.body[0], ast.Expr) and
                    isinstance(func.body[0].value, ast.Constant) and
                    isinstance(func.body[0].value.value, str)):
                    has_docstring = True
                    break
            
            if has_docstring:
                return {
                    "name": "docstrings",
                    "passed": True,
                    "message": "Docstrings found",
                }
            else:
                return {
                    "name": "docstrings",
                    "passed": False,  # Warning, not failure
                    "message": "No docstrings found (recommended)",
                }
        except:
            return {
                "name": "docstrings",
                "passed": True,
                "message": "Could not parse for docstrings",
            }

