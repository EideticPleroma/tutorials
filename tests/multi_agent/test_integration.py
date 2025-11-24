"""
Integration tests for multi-agent coordinator workflows.

These tests verify the complete coordinator → workers flow
using the message protocol and shared state.

Students complete these in Lab 2 Exercise 3 and 4.
"""

import pytest
from src.multi_agent import SharedState, Coordinator
from src.multi_agent.specialized import ResearchAgent, DataAgent, WriterAgent


def test_coordinator_delegates_to_workers():
    """
    Integration test: Coordinator delegates to worker agents.
    
    TODO: Students implement this test in Lab 2 Exercise 3
    
    After implementing coordinator delegation:
    1. Remove the pytest.skip() line
    2. Uncomment the test code
    3. Run to verify coordinator → worker communication
    
    Hints:
    - Coordinator should delegate tasks to appropriate workers
    - Each worker should execute and return results
    - Coordinator should aggregate results
    - Message protocol should be used for communication
    """
    pytest.skip("Students implement in Lab 2 Exercise 3")
    
    # TODO: Uncomment after implementing coordinator
    # shared_state = SharedState()
    # 
    # # Create coordinator and workers
    # research = ResearchAgent(shared_state)
    # data = DataAgent(shared_state)
    # writer = WriterAgent(shared_state)
    # 
    # coordinator = Coordinator(shared_state, {
    #     "research": research,
    #     "data": data,
    #     "writer": writer
    # })
    # 
    # # Test delegation
    # result = coordinator.process_request("Create market analysis report on EVs")
    # 
    # assert result["status"] == "success"
    # assert "report" in result or "output" in result


def test_full_research_workflow():
    """
    Integration test: Complete research → analysis → report workflow.
    
    TODO: Students implement this test in Lab 2 Exercise 4 (Challenge)
    
    This is the final challenge integration test that verifies the
    complete multi-agent system works end-to-end.
    
    After completing Lab 2 Challenge:
    1. Remove the pytest.skip() line
    2. Uncomment the test code
    3. Run to verify your complete system
    
    Hints:
    - Start with coordinator receiving user request
    - Coordinator delegates to research agent
    - Research gathers info, stores in shared_state
    - Coordinator delegates to data agent
    - Data analyzes findings, stores in shared_state
    - Coordinator delegates to writer agent
    - Writer creates report, stores in shared_state
    - Coordinator returns final report to user
    """
    pytest.skip("Students implement in Lab 2 Exercise 4 (Challenge)")
    
    # TODO: Uncomment after completing Challenge exercise
    # shared_state = SharedState()
    # 
    # # Create complete multi-agent system
    # research = ResearchAgent(shared_state)
    # data = DataAgent(shared_state)
    # writer = WriterAgent(shared_state)
    # 
    # coordinator = Coordinator(shared_state, {
    #     "research": research,
    #     "data": data,
    #     "writer": writer
    # })
    # 
    # # Execute full workflow
    # user_request = "Generate a comprehensive market analysis report on electric vehicles"
    # result = coordinator.process_request(user_request)
    # 
    # # Validate workflow completion
    # assert result["status"] == "success"
    # 
    # # Validate all stages completed
    # assert shared_state.get("research_findings") is not None, "Research should complete"
    # assert shared_state.get("data_analysis") is not None, "Data analysis should complete"
    # assert shared_state.get("final_report") is not None, "Report should be generated"
    # 
    # # Evaluate final output
    # report = shared_state.get("final_report")
    # assert len(report) > 300, "Report should have substantial content"
    # assert "##" in report, "Report should have markdown sections"
    # assert "source" in report.lower(), "Report should cite sources"


def test_error_handling_in_workflow():
    """
    Integration test: System handles errors gracefully.
    
    TODO: Students implement this test in Lab 2 Exercise 3
    
    Tests that errors in one agent don't crash the whole system.
    
    After implementing error handling:
    1. Remove the pytest.skip() line
    2. Uncomment the test code
    3. Run to verify error handling
    
    Hints:
    - Test what happens when shared_state is empty
    - Test what happens when an agent fails
    - Coordinator should return error status, not crash
    - Error messages should be informative
    """
    pytest.skip("Students implement in Lab 2 Exercise 3")
    
    # TODO: Uncomment after implementing error handling
    # shared_state = SharedState()
    # 
    # # Test data agent with no research findings
    # data = DataAgent(shared_state)
    # result = data.analyze_trends()
    # 
    # assert result["status"] == "error"
    # assert "error" in result
    # assert "research findings" in result["error"].lower()
    # 
    # # Test writer with no data
    # writer = WriterAgent(shared_state)
    # result = writer.create_report()
    # 
    # assert result["status"] == "error"
    # assert "error" in result

