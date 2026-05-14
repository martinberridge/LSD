# Dunder Methods Implemented in OldMoney

This document lists all the special (dunder) methods implemented in the `OldMoney` class, demonstrating Python's operator overloading and special method protocols.

## Phase 1: Initialization & Representation

### Object Creation & Initialization
- `__init__(self, pounds, shillings, pence, farthings)` - Constructor with component initialization
- `__new__` - (Not implemented, using default)

### String Representation
- `__repr__(self)` - Developer-friendly representation: `OldMoney(1, 5, 6, 0)`
- `__str__(self)` - User-friendly display: `£1 5s 6d`, with farthing symbols (¼, ½, ¾)

### Type Conversion
- `__float__(self)` - Convert to decimal pounds (3 decimal places): `float(money)`
- `__int__(self)` - Convert to total pence: `int(money)`
- `__bool__(self)` - Boolean conversion (False if zero): `bool(money)`, `if money:`

## Phase 2: Arithmetic Operations

### Binary Arithmetic
- `__add__(self, other)` - Addition: `money1 + money2`, `money + 0.5`
- `__sub__(self, other)` - Subtraction: `money1 - money2`, `money - 0.5`
- `__mul__(self, other)` - Multiplication: `money * 3`, `money * 2.5`
- `__truediv__(self, other)` - Division: `money / 2`, `money1 / money2`
- `__floordiv__(self, other)` - Floor division: `money // 3`
- `__mod__(self, other)` - Modulo: `money1 % money2`
- `__divmod__(self, other)` - Combined div and mod: `divmod(money1, money2)`

### Reverse Arithmetic (for float + OldMoney syntax)
- `__radd__(self, other)` - Right addition: `0.5 + money`
- `__rsub__(self, other)` - Right subtraction: `2.0 - money`
- `__rmul__(self, other)` - Right multiplication: `3 * money`
- `__rtruediv__(self, other)` - Right division: `1.0 / money`

### In-Place Arithmetic
- `__iadd__(self, other)` - In-place addition: `money += 0.5`
- `__isub__(self, other)` - In-place subtraction: `money -= 0.5`
- `__imul__(self, other)` - In-place multiplication: `money *= 2`
- `__itruediv__(self, other)` - In-place division: `money /= 2`
- `__ifloordiv__(self, other)` - In-place floor division: `money //= 3`
- `__imod__(self, other)` - In-place modulo: `money %= divisor`

### Unary Operations
- `__neg__(self)` - Negation: `-money`
- `__pos__(self)` - Unary plus (copy): `+money`
- `__abs__(self)` - Absolute value: `abs(money)`
- `__round__(self, ndigits)` - Rounding to nearest penny: `round(money)`

## Phase 2: Comparison Operations

### Rich Comparison Methods
- `__eq__(self, other)` - Equality: `money1 == money2`, `money == 1.0`
- `__ne__(self, other)` - Inequality: `money1 != money2`
- `__lt__(self, other)` - Less than: `money1 < money2`, `money < 2.0`
- `__le__(self, other)` - Less than or equal: `money1 <= money2`
- `__gt__(self, other)` - Greater than: `money1 > money2`, `money > 1.0`
- `__ge__(self, other)` - Greater than or equal: `money1 >= money2`

**Enables:**
- Sorting: `sorted(list_of_money)`
- Min/max: `min(amounts)`, `max(amounts)`
- Comparisons with floats (auto-converts)

## Phase 3: Coming Soon

### Container Protocol
- `__len__(self)` - Length (total pence)
- `__getitem__(self, key)` - Index access: `money[0]` for pounds
- `__setitem__(self, key, value)` - Index assignment
- `__iter__(self)` - Iteration over components
- `__contains__(self, item)` - Membership testing

### Hashing
- `__hash__(self)` - Make hashable for sets/dicts: `{money1, money2}`, `{money: value}`

### Advanced Formatting
- `__format__(self, format_spec)` - Custom format strings: `f"{money:compact}"`

### Attribute Access
- `__getattr__(self, name)` - Dynamic attribute access
- `__setattr__(self, name, value)` - Attribute assignment

## Summary Statistics

### Implemented (Phases 1-2): 34 Dunder Methods

**Category Breakdown:**
- **Initialization & Representation:** 3 methods
- **Type Conversion:** 3 methods
- **Binary Arithmetic:** 7 methods
- **Reverse Arithmetic:** 4 methods
- **In-Place Arithmetic:** 6 methods
- **Unary Operations:** 4 methods
- **Comparison:** 7 methods

### Coming in Phase 3: 6+ Methods
- Container protocol (4 methods)
- Hashing (1 method)
- Advanced formatting (1+ methods)

## Usage Examples by Category

### Basic Usage
```python
# Creation and representation
money = OldMoney(1, 5, 6)
print(money)          # __str__: £1 5s 6d
print(repr(money))    # __repr__: OldMoney(1, 5, 6, 0)
```

### Arithmetic
```python
# Binary operations
total = money1 + money2                   # __add__
difference = money1 - money2              # __sub__
bulk = price * quantity                   # __mul__
split = total / people                    # __truediv__

# With auto-conversion
result = money + 0.5                      # __add__ with float
result = 2.0 - money                      # __rsub__

# In-place
money += 0.5                              # __iadd__
money *= 2                                # __imul__
```

### Unary Operations
```python
debt = -money                             # __neg__
positive = abs(debt)                      # __abs__
rounded = round(money_with_farthings)     # __round__
```

### Comparisons
```python
# Equality
if money1 == money2:                      # __eq__
    pass

# Ordering
if money1 < money2:                       # __lt__
    pass

# Sorting
sorted_list = sorted(amounts)             # Uses __lt__, __le__, etc.

# Boolean
if money:                                 # __bool__
    print("Has value")
```

### Type Conversions
```python
decimal = float(money)                    # __float__: 1.275
pence = int(money)                        # __int__: 306
is_truthy = bool(money)                   # __bool__: True
```

## Design Patterns Used

1. **Factory Methods Pattern**: `from_decimal()`, `from_pence()`, `from_farthings()`
2. **Type Coercion**: Automatic conversion of numeric types in arithmetic
3. **Immutable-like Arithmetic**: Operations return new instances (like int, float)
4. **Rich Comparison Protocol**: Full ordering support
5. **Operator Overloading**: Natural mathematical syntax

## Key Features

- **Float Auto-Conversion**: Seamlessly mix OldMoney with decimal values
- **Reverse Operations**: Support both `money + 0.5` and `0.5 + money`
- **Farthing Precision**: Internal integer storage prevents floating-point errors
- **Negative Support**: Handle debts/credits naturally
- **Full Comparison**: Sort, min, max, and all comparison operators
- **Boolean Context**: Works naturally in if statements and boolean expressions
