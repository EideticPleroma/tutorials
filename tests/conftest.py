"""
Pytest configuration and shared fixtures for test suite.

This module configures the Python path to enable imports from the src/
directory in tests. It's automatically loaded by pytest before running
any tests.

The path modification allows tests to use:
    from src.agent.simple_agent import Agent
    from src.multi_agent import Coordinator

Instead of complex relative imports.
"""

import sys
import os

# Add project root to path to allow 'from src.agent import ...'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

