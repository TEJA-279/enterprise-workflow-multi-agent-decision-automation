import requests


class CurrencyToolError(ValueError):
    """Raised when currency conversion fails."""


def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
) -> dict:
    """
    Convert an amount from one currency to another.

    Example:
        convert_currency(100, "INR", "USD")
    """

    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        raise CurrencyToolError("Amount must be a number.")

    if amount < 0:
        raise CurrencyToolError("Amount cannot be negative.")

    from_currency = from_currency.strip().upper()
    to_currency = to_currency.strip().upper()

    if len(from_currency) != 3 or len(to_currency) != 3:
        raise CurrencyToolError(
            "Currency codes must be 3-letter ISO codes, e.g. INR or USD."
        )

    if from_currency == to_currency:
        return {
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "rate": 1.0,
            "converted_amount": amount,
        }

    url = "https://api.frankfurter.app/latest"

    params = {
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as exc:
        raise CurrencyToolError(
            f"Currency API request failed: {exc}"
        ) from exc

    except ValueError as exc:
        raise CurrencyToolError(
            "Currency API returned invalid JSON."
        ) from exc

    rates = data.get("rates", {})

    if to_currency not in rates:
        raise CurrencyToolError(
            f"Conversion from {from_currency} to {to_currency} is unavailable."
        )

    converted_amount = rates[to_currency]

    rate = converted_amount / amount if amount != 0 else 0.0

    return {
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "rate": rate,
        "converted_amount": converted_amount,
    }


currency_tool = convert_currency