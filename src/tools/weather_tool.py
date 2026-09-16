import os

import requests
from dotenv import load_dotenv


load_dotenv()


class WeatherToolError(ValueError):
    """Raised when weather information cannot be retrieved."""


def get_current_weather(city: str) -> dict:
    """
    Get current weather information for a city.
    """

    if not isinstance(city, str) or not city.strip():
        raise WeatherToolError("City name must be a non-empty string.")

    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        raise WeatherToolError(
            "OPENWEATHER_API_KEY is not configured."
        )

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city.strip(),
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        if response.status_code == 404:
            raise WeatherToolError(
                f"City '{city}' was not found."
            )

        if response.status_code == 401:
            raise WeatherToolError(
                "Invalid OpenWeather API key."
            )

        response.raise_for_status()
        data = response.json()

    except WeatherToolError:
        raise

    except requests.RequestException as exc:
        raise WeatherToolError(
            f"Weather API request failed: {exc}"
        ) from exc

    except ValueError as exc:
        raise WeatherToolError(
            "Weather API returned invalid JSON."
        ) from exc

    weather = data.get("weather", [{}])[0]
    main = data.get("main", {})

    return {
        "city": data.get("name", city),
        "country": data.get("sys", {}).get("country"),
        "temperature_celsius": main.get("temp"),
        "feels_like_celsius": main.get("feels_like"),
        "humidity_percent": main.get("humidity"),
        "condition": weather.get("main"),
        "description": weather.get("description"),
    }


weather_tool = get_current_weather