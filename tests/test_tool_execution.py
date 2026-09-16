from unittest.mock import MagicMock

from src.agents.business_agent import BusinessAgent


def test_calculator_tool_execution():
    agent = BusinessAgent()

    first_response = MagicMock()
    first_response.tool_calls = [
        {
            "name": "calculator",
            "args": {
                "expression": "25 * 4"
            },
            "id": "call_1",
        }
    ]
    first_response.content = ""

    second_response = MagicMock()
    second_response.tool_calls = []
    second_response.content = "The answer is 100."

    fake_model = MagicMock()
    fake_model.invoke.side_effect = [
        first_response,
        second_response,
    ]

    agent.model_with_tools = fake_model

    result = agent.ask("Calculate 25 * 4")

    assert result == "The answer is 100."
    assert fake_model.invoke.call_count == 2


def test_currency_tool_execution():
    agent = BusinessAgent()

    first_response = MagicMock()
    first_response.tool_calls = [
        {
            "name": "currency_converter",
            "args": {
                "amount": 100,
                "from_currency": "INR",
                "to_currency": "USD",
            },
            "id": "call_2",
        }
    ]
    first_response.content = ""

    second_response = MagicMock()
    second_response.tool_calls = []
    second_response.content = "100 INR is approximately 1.25 USD."

    fake_model = MagicMock()
    fake_model.invoke.side_effect = [
        first_response,
        second_response,
    ]

    agent.model_with_tools = fake_model

    result = agent.ask("Convert 100 INR to USD")

    assert "100 INR" in result
    assert "1.25 USD" in result
    assert fake_model.invoke.call_count == 2


def test_weather_tool_execution():
    agent = BusinessAgent()

    first_response = MagicMock()
    first_response.tool_calls = [
        {
            "name": "weather",
            "args": {
                "city": "Hyderabad"
            },
            "id": "call_3",
        }
    ]
    first_response.content = ""

    second_response = MagicMock()
    second_response.tool_calls = []
    second_response.content = (
        "The current temperature in Hyderabad is 30.5°C."
    )

    fake_model = MagicMock()
    fake_model.invoke.side_effect = [
        first_response,
        second_response,
    ]

    agent.model_with_tools = fake_model

    result = agent.ask(
        "What is the weather in Hyderabad?"
    )

    assert "Hyderabad" in result
    assert "30.5" in result
    assert fake_model.invoke.call_count == 2

def test_tool_error_is_handled():
    agent = BusinessAgent()

    first_response = MagicMock()
    first_response.tool_calls = [
        {
            "name": "calculator",
            "args": {
                "expression": "10 / 0"
            },
            "id": "call_error_1",
        }
    ]
    first_response.content = ""

    second_response = MagicMock()
    second_response.tool_calls = []
    second_response.content = (
        "The calculation could not be completed because "
        "division by zero is not allowed."
    )

    fake_model = MagicMock()
    fake_model.invoke.side_effect = [
        first_response,
        second_response,
    ]

    agent.model_with_tools = fake_model

    result = agent.ask("Calculate 10 / 0")

    assert "could not be completed" in result
    assert fake_model.invoke.call_count == 2