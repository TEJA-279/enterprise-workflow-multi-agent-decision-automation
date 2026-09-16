from unittest.mock import MagicMock, patch

from src.workflows.multi_agent_workflow import build_workflow


def test_workflow_runs_agents_in_order():

    with patch(
        "src.workflows.multi_agent_workflow.planning_agent"
    ) as planning, patch(
        "src.workflows.multi_agent_workflow.research_agent"
    ) as research, patch(
        "src.workflows.multi_agent_workflow.analysis_agent"
    ) as analysis, patch(
        "src.workflows.multi_agent_workflow.decision_agent"
    ) as decision:

        planning_state = {
            "user_query": "Should we expand into Hyderabad?",
            "plan": "Research market and competitors.",
            "research_results": "",
            "analysis": "",
            "decision": "",
            "errors": [],
        }

        research_state = {
            **planning_state,
            "research_results": "Growing market with strong competition.",
        }

        analysis_state = {
            **research_state,
            "analysis": "Good opportunity but competition is a major risk.",
        }

        decision_state = {
            **analysis_state,
            "decision": "Proceed with further evaluation.",
        }

        planning.run.return_value = planning_state
        research.run.return_value = research_state
        analysis.run.return_value = analysis_state
        decision.run.return_value = decision_state

        workflow = build_workflow()

        result = workflow.invoke(
            {
                "user_query": "Should we expand into Hyderabad?",
                "plan": "",
                "research_results": "",
                "analysis": "",
                "decision": "",
                "errors": [],
            }
        )

        assert result["plan"] == (
            "Research market and competitors."
        )

        assert result["research_results"] == (
            "Growing market with strong competition."
        )

        assert result["analysis"] == (
            "Good opportunity but competition is a major risk."
        )

        assert result["decision"] == (
            "Proceed with further evaluation."
        )

        planning.run.assert_called_once()
        research.run.assert_called_once()
        analysis.run.assert_called_once()
        decision.run.assert_called_once()
def test_workflow_stops_when_planning_fails():

    with patch(
        "src.workflows.multi_agent_workflow.planning_agent"
    ) as planning, patch(
        "src.workflows.multi_agent_workflow.research_agent"
    ) as research:

        planning.run.return_value = {
            "user_query": "Should we expand into Hyderabad?",
            "plan": "",
            "research_results": "",
            "analysis": "",
            "decision": "",
            "errors": ["Planning Agent failed."],
        }

        workflow = build_workflow()

        result = workflow.invoke(
            {
                "user_query": "Should we expand into Hyderabad?",
                "plan": "",
                "research_results": "",
                "analysis": "",
                "decision": "",
                "errors": [],
            }
        )

        assert result["errors"] == [
            "Planning Agent failed."
        ]

        research.run.assert_not_called()


def test_workflow_stops_when_research_fails():

    with patch(
        "src.workflows.multi_agent_workflow.planning_agent"
    ) as planning, patch(
        "src.workflows.multi_agent_workflow.research_agent"
    ) as research, patch(
        "src.workflows.multi_agent_workflow.analysis_agent"
    ) as analysis:

        planning.run.return_value = {
            "user_query": "Should we expand into Hyderabad?",
            "plan": "Research the Hyderabad market.",
            "research_results": "",
            "analysis": "",
            "decision": "",
            "errors": [],
        }

        research.run.return_value = {
            "user_query": "Should we expand into Hyderabad?",
            "plan": "Research the Hyderabad market.",
            "research_results": "",
            "analysis": "",
            "decision": "",
            "errors": ["Research Agent failed."],
        }

        workflow = build_workflow()

        result = workflow.invoke(
            {
                "user_query": "Should we expand into Hyderabad?",
                "plan": "",
                "research_results": "",
                "analysis": "",
                "decision": "",
                "errors": [],
            }
        )

        assert result["errors"] == [
            "Research Agent failed."
        ]

        analysis.run.assert_not_called()