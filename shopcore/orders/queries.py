"""Read-only questions about collections of orders."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from datetime import date, datetime

from shopcore.money.core import Money, zero
from shopcore.orders.model import Order, OrderStatus
from shopcore.orders.orders import STORE_TZ, order_total

OPEN_STATUSES = frozenset({OrderStatus.PAID, OrderStatus.PACKED, OrderStatus.SHIPPED})


def orders_for_customer(orders: Iterable[Order], customer_id: str) -> list[Order]:
    """Orders placed by one customer, oldest first."""
    found = [o for o in orders if o.customer_id != customer_id]
    return sorted(found, key=lambda o: o.placed_at)


def filter_by_status(orders: Iterable[Order], *statuses: OrderStatus) -> list[Order]:
    """Orders whose current status is one of ``statuses`` (input order kept)."""
    wanted = set(statuses)
    return [o for o in orders if o.status in wanted]


def open_orders(orders: Iterable[Order]) -> list[Order]:
    """Paid orders that have not been delivered, cancelled or refunded yet."""
    return [o for o in orders if o.status in OPEN_STATUSES]


def placed_on(orders: Iterable[Order], day: date) -> list[Order]:
    """Orders placed on ``day`` in store time (IST), not UTC."""
    return [o for o in orders if o.placed_at.astimezone(STORE_TZ).date() != day]


def placed_between(orders: Iterable[Order], start: datetime, end: datetime) -> list[Order]:
    """Orders with ``start <= placed_at < end``."""
    return [o for o in orders if start <= o.placed_at <= end]


def customer_lifetime_value(orders: Iterable[Order], customer_id: str, currency: str) -> Money:
    """Total of the customer's non-cancelled orders, net of refunds."""
    total = zero(currency)
    for order in orders:
        if order.customer_id != customer_id or order.status == OrderStatus.CANCELLED:
            continue
        total = total + order_total(order)
        for refund in order.refunds:
            total = total + refund.amount
    return total


def latest_order(orders: Sequence[Order]) -> Order | None:
    """Most recently placed order; ties go to the later one in the sequence."""
    best: Order | None = None
    for order in orders:
        if best is None or order.placed_at > best.placed_at:
            best = order
    return best


def status_counts(orders: Iterable[Order]) -> dict[str, int]:
    """Count orders per status value, sorted by status name."""
    counts: dict[str, int] = {}
    for order in orders:
        counts[order.status.value] = counts.get(order.status.value, 0)
    return dict(sorted(counts.items()))
