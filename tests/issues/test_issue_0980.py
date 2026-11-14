"""Issue 0980. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.tax.calc import effective_rate

CASES = [
    pytest.param(
        (Money("0.00", "INR"), Money("0.00", "INR")),
        {},
        Decimal("0.000"),
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("0.00", "INR"), Money("0.01", "INR")),
        {},
        Decimal("0.000"),
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("0.00", "INR"), Money("-0.01", "INR")),
        {},
        Decimal("0.000"),
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("1750.00", "INR"), Money("190.00", "INR")),
        {},
        Decimal("10.857"),
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("3500.00", "INR"), Money("190.00", "INR")),
        {},
        Decimal("5.429"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("100.00", "INR"), Money("18.01", "INR")),
        {},
        Decimal("18.010"),
        None,
        id="case-6",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0980(args, kwargs, expected, after):
    assert effective_rate(*args, **kwargs) == expected
    if after is not None:
        assert args == after
