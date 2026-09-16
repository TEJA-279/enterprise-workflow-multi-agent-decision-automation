from langchain_groq import ChatGroq

from src.config.settings import GROQ_API_KEY
from src.prompts.business_prompts import business_prompt
from src.tools.tool_registry import TOOLS


class BusinessAgent:

    def __init__(self, model=None):

        self.model = model or ChatGroq(
            model="openai/gpt-oss-20b",
            api_key=GROQ_API_KEY,
            temperature=0,
        )

        self.model_with_tools = self.model.bind_tools(TOOLS)

        self.tools_by_name = {
            tool.name: tool
            for tool in TOOLS
        }

        self.chain = business_prompt | self.model_with_tools

    def ask(self, question: str):

        messages = [
            {
                "role": "user",
                "content": question,
            }
        ]

        response = self.model_with_tools.invoke(messages)

        while response.tool_calls:

            messages.append(response)

            for tool_call in response.tool_calls:

                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                tool = self.tools_by_name.get(tool_name)

                if tool is None:
                    raise ValueError(
                        f"Unknown tool requested: {tool_name}"
                    )

                try:
                    tool_result = tool.invoke(tool_args)

                except Exception as exc:
                    tool_result = (
                        f"Tool '{tool_name}' failed: {exc}"
                    )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": str(tool_result),
                    }
                )

            response = self.model_with_tools.invoke(messages)

        content = response.content

        if isinstance(content, list):
            return "".join(
                item.get("text", "")
                for item in content
                if isinstance(item, dict)
            )

        return str(content)