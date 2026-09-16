from src.state.workflow_state import WorkflowState


def test_workflow_state_contains_shared_fields():

    state: WorkflowState = {
        "user_query": "Should we expand into Hyderabad?",
        "plan": "",
        "research_results": "",
        "analysis": "",
        "decision": "",
        "errors": [],
    }

    assert state["user_query"] == "Should we expand into Hyderabad?"
    assert state["plan"] == ""
    assert state["research_results"] == ""
    assert state["analysis"] == ""
    assert state["decision"] == ""
    assert state["errors"] == []