"""Issue 0767. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.pricing.tiers import Tier, next_tier_savings

CASES = [
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
            ],
            50,
        ),
        {},
        None,
        None,
        id="case-1",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("160.00", "INR")),
            ],
            50,
        ),
        {},
        None,
        None,
        id="case-2",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
            ],
            50,
        ),
        {},
        None,
        None,
        id="case-3",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.01", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
            ],
            50,
        ),
        {},
        None,
        None,
        id="case-4",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("89.99", "INR")),
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
            ],
            50,
        ),
        {},
        None,
        None,
        id="case-5",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=9, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
            ],
            50,
        ),
        {},
        None,
        None,
        id="case-6",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("79.99", "INR")),
            ],
            49,
        ),
        {},
        (1, Money("10.01", "INR")),
        None,
        id="case-7",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=51, unit_price=Money("80.00", "INR")),
            ],
            49,
        ),
        {},
        (2, Money("10.00", "INR")),
        None,
        id="case-8",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=9, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
            ],
            49,
        ),
        {},
        (1, Money("10.00", "INR")),
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0767(args, kwargs, expected, after):
    assert next_tier_savings(*args, **kwargs) == expected
    if after is not None:
        assert args == after
