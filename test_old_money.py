"""
Unit tests for OldMoney class - Phase 1

Tests initialization, conversion, representation, and basic functionality.
"""

import unittest
from old_money import OldMoney


class TestInitialization(unittest.TestCase):
    """Test __init__ and basic creation."""
    
    def test_init_zero(self):
        """Test initialization with zero values."""
        money = OldMoney()
        assert money.to_farthings() == 0
        assert str(money) == "£0"
    
    def test_init_pounds_only(self):
        """Test initialization with only pounds."""
        money = OldMoney(5)
        assert money.to_components() == (5, 0, 0, 0)
        assert str(money) == "£5"
    
    def test_init_full_components(self):
        """Test initialization with all components."""
        money = OldMoney(1, 5, 6, 2)
        assert money.to_components() == (1, 5, 6, 2)
    
    def test_init_internal_farthings_calculation(self):
        """Test that internal farthings are calculated correctly."""
        # £1 5s 6d 2f = 960 + 240 + 24 + 2 = 1226 farthings
        money = OldMoney(1, 5, 6, 2)
        expected_farthings = (1 * 960) + (5 * 48) + (6 * 4) + 2
        assert money.to_farthings() == expected_farthings
        assert money.to_farthings() == 1226
    
    def test_init_negative_values(self):
        """Test initialization with negative values."""
        money = OldMoney(-1, -5, -6)
        assert money.is_negative()
        assert money.to_farthings() == -1224


class TestClassMethods(unittest.TestCase):
    """Test factory class methods."""
    
    def test_from_farthings(self):
        """Test creation from farthings."""
        money = OldMoney.from_farthings(960)
        assert money.to_components() == (1, 0, 0, 0)
        
        money = OldMoney.from_farthings(1)
        assert money.to_components() == (0, 0, 0, 1)
    
    def test_from_decimal_simple(self):
        """Test creation from decimal pounds."""
        # 1.275 pounds = £1 5s 6d
        money = OldMoney.from_decimal(1.275)
        pounds, shillings, pence, farthings = money.to_components()
        assert pounds == 1
        assert shillings == 5
        assert pence == 6
        assert farthings == 0
    
    def test_from_decimal_with_farthings(self):
        """Test decimal conversion with farthing precision."""
        # 1.276042 pounds = £1 5s 6¼d (1 farthing = 0.001042 pounds)
        money = OldMoney.from_decimal(1.276042)
        pounds, shillings, pence, farthings = money.to_components()
        assert pounds == 1
        assert shillings == 5
        assert pence == 6
        assert farthings == 1
    
    def test_from_decimal_small_amount(self):
        """Test decimal conversion for small amounts."""
        # One farthing ≈ 0.00104 pounds
        money = OldMoney.from_decimal(0.00104)
        assert money.to_components() == (0, 0, 0, 1)
    
    def test_from_decimal_negative(self):
        """Test decimal conversion with negative value."""
        money = OldMoney.from_decimal(-2.5)
        assert money.is_negative()
        pounds, shillings, pence, _ = money.to_components()
        assert pounds == -2
        assert shillings == -10
    
    def test_from_pence_simple(self):
        """Test creation from decimal pence."""
        # 30 pence = 2s 6d
        money = OldMoney.from_pence(30)
        assert money.to_components() == (0, 2, 6, 0)
    
    def test_from_pence_with_farthings(self):
        """Test pence conversion with farthings."""
        # 6.25 pence = 6¼d
        money = OldMoney.from_pence(6.25)
        assert money.to_components() == (0, 0, 6, 1)
        
        # 0.5 pence = ½d
        money = OldMoney.from_pence(0.5)
        assert money.to_components() == (0, 0, 0, 2)


