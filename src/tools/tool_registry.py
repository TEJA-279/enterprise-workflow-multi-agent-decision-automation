from langchain_core.tools import tool

from src.tools.calculator_tool import calculate
from src.tools.currency_tool import convert_currency
from src.tools.weather_tool import get_current_weather


@tool
def calculator(expression: str) -> int | float:
    """
    Perform a mathematical calculation.

    Use this tool for arithmetic expressions such as:
    10 + 20
    25 * 4
    (10 + 5) / 3
    """
    return calculate(expression)


@tool
def currency_converter(
    amount: float,
    from_currency: str,
    to_currency: str,
) -> dict:
    """
    Convert money from one currency to another.

    Example:
    100 INR to USD
    """
    return convert_currency(
        amount,
        from_currency,
        to_currency,
    )


@tool
def weather(
    city: str,
) -> dict:
    """
    Get the current weather for a city.
    """
    return get_current_weather(city)


TOOLS = [
    calculator,
    currency_converter,
    weather,
]