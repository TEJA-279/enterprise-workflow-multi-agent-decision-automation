import pytest
import requests

from src.tools.weather_tool import get_current_weather, WeatherToolError


def test_empty_city():
    with pytest.raises(WeatherToolError, match="non-empty string"):
        get_current_weather("")


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)

    with pytest.raises(
        WeatherToolError,
        match="OPENWEATHER_API_KEY is not configured",
    ):
        get_current_weather("Hyderabad")


def test_successful_weather_request(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-api-key")

    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "name": "Hyderabad",
                    "sys": {
                        "country": "IN"
                    },
                    "main": {
                        "temp": 30.5,
                        "feels_like": 32.0,
                        "humidity": 60,
                    },
                    "weather": [
                        {
                            "main": "Clouds",
                            "description": "scattered clouds",
                        }
                    ],
                }

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    result = get_current_weather("Hyderabad")

    assert result["city"] == "Hyderabad"
    assert result["country"] == "IN"
    assert result["temperature_celsius"] == 30.5
    assert result["feels_like_celsius"] == 32.0
    assert result["humidity_percent"] == 60
    assert result["condition"] == "Clouds"
    assert result["description"] == "scattered clouds"


def test_city_not_found(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-api-key")

    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 404

            def raise_for_status(self):
                pass

            def json(self):
                return {}

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(WeatherToolError, match="was not found"):
        get_current_weather("UnknownCity")


def test_invalid_api_key(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "invalid-key")

    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 401

            def raise_for_status(self):
                pass

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(WeatherToolError, match="Invalid OpenWeather API key"):
        get_current_weather("Hyderabad")


def test_api_failure(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-api-key")

    def mock_get(*args, **kwargs):
        raise requests.RequestException("API unavailable")

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(
        WeatherToolError,
        match="Weather API request failed",
    ):
        get_current_weather("Hyderabad")


def test_invalid_json(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-api-key")

    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                raise ValueError("Invalid JSON")

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(
        WeatherToolError,
        match="Weather API returned invalid JSON",
    ):
        get_current_weather("Hyderabad")