from unittest.mock import MagicMock

from src.agents.decision_agent import DecisionAgent
from src.state.workflow_state import WorkflowState


def test_decision_agent_updates_shared_state():

    agent = DecisionAgent()

    fake_response = MagicMock()

    fake_response.content = (
        "Recommendation: Proceed with further evaluation "
        "before expanding into Hyderabad."
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
            "Several competitors are already operating."
        ),
        "analysis": (
            "Opportunities: Growing technology sector.\n"
            "Risks: Strong competition and uncertain costs."
        ),
        "decision": "",
        "errors": [],
    }

    result = agent.run(state)

    assert result["user_query"] == (
        "Should our company expand into Hyderabad?"
    )

    assert result["analysis"] != ""

    assert "Recommendation" in result["decision"]
    assert "Hyderabad" in result["decision"]

    assert result["errors"] == []

    agent.model.invoke.assert_called_once()


def test_decision_agent_handles_missing_analysis():

    agent = DecisionAgent()

    state: WorkflowState = {
        "user_query": "Should our company expand into Hyderabad?",
        "plan": "Research the Hyderabad market.",
        "research_results": "Some research.",
        "analysis": "",
        "decision": "",
        "errors": [],
    }

    result = agent.run(state)

    assert result["decision"] == ""

    assert any(
        "analysis is missing" in error
        for error in result["errors"]
    )
def test_decision_agent_receives_long_term_memory():

    agent = DecisionAgent()

    fake_response = MagicMock()

    fake_response.content = (
        "The previous decision should be reconsidered "
        "based on the new analysis."
    )

    agent.model = MagicMock()
    agent.model.invoke.return_value = fake_response

    state = {
        "user_query": "Should we reconsider the Hyderabad expansion?",
        "conversation_history": [],
        "long_term_memories": [
            "Previous decision: Further evaluation was recommended."
        ],
        "plan": "",
        "research_results": "",
        "analysis": (
            "New market data indicates stronger competition."
        ),
        "decision": "",
        "errors": [],
    }

    result = agent.run(state)

    assert "reconsidered" in result["decision"]

    prompt_used = agent.model.invoke.call_args[0][0]

    assert "Previous decision" in prompt_used
    assert "Hyderabad expansion" in prompt_used