"""Issue 0713. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import PricingError
from shopcore.money.core import Money
from shopcore.pricing.price_rules import markup_price

CASES = [
    pytest.param(
        (Money("100.00", "INR"), Decimal("40")),
        {},
        Money("140.00", "INR"),
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("33.33", "USD"), Decimal("15")),
        {},
        Money("38.33", "USD"),
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("33.33", "USD"), Decimal("14")),
        {},
        Money("38.00", "USD"),
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("33.33", "USD"), Decimal("30")),
        {},
        Money("43.33", "USD"),
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("66.66", "USD"), Decimal("15")),
        {},
        Money("76.66", "USD"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("33.33", "USD"), Decimal("16")),
        {},
        Money("38.66", "USD"),
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("1.00", "USD"), Decimal("-1")),
        {},
        PricingError,
        None,
        id="case-7",
    ),
    pytest.param(
        (Money("1.01", "USD"), Decimal("-1")),
        {},
        PricingError,
        None,
        id="case-8",
    ),
    pytest.param(
        (Money("2.00", "USD"), Decimal("-1")),
        {},
        PricingError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0713(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            markup_price(*args, **kwargs)
    else:
        assert markup_price(*args, **kwargs) == expected
    if after is not None:
        assert args == after
