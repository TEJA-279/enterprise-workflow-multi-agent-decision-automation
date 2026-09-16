from typing import TypedDict


class WorkflowState(TypedDict, total=False):
    """
    Shared state passed between all agents.
    """

    user_query: str

    conversation_history: list[dict]
    long_term_memories: list[str]

    plan: str

    research_results: str

    analysis: str

    decision: str

    errors: list[str]

    run_id: str

    stage_timings_ms: dict[str, float]