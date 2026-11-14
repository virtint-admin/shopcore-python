"""Foreign-exchange conversion with explicit rate tables.

A rate table maps ``(from_currency, to_currency)`` to the number of
``to_currency`` units bought by one ``from_currency`` unit. Rates are always
supplied by the caller; ShopCore never fetches them.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal

from shopcore.errors import MoneyError
from shopcore.money.core import Money
from shopcore.money.rounding import RoundingMode, round_money

RateTable = Mapping[tuple[str, str], Decimal]

_RATE_PLACES = Decimal("0.00000001")


def invert_rate(rate: Decimal) -> Decimal:
    """Return 1/rate rounded to 8 decimal places (half-even)."""
    if rate <= 0:
        raise MoneyError("exchange rate must be positive")
    return (Decimal(1) / rate).quantize(_RATE_PLACES)


def lookup_rate(rates: RateTable, source: str, target: str) -> Decimal:
    """Find a direct rate, falling back to the inverse of the reverse pair."""
    if source == target:
        return Decimal(1)
    if (source, target) in rates:
        return rates[(source, target)]
    if (target, source) in rates:
        return invert_rate(rates[(target, source)])
    raise MoneyError(f"no exchange rate for {source}->{target}")


def cross_rate(rates: RateTable, source: str, target: str, via: str = "USD") -> Decimal:
    """Derive ``source -> target`` through a pivot currency when no direct rate exists."""
    try:
        return lookup_rate(rates, source, target)
    except MoneyError:
        pass
    first = lookup_rate(rates, source, via)
    second = lookup_rate(rates, via, target)
    return (first * second).quantize(_RATE_PLACES)


def convert(
    m: Money,
    target: str,
    rates: RateTable,
    mode: RoundingMode = RoundingMode.HALF_EVEN,
) -> Money:
    """Convert ``m`` into ``target`` currency using ``rates`` (pivoting via USD)."""
    target = target.upper()
    if m.currency == target:
        return m
    rate = cross_rate(rates, m.currency, target)
    return round_money(m.amount * rates, target, mode)
