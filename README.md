# Pre-Decimal British Currency (£sd) - Python Implementation

A Python class demonstrating dunder methods through implementation of pre-decimal British currency (pounds, shillings, and pence with farthing precision).

## Overview

This project implements `OldMoney`, a class representing the pre-decimal British currency system used until 1971:

- **1 pound (£)** = 20 shillings (s) = 240 pence (d) = 960 farthings
- **1 shilling** = 12 pence = 48 farthings
- **1 penny** = 4 farthings

Farthings are represented with special symbols: **¼d**, **½d**, **¾d**

## Features

### ✅ Phase 1: Initialization & Conversion (Complete)

- **Initialization**: Create amounts with pounds, shillings, pence, and farthings
- **Factory Methods**: Create from decimal pounds, decimal pence, or farthings
- **Decimal Conversion**: Convert to/from modern decimal currency (3 decimal places)
- **Component Extraction**: Get normalized components (£, s, d, f)
- **String Representation**: User-friendly (`£1 5s 6d`) and developer (`OldMoney(1, 5, 6, 0)`) formats
- **Type Conversion**: `float()`, `int()` support
- **Negative Values**: Support for debts/credits
- **Farthing Precision**: Exact calculations using internal farthing storage

### ✅ Phase 2: Arithmetic & Comparison (Complete)

- **Arithmetic Operations**: `+`, `-`, `*`, `/`, `//`, `%` with OldMoney and numeric types
- **Float Auto-Conversion**: Automatically converts floats in arithmetic (e.g., `OldMoney(1,0,0) + 0.5`)
- **Reverse Operations**: `__radd__`, `__rsub__`, `__rmul__`, etc. for natural syntax
- **In-Place Operations**: `+=`, `-=`, `*=`, `/=`, `//=`, `%=`
- **Unary Operations**: `-` (negation), `+` (copy), `abs()`, `round()`
- **Comparison**: `==`, `!=`, `<`, `<=`, `>`, `>=` with OldMoney and floats
- **Boolean Conversion**: `bool()` returns `False` for zero, `True` otherwise
- **Sorting**: Full comparison support enables sorting

### 🔜 Coming Soon

- **Phase 3**: Hashing, iteration, advanced formatting, `__getitem__`/`__setitem__`
- **Phase 4**: Interactive demo and historical context

## Installation

```bash
# Clone or download the repository
cd lsd

# No external dependencies required - uses Python standard library
```

## Usage

### Basic Creation

```python
from old_money import OldMoney

# Traditional notation
price = OldMoney(1, 5, 6)          # £1 5s 6d
print(price)                        # "£1 5s 6d"
print(float(price))                 # 1.275

# Farthing precision
halfpenny = OldMoney(0, 0, 0, 2)   # ½d
print(halfpenny)                    # "½d"
```

### Decimal Conversion

```python
# From decimal pounds
modern_price = OldMoney.from_decimal(2.50)
print(modern_price)                 # "£2 10s 0d"

# To decimal pounds (3 decimal places)
old_price = OldMoney(1, 5, 6)
decimal = float(old_price)          # 1.275

# Custom precision
precise = old_price.to_decimal(6)   # 1.275000
```

### Working with Pence

```python
# From pence
money = OldMoney.from_pence(30.5)
print(money)                        # "2s 6½d"

# To pence
pence = money.to_pence()            # 30.5
```

### Negative Values

```python
# Debts or credits
debt = OldMoney(-1, -5, -6)
print(debt)                         # "-£1 5s 6d"
print(debt.is_negative())           # True
```

### Arithmetic Operations (Phase 2)

```python
# Addition
total = OldMoney(1, 0, 0) + OldMoney(0, 5, 6)  # £1 + 5s 6d
with_float = OldMoney(1, 0, 0) + 0.5            # £1 + £0.5 = £1 10s

# Subtraction
change = OldMoney(1, 0, 0) - OldMoney(0, 2, 6)  # £1 - 2s 6d

# Multiplication
bulk = OldMoney(0, 2, 6) * 10                   # 2s 6d × 10

# Division
split = OldMoney(1, 0, 0) / 4                   # £1 ÷ 4 = 5s
ratio = OldMoney(1, 0, 0) / OldMoney(0, 10, 0)  # Returns 2.0

# Negation and absolute value
debt = -OldMoney(1, 5, 6)                       # -£1 5s 6d
amount = abs(debt)                               # £1 5s 6d
```