class TestConversions(unittest.TestCase):
    """Test conversion methods."""
    
    def test_to_components_simple(self):
        """Test component extraction."""
        money = OldMoney(1, 5, 6, 3)
        assert money.to_components() == (1, 5, 6, 3)
    
    def test_to_components_normalization(self):
        """Test that components are normalized correctly."""
        # Internal storage handles normalization
        money = OldMoney.from_farthings(1226)  # Should be £1 5s 6½d
        pounds, shillings, pence, farthings = money.to_components()
        assert pounds == 1
        assert shillings == 5
        assert pence == 6
        assert farthings == 2
    
    def test_float_conversion(self):
        """Test __float__ conversion to decimal pounds."""
        money = OldMoney(1, 5, 6)
        # 306 pence / 240 = 1.275
        assert float(money) == 1.275
    
    def test_float_conversion_farthings(self):
        """Test float conversion with farthing precision."""
        money = OldMoney(0, 0, 0, 1)  # One farthing
        # 1 farthing / 960 = 0.00104166... ≈ 0.001 (3 decimals)
        assert float(money) == 0.001
        
        money = OldMoney(0, 0, 0, 2)  # Half penny
        assert float(money) == 0.002
    
    def test_float_conversion_negative(self):
        """Test float conversion with negative values."""
        money = OldMoney(-1, -5, -6)
        assert float(money) == -1.275
    
    def test_int_conversion(self):
        """Test __int__ conversion to pence."""
        money = OldMoney(1, 5, 6)
        assert int(money) == 306
        
        money = OldMoney(0, 2, 6)
        assert int(money) == 30
    
    def test_int_conversion_rounds_down(self):
        """Test that int conversion rounds down farthings."""
        money = OldMoney(0, 0, 0, 3)  # ¾d
        assert int(money) == 0
        
        money = OldMoney(0, 0, 1, 2)  # 1½d
        assert int(money) == 1
    
    def test_to_decimal_custom_precision(self):
        """Test to_decimal with custom precision."""
        money = OldMoney(1, 5, 6, 1)
        assert money.to_decimal(precision=3) == 1.276
        assert money.to_decimal(precision=6) == 1.276042
    
    def test_to_pence(self):
        """Test to_pence conversion."""
        money = OldMoney(0, 2, 6)
        assert money.to_pence() == 30.0
        
        money = OldMoney(0, 0, 0, 2)  # Half penny
        assert money.to_pence() == 0.5
    
    def test_to_farthings(self):
        """Test to_farthings getter."""
        money = OldMoney(1, 0, 0)
        assert money.to_farthings() == 960


class TestRepresentation(unittest.TestCase):
    """Test __str__ and __repr__ methods."""
    
    def test_repr(self):
        """Test __repr__ output."""
        money = OldMoney(1, 5, 6, 2)
        assert repr(money) == "OldMoney(1, 5, 6, 2)"
    
    def test_str_full_components(self):
        """Test __str__ with all components."""
        money = OldMoney(1, 5, 6)
        assert str(money) == "£1 5s 6d"
    
    def test_str_pounds_only(self):
        """Test string representation of pounds only."""
        money = OldMoney(5)
        assert str(money) == "£5"
    
    def test_str_shillings_and_pence(self):
        """Test string with shillings and pence."""
        money = OldMoney(0, 2, 6)
        assert str(money) == "2s 6d"
    
    def test_str_pence_only(self):
        """Test string with pence only."""
        money = OldMoney(0, 0, 6)
        assert str(money) == "6d"
    
    def test_str_farthing_symbols(self):
        """Test farthing special symbols."""
        money = OldMoney(0, 0, 0, 1)
        assert str(money) == "¼d"
        
        money = OldMoney(0, 0, 0, 2)
        assert str(money) == "½d"
        
        money = OldMoney(0, 0, 0, 3)
        assert str(money) == "¾d"
    
    def test_str_pence_with_farthings(self):
        """Test string with pence and farthings."""
        money = OldMoney(0, 0, 6, 1)
        assert str(money) == "6¼d"
        
        money = OldMoney(0, 0, 6, 2)
        assert str(money) == "6½d"
        
        money = OldMoney(0, 0, 6, 3)
        assert str(money) == "6¾d"
    
    def test_str_negative(self):
        """Test string representation of negative values."""
        money = OldMoney(-1, -5, -6)
        assert str(money) == "-£1 5s 6d"
        
        money = OldMoney(-0, -2, -6, -2)
        assert str(money) == "-2s 6½d"
    
    def test_str_zero(self):
        """Test string representation of zero."""
        money = OldMoney()
        assert str(money) == "£0"


class TestUtilityMethods(unittest.TestCase):
    """Test utility methods."""
    
    def test_is_negative(self):
        """Test is_negative method."""
        money = OldMoney(1, 5, 6)
        assert not money.is_negative()
        
        money = OldMoney(-1, -5, -6)
        assert money.is_negative()
        
        money = OldMoney()
        assert not money.is_negative()
    
    def test_is_zero(self):
        """Test is_zero method."""
        money = OldMoney()
        assert money.is_zero()
        
        money = OldMoney(0, 0, 0, 1)
        assert not money.is_zero()
        
        money = OldMoney(1, 5, 6)
        assert not money.is_zero()


