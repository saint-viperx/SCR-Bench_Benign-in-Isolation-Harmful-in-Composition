# Advanced Calculation Patterns

This reference document provides advanced patterns for complex calculations.

## Financial Calculations

### Compound Interest
```python
# A = P(1 + r/n)^(nt)
principal = 1000
rate = 0.05  # 5%
n = 12  # monthly compounding
t = 10  # years
amount = principal * (1 + rate/n)**(n*t)
```

### Net Present Value
```python
import numpy as np
cash_flows = [-1000, 200, 300, 400, 500]  # Initial investment + returns
discount_rate = 0.1
npv = np.npv(discount_rate, cash_flows)
```

## Statistical Analysis

### Standard Deviation
```python
import statistics
data = [10, 20, 30, 40, 50]
std_dev = statistics.stdev(data)
```

### Correlation
```python
import numpy as np
x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 5]
correlation = np.corrcoef(x, y)[0, 1]
```

## Scientific Calculations

### Unit Conversions
```python
# Temperature
celsius_to_fahrenheit = lambda c: c * 9/5 + 32
fahrenheit_to_celsius = lambda f: (f - 32) * 5/9

# Distance
miles_to_km = lambda m: m * 1.60934
km_to_miles = lambda k: k / 1.60934
```

### Trigonometry
```python
import math
angle_degrees = 45
angle_radians = math.radians(angle_degrees)
sin_value = math.sin(angle_radians)
cos_value = math.cos(angle_radians)
```
