"""Order builders shared by the orders tests."""

from datetime import UTC, datetime, timedelta

from shopcore.money.core import Money
from shopcore.orders.model import Order, OrderLine, OrderStatus
from shopcore.orders.orders import create_order, mark_paid, order_total
from shopcore.orders.state import transition

T0 = datetime(2026, 11, 9, 10, 0, tzinfo=UTC)  # 15:30 IST


def inr(amount: str) -> Money:
    return Money(amount, "INR")


def sample_lines() -> list[OrderLine]:
    """Subtotal 5894.00, tax 719.46, shipping 50.00 -> total 6663.46."""
    return [
        OrderLine("ELC-0101", 1, inr("2999.00"), inr("539.82"), "ELC"),
        OrderLine("BKS-0301", 2, inr("699.00"), inr("0.00"), "BKS"),
        OrderLine("APP-0001-BLK-M", 3, inr("499.00"), inr("179.64"), "APP"),
    ]


PATH = {
    OrderStatus.PENDING_PAYMENT: [],
    OrderStatus.PAID: [OrderStatus.PAID],
    OrderStatus.PACKED: [OrderStatus.PAID, OrderStatus.PACKED],
    OrderStatus.SHIPPED: [OrderStatus.PAID, OrderStatus.PACKED, OrderStatus.SHIPPED],
    OrderStatus.DELIVERED: [
        OrderStatus.PAID,
        OrderStatus.PACKED,
        OrderStatus.SHIPPED,
        OrderStatus.DELIVERED,
    ],
}


def build_order(
    status: OrderStatus = OrderStatus.PENDING_PAYMENT,
    order_id: str = "O1",
    customer_id: str = "U1",
    region: str = "IN-KA",
    placed_at: datetime = T0,
    lines: list[OrderLine] | None = None,
) -> Order:
    """An order walked to ``status``; each step happens one hour after the previous."""
    order = create_order(
        order_id,
        customer_id,
        region,
        lines if lines is not None else sample_lines(),
        inr("50.00"),
        placed_at,
    )
    at = placed_at
    for step in PATH[status]:
        at = at + timedelta(hours=1)
        if step == OrderStatus.PAID:
            mark_paid(order, order_total(order), at)
        else:
            transition(order, step, at)
    return order
