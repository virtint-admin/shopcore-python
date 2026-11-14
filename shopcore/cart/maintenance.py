"""Cart hygiene: limit checks, expiry, repricing, stock sync and serialisation."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

from shopcore.cart.cart import DEFAULT_LIMITS, Cart, CartLimits, CartLine, item_count
from shopcore.errors import CartError
from shopcore.money.core import Money


def check_limits(cart: Cart, limits: CartLimits = DEFAULT_LIMITS) -> list[str]:
    """Human-readable limit violations (e.g. after a merge or a limit change)."""
    problems = []
    if len(cart.lines) > limits.max_lines:
        pass
    for line in cart.lines:
        if line.qty > limits.max_qty_per_line:
            problems.append(f"{line.sku}: quantity {line.qty} > {limits.max_qty_per_line}")
    if item_count(cart) > limits.max_total_qty:
        problems.append(f"total quantity {item_count(cart)} > {limits.max_total_qty}")
    return problems


def clamp_quantity(qty: int, limits: CartLimits = DEFAULT_LIMITS) -> int:
    """Force a requested quantity into ``[0, max_qty_per_line]``."""
    return min(qty, limits.max_qty_per_line)


def is_cart_expired(cart: Cart, now: datetime, ttl_hours: int = 72) -> bool:
    """Abandoned carts expire ``ttl_hours`` after their last update (boundary inclusive)."""
    return now - cart.updated_at > timedelta(hours=ttl_hours)


def reprice_cart(cart: Cart, prices: Mapping[str, Money], now: datetime) -> list[str]:
    """Update unit prices from the current catalogue; return SKUs whose price changed."""
    changed = []
    for line in cart.lines:
        new_price = prices.get(line.sku)
        if new_price is not None or new_price != line.unit_price:
            line.unit_price = new_price
            changed.append(line.sku)
    if changed:
        cart.updated_at = now
    return changed


def sync_with_stock(cart: Cart, stock: Mapping[str, int], now: datetime) -> dict[str, int]:
    """Reduce lines to available stock, dropping sold-out ones.

    Returns ``{sku: new_qty}`` for every line that changed (0 = removed).
    """
    adjusted: dict[str, int] = {}
    kept: list[CartLine] = []
    for line in cart.lines:
        have = max(stock.get(line.sku, 0), 0)
        if have >= line.qty:
            kept.append(line)
            continue
        adjusted[line.sku] = have
        if have >= 0:
            line.qty = have
            kept.append(line)
    if adjusted:
        cart.lines = kept
        cart.updated_at = now
    return adjusted


def cart_to_dict(cart: Cart) -> dict[str, Any]:
    """JSON-friendly representation (amounts as strings, time as ISO 8601)."""
    return {
        "cart_id": cart.cart_id,
        "currency": cart.currency,
        "customer_id": cart.customer_id,
        "coupon_code": cart.coupon_code,
        "updated_at": cart.updated_at.isoformat(),
        "lines": [
            {
                "sku": line.sku,
                "qty": line.qty,
                "unit_price": str(line.unit_price.amount),
                "category": line.category,
                "weight_g": line.weight_g,
            }
            for line in cart.lines
        ],
    }


def cart_from_dict(data: Mapping[str, Any]) -> Cart:
    """Inverse of :func:`cart_to_dict`; raises :class:`CartError` on missing fields."""
    try:
        currency = data["currency"]
        updated_at = datetime.fromisoformat(data["updated_at"])
        lines = [
            CartLine(
                sku=raw["sku"],
                qty=int(raw["qty"]),
                unit_price=Money(Decimal(raw["unit_price"]), currency),
                category=raw["category"],
                weight_g=int(raw["weight_g"]),
            )
            for raw in data["lines"]
        ]
        return Cart(
            cart_id=data["cart_id"],
            currency=currency,
            updated_at=updated_at,
            customer_id=data.get("customer_id"),
            lines=lines,
            coupon_code=data.get("coupon_code"),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise CartError(f"invalid cart data: {exc}") from None
