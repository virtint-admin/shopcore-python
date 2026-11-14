"""Issue 0033. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.cart.cart import Cart, CartLimits, CartLine
from shopcore.cart.maintenance import check_limits
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
                        qty=12,
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
            CartLimits(max_lines=2, max_qty_per_line=10, max_total_qty=10),
        ),
        {},
        ["too many lines (3 > 2)", "BKS-0301: quantity 12 > 10", "total quantity 14 > 10"],
        None,
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
                        weight_g=120,
                    ),
                    CartLine(
                        sku="BKS-0301",
                        qty=12,
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
            CartLimits(max_lines=2, max_qty_per_line=10, max_total_qty=0),
        ),
        {},
        ["too many lines (3 > 2)", "BKS-0301: quantity 12 > 10", "total quantity 14 > 0"],
        None,
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
                        qty=12,
                        unit_price=Money("699.00", "INR"),
                        category="BKS",
                        weight_g=551,
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
            CartLimits(max_lines=2, max_qty_per_line=10, max_total_qty=10),
        ),
        {},
        ["too many lines (3 > 2)", "BKS-0301: quantity 12 > 10", "total quantity 14 > 10"],
        None,
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
                        qty=12,
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
            CartLimits(max_lines=2, max_qty_per_line=10, max_total_qty=10),
        ),
        {},
        ["too many lines (3 > 2)", "BKS-0301: quantity 12 > 10", "total quantity 15 > 10"],
        None,
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
                        qty=11,
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
            CartLimits(max_lines=2, max_qty_per_line=10, max_total_qty=10),
        ),
        {},
        ["too many lines (3 > 2)", "BKS-0301: quantity 11 > 10", "total quantity 13 > 10"],
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
                        weight_g=119,
                    ),
                    CartLine(
                        sku="BKS-0301",
                        qty=12,
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
            CartLimits(max_lines=2, max_qty_per_line=10, max_total_qty=10),
        ),
        {},
        ["too many lines (3 > 2)", "BKS-0301: quantity 12 > 10", "total quantity 14 > 10"],
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
        ),
        {},
        [],
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
                        qty=3,
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
        [],
        None,
        id="case-8",
    ),
    pytest.param(
        (
            Cart(
                cart_id="C",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[],
                coupon_code=None,
            ),
        ),
        {},
        [],
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0033(args, kwargs, expected, after):
    assert check_limits(*args, **kwargs) == expected
    if after is not None:
        assert args == after
