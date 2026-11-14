"""Issue 0714. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import PricingError
from shopcore.money.core import Money
from shopcore.pricing.price_rules import margin_percent

CASES = [
    pytest.param(
        (Money("0.00", "INR"), Money("1.00", "INR")),
        {},
        PricingError,
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("0.00", "INR"), Money("1.01", "INR")),
        {},
        PricingError,
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("0.00", "INR"), Money("2.00", "INR")),
        {},
        PricingError,
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("0.00", "INR"), Money("0.99", "INR")),
        {},
        PricingError,
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("140.00", "INR"), Money("100.01", "INR")),
        {},
        Decimal("28.56"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("99.99", "INR"), Money("100.00", "INR")),
        {},
        Decimal("-0.01"),
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("200.00", "INR"), Money("100.00", "INR")),
        {},
        Decimal("50.00"),
        None,
        id="case-7",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0714(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            margin_percent(*args, **kwargs)
    else:
        assert margin_percent(*args, **kwargs) == expected
    if after is not None:
        assert args == after
