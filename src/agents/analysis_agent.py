from langchain_groq import ChatGroq

from src.config.settings import GROQ_API_KEY
from src.state.workflow_state import WorkflowState


class AnalysisAgent:

    def __init__(self):

        self.model = ChatGroq(
            model="openai/gpt-oss-20b",
            api_key=GROQ_API_KEY,
            temperature=0,
        )

    def run(self, state: WorkflowState) -> WorkflowState:

        research_results = state.get("research_results", "")

        if not research_results:
            state.setdefault("errors", []).append(
                "Analysis Agent cannot run because research results are missing."
            )
            return state

        prompt = f"""
You are the Analysis Agent in an enterprise multi-agent system.

Your responsibility is ONLY to analyze the research results.

Rules:
- Identify important findings.
- Identify opportunities.
- Identify risks.
- Identify missing or uncertain information.
- Do not perform new research.
- Do not use external tools.
- Do not make the final business decision.
- Base the analysis only on the provided research.

Research results:
{research_results}

Return a clear and structured analysis.
"""

        try:
            response = self.model.invoke(prompt)

            content = response.content

            if isinstance(content, list):
                analysis = "".join(
                    item.get("text", "")
                    for item in content
                    if isinstance(item, dict)
                )
            else:
                analysis = str(content)

            state["analysis"] = analysis

            return state

        except Exception as exc:

            state.setdefault("errors", []).append(
                f"Analysis Agent failed: {exc}"
            )

            return state