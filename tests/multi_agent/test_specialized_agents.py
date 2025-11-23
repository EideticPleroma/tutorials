"""
Tests for specialized agents using O.V.E. methodology.

Students complete these tests as they implement agents in Exercise 2.
"""

import pytest
from src.multi_agent import SharedState
from src.multi_agent.specialized import ResearchAgent, DataAgent, WriterAgent


def test_research_agent_initialization():
    """
    Observe: Research agent initializes correctly.
    Validate: Has name, shared_state, system_prompt.
    """
    shared_state = SharedState()
    research = ResearchAgent(shared_state)
    
    assert research.name == "research"
    assert research.shared_state is shared_state
    assert research.system_prompt is not None


def test_research_agent_gathers_info():
    """
    Observe: Research agent can gather information.
    Validate: Returns success status, writes to shared state.
    Evaluate: Findings are reasonable (basic check).
    
    Students implement gather_info() in Exercise 2.
    """
    shared_state = SharedState()
    research = ResearchAgent(shared_state)
    
    result = research.gather_info("electric vehicles")
    
    assert result["status"] == "success"
    assert "findings_count" in result
    
    # Check shared state was updated
    findings = shared_state.get("research_findings")
    assert findings is not None
    assert len(findings) >= 3  # At least 3 findings


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
    Observe: Data agent initializes correctly.
    Validate: Has name, shared_state, system_prompt.
    """
    shared_state = SharedState()
    data = DataAgent(shared_state)
    
    assert data.name == "data"
    assert data.shared_state is shared_state
    assert data.system_prompt is not None


def test_data_agent_analyzes_trends():
    """
    Observe: Data agent can analyze research findings.
    Validate: Returns success, writes analysis to state.
    
    Students implement analyze_trends() in Exercise 2.
    """
    shared_state = SharedState()
    
    # Setup: Add research findings
    shared_state.set("research_findings", [
        {"fact": "EV sales: 10M units", "source": "IEA"},
        {"fact": "Growth: 55%", "source": "IEA"}
    ])
    
    data = DataAgent(shared_state)
    result = data.analyze_trends()
    
    assert result["status"] == "success"
    assert "metrics_count" in result
    
    # Check analysis was written
    analysis = shared_state.get("data_analysis")
    assert analysis is not None
    assert "metrics" in analysis


def test_writer_agent_initialization():
    """
    Observe: Writer agent initializes correctly.
    Validate: Has name, shared_state, system_prompt.
    """
    shared_state = SharedState()
    writer = WriterAgent(shared_state)
    
    assert writer.name == "writer"
    assert writer.shared_state is shared_state
    assert writer.system_prompt is not None


def test_writer_agent_creates_report():
    """
    Observe: Writer agent can create formatted report.
    Validate: Returns success, report has content.
    Evaluate: Report structure (headings, sections).
    
    Students implement create_report() in Exercise 2.
    """
    shared_state = SharedState()
    
    # Setup: Add research and analysis
    shared_state.set("research_findings", [
        {"fact": "Finding 1", "source": "source1"},
        {"fact": "Finding 2", "source": "source2"}
    ])
    shared_state.set("data_analysis", {
        "metrics": {"count": 2},
        "insights": ["Insight 1"]
    })
    
    writer = WriterAgent(shared_state)
    result = writer.create_report()
    
    assert result["status"] == "success"
    assert "report" in result
    
    report = result["report"]
    assert len(report) > 100  # Substantial content
    assert "#" in report  # Has markdown headings
    
    # Check written to state
    final_report = shared_state.get("final_report")
    assert final_report is not None


def test_sequential_agent_workflow():
    """
    Integration test: Research → Data → Writer pipeline.
    Observe: All agents execute in sequence.
    Validate: Each agent reads previous output, writes own.
    Evaluate: Final report incorporates all stages.
    """
    shared_state = SharedState()
    
    # Step 1: Research
    research = ResearchAgent(shared_state)
    r_result = research.gather_info("EV market")
    assert r_result["status"] == "success"
    
    # Step 2: Data
    data = DataAgent(shared_state)
    d_result = data.analyze_trends()
    assert d_result["status"] == "success"
    
    # Step 3: Writer
    writer = WriterAgent(shared_state)
    w_result = writer.create_report()
    assert w_result["status"] == "success"
    
    # Validate pipeline
    assert shared_state.get("research_findings") is not None
    assert shared_state.get("data_analysis") is not None
    assert shared_state.get("final_report") is not None

