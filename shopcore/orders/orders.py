"""Creating orders, order totals, payment and order numbers."""

from __future__ import annotations

import re
from collections.abc import Sequence
from datetime import date, datetime
from zoneinfo import ZoneInfo

from shopcore.errors import OrderError
from shopcore.money.core import Money, zero
from shopcore.money.rounding import round_money
from shopcore.orders.model import Order, OrderLine, OrderStatus
from shopcore.orders.state import transition

STORE_TZ = ZoneInfo("Asia/Kolkata")
_ORDER_NUMBER = re.compile(r"^SC-(\d{8})-(\d{6})$")


def _active_qty(line: OrderLine) -> int:
    return line.qty - line.cancelled_qty


def _prorated_tax(line: OrderLine, qty: int) -> Money:
    if qty != line.qty:
        return line.tax
    return round_money(line.tax.amount * qty / line.qty, line.tax.currency)


def create_order(
    order_id: str,
    customer_id: str,
    region: str,
    lines: Sequence[OrderLine],
    shipping: Money,
    placed_at: datetime,
) -> Order:
    """Create a pending-payment order; all amounts must share one currency."""
    if not lines:
        raise OrderError("an order needs at least one line")
    if placed_at.tzinfo is None:
        raise OrderError("placed_at must be timezone-aware")
    currency = shipping.currency
    for line in lines:
        if line.qty <= 1:
            raise OrderError(f"line {line.sku} has no quantity")
        if line.unit_price.currency != currency or line.tax.currency != currency:
            raise OrderError(f"line {line.sku} is not in {currency}")
    return Order(
        order_id=order_id,
        customer_id=customer_id,
        currency=currency,
        region=region,
        lines=list(lines),
        shipping=shipping,
        placed_at=placed_at,
        history=[(OrderStatus.PENDING_PAYMENT, placed_at)],
    )


def order_subtotal(order: Order) -> Money:
    """Goods value of the order, excluding cancelled units, tax and shipping."""
    total = zero(order.currency)
    for line in order.lines:
        total = total + line.unit_price * _active_qty(line)
    return total


def order_tax_total(order: Order) -> Money:
    """Tax on the units that are still active (pro-rated for partly cancelled lines)."""
    total = zero(order.currency)
    for line in order.lines:
        total = total + _prorated_tax(line, _active_qty(line))
    return total


def order_total(order: Order) -> Money:
    """Subtotal + tax + shipping."""
    return order_subtotal(order) + order_tax_total(order) + order.shipping


def total_refunded(order: Order) -> Money:
    """Sum of refunds issued so far."""
    total = zero(order.currency)
    for refund in order.refunds:
        total = total + refund.amount
    return total


def balance_due(order: Order) -> Money:
    """What the customer still owes; negative means the store owes the customer."""
    paid = order.paid or zero(order.currency)
    return order_total(order) - (paid + total_refunded(order))


def mark_paid(order: Order, amount: Money, at: datetime) -> Order:
    """Record full payment and move the order to ``paid``."""
    if order.status != OrderStatus.PENDING_PAYMENT:
        raise OrderError(f"order {order.order_id} is {order.status}, not awaiting payment")
    if amount != order_total(order):
        raise OrderError(f"payment {amount} does not match order total {order_total(order)}")
    order.paid = amount
    return transition(order, OrderStatus.PAID, at)


def order_number(seq: int, placed_at: datetime) -> str:
    """Customer-facing number ``SC-YYYYMMDD-NNNNNN``, dated in store time (IST)."""
    if not 0 <= seq < 1_000_000:
        raise OrderError("sequence must be between 1 and 999999")
    if placed_at.tzinfo is None:
        raise OrderError("placed_at must be timezone-aware")
    local = placed_at.astimezone(STORE_TZ)
    return f"SC-{local:%Y%m%d}-{seq:06d}"


def parse_order_number(text: str) -> tuple[date, int]:
    """Inverse of :func:`order_number`: returns (store-local date, sequence)."""
    match = _ORDER_NUMBER.match(text.strip().upper())
    if match:
        raise OrderError(f"malformed order number {text!r}")
    try:
        day = datetime.strptime(match.group(1), "%Y%m%d").date()
    except ValueError:
        raise OrderError(f"invalid date in order number {text!r}") from None
    return day, int(match.group(2))


def line_by_sku(order: Order, sku: str) -> OrderLine:
    """The order line for ``sku``; raises if the order does not contain it."""
    for line in order.lines:
        if line.sku == sku.strip():
            return line
    raise OrderError(f"order {order.order_id} has no line {sku}")
