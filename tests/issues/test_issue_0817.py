"""Issue 0817. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.orders.model import Order, OrderLine, OrderStatus, Refund
from shopcore.reports.sales import refund_rate

CASES = [
    pytest.param(
        (
            [
                Order(
                    order_id="A",
                    customer_id="U-A",
                    currency="INR",
                    region="IN-KA",
                    lines=[
                        OrderLine(
                            sku="ELC-0101",
                            qty=1,
                            unit_price=Money("2999.00", "INR"),
                            tax=Money("539.82", "INR"),
                            category="ELC",
                            cancelled_qty=0,
                        ),
                        OrderLine(
                            sku="BKS-0301",
                            qty=2,
                            unit_price=Money("699.00", "INR"),
                            tax=Money("0.00", "INR"),
                            category="BKS",
                            cancelled_qty=0,
                        ),
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 9, 5, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.PAID,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="B",
                    customer_id="U-B",
                    currency="INR",
                    region="IN-MH",
                    lines=[
                        OrderLine(
                            sku="BKS-0301",
                            qty=1,
                            unit_price=Money("699.00", "INR"),
                            tax=Money("0.00", "INR"),
                            category="BKS",
                            cancelled_qty=0,
                        ),
                        OrderLine(
                            sku="GRC-0401",
                            qty=4,
                            unit_price=Money("325.00", "INR"),
                            tax=Money("65.00", "INR"),
                            category="GRC",
                            cancelled_qty=0,
                        ),
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 9, 19, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.DELIVERED,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="C",
                    customer_id="U-C",
                    currency="INR",
                    region="IN-KA",
                    lines=[
                        OrderLine(
                            sku="APP-0001-BLK-M",
                            qty=3,
                            unit_price=Money("499.00", "INR"),
                            tax=Money("179.64", "INR"),
                            category="APP",
                            cancelled_qty=1,
                        )
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 10, 6, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.SHIPPED,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="D",
                    customer_id="U-D",
                    currency="INR",
                    region="IN-DL",
                    lines=[
                        OrderLine(
                            sku="ELC-0105",
                            qty=1,
                            unit_price=Money("15999.00", "INR"),
                            tax=Money("2879.82", "INR"),
                            category="ELC",
                            cancelled_qty=1,
                        )
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 10, 7, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.CANCELLED,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="E",
                    customer_id="U-E",
                    currency="INR",
                    region="IN-KA",
                    lines=[
                        OrderLine(
                            sku="ELC-0101",
                            qty=2,
                            unit_price=Money("2999.00", "INR"),
                            tax=Money("1079.64", "INR"),
                            category="ELC",
                            cancelled_qty=0,
                        )
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 12, 8, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.PAID,
                    history=[],
                    paid=Money("7127.64", "INR"),
                    refunds=[
                        Refund(
                            refund_id="E-R1",
                            amount=Money("100.00", "INR"),
                            at=datetime.datetime(2026, 11, 13, 0, 0, tzinfo=datetime.timezone.utc),
                            reason="late",
                        )
                    ],
                ),
                Order(
                    order_id="F",
                    customer_id="U-F",
                    currency="INR",
                    region="IN-MH",
                    lines=[
                        OrderLine(
                            sku="TOY-0501",
                            qty=1,
                            unit_price=Money("799.00", "INR"),
                            tax=Money("143.82", "INR"),
                            category="TOY",
                            cancelled_qty=0,
                        )
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 12, 9, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.PENDING_PAYMENT,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
            ],
        ),
        {},
        Decimal("25.00"),
        None,
        id="case-1",
    ),
    pytest.param(
        (
            [
                Order(
                    order_id="A",
                    customer_id="U-A",
                    currency="INR",
                    region="IN-KA",
                    lines=[
                        OrderLine(
                            sku="ELC-0101",
                            qty=1,
                            unit_price=Money("2999.00", "INR"),
                            tax=Money("539.82", "INR"),
                            category="ELC",
                            cancelled_qty=0,
                        ),
                        OrderLine(
                            sku="BKS-0301",
                            qty=2,
                            unit_price=Money("699.00", "INR"),
                            tax=Money("0.00", "INR"),
                            category="BKS",
                            cancelled_qty=0,
                        ),
                    ],
                    shipping=Money("49.99", "INR"),
                    placed_at=datetime.datetime(2026, 11, 9, 4, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.PAID,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="B",
                    customer_id="U-B",
                    currency="INR",
                    region="IN-MH",
                    lines=[
                        OrderLine(
                            sku="BKS-0301",
                            qty=1,
                            unit_price=Money("699.00", "INR"),
                            tax=Money("0.00", "INR"),
                            category="BKS",
                            cancelled_qty=0,
                        ),
                        OrderLine(
                            sku="GRC-0401",
                            qty=4,
                            unit_price=Money("325.00", "INR"),
                            tax=Money("65.00", "INR"),
                            category="GRC",
                            cancelled_qty=0,
                        ),
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 9, 19, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.DELIVERED,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="C",
                    customer_id="U-C",
                    currency="INR",
                    region="IN-KA",
                    lines=[
                        OrderLine(
                            sku="APP-0001-BLK-M",
                            qty=3,
                            unit_price=Money("499.00", "INR"),
                            tax=Money("179.64", "INR"),
                            category="APP",
                            cancelled_qty=1,
                        )
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 10, 6, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.SHIPPED,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="D",
                    customer_id="U-D",
                    currency="INR",
                    region="IN-DL",
                    lines=[
                        OrderLine(
                            sku="ELC-0105",
                            qty=1,
                            unit_price=Money("15999.00", "INR"),
                            tax=Money("2879.82", "INR"),
                            category="ELC",
                            cancelled_qty=1,
                        )
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 10, 7, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.CANCELLED,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="E",
                    customer_id="U-E",
                    currency="INR",
                    region="IN-KA",
                    lines=[
                        OrderLine(
                            sku="ELC-0101",
                            qty=2,
                            unit_price=Money("2999.00", "INR"),
                            tax=Money("1079.64", "INR"),
                            category="ELC",
                            cancelled_qty=0,
                        )
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 12, 8, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.PAID,
                    history=[],
                    paid=Money("7127.64", "INR"),
                    refunds=[
                        Refund(
                            refund_id="E-R1",
                            amount=Money("100.00", "INR"),
                            at=datetime.datetime(2026, 11, 13, 0, 0, tzinfo=datetime.timezone.utc),
                            reason="late",
                        )
                    ],
                ),
                Order(
                    order_id="F",
                    customer_id="U-F",
                    currency="INR",
                    region="IN-MH",
                    lines=[
                        OrderLine(
                            sku="TOY-0501",
                            qty=1,
                            unit_price=Money("799.00", "INR"),
                            tax=Money("143.82", "INR"),
                            category="TOY",
                            cancelled_qty=0,
                        )
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 12, 9, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.PENDING_PAYMENT,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
            ],
        ),
        {},
        Decimal("25.00"),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            [
                Order(
                    order_id="A",
                    customer_id="U-A",
                    currency="INR",
                    region="IN-KA",
                    lines=[
                        OrderLine(
                            sku="ELC-0101",
                            qty=1,
                            unit_price=Money("2999.00", "INR"),
                            tax=Money("539.82", "INR"),
                            category="ELC",
                            cancelled_qty=0,
                        ),
                        OrderLine(
                            sku="BKS-0301",
                            qty=2,
                            unit_price=Money("699.00", "INR"),
                            tax=Money("0.00", "INR"),
                            category="BKS",
                            cancelled_qty=0,
                        ),
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 9, 4, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.PAID,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="B",
                    customer_id="U-B",
                    currency="INR",
                    region="IN-MH",
                    lines=[
                        OrderLine(
                            sku="BKS-0301",
                            qty=1,
                            unit_price=Money("699.00", "INR"),
                            tax=Money("0.00", "INR"),
                            category="BKS",
                            cancelled_qty=0,
                        ),
                        OrderLine(
                            sku="GRC-0401",
                            qty=4,
                            unit_price=Money("325.00", "INR"),
                            tax=Money("65.00", "INR"),
                            category="GRC",
                            cancelled_qty=0,
                        ),
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 9, 19, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.DELIVERED,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="C",
                    customer_id="U-C",
                    currency="INR",
                    region="IN-KA",
                    lines=[
                        OrderLine(
                            sku="APP-0001-BLK-M",
                            qty=3,
                            unit_price=Money("499.00", "INR"),
                            tax=Money("179.64", "INR"),
                            category="APP",
                            cancelled_qty=1,
                        )
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 10, 6, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.SHIPPED,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="D",
                    customer_id="U-D",
                    currency="INR",
                    region="IN-DL",
                    lines=[
                        OrderLine(
                            sku="ELC-0105",
                            qty=1,
                            unit_price=Money("15999.00", "INR"),
                            tax=Money("2879.82", "INR"),
                            category="ELC",
                            cancelled_qty=1,
                        )
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 10, 7, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.CANCELLED,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="E",
                    customer_id="U-E",
                    currency="INR",
                    region="IN-KA",
                    lines=[
                        OrderLine(
                            sku="ELC-0101",
                            qty=2,
                            unit_price=Money("2999.00", "INR"),
                            tax=Money("1079.64", "INR"),
                            category="ELC",
                            cancelled_qty=0,
                        )
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 12, 8, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.PAID,
                    history=[],
                    paid=Money("7127.64", "INR"),
                    refunds=[],
                ),
                Order(
                    order_id="F",
                    customer_id="U-F",
                    currency="INR",
                    region="IN-MH",
                    lines=[
                        OrderLine(
                            sku="TOY-0501",
                            qty=1,
                            unit_price=Money("799.00", "INR"),
                            tax=Money("143.82", "INR"),
                            category="TOY",
                            cancelled_qty=0,
                        )
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 12, 9, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.PENDING_PAYMENT,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
            ],
        ),
        {},
        Decimal("0.00"),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            [
                Order(
                    order_id="E",
                    customer_id="U-E",
                    currency="INR",
                    region="IN-KA",
                    lines=[
                        OrderLine(
                            sku="ELC-0101",
                            qty=2,
                            unit_price=Money("2999.00", "INR"),
                            tax=Money("1079.64", "INR"),
                            category="ELC",
                            cancelled_qty=0,
                        )
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 12, 8, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.PAID,
                    history=[],
                    paid=Money("7127.64", "INR"),
                    refunds=[
                        Refund(
                            refund_id="E-R1",
                            amount=Money("100.00", "INR"),
                            at=datetime.datetime(2026, 11, 13, 0, 0, tzinfo=datetime.timezone.utc),
                            reason="late",
                        )
                    ],
                ),
                Order(
                    order_id="B",
                    customer_id="U-B",
                    currency="INR",
                    region="IN-MH",
                    lines=[
                        OrderLine(
                            sku="BKS-0301",
                            qty=1,
                            unit_price=Money("699.00", "INR"),
                            tax=Money("0.00", "INR"),
                            category="BKS",
                            cancelled_qty=0,
                        ),
                        OrderLine(
                            sku="GRC-0401",
                            qty=4,
                            unit_price=Money("325.00", "INR"),
                            tax=Money("65.00", "INR"),
                            category="GRC",
                            cancelled_qty=0,
                        ),
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 9, 19, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.DELIVERED,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="A",
                    customer_id="U-A",
                    currency="INR",
                    region="IN-KA",
                    lines=[
                        OrderLine(
                            sku="ELC-0101",
                            qty=1,
                            unit_price=Money("2999.00", "INR"),
                            tax=Money("539.82", "INR"),
                            category="ELC",
                            cancelled_qty=0,
                        ),
                        OrderLine(
                            sku="BKS-0301",
                            qty=2,
                            unit_price=Money("699.00", "INR"),
                            tax=Money("0.00", "INR"),
                            category="BKS",
                            cancelled_qty=0,
                        ),
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 9, 4, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.PAID,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
            ],
        ),
        {},
        Decimal("33.33"),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            [
                Order(
                    order_id="A",
                    customer_id="U-A",
                    currency="INR",
                    region="IN-KA",
                    lines=[
                        OrderLine(
                            sku="ELC-0101",
                            qty=1,
                            unit_price=Money("2999.00", "INR"),
                            tax=Money("539.82", "INR"),
                            category="ELC",
                            cancelled_qty=0,
                        ),
                        OrderLine(
                            sku="BKS-0301",
                            qty=0,
                            unit_price=Money("699.00", "INR"),
                            tax=Money("0.00", "INR"),
                            category="BKS",
                            cancelled_qty=0,
                        ),
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 9, 4, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.PAID,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="B",
                    customer_id="U-B",
                    currency="INR",
                    region="IN-MH",
                    lines=[
                        OrderLine(
                            sku="BKS-0301",
                            qty=1,
                            unit_price=Money("699.00", "INR"),
                            tax=Money("0.00", "INR"),
                            category="BKS",
                            cancelled_qty=0,
                        ),
                        OrderLine(
                            sku="GRC-0401",
                            qty=4,
                            unit_price=Money("325.00", "INR"),
                            tax=Money("65.00", "INR"),
                            category="GRC",
                            cancelled_qty=0,
                        ),
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 9, 19, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.DELIVERED,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="E",
                    customer_id="U-E",
                    currency="INR",
                    region="IN-KA",
                    lines=[
                        OrderLine(
                            sku="ELC-0101",
                            qty=2,
                            unit_price=Money("2999.00", "INR"),
                            tax=Money("1079.64", "INR"),
                            category="ELC",
                            cancelled_qty=0,
                        )
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 12, 8, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.PAID,
                    history=[],
                    paid=Money("7127.64", "INR"),
                    refunds=[
                        Refund(
                            refund_id="E-R1",
                            amount=Money("100.00", "INR"),
                            at=datetime.datetime(2026, 11, 13, 0, 0, tzinfo=datetime.timezone.utc),
                            reason="late",
                        )
                    ],
                ),
            ],
        ),
        {},
        Decimal("33.33"),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            [
                Order(
                    order_id="A",
                    customer_id="U-A",
                    currency="INR",
                    region="IN-KA",
                    lines=[
                        OrderLine(
                            sku="ELC-0101",
                            qty=1,
                            unit_price=Money("2999.00", "INR"),
                            tax=Money("539.82", "INR"),
                            category="ELC",
                            cancelled_qty=0,
                        ),
                        OrderLine(
                            sku="BKS-0301",
                            qty=2,
                            unit_price=Money("699.00", "INR"),
                            tax=Money("0.00", "INR"),
                            category="BKS",
                            cancelled_qty=0,
                        ),
                    ],
                    shipping=Money("49.99", "INR"),
                    placed_at=datetime.datetime(2026, 11, 9, 4, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.PAID,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="B",
                    customer_id="U-B",
                    currency="INR",
                    region="IN-MH",
                    lines=[
                        OrderLine(
                            sku="BKS-0301",
                            qty=1,
                            unit_price=Money("699.00", "INR"),
                            tax=Money("0.00", "INR"),
                            category="BKS",
                            cancelled_qty=0,
                        ),
                        OrderLine(
                            sku="GRC-0401",
                            qty=4,
                            unit_price=Money("325.00", "INR"),
                            tax=Money("65.00", "INR"),
                            category="GRC",
                            cancelled_qty=0,
                        ),
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 9, 19, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.DELIVERED,
                    history=[],
                    paid=None,
                    refunds=[],
                ),
                Order(
                    order_id="E",
                    customer_id="U-E",
                    currency="INR",
                    region="IN-KA",
                    lines=[
                        OrderLine(
                            sku="ELC-0101",
                            qty=2,
                            unit_price=Money("2999.00", "INR"),
                            tax=Money("1079.64", "INR"),
                            category="ELC",
                            cancelled_qty=0,
                        )
                    ],
                    shipping=Money("50.00", "INR"),
                    placed_at=datetime.datetime(2026, 11, 12, 8, 0, tzinfo=datetime.timezone.utc),
                    status=OrderStatus.PAID,
                    history=[],
                    paid=Money("7127.64", "INR"),
                    refunds=[
                        Refund(
                            refund_id="E-R1",
                            amount=Money("100.00", "INR"),
                            at=datetime.datetime(2026, 11, 13, 0, 0, tzinfo=datetime.timezone.utc),
                            reason="late",
                        )
                    ],
                ),
            ],
        ),
        {},
        Decimal("33.33"),
        None,
        id="case-6",
    ),
    pytest.param(
        ([],),
        {},
        Decimal("0.00"),
        None,
        id="case-7",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0817(args, kwargs, expected, after):
    assert refund_rate(*args, **kwargs) == expected
    if after is not None:
        assert args == after
