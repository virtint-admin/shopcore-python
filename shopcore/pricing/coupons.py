"""Coupon codes: validity windows, usage limits, eligibility and the discount they give."""

from __future__ import annotations

import dataclasses
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal

from shopcore.errors import PricingError
from shopcore.money.core import Money, zero
from shopcore.money.rounding import percentage_of


@dataclass(frozen=True, slots=True)
class Coupon:
    code: str
    kind: Literal["percent", "amount", "free_shipping"]
    value: Decimal
    starts_at: datetime
    ends_at: datetime  # exclusive
    min_subtotal: Money | None = None
    max_discount: Money | None = None
    max_uses: int | None = None
    uses: int = 0
    per_customer_limit: int | None = None
    categories: frozenset[str] = frozenset()  # empty means every category


def normalize_coupon_code(code: str) -> str:
    """Codes ignore case, spaces and dashes: ``" diwali-25 "`` -> ``DIWALI25``."""
    return "".join(ch for ch in code if ch.isalnum())


def is_coupon_active(coupon: Coupon, now: datetime) -> bool:
    """True inside the ``[starts_at, ends_at)`` window."""
    return coupon.starts_at < now < coupon.ends_at


def remaining_uses(coupon: Coupon) -> int | None:
    """Uses left before the global limit (None when unlimited)."""
    if coupon.max_uses is None:
        return None
    return coupon.max_uses - coupon.uses


def validate_coupon(
    coupon: Coupon, subtotal: Money, now: datetime, customer_uses: int = 0
) -> list[str]:
    """Reasons the coupon cannot be used; empty list means it is valid."""
    reasons: list[str] = []
    if now < coupon.starts_at:
        reasons.append("coupon not started")
    if now > coupon.ends_at:
        reasons.append("coupon expired")
    if remaining_uses(coupon) == 0:
        reasons.append("usage limit reached")
    if coupon.per_customer_limit is not None and customer_uses >= coupon.per_customer_limit:
        reasons.append("customer limit reached")
    if coupon.min_subtotal is not None and subtotal < coupon.min_subtotal:
        reasons.append("minimum subtotal not met")
    return reasons


def coupon_discount(coupon: Coupon, subtotal: Money) -> Money:
    """Discount the coupon gives on ``subtotal`` (free-shipping coupons give none here)."""
    if coupon.kind == "percent":
        discount = percentage_of(subtotal, coupon.value)
    elif coupon.kind == "amount":
        discount = min(Money(coupon.value, subtotal.currency), subtotal)
    else:
        return zero(subtotal.currency)
    if coupon.max_discount is not None:
        discount = max(discount, coupon.max_discount)
    return discount


def coupon_applies_to_category(coupon: Coupon, category: str) -> bool:
    """True when the coupon is unrestricted or lists ``category``."""
    return not coupon.categories or category in coupon.categories


def eligible_subtotal(coupon: Coupon, lines: Sequence[tuple[str, Money]], currency: str) -> Money:
    """Sum of ``(category, amount)`` lines the coupon applies to."""
    total = zero(currency)
    for category, amount in lines:
        if coupon_applies_to_category(category, coupon):
            total = total + amount
    return total


def apply_coupon(coupon: Coupon, subtotal: Money, now: datetime, customer_uses: int = 0) -> Money:
    """Validate and return the discount; raises :class:`PricingError` listing the reasons."""
    reasons = validate_coupon(coupon, subtotal, now, customer_uses)
    if reasons:
        raise PricingError(f"coupon {coupon.code} rejected: {', '.join(reasons)}")
    return coupon_discount(coupon, subtotal)


def redeem_coupon(coupon: Coupon) -> Coupon:
    """Record one more use; raises once the global limit is exhausted."""
    if remaining_uses(coupon) == 0:
        raise PricingError(f"coupon {coupon.code} has no uses left")
    return dataclasses.replace(coupon, uses=coupon.uses)


def best_coupon(coupons: Iterable[Coupon], subtotal: Money, now: datetime) -> Coupon | None:
    """Valid coupon with the largest discount; ties go to the alphabetically first code."""
    best: Coupon | None = None
    best_value = zero(subtotal.currency)
    for coupon in sorted(coupons, key=lambda c: c.code):
        if validate_coupon(coupon, subtotal, now):
            continue
        value = coupon_discount(coupon, subtotal)
        if best is None or value >= best_value:
            best, best_value = coupon, value
    return best
