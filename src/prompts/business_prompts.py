from langchain_core.prompts import ChatPromptTemplate


business_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a helpful business AI assistant.

Answer every question in simple and clear English.
Give concise answers suitable for beginners.
"""
    ),
    (
        "human",
        "{question}"
    )
])