"""Issue 0015. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.cart.cart import Cart, new_cart

CASES = [
    pytest.param(
        ("C9", "inr", datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc)),
        {},
        Cart(
            cart_id="C9",
            currency="INR",
            updated_at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[],
            coupon_code=None,
        ),
        None,
        id="case-1",
    ),
    pytest.param(
        ("C9", "inr", datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc)),
        {},
        Cart(
            cart_id="C9",
            currency="INR",
            updated_at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[],
            coupon_code=None,
        ),
        None,
        id="case-2",
    ),
    pytest.param(
        ("C9", "inr", datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc)),
        {},
        Cart(
            cart_id="C9",
            currency="INR",
            updated_at=datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[],
            coupon_code=None,
        ),
        None,
        id="case-3",
    ),
    pytest.param(
        ("C9", "inr", datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc)),
        {},
        Cart(
            cart_id="C9",
            currency="INR",
            updated_at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[],
            coupon_code=None,
        ),
        None,
        id="case-4",
    ),
    pytest.param(
        ("C9", "inr", datetime.datetime(2026, 11, 8, 10, 0, tzinfo=datetime.timezone.utc)),
        {},
        Cart(
            cart_id="C9",
            currency="INR",
            updated_at=datetime.datetime(2026, 11, 8, 10, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[],
            coupon_code=None,
        ),
        None,
        id="case-5",
    ),
    pytest.param(
        ("C", "USD", datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc)),
        {},
        Cart(
            cart_id="C",
            currency="USD",
            updated_at=datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[],
            coupon_code=None,
        ),
        None,
        id="case-6",
    ),
    pytest.param(
        ("U", "INR", datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc)),
        {},
        Cart(
            cart_id="U",
            currency="INR",
            updated_at=datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[],
            coupon_code=None,
        ),
        None,
        id="case-7",
    ),
    pytest.param(
        ("U", "INR", datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc)),
        {},
        Cart(
            cart_id="U",
            currency="INR",
            updated_at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            customer_id=None,
            lines=[],
            coupon_code=None,
        ),
        None,
        id="case-8",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0015(args, kwargs, expected, after):
    assert new_cart(*args, **kwargs) == expected
    if after is not None:
        assert args == after
