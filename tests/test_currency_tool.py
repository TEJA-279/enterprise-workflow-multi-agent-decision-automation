import pytest
import requests

from src.tools.currency_tool import convert_currency, CurrencyToolError


def test_same_currency():
    result = convert_currency(100, "INR", "INR")

    assert result["amount"] == 100
    assert result["from_currency"] == "INR"
    assert result["to_currency"] == "INR"
    assert result["rate"] == 1.0
    assert result["converted_amount"] == 100


def test_currency_codes_are_normalized(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"rates": {"USD": 1.25}}

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    result = convert_currency(100, " inr ", " usd ")

    assert result["from_currency"] == "INR"
    assert result["to_currency"] == "USD"
    assert result["converted_amount"] == 1.25


def test_negative_amount():
    with pytest.raises(CurrencyToolError):
        convert_currency(-100, "INR", "USD")


def test_invalid_amount():
    with pytest.raises(CurrencyToolError):
        convert_currency("100", "INR", "USD")


def test_invalid_currency_code():
    with pytest.raises(CurrencyToolError):
        convert_currency(100, "INDIA", "USD")


def test_api_failure(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.RequestException("API unavailable")

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(CurrencyToolError, match="Currency API request failed"):
        convert_currency(100, "INR", "USD")


def test_invalid_json(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                raise ValueError("Invalid JSON")

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(CurrencyToolError, match="invalid JSON"):
        convert_currency(100, "INR", "USD")


def test_conversion_currency_unavailable(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"rates": {"EUR": 0.85}}

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(CurrencyToolError, match="unavailable"):
        convert_currency(100, "INR", "USD")