import ast
import operator


class CalculatorError(ValueError):
    """Raised when a calculation cannot be safely evaluated."""


_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression: str) -> float | int:
    """
    Safely evaluate a basic mathematical expression.

    Examples:
        calculate("10 + 20") -> 30
        calculate("25 * 4") -> 100
        calculate("(10 + 5) / 3") -> 5.0
    """
    if not isinstance(expression, str) or not expression.strip():
        raise CalculatorError("Expression must be a non-empty string.")

    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree.body)

        if isinstance(result, float) and result.is_integer():
            return int(result)

        return result

    except ZeroDivisionError:
        raise CalculatorError("Cannot divide by zero.")

    except (SyntaxError, ValueError, TypeError, OverflowError):
        raise CalculatorError(
            f"Invalid or unsupported mathematical expression: {expression}"
        )


def _evaluate(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise CalculatorError("Only numbers are allowed.")

    if isinstance(node, ast.UnaryOp):
        operation = _ALLOWED_OPERATORS.get(type(node.op))
        if operation is None:
            raise CalculatorError("Unsupported unary operator.")
        return operation(_evaluate(node.operand))

    if isinstance(node, ast.BinOp):
        operation = _ALLOWED_OPERATORS.get(type(node.op))
        if operation is None:
            raise CalculatorError("Unsupported mathematical operator.")

        left = _evaluate(node.left)
        right = _evaluate(node.right)

        # Prevent excessively large exponent calculations.
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise CalculatorError("Exponent is too large.")

        return operation(left, right)

    raise CalculatorError("Unsupported expression.")


# Optional alias useful when registering the tool with an agent.
calculator_tool = calculate