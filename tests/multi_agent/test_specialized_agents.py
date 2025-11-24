"""
Tests for specialized agents using O.V.E. methodology.

Students complete these tests as they implement agents in Exercise 2.

These tests verify that WorkerAgent subclasses correctly inherit from
Tutorial 1's Agent class and implement specialized behavior.
"""

import pytest
from src.multi_agent import SharedState
from src.multi_agent.specialized import ResearchAgent, DataAgent, WriterAgent


def test_research_agent_initialization():
    """
    Observe: Research agent initializes correctly with inheritance.
    Validate: Has name, shared_state, inherits from Agent, has filtered tools.
    """
    shared_state = SharedState()
    research = ResearchAgent(shared_state)

    # Test basic attributes
    assert research.name == "research"
    assert research.shared_state is shared_state

    # Test inheritance from Tutorial 1's Agent
    assert hasattr(research, "chat"), "Should inherit chat() from Agent"
    assert hasattr(research, "messages"), "Should inherit messages from Agent"

    # Test tool filtering
    assert research.allowed_tools == ["file_search", "read_file"]
    assert len(research.available_tools) <= 2, "Should only have allowed tools"


def test_research_agent_gathers_info():
    """
    Observe: Research agent can gather information using inherited LLM.
    Validate: Returns success status, writes to shared state.
    Evaluate: Findings are reasonable (basic check).

    TODO: Students implement this test in Lab 2 Exercise 2

    After implementing gather_info():
    1. Remove the pytest.skip() line
    2. Uncomment the test assertions
    3. Run the test to verify your implementation

    Hints:
    - gather_info() should use self.chat() to call LLM
    - Should return {"status": "success", "findings_count": N}
    - Should write findings to shared_state["research_findings"]
    - Each finding should have "fact" and "source" keys
    """
    pytest.skip("Students implement in Lab 2 Exercise 2")

    # TODO: Uncomment after implementing gather_info()
    # shared_state = SharedState()
    # research = ResearchAgent(shared_state)
    #
    # result = research.gather_info("electric vehicles")
    #
    # assert result["status"] == "success"
    # assert "findings_count" in result
    #
    # # Check shared state was updated
    # findings = shared_state.get("research_findings")
    # assert findings is not None
    # assert len(findings) >= 3  # At least 3 findings
    # assert all("fact" in f and "source" in f for f in findings)


def test_research_agent_stays_in_role():
    """
    Observe: Research agent output.
    Validate: Output contains facts, not analysis.
    Evaluate: Agent doesn't overstep boundaries.

    This test requires real LLM execution (optional evaluation test).
    """
    # TODO: Students can implement this with real LLM
    # to test that research agent doesn't analyze

    pytest.skip("Optional evaluation test with real LLM")


def test_data_agent_initialization():
    """
    Observe: Data agent initializes correctly with inheritance.
    Validate: Has name, shared_state, inherits from Agent, has filtered tools.
    """
    shared_state = SharedState()
    data = DataAgent(shared_state)

    # Test basic attributes
    assert data.name == "data"
    assert data.shared_state is shared_state

    # Test inheritance from Tutorial 1's Agent
    assert hasattr(data, "chat"), "Should inherit chat() from Agent"
    assert hasattr(data, "messages"), "Should inherit messages from Agent"

    # Test tool filtering
    assert data.allowed_tools == ["calculate"]
    assert len(data.available_tools) <= 1, "Should only have calculate tool"


def test_data_agent_analyzes_trends():
    """
    Observe: Data agent can analyze research findings using inherited LLM.
    Validate: Returns success, writes analysis to state.

    TODO: Students implement this test in Lab 2 Exercise 2

    After implementing analyze_trends():
    1. Remove the pytest.skip() line
    2. Uncomment the test assertions
    3. Run the test to verify your implementation

    Hints:
    - analyze_trends() should read from shared_state["research_findings"]
    - Should use self.chat() to ask LLM to analyze data
    - Should return {"status": "success", "metrics_count": N}
    - Should write to shared_state["data_analysis"]
    - Analysis should have "metrics" and "insights" keys
    """
    pytest.skip("Students implement in Lab 2 Exercise 2")

    # TODO: Implement this test


def test_writer_agent_initialization():
    """
    Observe: Writer agent initializes correctly with inheritance.
    Validate: Has name, shared_state, inherits from Agent, has no tools.
    """
    shared_state = SharedState()
    writer = WriterAgent(shared_state)

    # Test basic attributes
    assert writer.name == "writer"
    assert writer.shared_state is shared_state

    # Test inheritance from Tutorial 1's Agent
    assert hasattr(writer, "chat"), "Should inherit chat() from Agent"
    assert hasattr(writer, "messages"), "Should inherit messages from Agent"

    # Test tool filtering
    assert writer.allowed_tools == []  # Writer uses LLM only, no tools
    assert len(writer.available_tools) == 0, "Should have no tools"


def test_writer_agent_creates_report():
    """
    Observe: Writer agent can create formatted report using inherited LLM.
    Validate: Returns success, report has content.
    Evaluate: Report structure (headings, sections).

    TODO: Students implement this test in Lab 2 Exercise 2

    After implementing create_report():
    1. Remove the pytest.skip() line
    2. Uncomment the test assertions
    3. Run the test to verify your implementation

    Hints:
    - create_report() should read research_findings and data_analysis
    - Should use self.chat() to generate markdown report
    - Should return {"status": "success", "report": "..."}
    - Should write to shared_state["final_report"]
    - Report should have markdown headings (#, ##), sections, sources
    """
    pytest.skip("Students implement in Lab 2 Exercise 2")

    # TODO: Implement this test


def test_sequential_agent_workflow():
    """
    Integration test: Research → Data → Writer pipeline.
    Observe: All agents execute in sequence using real LLMs and tools.
    Validate: Each agent reads previous output, writes own.
    Evaluate: Final report incorporates all stages.

    TODO: Students implement this test in Lab 2 Exercise 3

    This is an integration test that verifies the full multi-agent workflow.
    Complete this after implementing all three agent methods.

    After implementing all agents:
    1. Remove the pytest.skip() line
    2. Uncomment the test code
    3. Run to verify end-to-end workflow

    Hints:
    - This tests the complete workflow from Tutorial 2
    - Research → findings → Data → analysis → Writer → report
    - Each agent should successfully complete before next starts
    - Verify data flows through shared_state correctly
    """
    pytest.skip("Students implement in Lab 2 Exercise 3")

    # TODO: Implement this test
