"""Issue 0067. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.cart.cart import Cart, CartLine
from shopcore.cart.totals import most_expensive_line
from shopcore.money.core import Money

CASES = [
    pytest.param(
        (
            Cart(
                cart_id="C",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="A", qty=1, unit_price=Money("10.00", "INR"), category="ELC", weight_g=1
                    ),
                    CartLine(
                        sku="B", qty=2, unit_price=Money("5.00", "INR"), category="ELC", weight_g=1
                    ),
                ],
                coupon_code=None,
            ),
        ),
        {},
        CartLine(sku="A", qty=1, unit_price=Money("10.00", "INR"), category="ELC", weight_g=1),
        None,
        id="case-1",
    ),
    pytest.param(
        (
            Cart(
                cart_id="C",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="A", qty=1, unit_price=Money("10.00", "INR"), category="ELC", weight_g=1
                    ),
                    CartLine(
                        sku="B", qty=2, unit_price=Money("5.00", "INR"), category="ELC", weight_g=1
                    ),
                ],
                coupon_code=None,
            ),
        ),
        {},
        CartLine(sku="A", qty=1, unit_price=Money("10.00", "INR"), category="ELC", weight_g=1),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Cart(
                cart_id="C",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="A", qty=1, unit_price=Money("10.00", "INR"), category="ELC", weight_g=1
                    ),
                    CartLine(
                        sku="B", qty=2, unit_price=Money("5.00", "INR"), category="ELC", weight_g=1
                    ),
                ],
                coupon_code=None,
            ),
        ),
        {},
        CartLine(sku="A", qty=1, unit_price=Money("10.00", "INR"), category="ELC", weight_g=1),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            Cart(
                cart_id="C",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="A", qty=1, unit_price=Money("10.00", "INR"), category="ELC", weight_g=2
                    ),
                    CartLine(
                        sku="B", qty=2, unit_price=Money("5.00", "INR"), category="ELC", weight_g=1
                    ),
                ],
                coupon_code=None,
            ),
        ),
        {},
        CartLine(sku="A", qty=1, unit_price=Money("10.00", "INR"), category="ELC", weight_g=2),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            Cart(
                cart_id="C",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="A", qty=1, unit_price=Money("10.00", "INR"), category="ELC", weight_g=1
                    ),
                    CartLine(
                        sku="B", qty=2, unit_price=Money("5.00", "INR"), category="ELC", weight_g=0
                    ),
                ],
                coupon_code=None,
            ),
        ),
        {},
        CartLine(sku="A", qty=1, unit_price=Money("10.00", "INR"), category="ELC", weight_g=1),
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
        ),
        {},
        CartLine(
            sku="ELC-0101", qty=1, unit_price=Money("2999.00", "INR"), category="ELC", weight_g=121
        ),
        None,
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
                        unit_price=Money("5998.00", "INR"),
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
        ),
        {},
        CartLine(
            sku="ELC-0101", qty=1, unit_price=Money("5998.00", "INR"), category="ELC", weight_g=120
        ),
        None,
        id="case-7",
    ),
    pytest.param(
        (
            Cart(
                cart_id="C",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[],
                coupon_code=None,
            ),
        ),
        {},
        None,
        None,
        id="case-8",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0067(args, kwargs, expected, after):
    assert most_expensive_line(*args, **kwargs) == expected
    if after is not None:
        assert args == after
