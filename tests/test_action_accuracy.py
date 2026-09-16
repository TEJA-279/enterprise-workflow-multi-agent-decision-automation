from unittest.mock import MagicMock

from src.agents.business_agent import BusinessAgent


def create_fake_response(tool_name, tool_args, tool_id):
    response = MagicMock()

    response.tool_calls = [
        {
            "name": tool_name,
            "args": tool_args,
            "id": tool_id,
        }
    ]

    response.content = ""

    return response


def create_final_response(content):
    response = MagicMock()

    response.tool_calls = []
    response.content = content

    return response


def test_calculator_action_accuracy():
    agent = BusinessAgent()

    fake_model = MagicMock()

    fake_model.invoke.side_effect = [
        create_fake_response(
            "calculator",
            {
                "expression": "25 * 4"
            },
            "calculator_call",
        ),
        create_final_response(
            "The answer is 100."
        ),
    ]

    agent.model_with_tools = fake_model

    result = agent.ask(
        "Calculate 25 * 4"
    )

    assert "100" in result
    assert fake_model.invoke.call_count == 2


def test_currency_action_accuracy():
    agent = BusinessAgent()

    fake_model = MagicMock()

    fake_model.invoke.side_effect = [
        create_fake_response(
            "currency_converter",
            {
                "amount": 100,
                "from_currency": "INR",
                "to_currency": "USD",
            },
            "currency_call",
        ),
        create_final_response(
            "100 INR was converted to approximately 1.25 USD."
        ),
    ]

    agent.model_with_tools = fake_model

    result = agent.ask(
        "Convert 100 INR to USD"
    )

    assert "100 INR" in result
    assert "1.25 USD" in result
    assert fake_model.invoke.call_count == 2


def test_weather_action_accuracy():
    agent = BusinessAgent()

    fake_model = MagicMock()

    fake_model.invoke.side_effect = [
        create_fake_response(
            "weather",
            {
                "city": "Hyderabad"
            },
            "weather_call",
        ),
        create_final_response(
            "The current temperature in Hyderabad is 30.5°C."
        ),
    ]

    agent.model_with_tools = fake_model

    result = agent.ask(
        "What is the weather in Hyderabad?"
    )

    assert "Hyderabad" in result
    assert "30.5" in result
    assert fake_model.invoke.call_count == 2