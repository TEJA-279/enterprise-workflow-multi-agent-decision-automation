from unittest.mock import MagicMock

from src.agents.business_agent import BusinessAgent


def create_mock_response(tool_name: str):
    response = MagicMock()

    response.tool_calls = [
        {
            "name": tool_name,
            "args": {},
        }
    ]

    return response


def test_agent_can_select_calculator():

    agent = BusinessAgent()

    agent.chain = MagicMock()

    agent.chain.invoke.return_value = create_mock_response(
        "calculator"
    )

    response = agent.chain.invoke(
        {
            "question": "Calculate 25 * 4"
        }
    )

    assert response.tool_calls

    assert response.tool_calls[0]["name"] == "calculator"


def test_agent_can_select_weather():

    agent = BusinessAgent()

    agent.chain = MagicMock()

    agent.chain.invoke.return_value = create_mock_response(
        "weather"
    )

    response = agent.chain.invoke(
        {
            "question": "What is the weather in Hyderabad?"
        }
    )

    assert response.tool_calls

    assert response.tool_calls[0]["name"] == "weather"


def test_agent_can_select_currency():

    agent = BusinessAgent()

    agent.chain = MagicMock()

    agent.chain.invoke.return_value = create_mock_response(
        "currency_converter"
    )

    response = agent.chain.invoke(
        {
            "question": "Convert 100 INR to USD"
        }
    )

    assert response.tool_calls

    assert response.tool_calls[0]["name"] == "currency_converter"