"""Issue 0049. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.cart.cart import Cart, CartLine
from shopcore.cart.maintenance import sync_with_stock
from shopcore.money.core import Money

CASES = [
    pytest.param(
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=120,
                    ),
                    CartLine(
                        sku="BKS-0301",
                        qty=2,
                        unit_price=Money("699.00", "INR"),
                        category="BKS",
                        weight_g=550,
                    ),
                    CartLine(
                        sku="GRC-0401",
                        qty=2,
                        unit_price=Money("325.00", "INR"),
                        category="GRC",
                        weight_g=520,
                    ),
                ],
                coupon_code=None,
            ),
            {"ELC-0101": 0, "BKS-0301": 1, "GRC-0401": 9},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        {"ELC-0101": 0, "BKS-0301": 1},
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="BKS-0301",
                        qty=1,
                        unit_price=Money("699.00", "INR"),
                        category="BKS",
                        weight_g=550,
                    ),
                    CartLine(
                        sku="GRC-0401",
                        qty=2,
                        unit_price=Money("325.00", "INR"),
                        category="GRC",
                        weight_g=520,
                    ),
                ],
                coupon_code=None,
            ),
            {"ELC-0101": 0, "BKS-0301": 1, "GRC-0401": 9},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        id="case-1",
    ),
    pytest.param(
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=121,
                    ),
                    CartLine(
                        sku="BKS-0301",
                        qty=2,
                        unit_price=Money("699.00", "INR"),
                        category="BKS",
                        weight_g=550,
                    ),
                    CartLine(
                        sku="GRC-0401",
                        qty=1,
                        unit_price=Money("325.00", "INR"),
                        category="GRC",
                        weight_g=520,
                    ),
                ],
                coupon_code=None,
            ),
            {"ELC-0101": 0, "BKS-0301": 1, "GRC-0401": 9},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        {"ELC-0101": 0, "BKS-0301": 1},
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="BKS-0301",
                        qty=1,
                        unit_price=Money("699.00", "INR"),
                        category="BKS",
                        weight_g=550,
                    ),
                    CartLine(
                        sku="GRC-0401",
                        qty=1,
                        unit_price=Money("325.00", "INR"),
                        category="GRC",
                        weight_g=520,
                    ),
                ],
                coupon_code=None,
            ),
            {"ELC-0101": 0, "BKS-0301": 1, "GRC-0401": 9},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        id="case-2",
    ),
    pytest.param(
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=120,
                    ),
                    CartLine(
                        sku="BKS-0301",
                        qty=2,
                        unit_price=Money("699.00", "INR"),
                        category="BKS",
                        weight_g=550,
                    ),
                    CartLine(
                        sku="GRC-0401",
                        qty=1,
                        unit_price=Money("325.00", "INR"),
                        category="GRC",
                        weight_g=0,
                    ),
                ],
                coupon_code=None,
            ),
            {"ELC-0101": 0, "BKS-0301": 1, "GRC-0401": 9},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        {"ELC-0101": 0, "BKS-0301": 1},
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="BKS-0301",
                        qty=1,
                        unit_price=Money("699.00", "INR"),
                        category="BKS",
                        weight_g=550,
                    ),
                    CartLine(
                        sku="GRC-0401",
                        qty=1,
                        unit_price=Money("325.00", "INR"),
                        category="GRC",
                        weight_g=0,
                    ),
                ],
                coupon_code=None,
            ),
            {"ELC-0101": 0, "BKS-0301": 1, "GRC-0401": 9},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        id="case-3",
    ),
    pytest.param(
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=120,
                    ),
                    CartLine(
                        sku="BKS-0301",
                        qty=2,
                        unit_price=Money("699.00", "INR"),
                        category="BKS",
                        weight_g=550,
                    ),
                    CartLine(
                        sku="GRC-0401",
                        qty=1,
                        unit_price=Money("325.00", "INR"),
                        category="GRC",
                        weight_g=520,
                    ),
                ],
                coupon_code=None,
            ),
            {},
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        {"ELC-0101": 0, "BKS-0301": 0, "GRC-0401": 0},
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[],
                coupon_code=None,
            ),
            {},
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
        ),
        id="case-4",
    ),
    pytest.param(
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=0,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=120,
                    ),
                    CartLine(
                        sku="BKS-0301",
                        qty=2,
                        unit_price=Money("699.00", "INR"),
                        category="BKS",
                        weight_g=550,
                    ),
                    CartLine(
                        sku="GRC-0401",
                        qty=1,
                        unit_price=Money("325.00", "INR"),
                        category="GRC",
                        weight_g=520,
                    ),
                ],
                coupon_code=None,
            ),
            {},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        {"BKS-0301": 0, "GRC-0401": 0},
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=0,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=120,
                    )
                ],
                coupon_code=None,
            ),
            {},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        id="case-5",
    ),
    pytest.param(
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 8, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=120,
                    ),
                    CartLine(
                        sku="BKS-0301",
                        qty=2,
                        unit_price=Money("699.00", "INR"),
                        category="BKS",
                        weight_g=550,
                    ),
                    CartLine(
                        sku="GRC-0401",
                        qty=1,
                        unit_price=Money("325.00", "INR"),
                        category="GRC",
                        weight_g=520,
                    ),
                ],
                coupon_code=None,
            ),
            {},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        {"ELC-0101": 0, "BKS-0301": 0, "GRC-0401": 0},
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[],
                coupon_code=None,
            ),
            {},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        id="case-6",
    ),
    pytest.param(
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=120,
                    ),
                    CartLine(
                        sku="BKS-0301",
                        qty=2,
                        unit_price=Money("699.00", "INR"),
                        category="BKS",
                        weight_g=550,
                    ),
                ],
                coupon_code=None,
            ),
            {"ELC-0101": 5, "BKS-0301": 2, "GRC-0401": 1},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        {},
        None,
        id="case-7",
    ),
    pytest.param(
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=120,
                    ),
                    CartLine(
                        sku="BKS-0301",
                        qty=2,
                        unit_price=Money("699.00", "INR"),
                        category="BKS",
                        weight_g=550,
                    ),
                    CartLine(
                        sku="GRC-0401",
                        qty=1,
                        unit_price=Money("325.00", "INR"),
                        category="GRC",
                        weight_g=520,
                    ),
                ],
                coupon_code=None,
            ),
            {"ELC-0101": 5, "BKS-0301": 2, "GRC-0401": 2},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        {},
        None,
        id="case-8",
    ),
    pytest.param(
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=120,
                    ),
                    CartLine(
                        sku="BKS-0301",
                        qty=2,
                        unit_price=Money("699.00", "INR"),
                        category="BKS",
                        weight_g=550,
                    ),
                    CartLine(
                        sku="GRC-0401",
                        qty=1,
                        unit_price=Money("325.00", "INR"),
                        category="GRC",
                        weight_g=520,
                    ),
                ],
                coupon_code=None,
            ),
            {"ELC-0101": 5, "BKS-0301": 2, "GRC-0401": 1},
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        {},
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0049(args, kwargs, expected, after):
    assert sync_with_stock(*args, **kwargs) == expected
    if after is not None:
        assert args == after
