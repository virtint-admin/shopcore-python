"""Issue 0690. Make this test pass by fixing the application code, not the test."""

import datetime
import zoneinfo
from decimal import Decimal

import pytest

from shopcore.pricing.coupons import Coupon, coupon_applies_to_category

CASES = [
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
                uses=0,
                per_customer_limit=None,
                categories=frozenset({"BKS"}),
            ),
            "bks",
        ),
        {},
        True,
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
                    2026, 11, 1, 1, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
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
            "bks",
        ),
        {},
        True,
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
                categories=frozenset({"BKS"}),
            ),
            "bks",
        ),
        {},
        True,
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
                    2026, 10, 31, 23, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
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
            "bks",
        ),
        {},
        True,
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
            "bks",
        ),
        {},
        True,
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
                    2026, 11, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                ends_at=datetime.datetime(
                    2026, 11, 15, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
                ),
                min_subtotal=None,
                max_discount=None,
                max_uses=None,
                uses=-1,
                per_customer_limit=None,
                categories=frozenset({"BKS"}),
            ),
            "bks",
        ),
        {},
        True,
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
                    2026, 11, 2, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
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
            "ELC",
        ),
        {},
        True,
        None,
        id="case-7",
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
            "ELC",
        ),
        {},
        False,
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
                    2026, 10, 31, 23, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")
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
            "ELC",
        ),
        {},
        False,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0690(args, kwargs, expected, after):
    assert coupon_applies_to_category(*args, **kwargs) == expected
    if after is not None:
        assert args == after
