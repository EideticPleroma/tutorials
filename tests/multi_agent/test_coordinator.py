"""
Tests for Coordinator agent using O.V.E. methodology.

Students complete these tests as they implement the coordinator in Exercise 1.
"""

import pytest
from src.multi_agent import Coordinator, SharedState
from src.multi_agent.message_protocol import Message, MessageType


class MockWorkerAgent:
    """Mock worker agent for testing coordinator logic."""
    
    def __init__(self, name="mock", return_status="success"):
        self.name = name
        self.return_status = return_status
        self.executed_actions = []
    
    def execute(self, action, payload):
        """Record execution and return mock response."""
        self.executed_actions.append((action, payload))
        return {
            "status": self.return_status,
            "result": f"Mock {action} result"
        }
    
    def execute_message(self, request: Message) -> Message:
        """Handle message protocol."""
        result = self.execute(request.action, request.payload)
        return Message(
            from_agent=self.name,
            to_agent=request.from_agent,
            message_type=MessageType.RESPONSE if result["status"] == "success" else MessageType.ERROR,
            payload=result,
            in_reply_to=request.message_id,
            trace_id=request.trace_id
        )


def test_coordinator_initialization():
    """
    Observe: Coordinator initializes with required components.
    Validate: Has shared_state and worker placeholders.
    """
    coordinator = Coordinator()
    
    assert coordinator.shared_state is not None
    # Worker agents will be None until students implement Exercise 2
    # or assigned as mocks for testing


def test_coordinator_delegation_to_mock_agent():
    """
    Observe: Coordinator can delegate to a mock worker agent.
    Validate: Message sent, response received, correct format.
    
    Students implement coordinator.delegate() in Exercise 1.
    """
    coordinator = Coordinator()
    mock_agent = MockWorkerAgent(name="research")
    
    # TODO: Students uncomment and make this work in Exercise 1
    # result = coordinator.delegate(
    #     agent=mock_agent,
    #     action="gather_info",
    #     payload={"query": "test"}
    # )
    # 
    # assert result["status"] == "success"
    # assert len(mock_agent.executed_actions) == 1
    # assert mock_agent.executed_actions[0][0] == "gather_info"
    
    # Placeholder for students to implement
    pytest.skip("Students implement delegate() in Exercise 1")


def test_coordinator_sequential_workflow():
    """
    Observe: Coordinator executes agents in correct sequence.
    Validate: Research → Data → Writer order maintained.
    
    Students implement coordinator.generate_report() in Exercise 1.
    """
    coordinator = Coordinator()
    
    # Setup mock agents that track execution order
    execution_order = []
    
    class TrackingAgent(MockWorkerAgent):
        def execute(self, action, payload):
            execution_order.append(self.name)
            return super().execute(action, payload)
    
    coordinator.research = TrackingAgent("research")
    coordinator.data = TrackingAgent("data")
    coordinator.writer = TrackingAgent("writer")
    
    # TODO: Students uncomment in Exercise 1
    # coordinator.generate_report("test query")
    # assert execution_order == ["research", "data", "writer"]
    
    pytest.skip("Students implement generate_report() in Exercise 1")


def test_coordinator_handles_agent_failure():
    """
    Observe: Coordinator behavior when agent fails.
    Validate: Error handled gracefully, doesn't crash.
    Evaluate: Returns meaningful error to user.
    """
    coordinator = Coordinator()
    
    # Mock agent that fails
    failing_agent = MockWorkerAgent("research", return_status="error")
    coordinator.research = failing_agent
    
    # TODO: Students implement error handling in Exercise 1
    # result = coordinator.generate_report("test query")
    # 
    # # Should return error, not crash
    # assert "error" in result.lower() or result.startswith("Error")
    
    pytest.skip("Students implement error handling in Exercise 1")


def test_coordinator_with_real_agents():
    """
    Integration test: Coordinator with real specialized agents.
    
    Students complete this after Exercise 2 (real agents implemented).
    """
    from src.multi_agent.specialized import ResearchAgent, DataAgent, WriterAgent
    
    shared_state = SharedState()
    coordinator = Coordinator(shared_state)
    
    coordinator.research = ResearchAgent(shared_state)
    coordinator.data = DataAgent(shared_state)
    coordinator.writer = WriterAgent(shared_state)
    
    # TODO: Students uncomment after Exercise 2
    # report = coordinator.generate_report("Analyze EV market")
    # 
    # assert isinstance(report, str)
    # assert len(report) > 100  # Substantial report
    # 
    # # Check state was updated
    # assert shared_state.get("research_findings") is not None
    # assert shared_state.get("data_analysis") is not None
    # assert shared_state.get("final_report") is not None
    
    pytest.skip("Students complete after Exercise 2")

