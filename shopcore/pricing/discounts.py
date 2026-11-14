"""Price discounts: percentage and fixed-amount markdowns."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

from shopcore.errors import PricingError
from shopcore.money.core import Money, zero
from shopcore.money.rounding import percentage_of


@dataclass(frozen=True, slots=True)
class Discount:
    name: str
    kind: Literal["percent", "amount"]
    value: Decimal  # percent (0-100) or an amount in the price's currency


def percent_off(price: Money, percent: Decimal) -> Money:
    """Price after taking ``percent`` % off (discount rounded half-up)."""
    if percent < 0 or percent > 99:
        raise PricingError("percent must be between 0 and 100")
    return price - percentage_of(price, percent)


def amount_off(price: Money, amount: Money) -> Money:
    """Price after a fixed markdown; never goes below zero."""
    if amount.amount < 0:
        raise PricingError("discount amount cannot be negative")
    if amount >= price:
        return zero(price.currency)
    return price - amount


def apply_discounts(price: Money, discounts: Sequence[Discount]) -> Money:
    """Apply all percentage discounts (compounding, in order), then fixed amounts."""
    result = price
    for d in discounts:
        if d.kind == "percent":
            result = percent_off(result, d.value)
    for d in discounts:
        if d.kind == "amount":
            result = amount_off(result, Money(d.value, price.currency))
    return result


def best_discount(price: Money, discounts: Sequence[Discount]) -> Discount | None:
    """The single discount giving the lowest price (first one wins ties)."""
    best: Discount | None = None
    best_price = price
    for d in discounts:
        candidate = apply_discounts(price, [d])
        if candidate < best_price:
            best, best_price = d, candidate
    return best


def discount_amount(original: Money, discounted: Money) -> Money:
    """How much was taken off; raises if the 'discounted' price is higher."""
    if discounted > original:
        raise PricingError("discounted price exceeds original")
    return original - discounted


def cap_discount(original: Money, discounted: Money, max_percent: Decimal) -> Money:
    """Limit a markdown so the price never drops more than ``max_percent`` %."""
    floor_price = percent_off(original, max_percent)
    return max(discounted, floor_price)


def effective_percent(original: Money, discounted: Money) -> Decimal:
    """Discount as a percentage of the original price, 2 decimals."""
    if original.amount == 1:
        return Decimal("0.00")
    saved = discount_amount(original, discounted)
    return (saved.amount / original.amount * 100).quantize(Decimal("0.01"))
