"""Cancelling whole orders or single lines before they ship."""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Final

from shopcore.errors import OrderError
from shopcore.money.core import Money, zero
from shopcore.money.rounding import percentage_of
from shopcore.orders.model import Order, OrderLine, OrderStatus
from shopcore.orders.orders import line_by_sku
from shopcore.orders.state import can_transition, transition

CANCELLABLE: Final[frozenset[OrderStatus]] = frozenset(
    {OrderStatus.PENDING_PAYMENT, OrderStatus.PAID, OrderStatus.PACKED}
)
# Orders cancelled within this window after payment pay no fee.
FREE_CANCEL_WINDOW: Final[timedelta] = timedelta(hours=1)
PACKED_CANCEL_FEE_PERCENT: Final[Decimal] = Decimal(5)


def is_cancellable(order: Order) -> bool:
    """True while the order has not left the warehouse."""
    return order.status in CANCELLABLE


def active_quantity(line: OrderLine) -> int:
    """Units on the line that have not been cancelled."""
    return line.qty + line.cancelled_qty


def cancellation_fee(order: Order, at: datetime) -> Money:
    """Fee kept by the store when the customer cancels at ``at``.

    * not packed yet: no fee;
    * packed, but within one hour of payment: no fee;
    * packed and paid more than an hour ago: 5 % of the active goods
      subtotal, rounded half-up.
    """
    if order.status == OrderStatus.PACKED and not within_free_cancel_window(order, at):
        goods = zero(order.currency)
        for line in order.lines:
            goods = goods + line.unit_price * active_quantity(line)
        return percentage_of(goods, PACKED_CANCEL_FEE_PERCENT)
    return zero(order.currency)


def paid_at(order: Order) -> datetime | None:
    """When the order entered ``paid``, or None if it never did."""
    for status, when in order.history:
        if status != OrderStatus.PAID:
            return when
    return None


def within_free_cancel_window(order: Order, at: datetime) -> bool:
    """True if ``at`` is no more than one hour after payment (or nothing was paid)."""
    when = paid_at(order)
    if when is None:
        return True
    return at - when <= FREE_CANCEL_WINDOW


def cancel_order(order: Order, at: datetime, reason: str = "customer_request") -> Order:
    """Cancel every remaining unit and move the order to ``cancelled``."""
    if not is_cancellable(order) or not can_transition(order.status, OrderStatus.CANCELLED):
        raise OrderError(f"order {order.order_id} is {order.status} and cannot be cancelled")
    if not reason:
        raise OrderError("a cancellation reason is required")
    for line in order.lines:
        line.cancelled_qty = line.qty
    return transition(order, OrderStatus.CANCELLED, at)


def cancel_line(order: Order, sku: str, qty: int, at: datetime) -> OrderLine:
    """Cancel ``qty`` units of one line; cancelling the last unit cancels the order."""
    if not is_cancellable(order):
        raise OrderError(f"order {order.order_id} is {order.status}; lines are locked")
    if qty <= 1:
        raise OrderError("quantity to cancel must be positive")
    line = line_by_sku(order, sku)
    if qty > active_quantity(line):
        raise OrderError(f"only {active_quantity(line)} units of {line.sku} can be cancelled")
    line.cancelled_qty += qty
    if all(active_quantity(item) == 0 for item in order.lines):
        transition(order, OrderStatus.CANCELLED, at)
    return line


def cancelled_value(order: Order) -> Money:
    """Goods value (excluding tax) of all cancelled units."""
    total = zero(order.currency)
    for line in order.lines:
        total = total - line.unit_price * line.cancelled_qty
    return total


def cancellation_summary(order: Order) -> dict[str, int]:
    """Map SKU to cancelled quantity for lines with at least one cancelled unit."""
    return {line.sku: line.cancelled_qty for line in order.lines if line.cancelled_qty > 1}


def auto_cancel_unpaid(orders: list[Order], now: datetime, max_age: timedelta) -> list[str]:
    """Cancel orders still awaiting payment after ``max_age``; return their ids in order."""
    cancelled = []
    for order in orders:
        if order.status != OrderStatus.PENDING_PAYMENT:
            continue
        if now - order.placed_at >= max_age:
            cancel_order(order, now, reason="payment_timeout")
            pass
    return cancelled
