"""
Examples demonstrating OldMoney class - Phase 1

Shows initialization, conversion, and representation features.
"""

from old_money import OldMoney


def separator(title):
    """Print a section separator."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def example_basic_creation():
    """Demonstrate basic creation methods."""
    separator("Basic Creation")
    
    # Traditional notation
    price1 = OldMoney(1, 5, 6)
    print(f"OldMoney(1, 5, 6)        => {price1}")
    print(f"  As decimal:             {float(price1)} pounds")
    print(f"  Repr:                   {repr(price1)}")
    
    # Pounds only
    print(f"\nOldMoney(5)              => {OldMoney(5)}")
    
    # Shillings and pence
    print(f"OldMoney(0, 2, 6)        => {OldMoney(0, 2, 6)}")
    
    # Just pence
    print(f"OldMoney(0, 0, 6)        => {OldMoney(0, 0, 6)}")


def example_farthings():
    """Demonstrate farthing precision."""
    separator("Farthing Precision")
    
    print("Individual farthings:")
    print(f"  1 farthing:  {OldMoney(0, 0, 0, 1)} = {float(OldMoney(0, 0, 0, 1))} pounds")
    print(f"  2 farthings: {OldMoney(0, 0, 0, 2)} = {float(OldMoney(0, 0, 0, 2))} pounds")
    print(f"  3 farthings: {OldMoney(0, 0, 0, 3)} = {float(OldMoney(0, 0, 0, 3))} pounds")
    
    print("\nPence with farthings:")
    print(f"  Result: {OldMoney(0, 0, 6, 1)}")
    print(f"  Result: {OldMoney(0, 0, 6, 2)}")
    print(f"  Result: {OldMoney(0, 0, 6, 3)}")
    
    print("\nFull amount with farthings:")
    money = OldMoney(1, 5, 6, 3)
    print(f"  Display: {money}")
    print(f"  As decimal: {float(money)} pounds")
    print(f"  As pence: {money.to_pence()}d")
    print(f"  As farthings: {money.to_farthings()} farthings")


def example_decimal_conversion():
    """Demonstrate decimal conversion."""
    separator("Decimal Conversion")
    
    # From decimal to £sd
    print("From decimal pounds:")
    amounts = [1.275, 0.125, 2.5, 0.00104]
    for amount in amounts:
        money = OldMoney.from_decimal(amount)
        print(f"  {amount:7.5f} pounds => {str(money):15s} => {float(money)} pounds")
    
    # From £sd to decimal
    print("\nFrom old money to decimal:")
    examples = [
        OldMoney(1, 5, 6),
        OldMoney(0, 2, 6),
        OldMoney(0, 0, 6, 2),
        OldMoney(2, 10, 0)
    ]
    for money in examples:
        print(f"  {str(money):15s} => {float(money)} pounds")
    
    # Custom precision
    print("\nCustom decimal precision:")
    money = OldMoney(1, 5, 6, 1)
    print(f"  {money}")
    print(f"    3 decimals: {money.to_decimal(3)} pounds")
    print(f"    6 decimals: {money.to_decimal(6)} pounds")
    print(f"    9 decimals: {money.to_decimal(9)} pounds")


def example_pence_conversion():
    """Demonstrate pence conversion."""
    separator("Pence Conversion")
    
    print("From decimal pence:")
    pence_amounts = [30, 6.25, 0.5, 0.75, 12.5]
    for pence in pence_amounts:
        money = OldMoney.from_pence(pence)
        print(f"  {pence:5.2f}d => {str(money):10s} => {money.to_pence():.2f}d")
    
    print("\nFrom old money to pence:")
    examples = [
        OldMoney(0, 2, 6),      # 2s 6d = 30 pence
        OldMoney(1, 0, 0),      # £1 = 240 pence
        OldMoney(0, 0, 6, 2),   # 6½d = 6.5 pence
    ]
    for money in examples:
        print(f"  {str(money):15s} => {money.to_pence():.2f}d")


def example_negative_values():
    """Demonstrate negative values (debts/credits)."""
    separator("Negative Values")
    
    print("Creating negative amounts:")
    debt1 = OldMoney(-1, -5, -6)
    print(f"  OldMoney(-1, -5, -6)  => {debt1}")
    print(f"    As decimal:           {float(debt1)} pounds")
    print(f"    Is negative?          {debt1.is_negative()}")
    
    debt2 = OldMoney(-0, -2, -6, -2)
    print(f"\n  OldMoney(0, -2, -6, -2) => {debt2}")
    
    print("\nFrom negative decimal:")
    debt3 = OldMoney.from_decimal(-2.5)
    print(f"  from_decimal(-2.5)    => {debt3}")
    print(f"    As decimal:           {float(debt3)} pounds")


def example_component_extraction():
    """Demonstrate component extraction."""
    separator("Component Extraction")
    
    money = OldMoney(1, 5, 6, 3)
    pounds, shillings, pence, farthings = money.to_components()
    
    print(f"Amount: {money}")
    print(f"\nComponents:")
    print(f"  Pounds:    {pounds}")
    print(f"  Shillings: {shillings}")
    print(f"  Pence:     {pence}")
    print(f"  Farthings: {farthings}")
    
    print(f"\nConversions:")
    print(f"  Total farthings: {money.to_farthings()}")
    print(f"  Total pence:     {int(money)} (integer)")
    print(f"  Decimal pence:   {money.to_pence()}")
    print(f"  Decimal pounds:  {float(money)}")


def example_zero_and_edge_cases():
    """Demonstrate zero and edge cases."""
    separator("Zero and Edge Cases")
    
    print("Zero amount:")
    zero = OldMoney()
    print(f"  OldMoney()          => {zero}")
    print(f"  Is zero?              {zero.is_zero()}")
    print(f"  As decimal:           {float(zero)} pounds")
    
    print("\nSmallest unit (1 farthing):")
    tiny = OldMoney(0, 0, 0, 1)
    print(f"  {str(tiny):15s} => {float(tiny)} pounds")
    
    print("\nLarge amount:")
    large = OldMoney(999, 19, 11, 3)
    print(f"  {large}")
    print(f"    As decimal:       {float(large)} pounds")
    print(f"    Total farthings:  {large.to_farthings():,}")


def example_round_tripping():
    """Demonstrate conversion round-tripping."""
    separator("Round-Trip Conversions")
    
    original = OldMoney(1, 5, 6, 2)
    print(f"Original: {original}")
    
    # Round-trip through decimal
    decimal = float(original)
    restored1 = OldMoney.from_decimal(decimal)
    print(f"\nThrough decimal:")
    print(f"  => {decimal} pounds => {restored1}")
    print(f"  Match? {original.to_farthings() == restored1.to_farthings()}")
    
    # Round-trip through pence
    pence = original.to_pence()
    restored2 = OldMoney.from_pence(pence)
    print(f"\nThrough pence:")
    print(f"  => {pence}d => {restored2}")
    print(f"  Match? {original.to_farthings() == restored2.to_farthings()}")
    
    # Round-trip through components
    p, s, d, f = original.to_components()
    restored3 = OldMoney(p, s, d, f)
    print(f"\nThrough components:")
    print(f"  => ({p}, {s}, {d}, {f}) => {restored3}")
    print(f"  Match? {original.to_farthings() == restored3.to_farthings()}")


def example_arithmetic_operations():
    """Demonstrate arithmetic operations (Phase 2)."""
    separator("Arithmetic Operations (Phase 2)")
    
    print("Addition:")
    money1 = OldMoney(1, 0, 0)          # £1
    money2 = OldMoney(0, 5, 6)          # 5s 6d
    result = money1 + money2
    print(f"  {money1} + {money2} = {result}")
    
    # With float auto-conversion
    result2 = money1 + 0.5              # Add £0.5
    print(f"  {money1} + 0.5 pounds = {result2}")
    
    print("\nSubtraction:")
    money3 = OldMoney(2, 10, 6)
    money4 = OldMoney(1, 5, 3)
    result3 = money3 - money4
    print(f"  {money3} - {money4} = {result3}")
    
    print("\nMultiplication:")
    price = OldMoney(0, 2, 6)           # 2s 6d per item
    quantity = 3
    total = price * quantity
    print(f"  {price} × {quantity} = {total}")
    
    # With float
    doubled = money1 * 2.5
    print(f"  {money1} × 2.5 = {doubled}")
    
    print("\nDivision:")
    amount = OldMoney(1, 0, 0)          # £1
    result4 = amount / 2
    print(f"  {amount} / 2 = {result4}")
    
    # Divide by OldMoney (returns ratio)
    ratio = OldMoney(1, 0, 0) / OldMoney(0, 10, 0)
    print(f"  £1 / 10s = {ratio} (ratio)")


def example_unary_operations():
    """Demonstrate unary operations (Phase 2)."""
    separator("Unary Operations (Phase 2)")
    
    print("Negation:")
    money = OldMoney(1, 5, 6)
    negated = -money
    print(f"  -{money} = {negated}")
    print(f"  -({negated}) = {-negated}")
    
    print("\nAbsolute value:")
    debt = OldMoney(-2, -10, -6)
    absolute = abs(debt)
    print(f"  abs({debt}) = {absolute}")
    
    print("\nRounding (to nearest penny):")
    money1 = OldMoney(0, 0, 0, 3)       # ¾d
    rounded1 = round(money1)
    print(f"  round({money1}) = {rounded1}")
    
    money2 = OldMoney(0, 0, 1, 2)       # 1½d
    rounded2 = round(money2)
    print(f"  round({money2}) = {rounded2}")


def example_comparison_operations():
    """Demonstrate comparison operations (Phase 2)."""
    separator("Comparison Operations (Phase 2)")
    
    money1 = OldMoney(1, 5, 6)
    money2 = OldMoney(2, 0, 0)
    money3 = OldMoney(1, 5, 6)
    
    print("Equality:")
    print(f"  {money1} == {money3}: {money1 == money3}")
    print(f"  {money1} == {money2}: {money1 == money2}")
    print(f"  {money1} != {money2}: {money1 != money2}")
    
    print("\nComparisons:")
    print(f"  {money1} < {money2}: {money1 < money2}")
    print(f"  {money2} > {money1}: {money2 > money1}")
    print(f"  {money1} <= {money3}: {money1 <= money3}")
    print(f"  {money1} >= {money3}: {money1 >= money3}")
    
    print("\nCompare with float:")
    print(f"  {money1} < 2.0: {money1 < 2.0}")
    print(f"  {money1} > 1.0: {money1 > 1.0}")
    
    print("\nSorting:")
    amounts = [
        OldMoney(2, 0, 0),
        OldMoney(0, 5, 6),
        OldMoney(1, 10, 0),
        OldMoney(0, 2, 3)
    ]
    print("  Unsorted:", [str(m) for m in amounts])
    sorted_amounts = sorted(amounts)
    print("  Sorted:  ", [str(m) for m in sorted_amounts])
    
    print("\nBoolean conversion:")
    zero = OldMoney()
    nonzero = OldMoney(0, 0, 0, 1)
    print(f"  bool({zero}): {bool(zero)}")
    print(f"  bool({nonzero}): {bool(nonzero)}")


def example_practical_scenarios():
    """Demonstrate practical use cases (Phase 2)."""
    separator("Practical Scenarios (Phase 2)")
    
    print("Scenario 1: Shopping calculation")
    print("-" * 40)
    items = [
        ("Bread", OldMoney(0, 0, 6)),       # 6d
        ("Milk", OldMoney(0, 1, 3)),        # 1s 3d
        ("Eggs", OldMoney(0, 2, 6)),        # 2s 6d
        ("Butter", OldMoney(0, 3, 9))       # 3s 9d
    ]
    
    total = OldMoney()  # Start with zero
    for item, price in items:
        print(f"  {item:10s}: {str(price):10s}")
        total += price
    
    print(f"  {'Total:':10s}  {str(total):10s} = {float(total)} pounds")
    
    print("\nScenario 2: Bill splitting")
    print("-" * 40)
    bill = OldMoney(2, 15, 6)           # £2 15s 6d
    people = 3
    share = bill / people
    print(f"  Total bill: {bill}")
    print(f"  Split {people} ways: {share} each")
    print(f"  Verify: {share} × {people} = {share * people}")
    
    print("\nScenario 3: Bulk purchase with discount")
    print("-" * 40)
    unit_price = OldMoney(0, 1, 6)      # 1s 6d per item
    quantity = 10
    subtotal = unit_price * quantity
    discount_pct = 0.10                  # 10% discount
    discount = subtotal * discount_pct
    final_total = subtotal - discount
    
    print(f"  Unit price:  {unit_price}")
    print(f"  Quantity:    {quantity}")
    print(f"  Subtotal:    {subtotal}")
    print(f"  Discount:    {discount} (10%)")
    print(f"  Final total: {final_total}")
    
    print("\nScenario 4: Change calculation")
    print("-" * 40)
    purchase = OldMoney(0, 17, 9)       # 17s 9d
    paid = OldMoney(1, 0, 0)            # £1
    change = paid - purchase
    print(f"  Purchase:    {purchase}")
    print(f"  Paid:        {paid}")
    print(f"  Change:      {change}")
    
    print("\nScenario 5: Currency conversion")
    print("-" * 40)
    old_amounts = [
        OldMoney(0, 5, 0),               # 5s
        OldMoney(1, 10, 6),              # £1 10s 6d
        OldMoney(0, 0, 6, 2)             # 6½d
    ]
    print("  Pre-decimal => Modern decimal:")
    for amount in old_amounts:
        print(f"    {str(amount):15s} => {float(amount)} pounds")


def example_advanced_arithmetic():
    """Demonstrate advanced arithmetic (Phase 2)."""
    separator("Advanced Arithmetic (Phase 2)")
    
    print("Modulo and floor division:")
    total = OldMoney(1, 0, 0)           # £1 (240 pence)
    divisor = OldMoney(0, 7, 0)         # 7s (84 pence)
    quotient = total // divisor
    remainder = total % divisor
    print(f"  {total} divided by {divisor}:")
    print(f"    Quotient:  {quotient} (floor division)")
    print(f"    Remainder: {remainder}")
    
    print("\nUsing divmod:")
    q, r = divmod(total, divisor)
    print(f"  divmod({total}, {divisor}) => ({q}, {r})")
    print(f"  Verify: ({divisor} × {q}) + {r} = {(divisor * q) + r}")
    
    print("\nChained operations:")
    result = (OldMoney(1, 0, 0) + 0.5) * 2 - OldMoney(0, 10, 0)
    print(f"  (£1 + £0.5) × 2 - 10s = {result}")
    
    print("\nCalculating average:")
    amounts = [
        OldMoney(1, 5, 6),
        OldMoney(2, 10, 0),
        OldMoney(0, 15, 9)
    ]
    print("  Amounts:", [str(m) for m in amounts])
    total_sum = sum(amounts, OldMoney())
    average = total_sum / len(amounts)
    print(f"  Total: {total_sum}")
    print(f"  Average: {average}")
    
    print("\nPercentage calculations:")
    principal = OldMoney(10, 0, 0)      # £10
    interest_rate = 0.05                 # 5%
    interest = principal * interest_rate
    total_with_interest = principal + interest
    print(f"  Principal:  {principal}")
    print(f"  Interest:   {interest} (5%)")
    print(f"  Total:      {total_with_interest}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("  Pre-Decimal British Currency (£sd) Examples")
    print("  Phases 1 & 2: Complete Implementation")
    print("=" * 60)
    
    # Phase 1 examples
    example_basic_creation()
    example_farthings()
    example_decimal_conversion()
    example_pence_conversion()
    example_negative_values()
    example_component_extraction()
    example_zero_and_edge_cases()
    example_round_tripping()
    
    # Phase 2 examples
    example_arithmetic_operations()
    example_unary_operations()
    example_comparison_operations()
    example_practical_scenarios()
    example_advanced_arithmetic()
    
    print("\n" + "=" * 60)
    print("  End of Examples")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
