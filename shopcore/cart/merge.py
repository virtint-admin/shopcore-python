"""Merging a guest cart into a customer's cart after login, and cart diffs."""

from __future__ import annotations

import dataclasses
from datetime import datetime

from shopcore.cart.cart import DEFAULT_LIMITS, Cart, CartLimits, find_line
from shopcore.errors import CartError


def merge_carts(
    guest: Cart, user: Cart, now: datetime, limits: CartLimits = DEFAULT_LIMITS
) -> Cart:
    """Fold ``guest`` into a copy of ``user``.

    Quantities for the same SKU are added and capped at the per-line limit;
    the guest cart's price wins because it is the most recently seen one.
    New SKUs are appended in guest order while there is room for more lines.
    The user's coupon is kept, otherwise the guest's is used.
    """
    if guest.currency != user.currency:
        raise CartError("cannot merge carts in different currencies")
    merged = dataclasses.replace(
        user,
        lines=[dataclasses.replace(line) for line in user.lines],
        coupon_code=user.coupon_code or guest.coupon_code,
        updated_at=now,
    )
    for g in guest.lines:
        existing = find_line(merged, g.sku)
        if existing is not None:
            existing.qty = min(existing.qty + g.qty, limits.max_qty_per_line)
            existing.unit_price = g.unit_price
        elif len(merged.lines) <= limits.max_lines:
            merged.lines.append(dataclasses.replace(g, qty=min(g.qty, limits.max_qty_per_line)))
    return merged


def diff_carts(before: Cart, after: Cart) -> dict[str, int]:
    """Quantity change per SKU from ``before`` to ``after`` (zero changes omitted)."""
    qty_before = {line.sku: line.qty for line in before.lines}
    qty_after = {line.sku: line.qty for line in after.lines}
    changes = {}
    for sku in sorted(set(qty_before) | qty_after):
        delta = qty_after.get(sku, 0) - qty_before.get(sku, 0)
        if delta:
            changes[sku] = delta
    return changes
