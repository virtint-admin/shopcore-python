"""Issue 0723. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import PricingError
from shopcore.money.core import Money
from shopcore.pricing.price_rules import charm_price

CASES = [
    pytest.param(
        (Money("12.30", "USD"),),
        {},
        Money("12.99", "USD"),
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("13.00", "USD"),),
        {},
        Money("13.99", "USD"),
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("24.60", "USD"),),
        {},
        Money("24.99", "USD"),
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("13.01", "USD"),),
        {},
        Money("13.99", "USD"),
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("450.00", "INR"), Decimal("100"), Decimal("0")),
        {},
        Money("500.00", "INR"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("450.00", "INR"), Decimal("1"), Decimal("0")),
        {},
        Money("450.00", "INR"),
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("450.00", "INR"), Decimal("1"), Decimal("1")),
        {},
        PricingError,
        None,
        id="case-7",
    ),
    pytest.param(
        (Money("900.00", "INR"), Decimal("1"), Decimal("1")),
        {},
        PricingError,
        None,
        id="case-8",
    ),
    pytest.param(
        (Money("450.00", "INR"), Decimal("2"), Decimal("1")),
        {},
        Money("451.00", "INR"),
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0723(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            charm_price(*args, **kwargs)
    else:
        assert charm_price(*args, **kwargs) == expected
    if after is not None:
        assert args == after
