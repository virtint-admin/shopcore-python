"""Issue 0751. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.pricing.tiers import Tier, unit_price_for_quantity

CASES = [
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
            ],
            1,
        ),
        {},
        Money("100.00", "INR"),
        None,
        id="case-1",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.01", "INR")),
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
            ],
            1,
        ),
        {},
        Money("100.00", "INR"),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=9, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
            ],
            1,
        ),
        {},
        Money("100.00", "INR"),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("160.00", "INR")),
            ],
            1,
        ),
        {},
        Money("100.00", "INR"),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("200.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
            ],
            1,
        ),
        {},
        Money("200.00", "INR"),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("80.01", "INR")),
            ],
            1,
        ),
        {},
        Money("100.00", "INR"),
        None,
        id="case-6",
    ),
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
        Money("80.00", "INR"),
        None,
        id="case-7",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
            ],
            49,
        ),
        {},
        Money("90.00", "INR"),
        None,
        id="case-8",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
            ],
            50,
        ),
        {},
        Money("90.00", "INR"),
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0751(args, kwargs, expected, after):
    assert unit_price_for_quantity(*args, **kwargs) == expected
    if after is not None:
        assert args == after
