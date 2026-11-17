
import ast
import math
import operator

# Allowed mathematical operations
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos
}

# Allowed mathematical functions and constants
FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "abs": abs,
    "round": round
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e
}


def safe_calculate(node):

    if isinstance(node, ast.Constant):
        if type(node.value) in (int, float):
            return node.value
        raise ValueError("Invalid number")

    elif isinstance(node, ast.BinOp):
        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported operation")

        left = safe_calculate(node.left)
        right = safe_calculate(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("Exponent too large")

        result = operation(left, right)

        if not math.isfinite(result) or abs(result) > 1e100:
            raise ValueError("Result too large")

        return result

    elif isinstance(node, ast.UnaryOp):
        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported operation")

        return operation(safe_calculate(node.operand))

    elif isinstance(node, ast.Name):
        if node.id in CONSTANTS:
            return CONSTANTS[node.id]
        raise ValueError("Unknown constant")

    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function")

        function = FUNCTIONS.get(node.func.id)

        if function is None or node.keywords:
            raise ValueError("Unsupported function")

        arguments = [safe_calculate(arg) for arg in node.args]
        result = function(*arguments)

        if not math.isfinite(result) or abs(result) > 1e100:
            raise ValueError("Result too large")

        return result

    raise ValueError("Invalid expression")


def calculate(expression):

    try:
        tree = ast.parse(expression, mode="eval")
        result = safe_calculate(tree.body)
        return str(result)

    except Exception:
        return "Sorry, I could not calculate this expression."
