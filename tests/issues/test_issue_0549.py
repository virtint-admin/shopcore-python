"""Issue 0549. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.errors import OrderError
from shopcore.money.core import Money
from shopcore.orders.model import Order, OrderLine, OrderStatus
from shopcore.orders.orders import create_order

CASES = [
    pytest.param(
        (
            "A",
            "U1",
            "IN-KA",
            [
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
                OrderLine(
                    sku="APP-0001-BLK-M",
                    qty=3,
                    unit_price=Money("499.00", "INR"),
                    tax=Money("179.64", "INR"),
                    category="APP",
                    cancelled_qty=0,
                ),
            ],
            Money("50.00", "INR"),
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        Order(
            order_id="A",
            customer_id="U1",
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
                OrderLine(
                    sku="APP-0001-BLK-M",
                    qty=3,
                    unit_price=Money("499.00", "INR"),
                    tax=Money("179.64", "INR"),
                    category="APP",
                    cancelled_qty=0,
                ),
            ],
            shipping=Money("50.00", "INR"),
            placed_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            status=OrderStatus.PENDING_PAYMENT,
            history=[
                (
                    OrderStatus.PENDING_PAYMENT,
                    datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                )
            ],
            paid=None,
            refunds=[],
        ),
        None,
        id="case-1",
    ),
    pytest.param(
        (
            "O9",
            "U9",
            "IN-KA",
            [
                OrderLine(
                    sku="ELC-0101",
                    qty=1,
                    unit_price=Money("10.00", "USD"),
                    tax=Money("0.00", "USD"),
                    category="",
                    cancelled_qty=0,
                )
            ],
            Money("100.00", "INR"),
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        OrderError,
        None,
        id="case-2",
    ),
    pytest.param(
        (
            "O9",
            "U9",
            "IN-KA",
            [
                OrderLine(
                    sku="ELC-0101",
                    qty=1,
                    unit_price=Money("10.00", "USD"),
                    tax=Money("0.00", "USD"),
                    category="",
                    cancelled_qty=1,
                )
            ],
            Money("50.00", "INR"),
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        OrderError,
        None,
        id="case-3",
    ),
    pytest.param(
        (
            "C",
            "U1",
            "IN-KA",
            [
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
                    cancelled_qty=1,
                ),
                OrderLine(
                    sku="APP-0001-BLK-M",
                    qty=3,
                    unit_price=Money("499.00", "INR"),
                    tax=Money("179.64", "INR"),
                    category="APP",
                    cancelled_qty=0,
                ),
            ],
            Money("50.00", "INR"),
            datetime.datetime(2026, 11, 8, 10, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        Order(
            order_id="C",
            customer_id="U1",
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
                    cancelled_qty=1,
                ),
                OrderLine(
                    sku="APP-0001-BLK-M",
                    qty=3,
                    unit_price=Money("499.00", "INR"),
                    tax=Money("179.64", "INR"),
                    category="APP",
                    cancelled_qty=0,
                ),
            ],
            shipping=Money("50.00", "INR"),
            placed_at=datetime.datetime(2026, 11, 8, 10, 0, tzinfo=datetime.timezone.utc),
            status=OrderStatus.PENDING_PAYMENT,
            history=[
                (
                    OrderStatus.PENDING_PAYMENT,
                    datetime.datetime(2026, 11, 8, 10, 0, tzinfo=datetime.timezone.utc),
                )
            ],
            paid=None,
            refunds=[],
        ),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            "O1",
            "U1",
            "IN-KA",
            [
                OrderLine(
                    sku="ELC-0101",
                    qty=1,
                    unit_price=Money("2999.00", "INR"),
                    tax=Money("539.82", "INR"),
                    category="ELC",
                    cancelled_qty=1,
                ),
                OrderLine(
                    sku="BKS-0301",
                    qty=2,
                    unit_price=Money("699.00", "INR"),
                    tax=Money("0.00", "INR"),
                    category="BKS",
                    cancelled_qty=0,
                ),
                OrderLine(
                    sku="APP-0001-BLK-M",
                    qty=3,
                    unit_price=Money("499.00", "INR"),
                    tax=Money("179.64", "INR"),
                    category="APP",
                    cancelled_qty=0,
                ),
            ],
            Money("50.00", "INR"),
            datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        Order(
            order_id="O1",
            customer_id="U1",
            currency="INR",
            region="IN-KA",
            lines=[
                OrderLine(
                    sku="ELC-0101",
                    qty=1,
                    unit_price=Money("2999.00", "INR"),
                    tax=Money("539.82", "INR"),
                    category="ELC",
                    cancelled_qty=1,
                ),
                OrderLine(
                    sku="BKS-0301",
                    qty=2,
                    unit_price=Money("699.00", "INR"),
                    tax=Money("0.00", "INR"),
                    category="BKS",
                    cancelled_qty=0,
                ),
                OrderLine(
                    sku="APP-0001-BLK-M",
                    qty=3,
                    unit_price=Money("499.00", "INR"),
                    tax=Money("179.64", "INR"),
                    category="APP",
                    cancelled_qty=0,
                ),
            ],
            shipping=Money("50.00", "INR"),
            placed_at=datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
            status=OrderStatus.PENDING_PAYMENT,
            history=[
                (
                    OrderStatus.PENDING_PAYMENT,
                    datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
                )
            ],
            paid=None,
            refunds=[],
        ),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            "O1",
            "U1",
            "IN-KA",
            [
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
                OrderLine(
                    sku="APP-0001-BLK-M",
                    qty=3,
                    unit_price=Money("499.00", "INR"),
                    tax=Money("179.64", "INR"),
                    category="APP",
                    cancelled_qty=0,
                ),
            ],
            Money("50.00", "INR"),
            datetime.datetime(2026, 11, 9, 17, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        Order(
            order_id="O1",
            customer_id="U1",
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
                OrderLine(
                    sku="APP-0001-BLK-M",
                    qty=3,
                    unit_price=Money("499.00", "INR"),
                    tax=Money("179.64", "INR"),
                    category="APP",
                    cancelled_qty=0,
                ),
            ],
            shipping=Money("50.00", "INR"),
            placed_at=datetime.datetime(2026, 11, 9, 17, 0, tzinfo=datetime.timezone.utc),
            status=OrderStatus.PENDING_PAYMENT,
            history=[
                (
                    OrderStatus.PENDING_PAYMENT,
                    datetime.datetime(2026, 11, 9, 17, 0, tzinfo=datetime.timezone.utc),
                )
            ],
            paid=None,
            refunds=[],
        ),
        None,
        id="case-6",
    ),
    pytest.param(
        (
            "O1",
            "U1",
            "IN-KA",
            [
                OrderLine(
                    sku="X-1",
                    qty=2,
                    unit_price=Money("5.00", "INR"),
                    tax=Money("-0.01", "INR"),
                    category="",
                    cancelled_qty=0,
                )
            ],
            Money("50.00", "INR"),
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        Order(
            order_id="O1",
            customer_id="U1",
            currency="INR",
            region="IN-KA",
            lines=[
                OrderLine(
                    sku="X-1",
                    qty=2,
                    unit_price=Money("5.00", "INR"),
                    tax=Money("-0.01", "INR"),
                    category="",
                    cancelled_qty=0,
                )
            ],
            shipping=Money("50.00", "INR"),
            placed_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            status=OrderStatus.PENDING_PAYMENT,
            history=[
                (
                    OrderStatus.PENDING_PAYMENT,
                    datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                )
            ],
            paid=None,
            refunds=[],
        ),
        None,
        id="case-7",
    ),
    pytest.param(
        (
            "O9",
            "U9",
            "IN-KA",
            [],
            Money("50.00", "INR"),
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        OrderError,
        None,
        id="case-8",
    ),
    pytest.param(
        (
            "O9",
            "U9",
            "IN-KA",
            [
                OrderLine(
                    sku="ELC-0101",
                    qty=0,
                    unit_price=Money("10.00", "INR"),
                    tax=Money("0.00", "INR"),
                    category="",
                    cancelled_qty=0,
                )
            ],
            Money("100.00", "INR"),
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        OrderError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0549(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            create_order(*args, **kwargs)
    else:
        assert create_order(*args, **kwargs) == expected
    if after is not None:
        assert args == after
