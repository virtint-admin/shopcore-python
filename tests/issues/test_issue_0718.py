"""Issue 0718. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import PricingError
from shopcore.money.core import Money
from shopcore.pricing.price_rules import price_for_margin

CASES = [
    pytest.param(
        (Money("70.00", "INR"), Decimal("100")),
        {},
        PricingError,
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("69.99", "INR"), Decimal("100")),
        {},
        PricingError,
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("140.00", "INR"), Decimal("100")),
        {},
        PricingError,
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("70.01", "INR"), Decimal("100")),
        {},
        PricingError,
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("100.00", "INR"), Decimal("21")),
        {},
        Money("126.58", "INR"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("70.00", "INR"), Decimal("101")),
        {},
        PricingError,
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("70.00", "INR"), Decimal("99")),
        {},
        Money("7000.00", "INR"),
        None,
        id="case-7",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0718(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            price_for_margin(*args, **kwargs)
    else:
        assert price_for_margin(*args, **kwargs) == expected
    if after is not None:
        assert args == after
