"""
OldMoney - Pre-decimal British Currency (£sd) with Farthing Precision

Represents pre-decimal British currency (used until 1971):
- 1 pound (£) = 20 shillings (s) = 240 pence (d) = 960 farthings
- 1 shilling = 12 pence = 48 farthings  
- 1 penny = 4 farthings

Farthings notation: ¼d, ½d, ¾d

Internal storage: total farthings (integer) for exact precision
"""


class OldMoney:
    """
    Pre-decimal British currency with farthing precision.
    
    Supports negative values. No maximum/minimum limits.
    Internally stores value as total farthings for precision.
    """
    
    # Conversion constants
    FARTHINGS_PER_PENNY = 4
    FARTHINGS_PER_SHILLING = 48  # 12 pence × 4
    FARTHINGS_PER_POUND = 960    # 240 pence × 4
    
    def __init__(self, pounds=0, shillings=0, pence=0, farthings=0):
        """
        Initialize OldMoney with pounds, shillings, pence, and farthings.
        
        Args:
            pounds: Number of pounds (can be negative)
            shillings: Number of shillings (can be negative)
            pence: Number of pence (can be negative)
            farthings: Number of farthings (can be negative)
            
        Examples:
            >>> OldMoney(1, 5, 6)        # £1 5s 6d
            >>> OldMoney(0, 0, 0, 1)     # ¼d (one farthing)
            >>> OldMoney(-1, -5, -6)     # -£1 5s 6d (debt)
        """
        # Convert all components to farthings and store internally
        self._farthings = (
            pounds * self.FARTHINGS_PER_POUND +
            shillings * self.FARTHINGS_PER_SHILLING +
            pence * self.FARTHINGS_PER_PENNY +
            farthings
        )
    
    @classmethod
    def from_decimal(cls, decimal_pounds):
        """
        Create OldMoney from decimal pounds.
        
        Args:
            decimal_pounds: Decimal value in pounds (e.g., 1.275)
            
        Returns:
            OldMoney instance
            
        Examples:
            >>> OldMoney.from_decimal(1.275)   # £1 5s 6d
            >>> OldMoney.from_decimal(0.00104) # ¼d (1 farthing)
        """
        # Convert to farthings and round to nearest farthing
        total_farthings = round(decimal_pounds * cls.FARTHINGS_PER_POUND)
        return cls.from_farthings(total_farthings)
    
    @classmethod
    def from_pence(cls, decimal_pence):
        """
        Create OldMoney from decimal pence.
        
        Args:
            decimal_pence: Decimal value in pence (e.g., 5.75 for 5¾d)
            
        Returns:
            OldMoney instance
            
        Examples:
            >>> OldMoney.from_pence(30.5)  # 2s 6½d
            >>> OldMoney.from_pence(6.25)  # 6¼d
        """
        total_farthings = round(decimal_pence * cls.FARTHINGS_PER_PENNY)
        return cls.from_farthings(total_farthings)
    
    @classmethod
    def from_farthings(cls, total_farthings):
        """
        Create OldMoney directly from total farthings.
        
        Args:
            total_farthings: Total number of farthings
            
        Returns:
            OldMoney instance
            
        Examples:
            >>> OldMoney.from_farthings(960)  # £1
            >>> OldMoney.from_farthings(1)    # ¼d
        """
        instance = cls()
        instance._farthings = int(total_farthings)
        return instance
    
    def to_components(self):
        """
        Convert internal farthings to (pounds, shillings, pence, farthings) tuple.
        
        Returns:
            Tuple of (pounds, shillings, pence, farthings)
            
        Examples:
            >>> money = OldMoney(1, 5, 6, 3)
            >>> money.to_components()
            (1, 5, 6, 3)
        """
        farthings = self._farthings
        negative = farthings < 0
        farthings = abs(farthings)
        
        pounds = farthings // self.FARTHINGS_PER_POUND
        farthings %= self.FARTHINGS_PER_POUND
        
        shillings = farthings // self.FARTHINGS_PER_SHILLING
        farthings %= self.FARTHINGS_PER_SHILLING
        
        pence = farthings // self.FARTHINGS_PER_PENNY
        farthings %= self.FARTHINGS_PER_PENNY
        
        if negative:
            pounds = -pounds if pounds else 0
            shillings = -shillings if shillings else 0
            pence = -pence if pence else 0
            farthings = -farthings if farthings else 0
        
        return (pounds, shillings, pence, farthings)
    
    def __repr__(self):
        """
        Developer-friendly representation.
        
        Returns:
            String like "OldMoney(1, 5, 6, 2)" for £1 5s 6½d
        """
        pounds, shillings, pence, farthings = self.to_components()
        return f"OldMoney({pounds}, {shillings}, {pence}, {farthings})"
    
    def __str__(self):
        """
        User-friendly representation with traditional notation.
        
        Returns:
            String like "£1 5s 6d" or "2s 6½d" or "¼d"
            Uses special symbols for farthings: ¼ ½ ¾
        """
        if self._farthings == 0:
            return "£0"
        
        pounds, shillings, pence, farthings = self.to_components()
        negative = self._farthings < 0
        
        # Work with absolute values for formatting
        pounds, shillings, pence, farthings = (
            abs(pounds), abs(shillings), abs(pence), abs(farthings)
        )
        
        parts = []
        
        # Add pounds if non-zero
        if pounds:
            parts.append(f"£{pounds}")
        
        # Add shillings if non-zero
        if shillings:
            parts.append(f"{shillings}s")
        
        # Add pence and farthings
        if pence or farthings:
            if farthings == 0:
                parts.append(f"{pence}d")
            elif farthings == 1:
                # Quarter penny
                if pence:
                    parts.append(f"{pence}¼d")
                else:
                    parts.append("¼d")
            elif farthings == 2:
                # Half penny
                if pence:
                    parts.append(f"{pence}½d")
                else:
                    parts.append("½d")
            elif farthings == 3:
                # Three farthings
                if pence:
                    parts.append(f"{pence}¾d")
                else:
                    parts.append("¾d")
        
        # Handle edge case: only farthings, no other units
        if not parts and farthings:
            if farthings == 1:
                parts.append("¼d")
            elif farthings == 2:
                parts.append("½d")
            elif farthings == 3:
                parts.append("¾d")
        
        result = " ".join(parts)
        return f"-{result}" if negative else result
    
    def __float__(self):
        """
        Convert to decimal pounds with 3 decimal places.
        
        Returns:
            Float value in pounds (e.g., 1.276 for £1 5s 6¼d)
            
        Examples:
            >>> float(OldMoney(1, 5, 6))    # 1.275
            >>> float(OldMoney(0, 0, 0, 1)) # 0.001
        """
        decimal_pounds = self._farthings / self.FARTHINGS_PER_POUND
        return round(decimal_pounds, 3)
    
    def __int__(self):
        """
        Convert to total pence (rounded down from farthings).
        
        Returns:
            Integer number of pence
            
        Examples:
            >>> int(OldMoney(1, 5, 6))     # 306
            >>> int(OldMoney(0, 0, 0, 3))  # 0 (¾d rounds down)
        """
        return self._farthings // self.FARTHINGS_PER_PENNY
    
    def to_decimal(self, precision=3):
        """
        Explicit conversion to decimal pounds with configurable precision.
        
        Args:
            precision: Number of decimal places (default 3)
            
        Returns:
            Float value in pounds
        """
        decimal_pounds = self._farthings / self.FARTHINGS_PER_POUND
        return round(decimal_pounds, precision)
    
    def to_pence(self):
        """
        Convert to decimal pence (including fractional farthings).
        
        Returns:
            Float value in pence
            
        Examples:
            >>> OldMoney(0, 2, 6).to_pence()    # 30.0
            >>> OldMoney(0, 0, 0, 2).to_pence() # 0.5 (half penny)
        """
        return self._farthings / self.FARTHINGS_PER_PENNY
    
    def to_farthings(self):
        """
        Get the internal farthing value.
        
        Returns:
            Integer number of farthings
        """
        return self._farthings
    
    def is_negative(self):
        """
        Check if the amount is negative (debt/credit).
        
        Returns:
            Boolean indicating if value is negative
        """
        return self._farthings < 0
    
    def is_zero(self):
        """
        Check if the amount is zero.
        
        Returns:
            Boolean indicating if value is zero
        """
        return self._farthings == 0
    
    # ============================================================
    # Arithmetic Operations (Phase 2)
    # ============================================================
    
    def __add__(self, other):
        """
        Add two OldMoney amounts or add a float (auto-converts from decimal pounds).
        
        Args:
            other: OldMoney instance or numeric value (treated as decimal pounds)
            
        Returns:
            New OldMoney instance with sum
            
        Examples:
            >>> OldMoney(1, 0, 0) + OldMoney(0, 5, 6)  # £1 + 5s 6d
            >>> OldMoney(1, 0, 0) + 0.5                 # £1 + £0.5 = £1 10s
        """
        if isinstance(other, OldMoney):
            return OldMoney.from_farthings(self._farthings + other._farthings)
        elif isinstance(other, (int, float)):
            other_money = OldMoney.from_decimal(other)
            return self + other_money
        return NotImplemented
    
    def __radd__(self, other):
        """Right-hand addition: support float + OldMoney."""
        return self.__add__(other)
    
    def __sub__(self, other):
        """
        Subtract two OldMoney amounts or subtract a float.
        
        Args:
            other: OldMoney instance or numeric value (treated as decimal pounds)
            
        Returns:
            New OldMoney instance with difference
            
        Examples:
            >>> OldMoney(1, 5, 6) - OldMoney(0, 5, 6)  # £1 5s 6d - 5s 6d = £1
            >>> OldMoney(2, 0, 0) - 0.5                 # £2 - £0.5 = £1 10s
        """
        if isinstance(other, OldMoney):
            return OldMoney.from_farthings(self._farthings - other._farthings)
        elif isinstance(other, (int, float)):
            other_money = OldMoney.from_decimal(other)
            return self - other_money
        return NotImplemented
    
    def __rsub__(self, other):
        """Right-hand subtraction: support float - OldMoney."""
        if isinstance(other, (int, float)):
            other_money = OldMoney.from_decimal(other)
            return other_money - self
        return NotImplemented
    
    def __mul__(self, other):
        """
        Multiply OldMoney by a scalar.
        
        Args:
            other: Numeric multiplier (int or float)
            
        Returns:
            New OldMoney instance with product
            
        Examples:
            >>> OldMoney(0, 2, 6) * 3      # 2s 6d × 3 = 7s 6d
            >>> OldMoney(1, 5, 6) * 2.5    # £1 5s 6d × 2.5
        """
        if isinstance(other, (int, float)):
            # Multiply farthings and round to nearest farthing
            new_farthings = round(self._farthings * other)
            return OldMoney.from_farthings(new_farthings)
        return NotImplemented
    
    def __rmul__(self, other):
        """Right-hand multiplication: support scalar * OldMoney."""
        return self.__mul__(other)
    
    def __truediv__(self, other):
        """
        Divide OldMoney by a scalar or by another OldMoney amount.
        
        Args:
            other: Numeric divisor (int/float) or OldMoney instance
            
        Returns:
            If other is numeric: New OldMoney instance with quotient
            If other is OldMoney: Float ratio between amounts
            
        Examples:
            >>> OldMoney(1, 0, 0) / 2       # £1 ÷ 2 = 10s
            >>> OldMoney(1, 0, 0) / OldMoney(0, 10, 0)  # £1 ÷ 10s = 2.0
        """
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            new_farthings = round(self._farthings / other)
            return OldMoney.from_farthings(new_farthings)
        elif isinstance(other, OldMoney):
            if other._farthings == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return self._farthings / other._farthings
        return NotImplemented
    
    def __rtruediv__(self, other):
        """Right-hand division: support float / OldMoney."""
        if isinstance(other, (int, float)):
            other_money = OldMoney.from_decimal(other)
            return other_money / self
        return NotImplemented
    
    def __floordiv__(self, other):
        """
        Floor division of OldMoney.
        
        Args:
            other: Numeric divisor (int/float) or OldMoney instance
            
        Returns:
            If other is numeric: New OldMoney instance with floor quotient
            If other is OldMoney: Integer ratio (floor division)
            
        Examples:
            >>> OldMoney(1, 0, 0) // 3      # £1 ÷ 3 (rounded down)
        """
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            new_farthings = self._farthings // other
            return OldMoney.from_farthings(new_farthings)
        elif isinstance(other, OldMoney):
            if other._farthings == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return self._farthings // other._farthings
        return NotImplemented
    
    def __mod__(self, other):
        """
        Modulo operation for OldMoney.
        
        Args:
            other: Numeric divisor (int/float) or OldMoney instance
            
        Returns:
            New OldMoney instance with remainder
            
        Examples:
            >>> OldMoney(1, 0, 0) % OldMoney(0, 7, 0)  # £1 mod 7s
        """
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            other_money = OldMoney.from_decimal(other)
            remainder_farthings = self._farthings % other_money._farthings
            return OldMoney.from_farthings(remainder_farthings)
        elif isinstance(other, OldMoney):
            if other._farthings == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            remainder_farthings = self._farthings % other._farthings
            return OldMoney.from_farthings(remainder_farthings)
        return NotImplemented
    
    def __divmod__(self, other):
        """
        Return quotient and remainder.
        
        Returns:
            Tuple of (quotient, remainder)
        """
        return (self // other, self % other)
    
    # In-place operations
    def __iadd__(self, other):
        """In-place addition."""
        result = self + other
        self._farthings = result._farthings
        return self
    
    def __isub__(self, other):
        """In-place subtraction."""
        result = self - other
        self._farthings = result._farthings
        return self
    
    def __imul__(self, other):
        """In-place multiplication."""
        result = self * other
        self._farthings = result._farthings
        return self
    
    def __itruediv__(self, other):
        """In-place division."""
        result = self / other
        if isinstance(result, OldMoney):
            self._farthings = result._farthings
            return self
        else:
            # Division by OldMoney returns float, can't do in-place
            return NotImplemented
    
    def __ifloordiv__(self, other):
        """In-place floor division."""
        result = self // other
        if isinstance(result, OldMoney):
            self._farthings = result._farthings
            return self
        else:
            return NotImplemented
    
    def __imod__(self, other):
        """In-place modulo."""
        result = self % other
        self._farthings = result._farthings
        return self
    
    # ============================================================
    # Unary Operations (Phase 2)
    # ============================================================
    
    def __neg__(self):
        """
        Negate the amount (change sign).
        
        Returns:
            New OldMoney instance with negated value
            
        Examples:
            >>> -OldMoney(1, 5, 6)  # -£1 5s 6d
        """
        return OldMoney.from_farthings(-self._farthings)
    
    def __pos__(self):
        """
        Unary plus (returns copy).
        
        Returns:
            New OldMoney instance with same value
        """
        return OldMoney.from_farthings(self._farthings)
    
    def __abs__(self):
        """
        Absolute value of amount.
        
        Returns:
            New OldMoney instance with absolute value
            
        Examples:
            >>> abs(OldMoney(-1, -5, -6))  # £1 5s 6d
        """
        return OldMoney.from_farthings(abs(self._farthings))
    
    def __round__(self, ndigits=None):
        """
        Round to nearest penny, shilling, or pound.
        
        Args:
            ndigits: Not used (for compatibility)
            
        Returns:
            New OldMoney instance rounded to nearest penny
        """
        # Round to nearest penny (4 farthings)
        pence_count = round(self._farthings / self.FARTHINGS_PER_PENNY)
        return OldMoney.from_farthings(pence_count * self.FARTHINGS_PER_PENNY)
    
    # ============================================================
    # Comparison Operations (Phase 2)
    # ============================================================
    
    def __eq__(self, other):
        """
        Check equality.
        
        Args:
            other: OldMoney instance or numeric value (decimal pounds)
            
        Returns:
            Boolean indicating equality
            
        Examples:
            >>> OldMoney(1, 0, 0) == OldMoney.from_decimal(1.0)  # True
        """
        if isinstance(other, OldMoney):
            return self._farthings == other._farthings
        elif isinstance(other, (int, float)):
            other_money = OldMoney.from_decimal(other)
            return self._farthings == other_money._farthings
        return NotImplemented
    
    def __ne__(self, other):
        """Check inequality."""
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    
    def __lt__(self, other):
        """
        Check if less than.
        
        Args:
            other: OldMoney instance or numeric value (decimal pounds)
            
        Returns:
            Boolean indicating if self < other
        """
        if isinstance(other, OldMoney):
            return self._farthings < other._farthings
        elif isinstance(other, (int, float)):
            other_money = OldMoney.from_decimal(other)
            return self._farthings < other_money._farthings
        return NotImplemented
    
    def __le__(self, other):
        """Check if less than or equal."""
        if isinstance(other, OldMoney):
            return self._farthings <= other._farthings
        elif isinstance(other, (int, float)):
            other_money = OldMoney.from_decimal(other)
            return self._farthings <= other_money._farthings
        return NotImplemented
    
    def __gt__(self, other):
        """Check if greater than."""
        if isinstance(other, OldMoney):
            return self._farthings > other._farthings
        elif isinstance(other, (int, float)):
            other_money = OldMoney.from_decimal(other)
            return self._farthings > other_money._farthings
        return NotImplemented
    
    def __ge__(self, other):
        """Check if greater than or equal."""
        if isinstance(other, OldMoney):
            return self._farthings >= other._farthings
        elif isinstance(other, (int, float)):
            other_money = OldMoney.from_decimal(other)
            return self._farthings >= other_money._farthings
        return NotImplemented
    
    def __bool__(self):
        """
        Boolean conversion (True if non-zero).
        
        Returns:
            False if zero, True otherwise
            
        Examples:
            >>> bool(OldMoney())        # False
            >>> bool(OldMoney(0, 0, 1)) # True
        """
        return self._farthings != 0


if __name__ == "__main__":
    # Quick demonstration
    print("=== Pre-Decimal British Currency Demo ===")
    print("Demonstrating Python Dunder Methods\n")
    
    print("--- Phase 1: Initialization & Conversion ---")
    # Basic creation
    price1 = OldMoney(1, 5, 6)
    print(f"Traditional: {price1}")
    print(f"Decimal: {float(price1)} pounds")
    print(f"Repr: {repr(price1)}\n")
    
    # From decimal
    price2 = OldMoney.from_decimal(1.275)
    print(f"From decimal 1.275: {price2}")
    print(f"Back to decimal: {float(price2)} pounds\n")
    
    # Farthings
    farthing = OldMoney(0, 0, 0, 1)
    halfpenny = OldMoney(0, 0, 0, 2)
    print(f"One farthing: {farthing} = {float(farthing)} pounds")
    print(f"Half penny: {halfpenny} = {float(halfpenny)} pounds\n")
    
    print("--- Phase 2: Arithmetic Operations ---")
    # Addition
    total = OldMoney(1, 0, 0) + OldMoney(0, 5, 6)
    print(f"Addition: £1 + 5s 6d = {total}")
    
    # Float auto-conversion
    with_float = OldMoney(1, 0, 0) + 0.5
    print(f"With float: £1 + 0.5 = {with_float}")
    
    # Multiplication
    bulk = OldMoney(0, 2, 6) * 4
    print(f"Multiply: 2s 6d × 4 = {bulk}")
    
    # Division
    split = OldMoney(1, 0, 0) / 2
    print(f"Division: £1 / 2 = {split}\n")
    
    print("--- Phase 2: Comparisons ---")
    money1 = OldMoney(1, 5, 6)
    money2 = OldMoney(2, 0, 0)
    print(f"{money1} < {money2}: {money1 < money2}")
    print(f"{money1} == {OldMoney(1, 5, 6)}: {money1 == OldMoney(1, 5, 6)}")
    
    # Sorting
    amounts = [OldMoney(2, 0, 0), OldMoney(0, 5, 6), OldMoney(1, 10, 0)]
    sorted_amounts = sorted(amounts)
    print(f"Sorted: {[str(m) for m in sorted_amounts]}\n")
    
    print("--- Phase 2: Unary Operations ---")
    # Negation
    debt = OldMoney(-2, -10, -6, -2)
    print(f"Debt: {debt}")
    print(f"Absolute: {abs(debt)}")
    print(f"As decimal: {float(debt)} pounds\n")
    
    print("Run examples.py for comprehensive demonstrations!")
    print("Run test_old_money.py to see all 83 tests pass!")
