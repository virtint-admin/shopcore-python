"""Issue 0469. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.money.formatting import format_money

CASES = [
    pytest.param(
        (Money("1234.50", "USD"),),
        {"symbol": False},
        "1,234.50 USD",
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("1234.51", "USD"),),
        {"symbol": False},
        "1,234.51 USD",
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("1234.49", "USD"),),
        {"symbol": False},
        "1,234.49 USD",
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("2469.00", "USD"),),
        {"symbol": False},
        "2,469.00 USD",
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("-5.00", "EUR"),),
        {},
        "-€5.00",
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("118000.01", "INR"),),
        {},
        "₹1,18,000.01",
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("-10.00", "EUR"),),
        {},
        "-€10.00",
        None,
        id="case-7",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0469(args, kwargs, expected, after):
    assert format_money(*args, **kwargs) == expected
    if after is not None:
        assert args == after
