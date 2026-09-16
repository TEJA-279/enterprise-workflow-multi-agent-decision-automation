from time import perf_counter

from langgraph.graph import END, START, StateGraph

from src.agents.planning_agent import PlanningAgent
from src.agents.research_agent import ResearchAgent
from src.agents.analysis_agent import AnalysisAgent
from src.agents.decision_agent import DecisionAgent
from src.state.workflow_state import WorkflowState


planning_agent = None
research_agent = None
analysis_agent = None
decision_agent = None


def _run_agent(
    state: WorkflowState,
    stage_name: str,
    agent,
    agent_class,
) -> WorkflowState:
    if agent is None:
        try:
            agent = agent_class()
        except Exception as exc:
            state.setdefault("errors", []).append(
                f"{stage_name.title()} Agent is not configured: {exc}"
            )
            return state

        globals()[f"{stage_name}_agent"] = agent

    return _run_stage(state, stage_name, agent)


def _run_stage(
    state: WorkflowState,
    stage_name: str,
    agent,
) -> WorkflowState:
    started_at = perf_counter()

    try:
        return agent.run(state)
    finally:
        timings = state.setdefault("stage_timings_ms", {})
        timings[stage_name] = round(
            (perf_counter() - started_at) * 1000,
            2,
        )


def planning_node(state: WorkflowState) -> WorkflowState:
    return _run_agent(
        state,
        "planning",
        planning_agent,
        PlanningAgent,
    )


def research_node(state: WorkflowState) -> WorkflowState:
    return _run_agent(
        state,
        "research",
        research_agent,
        ResearchAgent,
    )


def analysis_node(state: WorkflowState) -> WorkflowState:
    return _run_agent(
        state,
        "analysis",
        analysis_agent,
        AnalysisAgent,
    )


def decision_node(state: WorkflowState) -> WorkflowState:
    return _run_agent(
        state,
        "decision",
        decision_agent,
        DecisionAgent,
    )


def has_errors(state: WorkflowState) -> bool:
    return bool(state.get("errors", []))


def after_planning(state: WorkflowState):
    if has_errors(state):
        return END

    if not state.get("plan"):
        state.setdefault("errors", []).append(
            "Planning completed without producing a plan."
        )
        return END

    return "research"


def after_research(state: WorkflowState):
    if has_errors(state):
        return END

    if not state.get("research_results"):
        state.setdefault("errors", []).append(
            "Research completed without producing research results."
        )
        return END

    return "analysis"


def after_analysis(state: WorkflowState):
    if has_errors(state):
        return END

    if not state.get("analysis"):
        state.setdefault("errors", []).append(
            "Analysis completed without producing analysis."
        )
        return END

    return "decision"


def build_workflow():

    workflow = StateGraph(WorkflowState)

    workflow.add_node("planning", planning_node)
    workflow.add_node("research", research_node)
    workflow.add_node("analysis", analysis_node)
    workflow.add_node("decision", decision_node)

    workflow.add_edge(START, "planning")

    workflow.add_conditional_edges(
        "planning",
        after_planning,
        {
            "research": "research",
            END: END,
        },
    )

    workflow.add_conditional_edges(
        "research",
        after_research,
        {
            "analysis": "analysis",
            END: END,
        },
    )

    workflow.add_conditional_edges(
        "analysis",
        after_analysis,
        {
            "decision": "decision",
            END: END,
        },
    )

    workflow.add_edge("decision", END)

    return workflow.compile()