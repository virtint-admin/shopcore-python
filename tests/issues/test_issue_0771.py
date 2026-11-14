"""Issue 0771. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.pricing.tiers import Tier, tier_table

CASES = [
    pytest.param(
        ([Tier(min_qty=1, unit_price=Money("5.00", "USD"))],),
        {},
        ["1+: $5.00"],
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
        ),
        {},
        ["1-9: ₹100.00", "10-49: ₹90.01", "50+: ₹80.00"],
        None,
        id="case-2",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("80.01", "INR")),
            ],
        ),
        {},
        ["1-9: ₹100.00", "10-49: ₹90.00", "50+: ₹80.01"],
        None,
        id="case-3",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=0, unit_price=Money("80.00", "INR")),
            ],
        ),
        {},
        ["1-9: ₹100.00", "10--1: ₹90.00", "0+: ₹80.00"],
        None,
        id="case-4",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
            ],
        ),
        {},
        ["1-9: ₹100.00", "10+: ₹90.00"],
        None,
        id="case-5",
    ),
    pytest.param(
        ([Tier(min_qty=2, unit_price=Money("5.00", "USD"))],),
        {},
        ["2+: $5.00"],
        None,
        id="case-6",
    ),
    pytest.param(
        ([],),
        {},
        [],
        None,
        id="case-7",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0771(args, kwargs, expected, after):
    assert tier_table(*args, **kwargs) == expected
    if after is not None:
        assert args == after
