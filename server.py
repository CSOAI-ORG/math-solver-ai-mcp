"""Math Solver AI MCP Server — Math and statistics tools."""
import math
import re
import time
from typing import Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("math-solver-ai-mcp")
_calls: dict[str, list[float]] = {}
DAILY_LIMIT = 50

def _rate_check(tool: str) -> bool:
    now = time.time()
    _calls.setdefault(tool, [])
    _calls[tool] = [t for t in _calls[tool] if t > now - 86400]
    if len(_calls[tool]) >= DAILY_LIMIT:
        return False
    _calls[tool].append(now)
    return True

@mcp.tool()
def solve_equation(equation: str, variable: str = "x") -> dict[str, Any]:
    """Solve linear/quadratic equations. Format: '2x + 3 = 7' or 'x^2 - 5x + 6 = 0'."""
    if not _rate_check("solve_equation"):
        return {"error": "Rate limit exceeded (50/day)"}
    eq = equation.replace(" ", "")
    if "=" not in eq:
        return {"error": "Equation must contain '='"}
    left, right = eq.split("=", 1)
    # Move everything to left side (left - right = 0)
    def parse_terms(expr: str) -> dict[int, float]:
        """Parse into {power: coefficient}."""
        coeffs: dict[int, float] = {}
        expr = expr.replace("-", "+-")
        for term in expr.split("+"):
            term = term.strip()
            if not term:
                continue
            if variable + "^2" in term or variable + "**2" in term:
                coeff = term.replace(variable + "^2", "").replace(variable + "**2", "").replace("*", "")
                coeffs[2] = coeffs.get(2, 0) + (float(coeff) if coeff and coeff != "-" else (-1.0 if coeff == "-" else 1.0))
            elif variable in term:
                coeff = term.replace(variable, "").replace("*", "")
                coeffs[1] = coeffs.get(1, 0) + (float(coeff) if coeff and coeff != "-" else (-1.0 if coeff == "-" else 1.0))
            else:
                coeffs[0] = coeffs.get(0, 0) + float(term)
        return coeffs
    try:
        left_c = parse_terms(left)
        right_c = parse_terms(right)
        # Combine: left - right
        combined: dict[int, float] = {}
        for p in set(list(left_c.keys()) + list(right_c.keys())):
            combined[p] = left_c.get(p, 0) - right_c.get(p, 0)
        a = combined.get(2, 0)
        b = combined.get(1, 0)
        c = combined.get(0, 0)
    except (ValueError, ZeroDivisionError) as e:
        return {"error": f"Could not parse equation: {e}"}
    if a != 0:  # Quadratic
        discriminant = b**2 - 4*a*c
        if discriminant > 0:
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            solutions = [round(x1, 6), round(x2, 6)]
            nature = "two real roots"
        elif discriminant == 0:
            x1 = -b / (2*a)
            solutions = [round(x1, 6)]
            nature = "one repeated root"
        else:
            real = -b / (2*a)
            imag = math.sqrt(abs(discriminant)) / (2*a)
            solutions = [f"{round(real, 4)} + {round(imag, 4)}i", f"{round(real, 4)} - {round(imag, 4)}i"]
            nature = "two complex roots"
        return {"equation": equation, "type": "quadratic", "a": a, "b": b, "c": c,
                "discriminant": round(discriminant, 6), "solutions": solutions, "nature": nature}
    elif b != 0:  # Linear
        x = -c / b
        return {"equation": equation, "type": "linear", "solution": round(x, 6),
                "verification": f"{b}*{round(x, 6)} + {c} = {round(b*x + c, 10)}"}
    else:
        return {"equation": equation, "type": "constant", "result": "No solution" if c != 0 else "Identity (all values)"}

