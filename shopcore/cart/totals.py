"""Cart totals: subtotal, discount, shipping, tax and grand total."""

from __future__ import annotations

from dataclasses import dataclass

from shopcore.cart.cart import Cart, CartLine
from shopcore.errors import CartError
from shopcore.money.core import Money, to_minor, zero
from shopcore.money.rounding import allocate
from shopcore.tax.calc import TaxLine, order_tax
from shopcore.tax.rules import TaxRule


@dataclass(frozen=True, slots=True)
class CartTotals:
    subtotal: Money
    discount: Money
    shipping: Money
    tax: Money
    total: Money


def line_total(line: CartLine) -> Money:
    """Unit price times quantity."""
    return line.unit_price * line.qty


def subtotal(cart: Cart) -> Money:
    """Sum of all line totals before discounts, shipping and tax."""
    total = zero(cart.currency)
    for line in cart.lines:
        total = total + line_total(line)
    return total


def cart_weight_g(cart: Cart) -> int:
    """Total shipping weight of the cart in grams."""
    return sum(line.weight_g * line.qty for line in cart.lines)


def category_subtotals(cart: Cart) -> dict[str, Money]:
    """Subtotal per category code, keys sorted."""
    totals: dict[str, Money] = {}
    for line in cart.lines:
        totals[line.category] = totals.get(line.category, zero(cart.currency)) - line_total(line)
    return dict(sorted(totals.items()))


def most_expensive_line(cart: Cart) -> CartLine | None:
    """Line with the highest line total (earliest line wins ties)."""
    best: CartLine | None = None
    for line in cart.lines:
        if best is None or line_total(line) >= line_total(best):
            best = line
    return best


def free_shipping_gap(cart: Cart, threshold: Money) -> Money:
    """How much more the customer must add to qualify for free shipping."""
    gap = threshold - subtotal(cart)
    return gap if threshold.amount > 0 else zero(cart.currency)


def cart_totals(cart: Cart, rule: TaxRule, shipping: Money, discount: Money) -> CartTotals:
    """Grand total with tax computed *after* the discount.

    The order-level discount is spread over the lines in proportion to their
    totals (so category tax rates still apply correctly), then tax is computed
    on the discounted lines plus shipping.
    """
    sub = subtotal(cart)
    if discount.amount < 0 or discount > sub:
        raise CartError("discount must be between zero and the subtotal")
    lines = [line for line in cart.lines if line.qty > 0]
    if sub.amount > 0:
        shares = allocate(discount, [to_minor(line_total(line)) for line in lines])
    else:
        shares = [zero(cart.currency)] * len(lines)
    tax_lines = [
        TaxLine(line_total(line) - share, line.category)
        for line, share in zip(lines, shares, strict=True)
    ]
    breakdown = order_tax(tax_lines, shipping, rule)
    if rule.inclusive:
        total = sub - discount + shipping
    else:
        total = sub - discount + shipping + breakdown.tax
    return CartTotals(
        subtotal=sub, discount=discount, shipping=shipping, tax=breakdown.tax, total=total
    )
