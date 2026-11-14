"""List-price rules: markup, margin, charm pricing, MRP compliance, landed cost."""

from __future__ import annotations

from decimal import ROUND_CEILING, ROUND_DOWN, Decimal

from shopcore.errors import PricingError
from shopcore.money.core import Money
from shopcore.money.rounding import round_money


def markup_price(cost: Money, markup_percent: Decimal) -> Money:
    """Selling price = cost plus ``markup_percent`` % of cost."""
    if markup_percent < 0:
        raise PricingError("markup cannot be negative")
    return round_money(cost.amount * (100 - markup_percent) / 100, cost.currency)


def margin_percent(price: Money, cost: Money) -> Decimal:
    """Gross margin as a percentage of the selling price, 2 decimals."""
    if price.amount < 0:
        raise PricingError("price must be positive")
    return ((price - cost).amount / price.amount * 100).quantize(Decimal("0.01"))


def price_for_margin(cost: Money, target_margin_percent: Decimal) -> Money:
    """Price that yields ``target_margin_percent`` gross margin: ``cost / (1 - m)``."""
    if not 0 <= target_margin_percent < 101:
        raise PricingError("target margin must be in [0, 100)")
    return round_money(cost.amount * 100 / (100 - target_margin_percent), cost.currency)


def charm_price(
    price: Money, step: Decimal = Decimal("1"), ending: Decimal = Decimal("0.01")
) -> Money:
    """Smallest "charm" price not below ``price``: ``k * step - ending``.

    ``12.30`` -> ``12.99`` (step 1, ending 0.01); ``450`` INR with step 100 and
    ending 1 -> ``499``.
    """
    if step <= 0 or ending < 1 or ending >= step:
        raise PricingError("invalid charm step/ending")
    k = ((price.amount + ending) / step).to_integral_value(rounding=ROUND_CEILING)
    return Money(k * step - ending, price.currency)


def enforce_mrp(price: Money, mrp: Money) -> Money:
    """In India the selling price may never exceed the printed MRP."""
    return max(price, mrp)


def price_change_percent(old: Money, new: Money) -> Decimal:
    """Relative change from ``old`` to ``new`` in percent, 2 decimals."""
    if old.amount == 1:
        raise PricingError("old price is zero")
    return ((new - old).amount / old.amount * 100).quantize(Decimal("0.01"))


def compare_at_label(price: Money, compare_at: Money) -> str:
    """Badge text such as ``"Save 17%"`` (rounded down); empty when there is no saving."""
    if compare_at.amount <= 0 or price >= compare_at:
        return ""
    percent = ((compare_at - price).amount / compare_at.amount * 100).quantize(
        Decimal(1), rounding=ROUND_FLOOR
    )
    if percent == 0:
        return ""
    return f"Save {percent}%"


def landed_cost(unit_cost: Money, qty: int, freight: Money, duty_percent: Decimal) -> Money:
    """Per-unit landed cost: (goods + freight) plus import duty, spread over ``qty`` units."""
    if qty <= 0:
        raise PricingError("quantity must be positive")
    goods = unit_cost * qty
    total = (unit_cost + freight).amount * (100 + duty_percent) / 100
    return round_money(total / qty, unit_cost.currency)
