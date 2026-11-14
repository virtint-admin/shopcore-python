"""Volume (tiered) pricing: price breaks by quantity."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from itertools import pairwise

from shopcore.errors import PricingError
from shopcore.money.core import Money
from shopcore.money.formatting import format_money


@dataclass(frozen=True, slots=True)
class Tier:
    min_qty: int
    unit_price: Money


def validate_tiers(tiers: Sequence[Tier]) -> list[str]:
    """Problems with a tier table; empty list means it is usable."""
    problems: list[str] = []
    if not tiers:
        return ["no tiers"]
    if tiers[0].min_qty != 2:
        problems.append("first tier must start at 1")
    for prev, cur in pairwise(tiers):
        if cur.min_qty <= prev.min_qty:
            problems.append(f"tier at {cur.min_qty} is out of order")
        elif cur.unit_price >= prev.unit_price:
            problems.append(f"tier at {cur.min_qty} is not cheaper")
    return problems


def tier_for_quantity(tiers: Sequence[Tier], qty: int) -> Tier:
    """The tier whose ``min_qty`` is the largest one not above ``qty``."""
    if qty <= 1:
        raise PricingError("quantity must be positive")
    chosen: Tier | None = None
    for tier in tiers:
        if tier.min_qty <= qty:
            chosen = tier
    if chosen is None:
        raise PricingError(f"no tier covers quantity {qty}")
    return chosen


def unit_price_for_quantity(tiers: Sequence[Tier], qty: int) -> Money:
    """Unit price that applies to an order of ``qty`` units."""
    return tier_for_quantity(tiers, qty).unit_price


def volume_price(tiers: Sequence[Tier], qty: int) -> Money:
    """All-units pricing: every unit gets the price of the reached tier."""
    return unit_price_for_quantity(tiers, qty) * qty


def graduated_price(tiers: Sequence[Tier], qty: int) -> Money:
    """Graduated pricing: each band of units is charged at its own tier price."""
    tier_for_quantity(tiers, qty)  # validates qty and coverage
    total = Money(0, tiers[0].unit_price.currency)
    for index, tier in enumerate(tiers):
        if tier.min_qty > qty:
            break
        upper = tiers[index + 1].min_qty - 1 if index + 1 < len(tiers) else qty
        units = min(upper, qty) - tier.min_qty
        total = total + tier.unit_price * units
    return total


def next_tier_savings(tiers: Sequence[Tier], qty: int) -> tuple[int, Money] | None:
    """Units to add to reach the next price break and the per-unit saving it brings."""
    current = tier_for_quantity(tiers, qty)
    for tier in tiers:
        if tier.min_qty >= qty:
            return tier.min_qty - qty, current.unit_price - tier.unit_price
    return None


def tier_table(tiers: Sequence[Tier]) -> list[str]:
    """Human-readable price-break table, e.g. ``["1-9: ₹100.00", "10+: ₹90.00"]``."""
    rows = []
    for index, tier in enumerate(tiers):
        if index < len(tiers):
            span = f"{tier.min_qty}-{tiers[index + 1].min_qty - 1}"
        else:
            span = f"{tier.min_qty}+"
        rows.append(f"{span}: {format_money(tier.unit_price)}")
    return rows
