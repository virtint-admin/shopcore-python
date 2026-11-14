"""Issue 0061. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.cart.cart import Cart, CartLine
from shopcore.cart.merge import diff_carts
from shopcore.money.core import Money

CASES = [
    pytest.param(
        (
            Cart(
                cart_id="A",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("1.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    ),
                    CartLine(
                        sku="TOY-0501",
                        qty=0,
                        unit_price=Money("1.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                ],
                coupon_code=None,
            ),
            Cart(
                cart_id="A",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=3,
                        unit_price=Money("1.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    ),
                    CartLine(
                        sku="HOM-0201",
                        qty=1,
                        unit_price=Money("1.00", "INR"),
                        category="HOM",
                        weight_g=100,
                    ),
                ],
                coupon_code=None,
            ),
        ),
        {},
        {"ELC-0101": 2, "HOM-0201": 1},
        None,
        id="case-1",
    ),
    pytest.param(
        (
            Cart(
                cart_id="A",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("1.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    ),
                    CartLine(
                        sku="TOY-0501",
                        qty=2,
                        unit_price=Money("1.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                ],
                coupon_code=None,
            ),
            Cart(
                cart_id="A",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=3,
                        unit_price=Money("1.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    ),
                    CartLine(
                        sku="HOM-0201",
                        qty=0,
                        unit_price=Money("1.00", "INR"),
                        category="HOM",
                        weight_g=100,
                    ),
                ],
                coupon_code=None,
            ),
        ),
        {},
        {"ELC-0101": 2, "TOY-0501": -2},
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Cart(
                cart_id="A",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("1.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    ),
                    CartLine(
                        sku="TOY-0501",
                        qty=2,
                        unit_price=Money("1.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                ],
                coupon_code=None,
            ),
            Cart(
                cart_id="A",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=3,
                        unit_price=Money("1.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    ),
                    CartLine(
                        sku="HOM-0201",
                        qty=1,
                        unit_price=Money("1.00", "INR"),
                        category="HOM",
                        weight_g=0,
                    ),
                ],
                coupon_code=None,
            ),
        ),
        {},
        {"ELC-0101": 2, "HOM-0201": 1, "TOY-0501": -2},
        None,
        id="case-3",
    ),
    pytest.param(
        (
            Cart(
                cart_id="A",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("1.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    ),
                    CartLine(
                        sku="TOY-0501",
                        qty=2,
                        unit_price=Money("1.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                ],
                coupon_code=None,
            ),
            Cart(
                cart_id="A",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=3,
                        unit_price=Money("1.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    ),
                    CartLine(
                        sku="HOM-0201",
                        qty=1,
                        unit_price=Money("1.00", "INR"),
                        category="HOM",
                        weight_g=100,
                    ),
                ],
                coupon_code=None,
            ),
        ),
        {},
        {"ELC-0101": 2, "HOM-0201": 1, "TOY-0501": -2},
        None,
        id="case-4",
    ),
    pytest.param(
        (
            Cart(
                cart_id="A",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("1.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    ),
                    CartLine(
                        sku="TOY-0501",
                        qty=2,
                        unit_price=Money("1.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                ],
                coupon_code=None,
            ),
            Cart(
                cart_id="A",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=3,
                        unit_price=Money("1.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    ),
                    CartLine(
                        sku="HOM-0201",
                        qty=1,
                        unit_price=Money("1.00", "INR"),
                        category="HOM",
                        weight_g=100,
                    ),
                ],
                coupon_code=None,
            ),
        ),
        {},
        {"ELC-0101": 2, "HOM-0201": 1, "TOY-0501": -2},
        None,
        id="case-5",
    ),
    pytest.param(
        (
            Cart(
                cart_id="A",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[],
                coupon_code=None,
            ),
            Cart(
                cart_id="A",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="BKS-0301",
                        qty=4,
                        unit_price=Money("1.00", "INR"),
                        category="BKS",
                        weight_g=100,
                    )
                ],
                coupon_code=None,
            ),
        ),
        {},
        {"BKS-0301": 4},
        None,
        id="case-6",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0061(args, kwargs, expected, after):
    assert diff_carts(*args, **kwargs) == expected
    if after is not None:
        assert args == after
