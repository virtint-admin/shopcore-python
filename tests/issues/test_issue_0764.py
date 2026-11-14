"""Issue 0764. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import PricingError
from shopcore.money.core import Money
from shopcore.pricing.tiers import Tier, graduated_price

CASES = [
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
            ],
            13,
        ),
        {},
        Money("1260.00", "INR"),
        None,
        id="case-1",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=49, unit_price=Money("80.00", "INR")),
            ],
            12,
        ),
        {},
        Money("1170.00", "INR"),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
                Tier(min_qty=10, unit_price=Money("180.00", "INR")),
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
            ],
            9,
        ),
        {},
        Money("900.00", "INR"),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=1, unit_price=Money("200.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
            ],
            60,
        ),
        {},
        Money("6280.00", "INR"),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
            ],
            60,
        ),
        {},
        Money("1990.00", "INR"),
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
            10,
        ),
        {},
        Money("980.00", "INR"),
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
            0,
        ),
        {},
        PricingError,
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
            9,
        ),
        {},
        Money("0.00", "INR"),
        None,
        id="case-8",
    ),
    pytest.param(
        (
            [
                Tier(min_qty=50, unit_price=Money("80.00", "INR")),
                Tier(min_qty=10, unit_price=Money("90.00", "INR")),
                Tier(min_qty=1, unit_price=Money("100.00", "INR")),
            ],
            10,
        ),
        {},
        Money("0.00", "INR"),
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0764(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            graduated_price(*args, **kwargs)
    else:
        assert graduated_price(*args, **kwargs) == expected
    if after is not None:
        assert args == after