@mcp.tool()
def statistics_summary(numbers: str) -> dict[str, Any]:
    """Calculate comprehensive statistics. numbers: comma-separated values."""
    if not _rate_check("statistics_summary"):
        return {"error": "Rate limit exceeded (50/day)"}
    try:
        vals = [float(x.strip()) for x in numbers.split(",") if x.strip()]
    except ValueError:
        return {"error": "Invalid numbers. Use comma-separated values."}
    if not vals:
        return {"error": "No numbers provided"}
    n = len(vals)
    mean = sum(vals) / n
    sorted_v = sorted(vals)
    median = sorted_v[n // 2] if n % 2 else (sorted_v[n // 2 - 1] + sorted_v[n // 2]) / 2
    variance = sum((x - mean) ** 2 for x in vals) / n
    std_dev = math.sqrt(variance)
    # Mode
    freq: dict[float, int] = {}
    for v in vals:
        freq[v] = freq.get(v, 0) + 1
    max_freq = max(freq.values())
    mode = [k for k, v in freq.items() if v == max_freq] if max_freq > 1 else []
    # Quartiles
    q1_idx = n // 4
    q3_idx = 3 * n // 4
    q1 = sorted_v[q1_idx]
    q3 = sorted_v[q3_idx]
    iqr = q3 - q1
    return {
        "count": n, "sum": round(sum(vals), 6), "mean": round(mean, 6),
        "median": round(median, 6), "mode": mode,
        "min": min(vals), "max": max(vals), "range": round(max(vals) - min(vals), 6),
        "variance": round(variance, 6), "std_deviation": round(std_dev, 6),
        "q1": q1, "q3": q3, "iqr": round(iqr, 6),
        "coefficient_of_variation": round(std_dev / abs(mean) * 100, 2) if mean != 0 else None
    }

@mcp.tool()
def matrix_operations(matrix_a: str, matrix_b: str = "", operation: str = "multiply") -> dict[str, Any]:
    """Matrix operations. Matrices as JSON 2D arrays. Operations: multiply, add, subtract, transpose, determinant."""
    if not _rate_check("matrix_operations"):
        return {"error": "Rate limit exceeded (50/day)"}
    import json
    try:
        a = json.loads(matrix_a)
    except json.JSONDecodeError:
        return {"error": "Invalid matrix_a JSON"}
    if operation == "transpose":
        if not a or not a[0]:
            return {"error": "Empty matrix"}
        result = [[a[i][j] for i in range(len(a))] for j in range(len(a[0]))]
        return {"operation": "transpose", "result": result, "original_shape": f"{len(a)}x{len(a[0])}", "result_shape": f"{len(result)}x{len(result[0])}"}
    if operation == "determinant":
        if len(a) != len(a[0]):
            return {"error": "Matrix must be square for determinant"}
        def det(m):
            n = len(m)
            if n == 1: return m[0][0]
            if n == 2: return m[0][0]*m[1][1] - m[0][1]*m[1][0]
            d = 0
            for j in range(n):
                sub = [[m[i][k] for k in range(n) if k != j] for i in range(1, n)]
                d += ((-1)**j) * m[0][j] * det(sub)
            return d
        d = det(a)
        return {"operation": "determinant", "result": round(d, 6), "matrix_size": f"{len(a)}x{len(a)}", "is_invertible": d != 0}
    if not matrix_b:
        return {"error": f"matrix_b required for {operation}"}
    try:
        b = json.loads(matrix_b)
    except json.JSONDecodeError:
        return {"error": "Invalid matrix_b JSON"}
    if operation == "add" or operation == "subtract":
        if len(a) != len(b) or len(a[0]) != len(b[0]):
            return {"error": "Matrices must be same dimensions"}
        op = (lambda x, y: x + y) if operation == "add" else (lambda x, y: x - y)
        result = [[op(a[i][j], b[i][j]) for j in range(len(a[0]))] for i in range(len(a))]
        return {"operation": operation, "result": result, "shape": f"{len(a)}x{len(a[0])}"}
    if operation == "multiply":
        if len(a[0]) != len(b):
            return {"error": f"Cannot multiply {len(a)}x{len(a[0])} by {len(b)}x{len(b[0])}"}
        result = [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
        return {"operation": "multiply", "result": result, "result_shape": f"{len(a)}x{len(b[0])}"}
    return {"error": f"Unknown operation: {operation}"}

@mcp.tool()
def probability_calculator(event_type: str, n: int = 0, k: int = 0, p: float = 0.0, trials: int = 0) -> dict[str, Any]:
    """Calculate probabilities. Types: binomial, combination, permutation, expected_value, bayes."""
    if not _rate_check("probability_calculator"):
        return {"error": "Rate limit exceeded (50/day)"}
    if event_type == "combination":
        if n < 0 or k < 0 or k > n:
            return {"error": "Need 0 <= k <= n"}
        result = math.comb(n, k)
        return {"type": "combination", "n": n, "k": k, "result": result, "formula": f"C({n},{k}) = {n}! / ({k}! * {n-k}!)"}
    elif event_type == "permutation":
        if n < 0 or k < 0 or k > n:
            return {"error": "Need 0 <= k <= n"}
        result = math.perm(n, k)
        return {"type": "permutation", "n": n, "k": k, "result": result, "formula": f"P({n},{k}) = {n}! / {n-k}!"}
    elif event_type == "binomial":
        if not (0 <= p <= 1) or trials < 1 or k > trials:
            return {"error": "Need 0<=p<=1, trials>=1, k<=trials"}
        prob = math.comb(trials, k) * (p ** k) * ((1 - p) ** (trials - k))
        cumulative = sum(math.comb(trials, i) * (p ** i) * ((1 - p) ** (trials - i)) for i in range(k + 1))
        return {
            "type": "binomial", "trials": trials, "successes": k, "probability": p,
            "result": round(prob, 8), "cumulative_leq": round(cumulative, 8),
            "expected_value": round(trials * p, 4), "std_deviation": round(math.sqrt(trials * p * (1 - p)), 4)
        }
    elif event_type == "expected_value":
        return {"type": "expected_value", "trials": trials, "probability": p,
                "expected_value": round(trials * p, 4), "variance": round(trials * p * (1 - p), 4)}
    return {"error": f"Unknown type: {event_type}. Use: binomial, combination, permutation, expected_value"}

if __name__ == "__main__":
    mcp.run()
