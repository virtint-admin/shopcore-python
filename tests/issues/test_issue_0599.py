"""Issue 0599. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.errors import OrderError
from shopcore.money.core import Money
from shopcore.orders.model import Order, OrderLine, OrderStatus, Refund
from shopcore.orders.refunds import refund_order

CASES = [
    pytest.param(
        (
            Order(
                order_id="O1",
                customer_id="U1",
                currency="INR",
                region="IN-KA",
                lines=[
                    OrderLine(
                        sku="ELC-0101",
                        qty=0,
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
                status=OrderStatus.PAID,
                history=[
                    (
                        OrderStatus.PENDING_PAYMENT,
                        datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PAID,
                        datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                    ),
                ],
                paid=Money("6663.46", "INR"),
                refunds=[],
            ),
            datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        Refund(
            refund_id="O1-R1",
            amount=Money("6663.46", "INR"),
            at=datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
            reason="order_refunded",
        ),
        (
            Order(
                order_id="O1",
                customer_id="U1",
                currency="INR",
                region="IN-KA",
                lines=[
                    OrderLine(
                        sku="ELC-0101",
                        qty=0,
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
                status=OrderStatus.REFUNDED,
                history=[
                    (
                        OrderStatus.PENDING_PAYMENT,
                        datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PAID,
                        datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.REFUNDED,
                        datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                    ),
                ],
                paid=Money("6663.46", "INR"),
                refunds=[
                    Refund(
                        refund_id="O1-R1",
                        amount=Money("6663.46", "INR"),
                        at=datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                        reason="order_refunded",
                    )
                ],
            ),
            datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
        ),
        id="case-1",
    ),
    pytest.param(
        (
            Order(
                order_id="O1",
                customer_id="U1",
                currency="INR",
                region="IN-KA",
                lines=[
                    OrderLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.01", "INR"),
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
                status=OrderStatus.PAID,
                history=[
                    (
                        OrderStatus.PENDING_PAYMENT,
                        datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PAID,
                        datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                    ),
                ],
                paid=Money("6663.46", "INR"),
                refunds=[],
            ),
            datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        Refund(
            refund_id="O1-R1",
            amount=Money("6663.46", "INR"),
            at=datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
            reason="order_refunded",
        ),
        (
            Order(
                order_id="O1",
                customer_id="U1",
                currency="INR",
                region="IN-KA",
                lines=[
                    OrderLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.01", "INR"),
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
                status=OrderStatus.REFUNDED,
                history=[
                    (
                        OrderStatus.PENDING_PAYMENT,
                        datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PAID,
                        datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.REFUNDED,
                        datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                    ),
                ],
                paid=Money("6663.46", "INR"),
                refunds=[
                    Refund(
                        refund_id="O1-R1",
                        amount=Money("6663.46", "INR"),
                        at=datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                        reason="order_refunded",
                    )
                ],
            ),
            datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
        ),
        id="case-2",
    ),
    pytest.param(
        (
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
                placed_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                status=OrderStatus.RETURNED,
                history=[
                    (
                        OrderStatus.PENDING_PAYMENT,
                        datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PAID,
                        datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PACKED,
                        datetime.datetime(2026, 11, 8, 12, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.SHIPPED,
                        datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.DELIVERED,
                        datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.RETURNED,
                        datetime.datetime(2026, 11, 9, 15, 0, tzinfo=datetime.timezone.utc),
                    ),
                ],
                paid=Money("6663.46", "INR"),
                refunds=[
                    Refund(
                        refund_id="O1-R1",
                        amount=Money("663.46", "INR"),
                        at=datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                        reason="goodwill",
                    )
                ],
            ),
            datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
            "returned",
        ),
        {},
        Refund(
            refund_id="O1-R2",
            amount=Money("6000.00", "INR"),
            at=datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
            reason="returned",
        ),
        (
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
                placed_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                status=OrderStatus.REFUNDED,
                history=[
                    (
                        OrderStatus.PENDING_PAYMENT,
                        datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PAID,
                        datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PACKED,
                        datetime.datetime(2026, 11, 8, 12, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.SHIPPED,
                        datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.DELIVERED,
                        datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.RETURNED,
                        datetime.datetime(2026, 11, 9, 15, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.REFUNDED,
                        datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
                    ),
                ],
                paid=Money("6663.46", "INR"),
                refunds=[
                    Refund(
                        refund_id="O1-R1",
                        amount=Money("663.46", "INR"),
                        at=datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                        reason="goodwill",
                    ),
                    Refund(
                        refund_id="O1-R2",
                        amount=Money("6000.00", "INR"),
                        at=datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
                        reason="returned",
                    ),
                ],
            ),
            datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
            "returned",
        ),
        id="case-3",
    ),
    pytest.param(
        (
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
                        tax=Money("-0.01", "INR"),
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
                status=OrderStatus.RETURNED,
                history=[
                    (
                        OrderStatus.PENDING_PAYMENT,
                        datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PAID,
                        datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PACKED,
                        datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.SHIPPED,
                        datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.DELIVERED,
                        datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.RETURNED,
                        datetime.datetime(2026, 11, 9, 15, 0, tzinfo=datetime.timezone.utc),
                    ),
                ],
                paid=Money("6663.46", "INR"),
                refunds=[
                    Refund(
                        refund_id="O1-R1",
                        amount=Money("663.46", "INR"),
                        at=datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                        reason="goodwill",
                    )
                ],
            ),
            datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
            "returned",
        ),
        {},
        Refund(
            refund_id="O1-R2",
            amount=Money("6000.00", "INR"),
            at=datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
            reason="returned",
        ),
        (
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
                        tax=Money("-0.01", "INR"),
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
                status=OrderStatus.REFUNDED,
                history=[
                    (
                        OrderStatus.PENDING_PAYMENT,
                        datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PAID,
                        datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PACKED,
                        datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.SHIPPED,
                        datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.DELIVERED,
                        datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.RETURNED,
                        datetime.datetime(2026, 11, 9, 15, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.REFUNDED,
                        datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
                    ),
                ],
                paid=Money("6663.46", "INR"),
                refunds=[
                    Refund(
                        refund_id="O1-R1",
                        amount=Money("663.46", "INR"),
                        at=datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                        reason="goodwill",
                    ),
                    Refund(
                        refund_id="O1-R2",
                        amount=Money("6000.00", "INR"),
                        at=datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
                        reason="returned",
                    ),
                ],
            ),
            datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
            "returned",
        ),
        id="case-4",
    ),
    pytest.param(
        (
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
                placed_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                status=OrderStatus.RETURNED,
                history=[
                    (
                        OrderStatus.PENDING_PAYMENT,
                        datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PAID,
                        datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PACKED,
                        datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.SHIPPED,
                        datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.DELIVERED,
                        datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.RETURNED,
                        datetime.datetime(2026, 11, 9, 15, 0, tzinfo=datetime.timezone.utc),
                    ),
                ],
                paid=Money("6663.46", "INR"),
                refunds=[
                    Refund(
                        refund_id="O1-R1",
                        amount=Money("663.46", "INR"),
                        at=datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                        reason="goodwill",
                    )
                ],
            ),
            datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
            "returned",
        ),
        {},
        Refund(
            refund_id="O1-R2",
            amount=Money("6000.00", "INR"),
            at=datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
            reason="returned",
        ),
        (
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
                placed_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                status=OrderStatus.REFUNDED,
                history=[
                    (
                        OrderStatus.PENDING_PAYMENT,
                        datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PAID,
                        datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PACKED,
                        datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.SHIPPED,
                        datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.DELIVERED,
                        datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.RETURNED,
                        datetime.datetime(2026, 11, 9, 15, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.REFUNDED,
                        datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
                    ),
                ],
                paid=Money("6663.46", "INR"),
                refunds=[
                    Refund(
                        refund_id="O1-R1",
                        amount=Money("663.46", "INR"),
                        at=datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                        reason="goodwill",
                    ),
                    Refund(
                        refund_id="O1-R2",
                        amount=Money("6000.00", "INR"),
                        at=datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
                        reason="returned",
                    ),
                ],
            ),
            datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
            "returned",
        ),
        id="case-5",
    ),
    pytest.param(
        (
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
                placed_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                status=OrderStatus.RETURNED,
                history=[
                    (
                        OrderStatus.PENDING_PAYMENT,
                        datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PAID,
                        datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PACKED,
                        datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.SHIPPED,
                        datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.DELIVERED,
                        datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.RETURNED,
                        datetime.datetime(2026, 11, 9, 15, 0, tzinfo=datetime.timezone.utc),
                    ),
                ],
                paid=Money("6663.46", "INR"),
                refunds=[
                    Refund(
                        refund_id="O1-R1",
                        amount=Money("663.46", "INR"),
                        at=datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                        reason="goodwill",
                    )
                ],
            ),
            datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
            "returned",
        ),
        {},
        Refund(
            refund_id="O1-R2",
            amount=Money("6000.00", "INR"),
            at=datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
            reason="returned",
        ),
        (
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
                placed_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                status=OrderStatus.REFUNDED,
                history=[
                    (
                        OrderStatus.PENDING_PAYMENT,
                        datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PAID,
                        datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PACKED,
                        datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.SHIPPED,
                        datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.DELIVERED,
                        datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.RETURNED,
                        datetime.datetime(2026, 11, 9, 15, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.REFUNDED,
                        datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
                    ),
                ],
                paid=Money("6663.46", "INR"),
                refunds=[
                    Refund(
                        refund_id="O1-R1",
                        amount=Money("663.46", "INR"),
                        at=datetime.datetime(2026, 11, 9, 14, 0, tzinfo=datetime.timezone.utc),
                        reason="goodwill",
                    ),
                    Refund(
                        refund_id="O1-R2",
                        amount=Money("6000.00", "INR"),
                        at=datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
                        reason="returned",
                    ),
                ],
            ),
            datetime.datetime(2026, 11, 9, 16, 0, tzinfo=datetime.timezone.utc),
            "returned",
        ),
        id="case-6",
    ),
    pytest.param(
        (
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
                placed_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                status=OrderStatus.SHIPPED,
                history=[
                    (
                        OrderStatus.PENDING_PAYMENT,
                        datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PAID,
                        datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PACKED,
                        datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.SHIPPED,
                        datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                    ),
                ],
                paid=Money("6663.46", "INR"),
                refunds=[],
            ),
            datetime.datetime(2026, 11, 9, 19, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        OrderError,
        None,
        id="case-7",
    ),
    pytest.param(
        (
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
                placed_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                status=OrderStatus.SHIPPED,
                history=[
                    (
                        OrderStatus.PENDING_PAYMENT,
                        datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PAID,
                        datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PACKED,
                        datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                    ),
                ],
                paid=Money("6663.46", "INR"),
                refunds=[],
            ),
            datetime.datetime(2026, 11, 9, 19, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        OrderError,
        None,
        id="case-8",
    ),
    pytest.param(
        (
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
                placed_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                status=OrderStatus.SHIPPED,
                history=[
                    (
                        OrderStatus.PENDING_PAYMENT,
                        datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PAID,
                        datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.PACKED,
                        datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                    ),
                    (
                        OrderStatus.SHIPPED,
                        datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                    ),
                ],
                paid=Money("6663.46", "INR"),
                refunds=[],
            ),
            datetime.datetime(2026, 11, 9, 19, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        OrderError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0599(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            refund_order(*args, **kwargs)
    else:
        assert refund_order(*args, **kwargs) == expected
    if after is not None:
        assert args == after
