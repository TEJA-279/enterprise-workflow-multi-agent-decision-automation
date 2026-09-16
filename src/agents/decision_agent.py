from langchain_groq import ChatGroq

from src.config.settings import GROQ_API_KEY
from src.state.workflow_state import WorkflowState


class DecisionAgent:

    def __init__(self):

        self.model = ChatGroq(
            model="openai/gpt-oss-20b",
            api_key=GROQ_API_KEY,
            temperature=0,
        )

    def run(self, state: WorkflowState) -> WorkflowState:

        user_query = state.get("user_query", "")
        analysis = state.get("analysis", "")

        conversation_history = state.get(
            "conversation_history",
            [],
        )

        long_term_memories = state.get(
            "long_term_memories",
            [],
        )

        if not analysis:

            state.setdefault("errors", []).append(
                "Decision Agent cannot run because analysis is missing."
            )

            return state

        prompt = f"""
You are the final response agent in an enterprise multi-agent system.

Your responsibility is to provide the best final answer to the user's
original request using the available analysis.

Rules:
- Answer the original user request directly.
- Use the provided analysis.
- Use previous conversation when relevant.
- Use long-term memories when relevant.
- Respect the user's requested response length and format.
- If the user asks for a short answer, provide a short answer.
- If the user asks for one sentence, provide exactly one sentence.
- If the user asks for a detailed answer, provide an appropriately detailed answer.
- Do not automatically give a business recommendation.
- Give recommendations only when the user asks for advice, a decision,
  a recommendation, or a business strategy.
- Mention risks or limitations only when they are relevant to the request.
- Do not perform new research.
- Do not use external tools.
- Do not invent unsupported facts.
- Do not add unnecessary headings, explanations, or conclusions when
  the user requests a simple answer.

Original user request:
{user_query}

Previous conversation:
{conversation_history}

Previous long-term decisions:
{long_term_memories}

Current analysis:
{analysis}

Provide the final answer that best matches the user's request.
"""

        try:

            response = self.model.invoke(prompt)

            content = response.content

            if isinstance(content, list):

                decision = "".join(
                    item.get("text", "")
                    for item in content
                    if isinstance(item, dict)
                )

            else:

                decision = str(content)

            state["decision"] = decision

            return state

        except Exception as exc:

            state.setdefault("errors", []).append(
                f"Decision Agent failed: {exc}"
            )

            return state