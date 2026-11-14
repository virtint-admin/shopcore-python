"""Issue 0691. Make this test pass by fixing the application code, not the test."""

import datetime
import zoneinfo
from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.pricing.coupons import Coupon, eligible_subtotal

CASES = [
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
                categories=frozenset({"BKS"}),
            ),
            [
                ("BKS", Money("900.00", "INR")),
                ("ELC", Money("2999.00", "INR")),
                ("BKS", Money("350.00", "INR")),
            ],
            "INR",
        ),
        {},
        Money("1250.00", "INR"),
        None,
        id="case-1",
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
                    2026, 11, 14, 23, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=None,
                max_discount=None,
                max_uses=None,
                uses=0,
                per_customer_limit=None,
                categories=frozenset({"BKS"}),
            ),
            [
                ("BKS", Money("450.00", "INR")),
                ("ELC", Money("2999.00", "INR")),
                ("BKS", Money("350.00", "INR")),
            ],
            "INR",
        ),
        {},
        Money("800.00", "INR"),
        None,
        id="case-2",
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
                per_customer_limit=None,
                categories=frozenset({"BKS"}),
            ),
            [
                ("BKS", Money("450.00", "INR")),
                ("ELC", Money("2999.00", "INR")),
                ("BKS", Money("350.00", "INR")),
            ],
            "INR",
        ),
        {},
        Money("800.00", "INR"),
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
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=None,
                max_discount=None,
                max_uses=None,
                uses=0,
                per_customer_limit=None,
                categories=frozenset({"BKS"}),
            ),
            [
                ("BKS", Money("450.00", "INR")),
                ("ELC", Money("2999.00", "INR")),
                ("BKS", Money("349.99", "INR")),
            ],
            "INR",
        ),
        {},
        Money("799.99", "INR"),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            Coupon(
                code="FLAT100",
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
            [
                ("BKS", Money("450.00", "INR")),
                ("ELC", Money("2999.00", "INR")),
                ("BKS", Money("350.00", "INR")),
            ],
            "INR",
        ),
        {},
        Money("3799.00", "INR"),
        None,
        id="case-5",
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
            [
                ("BKS", Money("450.00", "INR")),
                ("ELC", Money("2999.00", "INR")),
                ("BKS", Money("350.00", "INR")),
            ],
            "INR",
        ),
        {},
        Money("3799.00", "INR"),
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
                uses=1,
                per_customer_limit=None,
                categories=frozenset(),
            ),
            [],
            "INR",
        ),
        {},
        Money("0.00", "INR"),
        None,
        id="case-7",
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
            [],
            "INR",
        ),
        {},
        Money("0.00", "INR"),
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
                    2026, 11, 15, 1, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=None,
                max_discount=None,
                max_uses=None,
                uses=0,
                per_customer_limit=None,
                categories=frozenset(),
            ),
            [],
            "INR",
        ),
        {},
        Money("0.00", "INR"),
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0691(args, kwargs, expected, after):
    assert eligible_subtotal(*args, **kwargs) == expected
    if after is not None:
        assert args == after
