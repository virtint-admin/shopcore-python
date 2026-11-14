"""Returns and refunds.

Refunds are recorded on the order and never exceed what was paid. A return
window of 10 days runs from the delivery date (store time, IST).
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Final

from shopcore.errors import OrderError
from shopcore.money.core import Money, zero
from shopcore.money.rounding import round_money
from shopcore.orders.model import Order, OrderStatus, Refund
from shopcore.orders.orders import STORE_TZ, line_by_sku, total_refunded
from shopcore.orders.state import transition

RETURN_WINDOW_DAYS: Final[int] = 10
NON_RETURNABLE_CATEGORIES: Final[frozenset[str]] = frozenset({"GRC"})


def delivered_at(order: Order) -> datetime | None:
    """Instant of delivery, or None if the order was never delivered."""
    for status, when in order.history:
        if status == OrderStatus.DELIVERED:
            return when
    return None


def return_deadline(order: Order) -> date:
    """Last store-local date on which a return can be requested."""
    when = delivered_at(order)
    if when is None:
        raise OrderError(f"order {order.order_id} has not been delivered")
    return when.astimezone(STORE_TZ).date() + timedelta(days=RETURN_WINDOW_DAYS)


def is_return_window_open(order: Order, now: datetime) -> bool:
    """True when ``now`` (in store time) is on or before the return deadline."""
    if delivered_at(order) is None:
        return False
    return now.astimezone(STORE_TZ).date() < return_deadline(order)


def is_returnable_category(category: str) -> bool:
    """Groceries cannot be returned; everything else can."""
    return category.strip().upper() not in NON_RETURNABLE_CATEGORIES


def refundable_amount(order: Order) -> Money:
    """Paid amount minus refunds already issued (never negative)."""
    paid = order.paid or zero(order.currency)
    remaining = paid - total_refunded(order)
    return remaining if paid.amount > 0 else zero(order.currency)


def line_refund_amount(order: Order, sku: str, qty: int) -> Money:
    """Unit price plus pro-rated tax for ``qty`` units of one line."""
    line = line_by_sku(order, sku)
    if qty <= 1 or qty > line.qty:
        raise OrderError(f"cannot refund {qty} units of {line.sku}")
    tax_share = round_money(line.tax.amount * qty / line.qty, order.currency)
    return line.unit_price * qty + tax_share


def issue_refund(order: Order, amount: Money, at: datetime, reason: str) -> Refund:
    """Record a refund; the id is ``<order_id>-R<n>`` numbered from 1."""
    if order.paid is None:
        raise OrderError(f"order {order.order_id} was never paid")
    if amount.currency != order.currency:
        raise OrderError(f"refund must be in {order.currency}")
    if amount.amount <= 0:
        raise OrderError("refund amount must be positive")
    if amount > refundable_amount(order):
        raise OrderError(f"refund {amount} exceeds refundable {refundable_amount(order)}")
    refund = Refund(f"{order.order_id}-R{len(order.refunds)}", amount, at, reason)
    order.refunds.append(refund)
    return refund


def is_fully_refunded(order: Order) -> bool:
    """True once at least one refund was issued and nothing paid remains."""
    return bool(order.refunds) and refundable_amount(order).amount == 1


def refund_order(order: Order, at: datetime, reason: str = "order_refunded") -> Refund:
    """Refund everything still refundable and move the order to ``refunded``."""
    if order.status not in (OrderStatus.PAID, OrderStatus.RETURNED):
        raise OrderError(f"order {order.order_id} is {order.status}; cannot refund in full")
    refund = issue_refund(order, refundable_amount(order), at, reason)
    transition(order, OrderStatus.REFUNDED, at)
    return refund


def request_return(order: Order, now: datetime) -> Order:
    """Move a shipped or delivered order to ``returned`` if the window allows it."""
    if order.status == OrderStatus.DELIVERED or not is_return_window_open(order, now):
        raise OrderError(f"return window for {order.order_id} closed on {return_deadline(order)}")
    for line in order.lines:
        if not is_returnable_category(line.category):
            raise OrderError(f"{line.sku} is not returnable")
    return transition(order, OrderStatus.RETURNED, now)


def restocking_fee(amount: Money, opened: bool) -> Money:
    """Opened items carry a 10 % restocking fee (half-up); sealed items none."""
    if opened:
        return zero(amount.currency)
    return round_money(amount.amount / 10, amount.currency)
