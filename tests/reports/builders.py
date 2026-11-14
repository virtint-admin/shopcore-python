"""A small fleet of orders spanning 9-12 Nov 2026 (IST)."""

from datetime import UTC, datetime

from shopcore.money.core import Money
from shopcore.orders.model import Order, OrderLine, OrderStatus, Refund


def inr(amount: str) -> Money:
    return Money(amount, "INR")


def make_order(
    order_id: str,
    region: str,
    placed_at: datetime,
    status: OrderStatus,
    lines: list[OrderLine],
) -> Order:
    return Order(
        order_id=order_id,
        customer_id=f"U-{order_id}",
        currency="INR",
        region=region,
        lines=lines,
        shipping=inr("50.00"),
        placed_at=placed_at,
        status=status,
    )


def fleet() -> list[Order]:
    """Counted: A, B, C, E (revenue 13392.00). D is cancelled, F unpaid.

    A  IN-KA  9 Nov 09:30 IST  4397.00  paid
    B  IN-MH 10 Nov 00:30 IST  1999.00  delivered (placed 19:00 UTC on the 9th)
    C  IN-KA 10 Nov 11:30 IST   998.00  shipped, 1 of 3 tees cancelled
    D  IN-DL 10 Nov           15999.00  cancelled
    E  IN-KA 12 Nov 13:30 IST  5998.00  paid, partly refunded
    F  IN-MH 12 Nov             799.00  pending payment
    """
    e = make_order(
        "E",
        "IN-KA",
        datetime(2026, 11, 12, 8, 0, tzinfo=UTC),
        OrderStatus.PAID,
        [OrderLine("ELC-0101", 2, inr("2999.00"), inr("1079.64"), "ELC")],
    )
    e.paid = inr("7127.64")
    e.refunds.append(Refund("E-R1", inr("100.00"), datetime(2026, 11, 13, tzinfo=UTC), "late"))
    return [
        make_order(
            "A",
            "IN-KA",
            datetime(2026, 11, 9, 4, 0, tzinfo=UTC),
            OrderStatus.PAID,
            [
                OrderLine("ELC-0101", 1, inr("2999.00"), inr("539.82"), "ELC"),
                OrderLine("BKS-0301", 2, inr("699.00"), inr("0.00"), "BKS"),
            ],
        ),
        make_order(
            "B",
            "IN-MH",
            datetime(2026, 11, 9, 19, 0, tzinfo=UTC),
            OrderStatus.DELIVERED,
            [
                OrderLine("BKS-0301", 1, inr("699.00"), inr("0.00"), "BKS"),
                OrderLine("GRC-0401", 4, inr("325.00"), inr("65.00"), "GRC"),
            ],
        ),
        make_order(
            "C",
            "IN-KA",
            datetime(2026, 11, 10, 6, 0, tzinfo=UTC),
            OrderStatus.SHIPPED,
            [OrderLine("APP-0001-BLK-M", 3, inr("499.00"), inr("179.64"), "APP", 1)],
        ),
        make_order(
            "D",
            "IN-DL",
            datetime(2026, 11, 10, 7, 0, tzinfo=UTC),
            OrderStatus.CANCELLED,
            [OrderLine("ELC-0105", 1, inr("15999.00"), inr("2879.82"), "ELC", 1)],
        ),
        e,
        make_order(
            "F",
            "IN-MH",
            datetime(2026, 11, 12, 9, 0, tzinfo=UTC),
            OrderStatus.PENDING_PAYMENT,
            [OrderLine("TOY-0501", 1, inr("799.00"), inr("143.82"), "TOY")],
        ),
    ]
