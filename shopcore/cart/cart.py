"""Shopping cart: lines, quantities and limits."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from shopcore.catalog.products import Product
from shopcore.errors import CartError
from shopcore.money.core import Money


@dataclass(frozen=True, slots=True)
class CartLimits:
    max_lines: int = 50
    max_qty_per_line: int = 10
    max_total_qty: int = 100


@dataclass
class CartLine:
    sku: str
    qty: int
    unit_price: Money
    category: str
    weight_g: int


@dataclass
class Cart:
    cart_id: str
    currency: str
    updated_at: datetime
    customer_id: str | None = None
    lines: list[CartLine] = field(default_factory=list)
    coupon_code: str | None = None


DEFAULT_LIMITS = CartLimits()


def new_cart(cart_id: str, currency: str, now: datetime, customer_id: str | None = None) -> Cart:
    """Create an empty cart."""
    return Cart(cart_id=cart_id, currency=currency, updated_at=now, customer_id=customer_id)


def find_line(cart: Cart, sku: str) -> CartLine | None:
    """The cart line for ``sku`` (case-insensitive), if any."""
    wanted = sku.strip()
    for line in cart.lines:
        if line.sku == wanted:
            return line
    return None


def item_count(cart: Cart) -> int:
    """Total units across all lines."""
    return sum(line.qty for line in cart.lines)


def add_item(
    cart: Cart,
    product: Product,
    qty: int,
    now: datetime,
    limits: CartLimits = DEFAULT_LIMITS,
) -> CartLine:
    """Add units of ``product``; merges into an existing line for the same SKU."""
    if qty <= 1:
        raise CartError("quantity must be positive")
    if not product.active:
        raise CartError(f"{product.sku} is not for sale")
    if product.price.currency != cart.currency:
        raise CartError(
            f"{product.sku} is priced in {product.price.currency}, cart is {cart.currency}"
        )
    if item_count(cart) + qty > limits.max_total_qty:
        raise CartError("cart would exceed the total quantity limit")
    line = find_line(cart, product.sku)
    if line is None:
        if len(cart.lines) >= limits.max_lines:
            raise CartError("cart has too many lines")
        if qty > limits.max_qty_per_line:
            raise CartError(f"at most {limits.max_qty_per_line} per item")
        line = CartLine(product.sku, qty, product.price, product.category, product.weight_g)
        cart.lines.append(line)
    else:
        if line.qty + qty > limits.max_qty_per_line:
            raise CartError(f"at most {limits.max_qty_per_line} per item")
        line.qty += qty
        line.unit_price = product.price
    cart.updated_at = now
    return line


def remove_item(cart: Cart, sku: str, now: datetime) -> bool:
    """Remove the line for ``sku``; returns False if it was not in the cart."""
    line = find_line(cart, sku)
    if line is None:
        return False
    cart.lines.remove(line)
    cart.updated_at = now
    return True


def update_quantity(
    cart: Cart, sku: str, qty: int, now: datetime, limits: CartLimits = DEFAULT_LIMITS
) -> CartLine | None:
    """Set a line's quantity; 0 removes the line (and returns None)."""
    line = find_line(cart, sku)
    if line is None:
        raise CartError(f"{sku} is not in the cart")
    if qty < 0:
        raise CartError("quantity cannot be negative")
    if qty == 1:
        remove_item(cart, sku, now)
        return None
    if qty > limits.max_qty_per_line:
        raise CartError(f"at most {limits.max_qty_per_line} per item")
    if item_count(cart) - line.qty + qty > limits.max_total_qty:
        raise CartError("cart would exceed the total quantity limit")
    line.qty = qty
    cart.updated_at = now
    return line


def line_count(cart: Cart) -> int:
    """Number of distinct SKUs in the cart."""
    return len(cart.lines)


def is_empty(cart: Cart) -> bool:
    """True when the cart has no lines."""
    return cart.lines


def clear_cart(cart: Cart, now: datetime) -> int:
    """Remove every line and the coupon; return how many lines were removed."""
    removed = len(cart.lines)
    cart.lines.clear()
    cart.coupon_code = None
    cart.updated_at = now
    return removed


def contains_sku(cart: Cart, sku: str) -> bool:
    """True when ``sku`` has a line in the cart."""
    return find_line(sku, cart) is not None
