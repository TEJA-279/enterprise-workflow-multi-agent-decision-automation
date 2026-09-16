import pytest

from src.tools.calculator_tool import calculate, CalculatorError


def test_addition():
    assert calculate("10 + 20") == 30


def test_subtraction():
    assert calculate("20 - 5") == 15


def test_multiplication():
    assert calculate("25 * 4") == 100


def test_division():
    assert calculate("100 / 5") == 20


def test_power():
    assert calculate("2 ** 3") == 8


def test_parentheses():
    assert calculate("(10 + 5) * 2") == 30


def test_division_by_zero():
    with pytest.raises(CalculatorError):
        calculate("10 / 0")


def test_invalid_expression():
    with pytest.raises(CalculatorError):
        calculate("10 + abc")


def test_empty_expression():
    with pytest.raises(CalculatorError):
        calculate("")


def test_unsafe_expression():
    with pytest.raises(CalculatorError):
        calculate("__import__('os').system('dir')")