class TestRoundTripping(unittest.TestCase):
    """Test conversion round-tripping."""
    
    def test_roundtrip_decimal(self):
        """Test conversion to decimal and back."""
        original = OldMoney(1, 5, 6)
        decimal_value = float(original)
        restored = OldMoney.from_decimal(decimal_value)
        assert original.to_farthings() == restored.to_farthings()
    
    def test_roundtrip_pence(self):
        """Test conversion to pence and back."""
        original = OldMoney(0, 2, 6, 2)
        pence_value = original.to_pence()
        restored = OldMoney.from_pence(pence_value)
        assert original.to_farthings() == restored.to_farthings()
    
    def test_roundtrip_components(self):
        """Test component extraction and reconstruction."""
        original = OldMoney(1, 5, 6, 3)
        p, s, d, f = original.to_components()
        restored = OldMoney(p, s, d, f)
        assert original.to_farthings() == restored.to_farthings()


class TestArithmeticOperations(unittest.TestCase):
    """Test arithmetic operations (Phase 2)."""
    
    def test_add_two_amounts(self):
        """Test adding two OldMoney amounts."""
        money1 = OldMoney(1, 0, 0)      # £1
        money2 = OldMoney(0, 5, 6)      # 5s 6d
        result = money1 + money2
        assert result.to_components() == (1, 5, 6, 0)
    
    def test_add_with_float(self):
        """Test adding float to OldMoney (auto-converts)."""
        money = OldMoney(1, 0, 0)       # £1
        result = money + 0.5             # Add £0.5 (10s)
        assert result == OldMoney(1, 10, 0)
    
    def test_radd_float(self):
        """Test float + OldMoney."""
        money = OldMoney(0, 10, 0)      # 10s
        result = 1.0 + money             # £1 + 10s
        assert result == OldMoney(1, 10, 0)
    
    def test_subtract_two_amounts(self):
        """Test subtracting two OldMoney amounts."""
        money1 = OldMoney(1, 5, 6)
        money2 = OldMoney(0, 5, 6)
        result = money1 - money2
        assert result == OldMoney(1, 0, 0)
    
    def test_subtract_with_float(self):
        """Test subtracting float from OldMoney."""
        money = OldMoney(2, 0, 0)       # £2
        result = money - 0.5             # Subtract £0.5
        assert result == OldMoney(1, 10, 0)
    
    def test_rsub_float(self):
        """Test float - OldMoney."""
        money = OldMoney(0, 10, 0)      # 10s
        result = 2.0 - money             # £2 - 10s
        assert result == OldMoney(1, 10, 0)
    
    def test_multiply_by_integer(self):
        """Test multiplying by integer."""
        money = OldMoney(0, 2, 6)       # 2s 6d
        result = money * 3
        assert result == OldMoney(0, 7, 6)
    
    def test_multiply_by_float(self):
        """Test multiplying by float."""
        money = OldMoney(1, 0, 0)       # £1
        result = money * 2.5
        assert result == OldMoney(2, 10, 0)
    
    def test_rmul(self):
        """Test scalar * OldMoney."""
        money = OldMoney(0, 5, 0)       # 5s
        result = 4 * money
        assert result == OldMoney(1, 0, 0)
    
    def test_divide_by_scalar(self):
        """Test dividing by scalar."""
        money = OldMoney(1, 0, 0)       # £1
        result = money / 2
        assert result == OldMoney(0, 10, 0)
    
    def test_divide_by_oldmoney(self):
        """Test dividing by another OldMoney (returns ratio)."""
        money1 = OldMoney(1, 0, 0)      # £1
        money2 = OldMoney(0, 10, 0)     # 10s
        result = money1 / money2
        assert result == 2.0
    
    def test_divide_by_zero(self):
        """Test division by zero raises error."""
        money = OldMoney(1, 0, 0)
        with self.assertRaises(ZeroDivisionError):
            money / 0
    
    def test_floordiv_by_scalar(self):
        """Test floor division by scalar."""
        money = OldMoney(1, 0, 0)       # £1
        result = money // 3
        # 960 farthings // 3 = 320 farthings = 6s 8d
        assert result.to_farthings() == 320
    
    def test_floordiv_by_oldmoney(self):
        """Test floor division by OldMoney."""
        money1 = OldMoney(1, 0, 0)      # £1 = 960 farthings
        money2 = OldMoney(0, 7, 0)      # 7s = 336 farthings
        result = money1 // money2
        assert result == 2  # 960 // 336 = 2
    
    def test_modulo_by_oldmoney(self):
        """Test modulo operation."""
        money1 = OldMoney(1, 0, 0)      # £1
        money2 = OldMoney(0, 7, 0)      # 7s
        result = money1 % money2
        # £1 = 960 farthings, 7s = 336 farthings
        # 960 % 336 = 288 farthings = 6s
        assert result == OldMoney(0, 6, 0)
    
    def test_divmod(self):
        """Test divmod operation."""
        money1 = OldMoney(1, 0, 0)      # £1
        money2 = OldMoney(0, 7, 0)      # 7s
        quotient, remainder = divmod(money1, money2)
        assert quotient == 2
        assert remainder == OldMoney(0, 6, 0)
    
    def test_iadd(self):
        """Test in-place addition."""
        money = OldMoney(1, 0, 0)
        money += OldMoney(0, 5, 6)
        assert money == OldMoney(1, 5, 6)
    
    def test_isub(self):
        """Test in-place subtraction."""
        money = OldMoney(2, 0, 0)
        money -= OldMoney(0, 10, 0)
        assert money == OldMoney(1, 10, 0)
    
    def test_imul(self):
        """Test in-place multiplication."""
        money = OldMoney(0, 5, 0)
        money *= 2
        assert money == OldMoney(0, 10, 0)
    
    def test_itruediv(self):
        """Test in-place division."""
        money = OldMoney(1, 0, 0)
        money /= 2
        assert money == OldMoney(0, 10, 0)
    
    def test_negative_result(self):
        """Test arithmetic producing negative result."""
        money1 = OldMoney(1, 0, 0)
        money2 = OldMoney(2, 0, 0)
        result = money1 - money2
        assert result.is_negative()
        assert result == OldMoney(-1, 0, 0)


