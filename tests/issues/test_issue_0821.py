"""Issue 0821. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.reports.sales import growth_percent

CASES = [
    pytest.param(
        (Money("100.00", "INR"), Money("125.01", "INR")),
        {},
        Decimal("25.01"),
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("100.01", "INR"), Money("125.00", "INR")),
        {},
        Decimal("24.99"),
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("300.01", "INR"), Money("200.00", "INR")),
        {},
        Decimal("-33.34"),
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("8.00", "INR"), Money("9.01", "INR")),
        {},
        Decimal("12.63"),
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("7.99", "INR"), Money("9.00", "INR")),
        {},
        Decimal("12.64"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("16.00", "INR"), Money("9.00", "INR")),
        {},
        Decimal("-43.75"),
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("0.00", "INR"), Money("20.00", "INR")),
        {},
        None,
        None,
        id="case-7",
    ),
    pytest.param(
        (Money("0.00", "INR"), Money("9.99", "INR")),
        {},
        None,
        None,
        id="case-8",
    ),
    pytest.param(
        (Money("0.00", "INR"), Money("10.01", "INR")),
        {},
        None,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0821(args, kwargs, expected, after):
    assert growth_percent(*args, **kwargs) == expected
    if after is not None:
        assert args == after
