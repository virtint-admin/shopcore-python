"""Issue 0661. Make this test pass by fixing the application code, not the test."""

import datetime
import zoneinfo
from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.pricing.coupons import Coupon, best_coupon

CASES = [
    pytest.param(
        (
            [
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
                Coupon(
                    code="AAA100",
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
            ],
            Money("900.00", "INR"),
            datetime.datetime(2026, 11, 9, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        Coupon(
            code="AAA100",
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
        None,
        id="case-1",
    ),
    pytest.param(
        (
            [
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
                Coupon(
                    code="AAA100",
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
                    per_customer_limit=None,
                    categories=frozenset(),
                ),
            ],
            Money("900.00", "INR"),
            datetime.datetime(2026, 11, 9, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        Coupon(
            code="AAA100",
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
            per_customer_limit=None,
            categories=frozenset(),
        ),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            [
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
                Coupon(
                    code="AAA100",
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
                    uses=0,
                    per_customer_limit=None,
                    categories=frozenset(),
                ),
            ],
            Money("900.00", "INR"),
            datetime.datetime(2026, 11, 9, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        Coupon(
            code="AAA100",
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
            uses=0,
            per_customer_limit=None,
            categories=frozenset(),
        ),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            [
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
                Coupon(
                    code="AAA100",
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
            ],
            Money("900.00", "INR"),
            datetime.datetime(2026, 11, 10, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        Coupon(
            code="AAA100",
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
        None,
        id="case-4",
    ),
    pytest.param(
        (
            [
                Coupon(
                    code="FLAT100",
                    kind="amount",
                    value=Decimal("100"),
                    starts_at=datetime.datetime(
                        2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                    ),
                    ends_at=datetime.datetime(
                        2026, 11, 15, 1, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                    ),
                    min_subtotal=None,
                    max_discount=None,
                    max_uses=None,
                    uses=0,
                    per_customer_limit=None,
                    categories=frozenset(),
                ),
                Coupon(
                    code="AAA100",
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
            ],
            Money("900.00", "INR"),
            datetime.datetime(2026, 11, 9, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        Coupon(
            code="AAA100",
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
        None,
        id="case-5",
    ),
    pytest.param(
        (
            [
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
                Coupon(
                    code="AAA100",
                    kind="amount",
                    value=Decimal("100"),
                    starts_at=datetime.datetime(
                        2026, 10, 31, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
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
            ],
            Money("900.00", "INR"),
            datetime.datetime(2026, 11, 9, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        Coupon(
            code="AAA100",
            kind="amount",
            value=Decimal("100"),
            starts_at=datetime.datetime(
                2026, 10, 31, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
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
        None,
        id="case-6",
    ),
    pytest.param(
        (
            [
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
            ],
            Money("1200.00", "INR"),
            datetime.datetime(2026, 11, 9, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
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
            max_uses=100,
            uses=0,
            per_customer_limit=None,
            categories=frozenset(),
        ),
        None,
        id="case-7",
    ),
    pytest.param(
        (
            [
                Coupon(
                    code="FLAT100",
                    kind="amount",
                    value=Decimal("100"),
                    starts_at=datetime.datetime(
                        2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                    ),
                    ends_at=datetime.datetime(
                        2026, 11, 15, 1, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                    ),
                    min_subtotal=None,
                    max_discount=None,
                    max_uses=None,
                    uses=0,
                    per_customer_limit=None,
                    categories=frozenset(),
                ),
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
            ],
            Money("1200.00", "INR"),
            datetime.datetime(2026, 11, 9, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
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
            max_uses=100,
            uses=0,
            per_customer_limit=None,
            categories=frozenset(),
        ),
        None,
        id="case-8",
    ),
    pytest.param(
        (
            [
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
                    uses=0,
                    per_customer_limit=None,
                    categories=frozenset(),
                ),
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
            ],
            Money("1200.00", "INR"),
            datetime.datetime(2026, 11, 9, 15, 30, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
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
            max_uses=100,
            uses=0,
            per_customer_limit=None,
            categories=frozenset(),
        ),
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0661(args, kwargs, expected, after):
    assert best_coupon(*args, **kwargs) == expected
    if after is not None:
        assert args == after