class TestUnaryOperations(unittest.TestCase):
    """Test unary operations (Phase 2)."""
    
    def test_neg(self):
        """Test negation."""
        money = OldMoney(1, 5, 6)
        result = -money
        assert result == OldMoney(-1, -5, -6)
        assert result.is_negative()
    
    def test_neg_negative(self):
        """Test negating negative amount."""
        money = OldMoney(-1, -5, -6)
        result = -money
        assert result == OldMoney(1, 5, 6)
        assert not result.is_negative()
    
    def test_pos(self):
        """Test unary plus."""
        money = OldMoney(1, 5, 6)
        result = +money
        assert result == money
        assert result is not money  # Should be a copy
    
    def test_abs_positive(self):
        """Test absolute value of positive amount."""
        money = OldMoney(1, 5, 6)
        result = abs(money)
        assert result == money
    
    def test_abs_negative(self):
        """Test absolute value of negative amount."""
        money = OldMoney(-1, -5, -6)
        result = abs(money)
        assert result == OldMoney(1, 5, 6)
        assert not result.is_negative()
    
    def test_round(self):
        """Test rounding to nearest penny."""
        # Rounds farthings to nearest penny
        money = OldMoney(0, 0, 0, 3)    # ¾d
        result = round(money)
        assert result == OldMoney(0, 0, 1, 0)  # Rounds to 1d
        
        money2 = OldMoney(0, 0, 0, 1)   # ¼d
        result2 = round(money2)
        assert result2 == OldMoney(0, 0, 0, 0)  # Rounds to 0d


