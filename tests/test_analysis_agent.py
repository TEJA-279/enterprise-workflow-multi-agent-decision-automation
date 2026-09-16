from unittest.mock import MagicMock

from src.agents.analysis_agent import AnalysisAgent
from src.state.workflow_state import WorkflowState


def test_analysis_agent_updates_shared_state():

    agent = AnalysisAgent()

    fake_response = MagicMock()

    fake_response.content = (
        "Opportunities: Growing technology sector.\n"
        "Risks: Strong competition.\n"
        "Conclusion: Further evaluation is required."
    )

    agent.model = MagicMock()
    agent.model.invoke.return_value = fake_response

    state: WorkflowState = {
        "user_query": "Should our company expand into Hyderabad?",
        "plan": (
            "1. Research the Hyderabad market.\n"
            "2. Identify competitors."
        ),
        "research_results": (
            "Hyderabad has a growing technology sector.\n"
            "Several competitors are already operating in the market."
        ),
        "analysis": "",
        "decision": "",
        "errors": [],
    }

    result = agent.run(state)

    assert result["user_query"] == (
        "Should our company expand into Hyderabad?"
    )

    assert result["plan"] != ""

    assert result["research_results"] != ""

    assert "Opportunities" in result["analysis"]
    assert "Risks" in result["analysis"]
    assert "competition" in result["analysis"]

    assert result["decision"] == ""
    assert result["errors"] == []

    agent.model.invoke.assert_called_once()
def test_analysis_agent_handles_missing_research():

    agent = AnalysisAgent()

    state: WorkflowState = {
        "user_query": "Should our company expand into Hyderabad?",
        "plan": "Research the Hyderabad market.",
        "research_results": "",
        "analysis": "",
        "decision": "",
        "errors": [],
    }

    result = agent.run(state)

    assert result["analysis"] == ""

    assert any(
        "research results are missing" in error
        for error in result["errors"]
    )