### Comparison Operations (Phase 2)

```python
# Comparisons work with OldMoney and floats
money1 = OldMoney(1, 5, 6)
money2 = OldMoney(2, 0, 0)

money1 < money2                                  # True
money1 == OldMoney(1, 5, 6)                     # True
money1 > 1.0                                     # True

# Sorting
amounts = [OldMoney(2, 0, 0), OldMoney(0, 5, 6), OldMoney(1, 10, 0)]
sorted_amounts = sorted(amounts)

# Boolean conversion
if OldMoney(0, 5, 6):                           # True (non-zero)
    print("Has value")
```

## Running Examples

```bash
# Run the main class demo
python old_money.py

# Run comprehensive examples
python examples.py

# Run tests
pytest test_old_money.py -v
```

## Technical Details

### Internal Storage

The class stores amounts internally as **total farthings** (integer) for exact precision, avoiding floating-point errors. All operations work on this integer representation.

```python
# Example: £1 5s 6¼d
# = (1 × 960) + (5 × 48) + (6 × 4) + 1
# = 960 + 240 + 24 + 1
# = 1225 farthings
```

### Conversion Formula

**£sd → Decimal:**
```
decimal_pounds = total_farthings / 960
rounded to 3 decimal places
```

**Decimal → £sd:**
```
total_farthings = round(decimal_pounds × 960)
then normalize to components
```

## Design Decisions

1. **Storage**: Internal farthings (integer) for precision
2. **Precision**: Farthings (¼d) supported with special symbols
3. **Float Conversion**: 3 decimal places by default
4. **Float Arithmetic**: Auto-converts floats to OldMoney (Phase 2)
5. **Negative Values**: Fully supported, no min/max limits
6. **Immutability**: To be determined in Phase 2

## Examples Output

**Phase 1 - Conversion:**
```
Traditional: £1 5s 6d
Decimal: £1.275

From decimal 1.275: £1 5s 6d
Back to decimal: £1.275

One farthing: ¼d = £0.001
Half penny: ½d = £0.002
```

**Phase 2 - Arithmetic:**
```
£1 + 5s 6d = £1 5s 6d
£2 10s 6d - £1 5s 3d = £1 5s 3d
2s 6d × 3 = 7s 6d
£1 / 2 = 10s

Shopping total: £0 7s 6d
Bill split 3 ways: 18s 6d each
```

## Testing

Comprehensive test suite covering:

**Phase 1:**
- Initialization and factory methods
- Decimal/pence conversion accuracy
- Round-trip conversions
- Farthing precision
- Negative values
- Edge cases (zero, very small/large amounts)
- String representations

**Phase 2:**
- All arithmetic operations (`+`, `-`, `*`, `/`, `//`, `%`)
- Float auto-conversion in arithmetic
- Reverse operations (`__radd__`, `__rsub__`, etc.)
- In-place operations (`+=`, `-=`, etc.)
- Unary operations (`-`, `+`, `abs()`, `round()`)
- All comparison operations (`==`, `<`, `<=`, `>`, `>=`)
- Comparisons with floats
- Sorting and boolean conversion
- Complex mixed operations

Run tests:
```bash
python test_old_money.py
```

Currently: **90+ passing tests**

## Project Structure

```
lsd/
├── old_money.py          # Main OldMoney class
├── examples.py           # Comprehensive examples
├── test_old_money.py     # Unit tests
└── README.md            # This file
```

## Historical Context

Pre-decimal British currency (£sd or LSD from Latin *librae, solidi, denarii*) was used in the UK until decimalization on 15 February 1971. The system's complexity makes it an excellent demonstration of Python's dunder methods!

### Common Pre-Decimal Amounts

- **Guinea**: 21 shillings (£1 1s)
- **Crown**: 5 shillings
- **Half-crown**: 2s 6d
- **Florin**: 2 shillings
- **Shilling**: 12 pence
- **Sixpence**: 6d
- **Threepence**: 3d