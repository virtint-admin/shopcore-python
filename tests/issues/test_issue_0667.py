"""Issue 0667. Make this test pass by fixing the application code, not the test."""

import datetime
import zoneinfo
from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.pricing.coupons import Coupon, remaining_uses

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
                uses=150,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
        0,
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
                uses=150,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
        0,
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Coupon(
                code="DIWALI25",
                kind="percent",
                value=Decimal("24"),
                starts_at=datetime.datetime(
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("1000.00", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=150,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
        0,
        None,
        id="case-3",
    ),
    pytest.param(
        (
            Coupon(
                code="DIWALI25",
                kind="percent",
                value=Decimal("26"),
                starts_at=datetime.datetime(
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("1000.00", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=150,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
        0,
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
                max_discount=Money("499.99", "INR"),
                max_uses=100,
                uses=150,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
        0,
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
                    2026, 11, 14, 23, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("1000.00", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=150,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
        0,
        None,
        id="case-6",
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
                uses=0,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
        None,
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
                    2026, 10, 31, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("1000.00", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=40,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
        60,
        None,
        id="case-8",
    ),
    pytest.param(
        (
            Coupon(
                code="FLAT100",
                kind="amount",
                value=Decimal("99"),
                starts_at=datetime.datetime(
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=None,
                max_discount=None,
                max_uses=None,
                uses=0,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
        None,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0667(args, kwargs, expected, after):
    assert remaining_uses(*args, **kwargs) == expected
    if after is not None:
        assert args == after
