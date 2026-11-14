"""Issue 0651. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import PricingError
from shopcore.money.core import Money
from shopcore.pricing.bundles import buy_x_get_y

CASES = [
    pytest.param(
        (2, Money("100.00", "INR"), 2, 1),
        {},
        Money("0.00", "INR"),
        None,
        id="case-1",
    ),
    pytest.param(
        (6, Money("100.00", "INR"), 2, 1),
        {},
        Money("200.00", "INR"),
        None,
        id="case-2",
    ),
    pytest.param(
        (7, Money("99.99", "INR"), 2, 1),
        {},
        Money("199.98", "INR"),
        None,
        id="case-3",
    ),
    pytest.param(
        (0, Money("100.00", "INR"), 2, 1),
        {},
        Money("0.00", "INR"),
        None,
        id="case-4",
    ),
    pytest.param(
        (2, Money("200.00", "INR"), 2, 1),
        {},
        Money("0.00", "INR"),
        None,
        id="case-5",
    ),
    pytest.param(
        (6, Money("49.99", "INR"), 1, 1),
        {},
        Money("149.97", "INR"),
        None,
        id="case-6",
    ),
    pytest.param(
        (7, Money("100.00", "INR"), 0, 1),
        {},
        PricingError,
        None,
        id="case-7",
    ),
    pytest.param(
        (5, Money("50.00", "INR"), 0, 1),
        {},
        PricingError,
        None,
        id="case-8",
    ),
    pytest.param(
        (-1, Money("50.00", "INR"), 1, 2),
        {},
        PricingError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0651(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            buy_x_get_y(*args, **kwargs)
    else:
        assert buy_x_get_y(*args, **kwargs) == expected
    if after is not None:
        assert args == after
