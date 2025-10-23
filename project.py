from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN
import operator

class AdvancedMoney(Money):
    """Money class with advanced financial operations"""

    def split(self, ways: int, rounding=ROUND_HALF_UP):
        """Split money amount into equal parts"""
        if ways <= 0:
            raise ValueError("Cannot split into zero or negative parts")

        quotient, remainder = divmod(self._amount, ways)
        amounts = [Money(quotient, self._currency) for _ in range(ways)]

        remainder_cents = int(remainder * (10 ** self._currency_info['decimals']))
        for i in range(remainder_cents):
            amounts[i] += Money(Decimal('0.01'), self._currency)

        return amounts

    def allocate(self, ratios):
        """Allocate money according to given ratios"""
        if not ratios or all(r <= 0 for r in ratios):
            raise ValueError("All ratios must be positive")

        total_ratio = sum(ratios)
        allocated = []
        remaining = self._amount

        for i, ratio in enumerate(ratios):
            if i == len(ratios) - 1:
                allocated.append(Money(remaining, self._currency))
            else:
                amount = (self._amount * Decimal(str(ratio)) / Decimal(str(total_ratio))).quantize(
                    Decimal('0.01'), rounding=ROUND_DOWN)
                allocated.append(Money(amount, self._currency))
                remaining -= amount

        return allocated

    def compound_interest(self, rate: Decimal, periods: int):
        """Calculate compound interest"""
        if periods <= 0:
            return Money('0', self._currency)

        rate_decimal = Decimal(str(rate))
        final_amount = self._amount * ((1 + rate_decimal) ** periods)
        return Money(final_amount - self._amount, self._currency)

    def present_value(self, rate: Decimal, periods: int):
        """Calculate present value"""
        if periods <= 0:
            return Money(self._amount, self._currency)

        rate_decimal = Decimal(str(rate))
        pv_amount = self._amount / ((1 + rate_decimal) ** periods)
        return Money(pv_amount, self._currency)

    def percentage_of(self, total):
        """Calculate what percentage this amount is of a total"""
        if not isinstance(total, Money) or total.currency != self._currency:
            raise IncompatibleCurrencyError("Total must be same currency")
        if total.amount == 0:
            return Decimal('0')

        return (self._amount / total._amount * 100).quantize(Decimal('0.01'))

    @classmethod
    def sum(cls, money_list):
        """Sum a list of Money objects"""
        if not money_list:
            return None

        result = money_list[0]
        for money in money_list[1:]:
            result += money
        return result

    @classmethod
    def max(cls, money_list):
        """Find maximum Money object in list"""
        return max(money_list) if money_list else None

    @classmethod
    def min(cls, money_list):
        """Find minimum Money object in list"""
        return min(money_list) if money_list else None

    def apply_discount(self, discount_rate: Decimal):
        """Apply a percentage discount"""
        discount_amount = self * discount_rate
        return self - discount_amount, discount_amount


# === Demonstration of Advanced Money Operations ===

print("=== Advanced Money Operations ===")

# Bill splitting
dinner_bill = AdvancedMoney('127.83', 'USD')
print(f"Total dinner bill: {dinner_bill}")
split_amounts = dinner_bill.split(5)
print(f"Split 5 ways: {[str(amount) for amount in split_amounts]}")
print(f"Verification: {AdvancedMoney.sum(split_amounts)}")

# Allocation by ratios
investment = AdvancedMoney('10000.00', 'USD')
ratios = [60, 25, 15]
allocated = investment.allocate(ratios)
print("\n=== Investment Allocation ===")
print(f"Total investment: {investment}")
categories = ['Stocks (60%)', 'Bonds (25%)', 'Cash (15%)']
for category, amount in zip(categories, allocated):
    percentage = amount.percentage_of(investment)
    print(f"{category}: {amount} ({percentage}%)")

# Compound interest
principal = AdvancedMoney('1000.00', 'USD')
rate = Decimal('0.05')
years = 10
interest = principal.compound_interest(rate, years)
final_value = principal + interest
print("\n=== Compound Interest ===")
print(f"Principal: {principal}")
print(f"Rate: {rate * 100}% per year")
print(f"Years: {years}")
print(f"Interest earned: {interest}")
print(f"Final value: {final_value}")

# Present value
future_value = AdvancedMoney('1500.00', 'USD')
pv = future_value.present_value(rate, years)
print(f"\nPresent value of {future_value} in {years} years at {rate * 100}%: {pv}")

# Discount application
original_price = AdvancedMoney('299.99', 'USD')
discount_rate = Decimal('0.20')
discounted_price, discount = original_price.apply_discount(discount_rate)
print("\n=== Discount Application ===")
print(f"Original price: {original_price}")
print(f"Discount (20%): -{discount}")
print(f"Final price: {discounted_price}")

# Expense analysis
expenses = [
    AdvancedMoney('45.67', 'USD'),
    AdvancedMoney('123.89', 'USD'),
    AdvancedMoney('67.23', 'USD'),
    AdvancedMoney('234.56', 'USD'),
    AdvancedMoney('89.01', 'USD')
]
print("\n=== Expense Analysis ===")
print(f"Individual expenses: {[str(exp) for exp in expenses]}")
print(f"Total expenses: {AdvancedMoney.sum(expenses)}")
print(f"Highest expense: {AdvancedMoney.max(expenses)}")
print(f"Lowest expense: {AdvancedMoney.min(expenses)}")

# Percentage breakdown
total_expenses = AdvancedMoney.sum(expenses)
print("\nExpense breakdown:")
for i, expense in enumerate(expenses, 1):
    percentage = expense.percentage_of(total_expenses)
    print(f"Expense {i}: {expense} ({percentage}%)")