"""Issue 0658. Make this test pass by fixing the application code, not the test."""

import datetime
import zoneinfo
from decimal import Decimal

import pytest

from shopcore.errors import PricingError
from shopcore.money.core import Money
from shopcore.pricing.coupons import Coupon, redeem_coupon

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
                max_uses=101,
                uses=0,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
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
            uses=1,
            per_customer_limit=None,
            categories=frozenset(),
        ),
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
                    2026, 10, 31, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
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
        ),
        {},
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
            uses=1,
            per_customer_limit=None,
            categories=frozenset(),
        ),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Coupon(
                code="FLAT100",
                kind="amount",
                value=Decimal("200"),
                starts_at=datetime.datetime(
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=None,
                max_discount=None,
                max_uses=None,
                uses=10000,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
        Coupon(
            code="FLAT100",
            kind="amount",
            value=Decimal("200"),
            starts_at=datetime.datetime(
                2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
            ),
            ends_at=datetime.datetime(
                2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
            ),
            min_subtotal=None,
            max_discount=None,
            max_uses=None,
            uses=10001,
            per_customer_limit=None,
            categories=frozenset(),
        ),
        None,
        id="case-3",
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
                    2026, 11, 14, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=None,
                max_discount=None,
                max_uses=None,
                uses=10000,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
        Coupon(
            code="FLAT100",
            kind="amount",
            value=Decimal("100"),
            starts_at=datetime.datetime(
                2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
            ),
            ends_at=datetime.datetime(
                2026, 11, 14, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
            ),
            min_subtotal=None,
            max_discount=None,
            max_uses=None,
            uses=10001,
            per_customer_limit=None,
            categories=frozenset(),
        ),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            Coupon(
                code="FLAT100",
                kind="amount",
                value=Decimal("101"),
                starts_at=datetime.datetime(
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=None,
                max_discount=None,
                max_uses=None,
                uses=10000,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
        Coupon(
            code="FLAT100",
            kind="amount",
            value=Decimal("101"),
            starts_at=datetime.datetime(
                2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
            ),
            ends_at=datetime.datetime(
                2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
            ),
            min_subtotal=None,
            max_discount=None,
            max_uses=None,
            uses=10001,
            per_customer_limit=None,
            categories=frozenset(),
        ),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            Coupon(
                code="FLAT100",
                kind="amount",
                value=Decimal("100"),
                starts_at=datetime.datetime(
                    2026, 11, 2, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=None,
                max_discount=None,
                max_uses=None,
                uses=10000,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
        Coupon(
            code="FLAT100",
            kind="amount",
            value=Decimal("100"),
            starts_at=datetime.datetime(
                2026, 11, 2, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
            ),
            ends_at=datetime.datetime(
                2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
            ),
            min_subtotal=None,
            max_discount=None,
            max_uses=None,
            uses=10001,
            per_customer_limit=None,
            categories=frozenset(),
        ),
        None,
        id="case-6",
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
                uses=100,
                per_customer_limit=None,
                categories=frozenset(),
            ),
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
                    2026, 10, 31, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("1000.00", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=100,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
        PricingError,
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
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 14, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=Money("1000.00", "INR"),
                max_discount=Money("500.00", "INR"),
                max_uses=100,
                uses=100,
                per_customer_limit=None,
                categories=frozenset(),
            ),
        ),
        {},
        PricingError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0658(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            redeem_coupon(*args, **kwargs)
    else:
        assert redeem_coupon(*args, **kwargs) == expected
    if after is not None:
        assert args == after
