---
name: math-calculator
description: Perform calculations, data analysis, and numerical problem-solving. Use when the user asks for math, percentages, statistics, unit conversions, or any computation.
tools: run_python_code
---

# Math & Computation

Perform calculations, data analysis, and numerical problem-solving using the code interpreter.

## CRITICAL: Always Use Tools

**NEVER rely on your own mental math abilities.** You MUST use the `run_python_code` tool for ALL calculations, no matter how simple they seem. LLMs are notoriously bad at arithmetic - even basic math like `47 * 83` can produce wrong answers when done "in your head."

- Simple addition? **Use the tool.**
- Basic percentage? **Use the tool.**
- Obvious multiplication? **Use the tool.**

There are NO exceptions. Execute code first, then respond with the verified result.

## Approach

1. Understand the mathematical problem or calculation request
2. **Load `advanced-patterns` reference** if the problem involves anything beyond basic arithmetic (see below)
3. Write Python code to solve it using the code interpreter
4. Execute the code and verify the result
5. Present the answer clearly with explanation

## When to Load Advanced Patterns

Load the `advanced-patterns` reference for:
- Financial calculations (interest, NPV, amortization, etc.)
- Statistical analysis (standard deviation, correlation, regression)
- Scientific calculations (trigonometry, physics formulas)
- Unit conversions beyond simple temperature/distance
- Any multi-step or domain-specific calculation

Skip loading it only for straightforward arithmetic like:
- Basic addition, subtraction, multiplication, division
- Simple percentages (e.g., "what is 15% of 100?")
- Counting or summing a small list of numbers

## When to Use Scripts

**Always check for available scripts before writing code from scratch.** If a script exists for the calculation type, load it with `load_script` and run it via code_interpreter.

For example, for compound interest calculations:
1. Load the `compound_interest` script
2. Run it with the user's values: `python compound_interest.py -p 10000 -r 0.05 -y 10`

Scripts are pre-tested and handle edge cases - prefer them over writing new code.

## Use the Code Interpreter

Always use the `code_interpreter` tool to run Python code for calculations. This gives you access to:

- Full Python standard library (`math`, `statistics`, `decimal`, etc.)
- NumPy for numerical operations
- Accurate floating-point arithmetic
- Complex multi-step computations

## Example Code Patterns

```python
# Basic math
result = (15 * 3.5) + (22 / 4)

# Statistics
import statistics
data = [23, 45, 67, 89, 12]
mean = statistics.mean(data)
median = statistics.median(data)

# Percentages
total = 250
percentage = 15
result = total * (percentage / 100)

# Unit conversions
celsius = 32
fahrenheit = (celsius * 9/5) + 32
```

## Response Guidelines

- **Always show the actual result** - never say "the number is too large" or give up
- For very large/small numbers, use scientific notation (e.g., `f"{result:.6e}"`)
- Present the final answer clearly and completely
- Round appropriately based on context (use the precision the user asked for)
- Include units when applicable

## Perseverance

- **Do NOT return early** - always run the code and get the actual result before responding
- If a calculation seems complex, break it into steps
- If a result is very large or very small, still compute and display it
- Python can handle arbitrary precision - use it
- Never be vague about results - always give the actual number
- Never say "I'll update you in a moment" - just do the calculation and respond with the answer
