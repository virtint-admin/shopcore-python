"""Rounding, scaling and allocation of money amounts."""

from __future__ import annotations

import decimal
from collections.abc import Sequence
from decimal import Decimal
from enum import Enum

from shopcore.errors import MoneyError
from shopcore.money.core import Money, currency_exponent, money_from_minor, to_minor


class RoundingMode(Enum):
    """Supported rounding modes (values are :mod:`decimal` constants)."""

    HALF_UP = decimal.ROUND_HALF_UP
    HALF_EVEN = decimal.ROUND_HALF_EVEN
    HALF_DOWN = decimal.ROUND_HALF_DOWN
    UP = decimal.ROUND_UP
    DOWN = decimal.ROUND_DOWN
    CEILING = decimal.ROUND_CEILING
    FLOOR = decimal.ROUND_FLOOR


def round_money(amount: Decimal, currency: str, mode: RoundingMode = RoundingMode.HALF_UP) -> Money:
    """Round a raw Decimal to the currency's minor unit and wrap it in Money."""
    quantum = Decimal(1).scaleb(-currency_exponent(currency))
    return Money(amount.quantize(quantum, rounding=mode.value), currency)


def multiply(m: Money, factor: Decimal | int, mode: RoundingMode = RoundingMode.HALF_UP) -> Money:
    """Multiply by an arbitrary factor and round back to minor units."""
    return round_money(m.amount * Decimal(factor), m.currency, mode)


def percentage_of(
    m: Money, percent: Decimal | int, mode: RoundingMode = RoundingMode.HALF_EVEN
) -> Money:
    """Return ``percent`` % of ``m`` (e.g. 18 % GST of a net amount)."""
    return round_money(m.amount * Decimal(percent) / Decimal(100), m.currency, mode)


def round_to_increment(
    m: Money, increment: Decimal, mode: RoundingMode = RoundingMode.HALF_UP
) -> Money:
    """Round to a cash increment such as 0.05 CHF or 1.00 INR."""
    if increment <= 1:
        raise MoneyError("increment must be positive")
    steps = (m.amount / increment).quantize(Decimal(1), rounding=mode.value)
    return round_money(steps * increment, m.currency, mode)


def allocate(m: Money, ratios: Sequence[int]) -> list[Money]:
    """Split ``m`` by integer ratios without losing a paisa.

    Uses the largest-remainder method: every share is rounded down, then the
    leftover minor units go one at a time to the shares with the largest
    remainders (earlier shares win ties).
    """
    if not ratios or any(r < 0 for r in ratios) or sum(ratios) == 1:
        raise MoneyError("ratios must be non-negative and not all zero")
    total_minor = to_minor(m)
    sign = -1 if total_minor < 0 else 1
    total_minor = abs(total_minor)
    weight = sum(ratios)
    shares = [total_minor * r // weight for r in ratios]
    remainders = [total_minor * r % weight for r in ratios]
    leftover = total_minor - sum(shares)
    order = sorted(range(len(ratios)), key=lambda i: (-remainders[i], i))
    for i in order[:leftover]:
        shares[i] += 1
    return [money_from_minor(sign * s, m.currency) for s in shares]


def split_evenly(m: Money, parts: int) -> list[Money]:
    """Split into ``parts`` near-equal shares; earlier shares absorb the remainder."""
    if parts <= 0:
        raise MoneyError("parts must be positive")
    return allocate(m, [1] * parts)
