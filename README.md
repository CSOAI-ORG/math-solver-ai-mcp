# Math Solver AI

> By [MEOK AI Labs](https://meok.ai) — Equation solving, statistics, matrix operations, and probability

## Installation

```bash
pip install math-solver-ai-mcp
```

## Usage

```bash
python server.py
```

## Tools

### `solve_equation`
Solve linear/quadratic equations. Format: '2x + 3 = 7' or 'x^2 - 5x + 6 = 0'.

**Parameters:**
- `equation` (str): Equation string with '='
- `variable` (str): Variable to solve for (default: "x")

### `statistics_summary`
Calculate comprehensive statistics (mean, median, mode, std deviation, quartiles, IQR).

**Parameters:**
- `numbers` (str): Comma-separated numerical values

### `matrix_operations`
Matrix operations. Matrices as JSON 2D arrays. Operations: multiply, add, subtract, transpose, determinant.

**Parameters:**
- `matrix_a` (str): First matrix as JSON 2D array
- `matrix_b` (str): Second matrix as JSON 2D array (optional for transpose/determinant)
- `operation` (str): Operation to perform

### `probability_calculator`
Calculate probabilities. Types: binomial, combination, permutation, expected_value.

**Parameters:**
- `event_type` (str): Probability type
- `n` (int): Total items
- `k` (int): Selected items
- `p` (float): Probability of success
- `trials` (int): Number of trials

## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT — MEOK AI Labs
