# Common Code Review Patterns

## Pattern: Extract Function
When a function is too long or has multiple responsibilities, extract into smaller functions.

**Before:**
```python
def process_user_data(user_data):
    # Validate email
    if '@' not in user_data['email']:
        raise ValueError("Invalid email")
    
    # Validate age
    if user_data['age'] < 18:
        raise ValueError("User must be 18+")
    
    # Process data
    name = user_data['name'].strip().title()
    email = user_data['email'].lower()
    
    return {
        'name': name,
        'email': email,
        'age': user_data['age']
    }
```

**After:**
```python
def validate_user_data(user_data):
    validate_email(user_data['email'])
    validate_age(user_data['age'])

def validate_email(email):
    if '@' not in email:
        raise ValueError("Invalid email")

def validate_age(age):
    if age < 18:
        raise ValueError("User must be 18+")

def normalize_user_data(user_data):
    return {
        'name': user_data['name'].strip().title(),
        'email': user_data['email'].lower(),
        'age': user_data['age']
    }

def process_user_data(user_data):
    validate_user_data(user_data)
    return normalize_user_data(user_data)
```

## Pattern: Replace Magic Numbers
Replace unexplained numbers with named constants.

**Before:**
```python
if user.age > 21:
    tax_rate = 0.125
```

**After:**
```python
LEGAL_DRINKING_AGE = 21
SALES_TAX_RATE = 0.125

if user.age > LEGAL_DRINKING_AGE:
    tax_rate = SALES_TAX_RATE
```

## Pattern: Add Type Hints
Make code more readable and enable IDE support.

**Before:**
```python
def calculate_discount(price, quantity):
    if quantity > 10:
        return price * 0.9
    return price
```

**After:**
```python
def calculate_discount(price: float, quantity: int) -> float:
    if quantity > 10:
        return price * 0.9
    return price
```

## Pattern: Use Composition over Inheritance
Prefer composition for more flexible code.

**Before:**
```python
class Animal:
    def eat(self): pass
    def sleep(self): pass

class Dog(Animal):
    def eat(self): print("Eating dog food")
    def bark(self): print("Woof!")
```

**After:**
```python
class Eater:
    def eat(self): pass

class Sleeper:
    def sleep(self): pass

class Dog:
    def __init__(self):
        self.eater = Eater()
        self.sleeper = Sleeper()
    
    def bark(self):
        print("Woof!")
```

## Pattern: Guard Clauses
Use early returns to reduce nesting.

**Before:**
```python
def process_order(order):
    if order is not None:
        if order.items:
            total = 0
            for item in order.items:
                total += item.price
            return total
    return None
```

**After:**
```python
def process_order(order):
    if order is None:
        return None
    
    if not order.items:
        return None
    
    return sum(item.price for item in order.items)
```

