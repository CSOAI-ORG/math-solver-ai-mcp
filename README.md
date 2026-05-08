<div align="center">

# Math Solver Ai MCP

**Math Solver AI MCP Server — Math and statistics tools.**

[![PyPI](https://img.shields.io/pypi/v/meok-math-solver-ai-mcp)](https://pypi.org/project/meok-math-solver-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Math Solver AI MCP Server — Math and statistics tools.

## Tools

| Tool | Description |
|------|-------------|
| `solve_equation` | Solve linear/quadratic equations. Format: '2x + 3 = 7' or 'x^2 - 5x + 6 = 0'. |
| `statistics_summary` | Calculate comprehensive statistics. numbers: comma-separated values. |
| `matrix_operations` | Matrix operations. Matrices as JSON 2D arrays. Operations: multiply, add, subtra |
| `probability_calculator` | Calculate probabilities. Types: binomial, combination, permutation, expected_val |

## Installation

```bash
pip install meok-math-solver-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "math-solver-ai": {
      "command": "python",
      "args": ["-m", "meok_math_solver_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
