from unittest.mock import MagicMock, patch

from src.workflows.multi_agent_workflow import build_workflow


def test_complete_multi_agent_workflow():

    planning_result = {
        "user_query": "Should our company expand into Hyderabad?",
        "plan": (
            "1. Research Hyderabad market.\n"
            "2. Identify competitors.\n"
            "3. Evaluate risks."
        ),
        "research_results": "",
        "analysis": "",
        "decision": "",
        "errors": [],
    }

    research_result = {
        **planning_result,
        "research_results": (
            "Hyderabad has a growing technology sector. "
            "Competition is strong."
        ),
    }

    analysis_result = {
        **research_result,
        "analysis": (
            "Opportunity: growing technology sector.\n"
            "Risk: strong competition."
        ),
    }

    decision_result = {
        **analysis_result,
        "decision": (
            "Recommendation: conduct further evaluation "
            "before expansion."
        ),
    }

    with patch(
        "src.workflows.multi_agent_workflow.planning_agent"
    ) as planning, patch(
        "src.workflows.multi_agent_workflow.research_agent"
    ) as research, patch(
        "src.workflows.multi_agent_workflow.analysis_agent"
    ) as analysis, patch(
        "src.workflows.multi_agent_workflow.decision_agent"
    ) as decision:

        planning.run.return_value = planning_result
        research.run.return_value = research_result
        analysis.run.return_value = analysis_result
        decision.run.return_value = decision_result

        workflow = build_workflow()

        result = workflow.invoke(
            {
                "user_query": (
                    "Should our company expand into Hyderabad?"
                ),
                "plan": "",
                "research_results": "",
                "analysis": "",
                "decision": "",
                "errors": [],
            }
        )

        assert result["plan"] != ""
        assert result["research_results"] != ""
        assert result["analysis"] != ""
        assert result["decision"] != ""

        assert "Recommendation" in result["decision"]

        assert result["errors"] == []

        planning.run.assert_called_once()
        research.run.assert_called_once()
        analysis.run.assert_called_once()
        decision.run.assert_called_once()