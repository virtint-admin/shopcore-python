"""Issue 0744. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.pricing.tiers import Tier, validate_tiers

CASES = [
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("79.99", "INR")),
            ],
        ),
        {},
        [],
        None,
        id="case-1",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=51, unit_price=Money("80.00", "INR")),
            ],
        ),
        {},
        [],
        None,
        id="case-2",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.01", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
            ],
        ),
        {},
        [],
        None,
        id="case-3",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=2, unit_price=Money("100.00", "INR")),
                Tier(min_qty=2, unit_price=Money("90.00", "INR")),
                Tier(min_qty=5, unit_price=Money("95.01", "INR")),
            ],
        ),
        {},
        ["first tier must start at 1", "tier at 2 is out of order", "tier at 5 is not cheaper"],
        None,
        id="case-4",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=2, unit_price=Money("100.00", "INR")),
                Tier(min_qty=2, unit_price=Money("90.00", "INR")),
                Tier(min_qty=6, unit_price=Money("95.00", "INR")),
            ],
        ),
        {},
        ["first tier must start at 1", "tier at 2 is out of order", "tier at 6 is not cheaper"],
        None,
        id="case-5",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=2, unit_price=Money("100.00", "INR")),
                Tier(min_qty=2, unit_price=Money("90.00", "INR")),
                Tier(min_qty=5, unit_price=Money("94.99", "INR")),
            ],
        ),
        {},
        ["first tier must start at 1", "tier at 2 is out of order", "tier at 5 is not cheaper"],
        None,
        id="case-6",
    ),
    pytest.param(
        ([],),
        {},
        ["no tiers"],
        None,
        id="case-7",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
            ],
        ),
        {},
        ["first tier must start at 1", "tier at 10 is out of order", "tier at 1 is out of order"],
        None,
        id="case-8",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=0, unit_price=Money("100.00", "INR")),
                Tier(min_qty=2, unit_price=Money("90.00", "INR")),
                Tier(min_qty=5, unit_price=Money("95.00", "INR")),
            ],
        ),
        {},
        ["first tier must start at 1", "tier at 5 is not cheaper"],
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0744(args, kwargs, expected, after):
    assert validate_tiers(*args, **kwargs) == expected
    if after is not None:
        assert args == after
