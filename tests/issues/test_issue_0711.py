"""Issue 0711. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import PricingError
from shopcore.money.core import Money
from shopcore.pricing.discounts import effective_percent

CASES = [
    pytest.param(
        (Money("0.00", "INR"), Money("0.00", "INR")),
        {},
        Decimal("0.00"),
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("0.00", "INR"), Money("0.01", "INR")),
        {},
        Decimal("0.00"),
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("0.00", "INR"), Money("-0.01", "INR")),
        {},
        Decimal("0.00"),
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("1000.00", "INR"), Money("1510.00", "INR")),
        {},
        PricingError,
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("999.99", "INR"), Money("755.00", "INR")),
        {},
        Decimal("24.50"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("1000.01", "INR"), Money("755.00", "INR")),
        {},
        Decimal("24.50"),
        None,
        id="case-6",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0711(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            effective_percent(*args, **kwargs)
    else:
        assert effective_percent(*args, **kwargs) == expected
    if after is not None:
        assert args == after
