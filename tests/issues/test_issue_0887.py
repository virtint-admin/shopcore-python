"""Issue 0887. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import ShippingError
from shopcore.money.core import Money
from shopcore.shipping.rates import Rate, weight_cost

CASES = [
    pytest.param(
        (
            Rate(
                service="standard",
                zone="LOCAL",
                base=Money("40.00", "INR"),
                per_step=Money("20.00", "INR"),
                transit_days=2,
                step_g=500,
            ),
            0,
        ),
        {},
        ShippingError,
        None,
        id="case-1",
    ),
    pytest.param(
        (
            Rate(
                service="standard",
                zone="NATIONAL",
                base=Money("70.00", "INR"),
                per_step=Money("45.00", "INR"),
                transit_days=6,
                step_g=500,
            ),
            0,
        ),
        {},
        ShippingError,
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Rate(
                service="standard",
                zone="NATIONAL",
                base=Money("70.00", "INR"),
                per_step=Money("45.00", "INR"),
                transit_days=6,
                step_g=500,
            ),
            5200,
        ),
        {},
        Money("520.00", "INR"),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            Rate(
                service="standard",
                zone="LOCAL",
                base=Money("40.00", "INR"),
                per_step=Money("20.00", "INR"),
                transit_days=2,
                step_g=499,
            ),
            1200,
        ),
        {},
        Money("80.00", "INR"),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            Rate(
                service="standard",
                zone="LOCAL",
                base=Money("40.00", "INR"),
                per_step=Money("20.00", "INR"),
                transit_days=2,
                step_g=500,
            ),
            1199,
        ),
        {},
        Money("80.00", "INR"),
        None,
        id="case-5",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0887(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            weight_cost(*args, **kwargs)
    else:
        assert weight_cost(*args, **kwargs) == expected
    if after is not None:
        assert args == after
