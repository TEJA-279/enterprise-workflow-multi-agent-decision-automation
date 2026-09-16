from langchain_groq import ChatGroq

from src.config.settings import GROQ_API_KEY
from src.state.workflow_state import WorkflowState


class PlanningAgent:

    def __init__(self):

        self.model = ChatGroq(
            model="openai/gpt-oss-20b",
            api_key=GROQ_API_KEY,
            temperature=0,
        )

    def run(self, state: WorkflowState) -> WorkflowState:

        user_query = state["user_query"]

        conversation_history = state.get(
            "conversation_history",
            [],
        )

        long_term_memories = state.get(
            "long_term_memories",
            [],
        )

        prompt = f"""
You are the Planning Agent in an enterprise multi-agent system.

Your responsibility is ONLY to create a clear plan for the user's request.

Rules:
- Break the request into actionable tasks.
- Use previous conversation when it is relevant.
- Use long-term memories when they are relevant.
- Do not perform research.
- Do not use tools.
- Do not perform analysis.
- Do not make the final decision.

Previous conversation:
{conversation_history}

Relevant long-term memories:
{long_term_memories}

Current user request:
{user_query}

Return a numbered list of tasks that the Research Agent can execute.
"""

        try:

            response = self.model.invoke(prompt)

            content = response.content

            if isinstance(content, list):
                plan = "".join(
                    item.get("text", "")
                    for item in content
                    if isinstance(item, dict)
                )
            else:
                plan = content

            state["plan"] = plan

            return state

        except Exception as exc:

            state.setdefault("errors", []).append(
                f"Planning Agent failed: {exc}"
            )

            return state