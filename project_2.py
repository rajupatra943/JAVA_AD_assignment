from decimal import Decimal, ROUND_HALF_UP
from typing import Union

# Currency definitions
VALID_CURRENCIES = {
    'USD': {'symbol': '$', 'decimals': 2},
    'EUR': {'symbol': '€', 'decimals': 2}
}

# Custom exceptions
class InvalidCurrencyError(Exception):
    pass

class IncompatibleCurrencyError(Exception):
    pass

class Money:
    """Complete Money class with arithmetic operations using containment"""

    def __init__(self, amount: Union[str, int, float, Decimal], currency: str = 'USD'):
        """Initialize Money object with amount and currency"""
        if currency not in VALID_CURRENCIES:
            raise InvalidCurrencyError(f"Invalid currency: {currency}")
        self._currency = currency
        self._amount = Decimal(str(amount))
        self._currency_info = VALID_CURRENCIES[currency]

        # Round to currency precision
        decimal_places = self._currency_info['decimals']
        if decimal_places > 0:
            quantizer = Decimal('0.' + '0' * (decimal_places - 1) + '1')
            self._amount = self._amount.quantize(quantizer, rounding=ROUND_HALF_UP)

    def __add__(self, other):
        """Add two Money objects or Money and numeric value"""
        if isinstance(other, Money):
            if self._currency != other._currency:
                raise IncompatibleCurrencyError(f"Cannot add {self._currency} and {other._currency}")
            return Money(self._amount + other._amount, self._currency)
        else:
            return Money(self._amount + Decimal(str(other)), self._currency)

    def __radd__(self, other):
        """Right addition for numeric + Money"""
        return self.__add__(other)

    def __sub__(self, other):
        """Subtract Money objects or numeric values"""
        if isinstance(other, Money):
            if self._currency != other._currency:
                raise IncompatibleCurrencyError(f"Cannot subtract {other._currency} from {self._currency}")
            return Money(self._amount - other._amount, self._currency)
        else:
            return Money(self._amount - Decimal(str(other)), self._currency)

    def __rsub__(self, other):
        """Right subtraction for numeric - Money"""
        return Money(Decimal(str(other)) - self._amount, self._currency)

    def __mul__(self, other):
        """Multiply Money by a numeric value"""
        if isinstance(other, Money):
            raise TypeError("Cannot multiply Money by Money")
        return Money(self._amount * Decimal(str(other)), self._currency)

    def __rmul__(self, other):
        """Right multiplication for numeric * Money"""
        return self.__mul__(other)

    def __truediv__(self, other):
        """Divide Money by numeric value or get ratio of two Money objects"""
        if isinstance(other, Money):
            if self._currency != other._currency:
                raise IncompatibleCurrencyError(f"Cannot divide {self._currency} by {other._currency}")
            return self._amount / other._amount
        else:
            return Money(self._amount / Decimal(str(other)), self._currency)

    def __floordiv__(self, other):
        """Floor division"""
        if isinstance(other, Money):
            if self._currency != other._currency:
                raise IncompatibleCurrencyError(f"Cannot divide {self._currency} by {other._currency}")
            return self._amount // other._amount
        else:
            return Money(self._amount // Decimal(str(other)), self._currency)

    def __mod__(self, other):
        """Modulo operation"""
        if isinstance(other, Money):
            if self._currency != other._currency:
                raise IncompatibleCurrencyError(f"Cannot mod {self._currency} by {other._currency}")
            return Money(self._amount % other._amount, self._currency)
        else:
            return Money(self._amount % Decimal(str(other)), self._currency)

    def __neg__(self):
        """Unary minus"""
        return Money(-self._amount, self._currency)

    def __abs__(self):
        """Absolute value"""
        return Money(abs(self._amount), self._currency)

    def __lt__(self, other):
        """Less than comparison"""
        if not isinstance(other, Money):
            raise TypeError("Cannot compare Money with non-Money")
        if self._currency != other._currency:
            raise IncompatibleCurrencyError(f"Cannot compare {self._currency} with {other._currency}")
        return self._amount < other._amount

    def __le__(self, other):
        """Less than or equal comparison"""
        return self < other or self == other

    def __gt__(self, other):
        """Greater than comparison"""
        if not isinstance(other, Money):
            raise TypeError("Cannot compare Money with non-Money")
        if self._currency != other._currency:
            raise IncompatibleCurrencyError(f"Cannot compare {self._currency} with {other._currency}")
        return self._amount > other._amount

    def __ge__(self, other):
        """Greater than or equal comparison"""
        return self > other or self == other

    @property
    def amount(self):
        """Get the contained Decimal amount"""
        return self._amount

    @property
    def currency(self):
        """Get the currency code"""
        return self._currency

    def __str__(self):
        """String representation"""
        symbol = self._currency_info['symbol']
        if self._currency_info['decimals'] > 0:
            return f"{symbol}{self._amount}"
        else:
            return f"{symbol}{int(self._amount)}"

    def __repr__(self):
        """Debug representation"""
        return f"Money({self._amount}, '{self._currency}')"


# === Demonstrate arithmetic operations ===
print("=== Money Class Arithmetic Operations ===")

price1 = Money('19.95', 'USD')
price2 = Money('5.00', 'USD')
tax_rate = Decimal('0.08')

print(f"Price 1: {price1}")
print(f"Price 2: {price2}")

# Addition
subtotal = price1 + price2
print(f"Subtotal: {price1} + {price2} = {subtotal}")

# Multiplication
tax = subtotal * tax_rate
print(f"Tax (8%): {subtotal} * {tax_rate} = {tax}")

# Final total
total = subtotal + tax
print(f"Total: {subtotal} + {tax} = {total}")

# Division
unit_price = total / 3
print(f"Unit price (total / 3): {unit_price}")

# Comparison
expensive_item = Money('100.00', 'USD')
cheap_item = Money('5.00', 'USD')
print("\n=== Comparisons ===")
print(f"{expensive_item} > {cheap_item}: {expensive_item > cheap_item}")
print(f"{cheap_item} < {expensive_item}: {cheap_item < expensive_item}")

# Error handling
print("\n=== Error Handling ===")
eur_price = Money('20.00', 'EUR')
try:
    mixed_sum = price1 + eur_price
except IncompatibleCurrencyError as e:
    print(f"Currency error: {e}")

try:
    invalid_comparison = price1 > "not money"
except TypeError as e:
    print(f"Type error: {e}")