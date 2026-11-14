"""Issue 0741. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import PricingError
from shopcore.money.core import Money
from shopcore.pricing.price_rules import landed_cost

CASES = [
    pytest.param(
        (Money("10.00", "USD"), 100, Money("50.00", "USD"), Decimal("20")),
        {},
        Money("12.60", "USD"),
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("10.00", "USD"), 100, Money("50.01", "USD"), Decimal("10")),
        {},
        Money("11.55", "USD"),
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("10.00", "USD"), 99, Money("50.00", "USD"), Decimal("10")),
        {},
        Money("11.56", "USD"),
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("20.00", "USD"), 3, Money("0.00", "USD"), Decimal("0")),
        {},
        Money("20.00", "USD"),
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("1.01", "USD"), 3, Money("1.00", "USD"), Decimal("0")),
        {},
        Money("1.34", "USD"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("1.00", "USD"), 3, Money("1.00", "USD"), Decimal("-1")),
        {},
        Money("1.32", "USD"),
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("1.00", "USD"), 0, Money("1.00", "USD"), Decimal("1")),
        {},
        PricingError,
        None,
        id="case-7",
    ),
    pytest.param(
        (Money("1.00", "USD"), 0, Money("0.99", "USD"), Decimal("0")),
        {},
        PricingError,
        None,
        id="case-8",
    ),
    pytest.param(
        (Money("1.00", "USD"), 0, Money("1.00", "USD"), Decimal("-1")),
        {},
        PricingError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0741(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            landed_cost(*args, **kwargs)
    else:
        assert landed_cost(*args, **kwargs) == expected
    if after is not None:
        assert args == after
