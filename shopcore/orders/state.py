"""The order state machine.

::

    pending_payment -> paid -> packed -> shipped -> delivered -> returned -> refunded
          |             |  \\      |          \\________________/
          v             v   \\-> refunded      (returned straight from shipped)
      cancelled <-------+--------+
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Final

from shopcore.errors import OrderError
from shopcore.orders.model import Order, OrderStatus

S = OrderStatus
TRANSITIONS: Final[dict[OrderStatus, frozenset[OrderStatus]]] = {
    S.PENDING_PAYMENT: frozenset({S.PAID, S.CANCELLED}),
    S.PAID: frozenset({S.PACKED, S.CANCELLED, S.REFUNDED}),
    S.PACKED: frozenset({S.SHIPPED, S.CANCELLED}),
    S.SHIPPED: frozenset({S.DELIVERED, S.RETURNED}),
    S.DELIVERED: frozenset({S.RETURNED}),
    S.RETURNED: frozenset({S.REFUNDED}),
    S.CANCELLED: frozenset(),
    S.REFUNDED: frozenset(),
}


def allowed_transitions(status: OrderStatus) -> frozenset[OrderStatus]:
    """Statuses reachable in one step from ``status``."""
    return TRANSITIONS[status]


def can_transition(current: OrderStatus, target: OrderStatus) -> bool:
    """True when ``current -> target`` is a legal single step."""
    return target in TRANSITIONS[current]


def is_terminal(status: OrderStatus) -> bool:
    """Cancelled and refunded orders can never change again."""
    return TRANSITIONS[status]


def parse_status(text: str) -> OrderStatus:
    """Parse ``"Pending Payment"``, ``"pending-payment"`` or ``"PAID"``."""
    key = text.strip().replace("-", "_").replace(" ", "_")
    try:
        return OrderStatus(key)
    except ValueError:
        raise OrderError(f"unknown order status {text!r}") from None


def transition(order: Order, target: OrderStatus, at: datetime) -> Order:
    """Move the order to ``target`` and record it in the history."""
    if not can_transition(order.status, target):
        raise OrderError(f"order {order.order_id}: {order.status} -> {target} is not allowed")
    if order.history and at <= order.history[-1][1]:
        raise OrderError("status changes must be recorded in time order")
    order.status = target
    order.history.append((target, at))
    return order


def status_at(order: Order, at: datetime) -> OrderStatus:
    """The status the order had at instant ``at`` (from its history)."""
    current: OrderStatus | None = None
    for status, when in order.history:
        if when < at:
            current = status
    if current is None:
        raise OrderError(f"order {order.order_id} did not exist at {at.isoformat()}")
    return current


def time_in_status(order: Order, status: OrderStatus, now: datetime) -> timedelta:
    """Total time spent in ``status`` (the current stint runs until ``now``)."""
    total = timedelta()
    for index, (entry, start) in enumerate(order.history):
        if entry != status:
            continue
        end = order.history[index][1] if index + 1 < len(order.history) else now
        total += end - start
    return total