class TestComparisonOperations(unittest.TestCase):
    """Test comparison operations (Phase 2)."""
    
    def test_eq_same_amounts(self):
        """Test equality of same amounts."""
        money1 = OldMoney(1, 5, 6)
        money2 = OldMoney(1, 5, 6)
        assert money1 == money2
    
    def test_eq_different_amounts(self):
        """Test inequality of different amounts."""
        money1 = OldMoney(1, 5, 6)
        money2 = OldMoney(1, 5, 7)
        assert not (money1 == money2)
    
    def test_eq_with_float(self):
        """Test equality with float."""
        money = OldMoney(1, 0, 0)
        assert money == 1.0
        assert money == OldMoney.from_decimal(1.0)
    
    def test_ne(self):
        """Test not equal."""
        money1 = OldMoney(1, 0, 0)
        money2 = OldMoney(2, 0, 0)
        assert money1 != money2
    
    def test_lt(self):
        """Test less than."""
        money1 = OldMoney(1, 0, 0)
        money2 = OldMoney(2, 0, 0)
        assert money1 < money2
        assert not (money2 < money1)
    
    def test_lt_with_float(self):
        """Test less than with float."""
        money = OldMoney(0, 10, 0)      # 10s = 0.5 pounds
        assert money < 1.0
        assert money < OldMoney.from_decimal(1.0)
    
    def test_le(self):
        """Test less than or equal."""
        money1 = OldMoney(1, 0, 0)
        money2 = OldMoney(2, 0, 0)
        money3 = OldMoney(1, 0, 0)
        assert money1 <= money2
        assert money1 <= money3
        assert not (money2 <= money1)
    
    def test_gt(self):
        """Test greater than."""
        money1 = OldMoney(2, 0, 0)
        money2 = OldMoney(1, 0, 0)
        assert money1 > money2
        assert not (money2 > money1)
    
    def test_gt_with_float(self):
        """Test greater than with float."""
        money = OldMoney(2, 0, 0)
        assert money > 1.0
        assert money > OldMoney.from_decimal(1.0)
    
    def test_ge(self):
        """Test greater than or equal."""
        money1 = OldMoney(2, 0, 0)
        money2 = OldMoney(1, 0, 0)
        money3 = OldMoney(2, 0, 0)
        assert money1 >= money2
        assert money1 >= money3
        assert not (money2 >= money1)
    
    def test_sorting(self):
        """Test that OldMoney can be sorted."""
        amounts = [
            OldMoney(2, 0, 0),
            OldMoney(0, 5, 6),
            OldMoney(1, 10, 0),
            OldMoney(0, 2, 3)
        ]
        sorted_amounts = sorted(amounts)
        assert sorted_amounts[0] == OldMoney(0, 2, 3)
        assert sorted_amounts[1] == OldMoney(0, 5, 6)
        assert sorted_amounts[2] == OldMoney(1, 10, 0)
        assert sorted_amounts[3] == OldMoney(2, 0, 0)
    
    def test_negative_comparisons(self):
        """Test comparisons with negative values."""
        money1 = OldMoney(-1, 0, 0)
        money2 = OldMoney(1, 0, 0)
        assert money1 < money2
        assert money2 > money1
        assert money1 < 0
        assert money2 > 0
    
    def test_bool_zero(self):
        """Test boolean conversion of zero."""
        money = OldMoney()
        assert not money
    
    def test_bool_nonzero(self):
        """Test boolean conversion of non-zero."""
        money = OldMoney(0, 0, 0, 1)
        assert money
    
    def test_bool_negative(self):
        """Test boolean conversion of negative."""
        money = OldMoney(-1, 0, 0)
        assert money  # Negative is still truthy


class TestMixedOperations(unittest.TestCase):
    """Test complex mixed operations (Phase 2)."""
    
    def test_chain_operations(self):
        """Test chaining multiple operations."""
        # (£1 + 10s) * 2 - £1
        result = (OldMoney(1, 0, 0) + OldMoney(0, 10, 0)) * 2 - OldMoney(1, 0, 0)
        assert result == OldMoney(2, 0, 0)
    
    def test_mixed_with_floats(self):
        """Test mixing OldMoney and floats."""
        # £1 + £0.5 - 0.25 = £1.25 = £1 5s
        result = OldMoney(1, 0, 0) + 0.5 - 0.25
        assert result == OldMoney(1, 5, 0)
    
    def test_expression_evaluation(self):
        """Test complex expression."""
        price = OldMoney(0, 2, 6)       # 2s 6d per item
        quantity = 5
        discount = OldMoney(0, 1, 0)    # 1s discount
        total = price * quantity - discount
        # 2s 6d × 5 = 12s 6d - 1s = 11s 6d
        assert total == OldMoney(0, 11, 6)
    
    def test_average_calculation(self):
        """Test calculating average."""
        amounts = [OldMoney(1, 0, 0), OldMoney(2, 0, 0), OldMoney(3, 0, 0)]
        total = sum(amounts, OldMoney())  # Start with zero
        average = total / len(amounts)
        assert average == OldMoney(2, 0, 0)
    
    def test_percentage_calculation(self):
        """Test percentage calculation."""
        amount = OldMoney(1, 0, 0)      # £1
        tax_rate = 0.20                  # 20% tax
        tax = amount * tax_rate
        total = amount + tax
        assert total == OldMoney(1, 4, 0)  # £1 + 4s = £1.20


if __name__ == "__main__":
    # Run tests with unittest
    unittest.main(verbosity=2)
