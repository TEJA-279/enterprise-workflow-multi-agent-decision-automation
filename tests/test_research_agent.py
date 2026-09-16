from unittest.mock import MagicMock

from src.agents.research_agent import ResearchAgent
from src.state.workflow_state import WorkflowState


def test_research_agent_updates_shared_state():

    agent = ResearchAgent()

    fake_response = MagicMock()

    fake_response.content = (
        "Hyderabad has a growing technology sector.\n"
        "Several competitors are already operating in the market."
    )

    agent.model_with_tools = MagicMock()
    agent.model_with_tools.invoke.return_value = fake_response

    state: WorkflowState = {
        "user_query": "Should our company expand into Hyderabad?",
        "plan": (
            "1. Research the Hyderabad market.\n"
            "2. Identify competitors."
        ),
        "research_results": "",
        "analysis": "",
        "decision": "",
        "errors": [],
    }

    result = agent.run(state)

    assert result["plan"] == (
        "1. Research the Hyderabad market.\n"
        "2. Identify competitors."
    )

    assert "Hyderabad" in result["research_results"]
    assert "competitors" in result["research_results"]

    assert result["analysis"] == ""
    assert result["decision"] == ""

    assert result["errors"] == []

    agent.model_with_tools.invoke.assert_called_once()


def test_research_agent_interprets_tool_results():

    agent = ResearchAgent()

    tool_response = MagicMock()
    tool_response.tool_calls = [
        {
            "name": "calculator",
            "args": {"expression": "25 * 4"},
        }
    ]
    tool_response.content = ""

    final_response = MagicMock()
    final_response.content = "The calculation result is 100."

    agent.model_with_tools = MagicMock()
    agent.model_with_tools.invoke.return_value = tool_response
    agent.model = MagicMock()
    agent.model.invoke.return_value = final_response

    result = agent.run(
        {
            "user_query": "Calculate 25 * 4.",
            "plan": "Calculate the requested value.",
            "research_results": "",
            "analysis": "",
            "decision": "",
            "errors": [],
        }
    )

    assert result["research_results"] == (
        "The calculation result is 100."
    )
    agent.model.invoke.assert_called_once()