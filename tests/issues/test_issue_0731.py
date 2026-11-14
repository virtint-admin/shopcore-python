"""Issue 0731. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import PricingError
from shopcore.money.core import Money
from shopcore.pricing.price_rules import price_change_percent

CASES = [
    pytest.param(
        (Money("0.00", "USD"), Money("4.00", "USD")),
        {},
        PricingError,
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("0.00", "USD"), Money("3.99", "USD")),
        {},
        PricingError,
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("0.00", "USD"), Money("4.01", "USD")),
        {},
        PricingError,
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("0.00", "USD"), Money("8.00", "USD")),
        {},
        PricingError,
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("3.00", "USD"), Money("4.00", "USD")),
        {},
        Decimal("33.33"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("6.00", "USD"), Money("4.00", "USD")),
        {},
        Decimal("-33.33"),
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("0.01", "USD"), Money("4.00", "USD")),
        {},
        Decimal("39900.00"),
        None,
        id="case-7",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0731(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            price_change_percent(*args, **kwargs)
    else:
        assert price_change_percent(*args, **kwargs) == expected
    if after is not None:
        assert args == after
