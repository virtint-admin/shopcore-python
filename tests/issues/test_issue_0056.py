"""Issue 0056. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.cart.cart import Cart, CartLimits, CartLine
from shopcore.cart.merge import merge_carts
from shopcore.errors import CartError
from shopcore.money.core import Money

CASES = [
    pytest.param(
        (
            Cart(
                cart_id="G",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="TOY-0501",
                        qty=1,
                        unit_price=Money("799.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                    CartLine(
                        sku="TOY-0502",
                        qty=1,
                        unit_price=Money("1999.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                ],
                coupon_code=None,
            ),
            Cart(
                cart_id="U",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    )
                ],
                coupon_code=None,
            ),
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            CartLimits(max_lines=2, max_qty_per_line=10, max_total_qty=100),
        ),
        {},
        Cart(
            cart_id="U",
            currency="INR",
            updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[
                CartLine(
                    sku="ELC-0101",
                    qty=1,
                    unit_price=Money("2999.00", "INR"),
                    category="ELC",
                    weight_g=100,
                ),
                CartLine(
                    sku="TOY-0501",
                    qty=1,
                    unit_price=Money("799.00", "INR"),
                    category="TOY",
                    weight_g=100,
                ),
            ],
            coupon_code=None,
        ),
        None,
        id="case-1",
    ),
    pytest.param(
        (
            Cart(
                cart_id="G",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="TOY-0501",
                        qty=1,
                        unit_price=Money("799.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                    CartLine(
                        sku="TOY-0502",
                        qty=1,
                        unit_price=Money("1999.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                ],
                coupon_code=None,
            ),
            Cart(
                cart_id="U",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    )
                ],
                coupon_code=None,
            ),
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            CartLimits(max_lines=2, max_qty_per_line=10, max_total_qty=0),
        ),
        {},
        Cart(
            cart_id="U",
            currency="INR",
            updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[
                CartLine(
                    sku="ELC-0101",
                    qty=1,
                    unit_price=Money("2999.00", "INR"),
                    category="ELC",
                    weight_g=100,
                ),
                CartLine(
                    sku="TOY-0501",
                    qty=1,
                    unit_price=Money("799.00", "INR"),
                    category="TOY",
                    weight_g=100,
                ),
            ],
            coupon_code=None,
        ),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Cart(
                cart_id="G",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="TOY-0501",
                        qty=1,
                        unit_price=Money("799.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                    CartLine(
                        sku="TOY-0502",
                        qty=1,
                        unit_price=Money("1999.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                ],
                coupon_code=None,
            ),
            Cart(
                cart_id="U",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=101,
                    )
                ],
                coupon_code=None,
            ),
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            CartLimits(max_lines=2, max_qty_per_line=10, max_total_qty=100),
        ),
        {},
        Cart(
            cart_id="U",
            currency="INR",
            updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[
                CartLine(
                    sku="ELC-0101",
                    qty=1,
                    unit_price=Money("2999.00", "INR"),
                    category="ELC",
                    weight_g=101,
                ),
                CartLine(
                    sku="TOY-0501",
                    qty=1,
                    unit_price=Money("799.00", "INR"),
                    category="TOY",
                    weight_g=100,
                ),
            ],
            coupon_code=None,
        ),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            Cart(
                cart_id="G",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="TOY-0501",
                        qty=1,
                        unit_price=Money("799.00", "INR"),
                        category="TOY",
                        weight_g=101,
                    ),
                    CartLine(
                        sku="TOY-0502",
                        qty=1,
                        unit_price=Money("1999.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                ],
                coupon_code=None,
            ),
            Cart(
                cart_id="U",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    )
                ],
                coupon_code=None,
            ),
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            CartLimits(max_lines=2, max_qty_per_line=10, max_total_qty=100),
        ),
        {},
        Cart(
            cart_id="U",
            currency="INR",
            updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[
                CartLine(
                    sku="ELC-0101",
                    qty=1,
                    unit_price=Money("2999.00", "INR"),
                    category="ELC",
                    weight_g=100,
                ),
                CartLine(
                    sku="TOY-0501",
                    qty=1,
                    unit_price=Money("799.00", "INR"),
                    category="TOY",
                    weight_g=101,
                ),
            ],
            coupon_code=None,
        ),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            Cart(
                cart_id="G",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="TOY-0501",
                        qty=1,
                        unit_price=Money("799.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                    CartLine(
                        sku="TOY-0502",
                        qty=1,
                        unit_price=Money("1999.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                ],
                coupon_code=None,
            ),
            Cart(
                cart_id="U",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    )
                ],
                coupon_code=None,
            ),
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            CartLimits(max_lines=2, max_qty_per_line=10, max_total_qty=100),
        ),
        {},
        Cart(
            cart_id="U",
            currency="INR",
            updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[
                CartLine(
                    sku="ELC-0101",
                    qty=1,
                    unit_price=Money("2999.00", "INR"),
                    category="ELC",
                    weight_g=100,
                ),
                CartLine(
                    sku="TOY-0501",
                    qty=1,
                    unit_price=Money("799.00", "INR"),
                    category="TOY",
                    weight_g=100,
                ),
            ],
            coupon_code=None,
        ),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            Cart(
                cart_id="G",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="TOY-0501",
                        qty=1,
                        unit_price=Money("799.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                    CartLine(
                        sku="TOY-0502",
                        qty=1,
                        unit_price=Money("1999.00", "INR"),
                        category="TOY",
                        weight_g=100,
                    ),
                ],
                coupon_code=None,
            ),
            Cart(
                cart_id="U",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=1,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=0,
                    )
                ],
                coupon_code=None,
            ),
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            CartLimits(max_lines=2, max_qty_per_line=10, max_total_qty=100),
        ),
        {},
        Cart(
            cart_id="U",
            currency="INR",
            updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[
                CartLine(
                    sku="ELC-0101",
                    qty=1,
                    unit_price=Money("2999.00", "INR"),
                    category="ELC",
                    weight_g=0,
                ),
                CartLine(
                    sku="TOY-0501",
                    qty=1,
                    unit_price=Money("799.00", "INR"),
                    category="TOY",
                    weight_g=100,
                ),
            ],
            coupon_code=None,
        ),
        None,
        id="case-6",
    ),
    pytest.param(
        (
            Cart(
                cart_id="G",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=8,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    )
                ],
                coupon_code=None,
            ),
            Cart(
                cart_id="U",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[
                    CartLine(
                        sku="ELC-0101",
                        qty=5,
                        unit_price=Money("2999.00", "INR"),
                        category="ELC",
                        weight_g=100,
                    )
                ],
                coupon_code=None,
            ),
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        Cart(
            cart_id="U",
            currency="INR",
            updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[
                CartLine(
                    sku="ELC-0101",
                    qty=10,
                    unit_price=Money("2999.00", "INR"),
                    category="ELC",
                    weight_g=100,
                )
            ],
            coupon_code=None,
        ),
        None,
        id="case-7",
    ),
    pytest.param(
        (
            Cart(
                cart_id="G",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[],
                coupon_code="GUEST10",
            ),
            Cart(
                cart_id="U",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[],
                coupon_code=None,
            ),
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        Cart(
            cart_id="U",
            currency="INR",
            updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[],
            coupon_code="GUEST10",
        ),
        None,
        id="case-8",
    ),
    pytest.param(
        (
            Cart(
                cart_id="G",
                currency="USD",
                updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[],
                coupon_code=None,
            ),
            Cart(
                cart_id="U",
                currency="INR",
                updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                customer_id=None,
                lines=[],
                coupon_code=None,
            ),
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        CartError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0056(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            merge_carts(*args, **kwargs)
    else:
        assert merge_carts(*args, **kwargs) == expected
    if after is not None:
        assert args == after
