from time import perf_counter
from uuid import uuid4

from src.memory.long_term import LongTermMemory
from src.memory.short_term import ShortTermMemory
from src.state.workflow_state import WorkflowState
from src.workflows.multi_agent_workflow import build_workflow


class MemoryWorkflow:

    def __init__(
        self,
        long_term_database: str = "memory.db",
    ):

        self.short_term_memory = ShortTermMemory()

        self.long_term_memory = LongTermMemory(
            long_term_database
        )

        self.workflow = build_workflow()

    def run(
        self,
        session_id: str,
        user_query: str,
    ) -> WorkflowState:

        conversation_history = self.short_term_memory.get_messages(
            session_id
        )

        if not conversation_history:
            conversation_history = (
                self.long_term_memory.retrieve_messages(
                    session_id
                )
            )

        long_term_memories = (
            self.long_term_memory.retrieve(
                session_id,
                "decision",
            )
        )

        self.short_term_memory.add_message(
            session_id,
            "user",
            user_query,
        )

        self.long_term_memory.save_message(
            session_id,
            "user",
            user_query,
        )

        state: WorkflowState = {
            "run_id": uuid4().hex,
            "user_query": user_query,
            "conversation_history": conversation_history,
            "long_term_memories": long_term_memories,
            "plan": "",
            "research_results": "",
            "analysis": "",
            "decision": "",
            "errors": [],
            "stage_timings_ms": {},
        }

        started_at = perf_counter()
        result = self.workflow.invoke(state)
        result["stage_timings_ms"]["total"] = round(
            (perf_counter() - started_at) * 1000,
            2,
        )

        decision = result.get("decision", "")

        if decision:

            self.short_term_memory.add_message(
                session_id,
                "assistant",
                decision,
            )

            self.long_term_memory.save_message(
                session_id,
                "assistant",
                decision,
            )

            self.long_term_memory.save(
                session_id,
                "decision",
                decision,
            )

        return result