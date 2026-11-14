"""Issue 0043. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.cart.cart import Cart, CartLine
from shopcore.cart.maintenance import reprice_cart
from shopcore.money.core import Money

CASES = [
    pytest.param(
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
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
            {"ELC-0101": Money("2799.00", "INR"), "BKS-0301": Money("699.00", "INR")},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        ["ELC-0101"],
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2799.00", "INR"),
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
            {"ELC-0101": Money("2799.00", "INR"), "BKS-0301": Money("699.00", "INR")},
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
            {"ELC-0101": Money("2799.00", "INR"), "BKS-0301": Money("699.00", "INR")},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        ["ELC-0101"],
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2799.00", "INR"),
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
            {"ELC-0101": Money("2799.00", "INR"), "BKS-0301": Money("699.00", "INR")},
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
            {"ELC-0101": Money("2799.00", "INR"), "BKS-0301": Money("699.00", "INR")},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        ["ELC-0101"],
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                customer_id="U1",
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2799.00", "INR"),
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
            {"ELC-0101": Money("2799.00", "INR"), "BKS-0301": Money("699.00", "INR")},
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
            {"BKS-0301": Money("698.99", "INR")},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        ["BKS-0301"],
        (
            Cart(
                cart_id="C1",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
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
                        unit_price=Money("698.99", "INR"),
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
            {"BKS-0301": Money("698.99", "INR")},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
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
                        weight_g=549,
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
            {"TOY-0501": Money("1.00", "INR")},
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        [],
        None,
        id="case-5",
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
            {"TOY-0501": Money("1.00", "INR")},
            datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        [],
        None,
        id="case-6",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0043(args, kwargs, expected, after):
    assert reprice_cart(*args, **kwargs) == expected
    if after is not None:
        assert args == after
