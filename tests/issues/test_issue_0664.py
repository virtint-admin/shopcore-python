"""Issue 0664. Make this test pass by fixing the application code, not the test."""

import datetime
import zoneinfo
from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.pricing.coupons import Coupon, is_coupon_active

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
                    2026, 11, 16, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("1000.00", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=0,
                per_customer_limit=None,
                categories=frozenset(),
            ),
            datetime.datetime(2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        True,
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
                max_uses=101,
                uses=0,
                per_customer_limit=None,
                categories=frozenset(),
            ),
            datetime.datetime(2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        True,
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Coupon(
                code="DIWALI25",
                kind="percent",
                value=Decimal("50"),
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
            datetime.datetime(2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        True,
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
                min_subtotal=Money("999.99", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=0,
                per_customer_limit=None,
                categories=frozenset(),
            ),
            datetime.datetime(2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        True,
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
                uses=-1,
                per_customer_limit=None,
                categories=frozenset(),
            ),
            datetime.datetime(2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        True,
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
                    2026, 11, 15, 1, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("1000.00", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=0,
                per_customer_limit=None,
                categories=frozenset(),
            ),
            datetime.datetime(2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        True,
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
            datetime.datetime(2026, 11, 14, 23, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        True,
        None,
        id="case-7",
    ),
    pytest.param(
        (
            Coupon(
                code="DIWALI25",
                kind="percent",
                value=Decimal("50"),
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
            datetime.datetime(2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        False,
        None,
        id="case-8",
    ),
    pytest.param(
        (
            Coupon(
                code="DIWALI25",
                kind="percent",
                value=Decimal("25"),
                starts_at=datetime.datetime(
                    2026, 11, 1, 1, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
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
            datetime.datetime(2026, 11, 14, 18, 29, tzinfo=datetime.timezone.utc),
        ),
        {},
        True,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0664(args, kwargs, expected, after):
    assert is_coupon_active(*args, **kwargs) == expected
    if after is not None:
        assert args == after
