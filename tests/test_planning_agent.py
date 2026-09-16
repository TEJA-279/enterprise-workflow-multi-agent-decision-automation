from unittest.mock import MagicMock

from src.agents.planning_agent import PlanningAgent
from src.state.workflow_state import WorkflowState


def test_planning_agent_updates_shared_state():

    agent = PlanningAgent()

    fake_response = MagicMock()

    fake_response.content = (
        "1. Research the Hyderabad market.\n"
        "2. Identify competitors.\n"
        "3. Analyze risks and opportunities."
    )

    agent.model = MagicMock()
    agent.model.invoke.return_value = fake_response

    state: WorkflowState = {
        "user_query": "Should our company expand into Hyderabad?",
        "plan": "",
        "research_results": "",
        "analysis": "",
        "decision": "",
        "errors": [],
    }

    result = agent.run(state)

    assert result["user_query"] == (
        "Should our company expand into Hyderabad?"
    )

    assert "Research the Hyderabad market" in result["plan"]

    assert result["research_results"] == ""
    assert result["analysis"] == ""
    assert result["decision"] == ""

    assert result["errors"] == []

    agent.model.invoke.assert_called_once()