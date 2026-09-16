from langchain_groq import ChatGroq

from src.config.settings import GROQ_API_KEY
from src.state.workflow_state import WorkflowState
from src.tools.tool_registry import TOOLS


class ResearchAgent:

    @staticmethod
    def _content_to_text(content) -> str:
        if isinstance(content, list):
            return "".join(
                item.get("text", "")
                for item in content
                if isinstance(item, dict)
            )

        return str(content)

    def __init__(self):

        self.model = ChatGroq(
            model="openai/gpt-oss-20b",
            api_key=GROQ_API_KEY,
            temperature=0,
        )

        self.model_with_tools = self.model.bind_tools(TOOLS)

        self.tools_by_name = {
            tool.name: tool
            for tool in TOOLS
        }

    def run(self, state: WorkflowState) -> WorkflowState:

        plan = state.get("plan", "")

        prompt = f"""
You are the Research Agent in an enterprise multi-agent system.

Your responsibility is to collect information required by the plan.

Rules:
- Follow the provided plan.
- Use available tools when appropriate.
- Do not make the final business decision.
- Do not perform the final analysis.
- Clearly report the information you found.
- If information cannot be obtained, report the limitation.

Plan:
{plan}

Provide the research findings in a clear, structured format.
"""

        try:

            response = self.model_with_tools.invoke(prompt)

            # Get actual tool calls safely.
            tool_calls = getattr(response, "tool_calls", None)

            if isinstance(tool_calls, list) and tool_calls:

                tool_results = []

                for tool_call in tool_calls:

                    tool_name = tool_call.get("name", "unknown")
                    tool_args = tool_call.get("args", {})

                    tool = self.tools_by_name.get(tool_name)

                    if tool is None:

                        tool_results.append(
                            f"Tool '{tool_name}' is not available."
                        )

                        continue

                    try:

                        result = tool.invoke(tool_args)

                        tool_results.append(
                            f"{tool_name} result: {result}"
                        )

                    except Exception as exc:

                        tool_results.append(
                            f"{tool_name} failed: {exc}"
                        )

                tool_context = "\n".join(tool_results)
                follow_up_prompt = f"""
You are completing the research phase.

Original plan:
{plan}

Tool results:
{tool_context}

Interpret the tool results and return clear, structured research findings.
Do not make the final business decision.
"""
                follow_up_response = self.model.invoke(
                    follow_up_prompt
                )
                research_results = self._content_to_text(
                    follow_up_response.content
                )

                if not research_results.strip():
                    research_results = tool_context

            else:

                content = response.content

                research_results = self._content_to_text(content)

            if not research_results.strip():

                research_results = (
                    "No research findings were produced."
                )

            state["research_results"] = research_results

            return state

        except Exception as exc:

            state.setdefault("errors", []).append(
                f"Research Agent failed: {exc}"
            )

            return state