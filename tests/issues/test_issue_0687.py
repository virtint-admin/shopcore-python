"""Issue 0687. Make this test pass by fixing the application code, not the test."""

import datetime
import zoneinfo
from decimal import Decimal

import pytest

from shopcore.errors import PricingError
from shopcore.money.core import Money
from shopcore.pricing.coupons import Coupon, apply_coupon

CASES = [
    pytest.param(
        (
            Coupon(
                code="DIWALI25",
                kind="percent",
                value=Decimal("25"),
                starts_at=datetime.datetime(
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("1000.00", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=-1,
                per_customer_limit=None,
                categories=frozenset(),
            ),
            Money("1200.00", "INR"),
            datetime.datetime(2026, 11, 9, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        Money("300.00", "INR"),
        None,
        id="case-1",
    ),
    pytest.param(
        (
            Coupon(
                code="DIWALI25",
                kind="percent",
                value=Decimal("25"),
                starts_at=datetime.datetime(
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("1000.00", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=0,
                per_customer_limit=None,
                categories=frozenset(),
            ),
            Money("1200.00", "INR"),
            datetime.datetime(2026, 11, 8, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        Money("300.00", "INR"),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Coupon(
                code="DIWALI25",
                kind="percent",
                value=Decimal("25"),
                starts_at=datetime.datetime(
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 14, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("1000.00", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=0,
                per_customer_limit=None,
                categories=frozenset(),
            ),
            Money("1200.00", "INR"),
            datetime.datetime(2026, 11, 9, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        Money("300.00", "INR"),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            Coupon(
                code="DIWALI25",
                kind="percent",
                value=Decimal("25"),
                starts_at=datetime.datetime(
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("1000.00", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=0,
                per_customer_limit=None,
                categories=frozenset(),
            ),
            Money("1200.00", "INR"),
            datetime.datetime(2026, 11, 10, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        Money("300.00", "INR"),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            Coupon(
                code="DIWALI25",
                kind="percent",
                value=Decimal("25"),
                starts_at=datetime.datetime(
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("1000.00", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=0,
                per_customer_limit=None,
                categories=frozenset(),
            ),
            Money("1200.00", "INR"),
            datetime.datetime(2026, 11, 9, 16, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        Money("300.00", "INR"),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            Coupon(
                code="DIWALI25",
                kind="percent",
                value=Decimal("25"),
                starts_at=datetime.datetime(
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("999.99", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=0,
                per_customer_limit=None,
                categories=frozenset(),
            ),
            Money("1200.00", "INR"),
            datetime.datetime(2026, 11, 9, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        Money("300.00", "INR"),
        None,
        id="case-6",
    ),
    pytest.param(
        (
            Coupon(
                code="DIWALI25",
                kind="percent",
                value=Decimal("25"),
                starts_at=datetime.datetime(
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("1000.00", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=0,
                per_customer_limit=None,
                categories=frozenset(),
            ),
            Money("10.00", "INR"),
            datetime.datetime(2026, 11, 9, 16, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        PricingError,
        None,
        id="case-7",
    ),
    pytest.param(
        (
            Coupon(
                code="DIWALI25",
                kind="percent",
                value=Decimal("25"),
                starts_at=datetime.datetime(
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("1000.00", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=0,
                per_customer_limit=None,
                categories=frozenset(),
            ),
            Money("20.00", "INR"),
            datetime.datetime(2026, 11, 9, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        PricingError,
        None,
        id="case-8",
    ),
    pytest.param(
        (
            Coupon(
                code="FLAT100",
                kind="amount",
                value=Decimal("100"),
                starts_at=datetime.datetime(
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=None,
                max_discount=None,
                max_uses=None,
                uses=1,
                per_customer_limit=1,
                categories=frozenset(),
            ),
            Money("500.00", "INR"),
            datetime.datetime(2026, 11, 9, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {"customer_uses": 1},
        PricingError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0687(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            apply_coupon(*args, **kwargs)
    else:
        assert apply_coupon(*args, **kwargs) == expected
    if after is not None:
        assert args == after
