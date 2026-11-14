"""Issue 0477. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import MoneyError
from shopcore.money.core import Money
from shopcore.money.formatting import parse_money

CASES = [
    pytest.param(
        ("₹1,18,000.00",),
        {},
        Money("118000.00", "INR"),
        None,
        id="case-1",
    ),
    pytest.param(
        ("S$4.20",),
        {},
        Money("4.20", "SGD"),
        None,
        id="case-2",
    ),
    pytest.param(
        ("-$3.10",),
        {},
        Money("-3.10", "USD"),
        None,
        id="case-3",
    ),
    pytest.param(
        ("$12abc",),
        {},
        MoneyError,
        None,
        id="case-4",
    ),
    pytest.param(
        ("INR 118.00",),
        {},
        Money("118.00", "INR"),
        None,
        id="case-5",
    ),
    pytest.param(
        ("12.50 usd",),
        {},
        Money("12.50", "USD"),
        None,
        id="case-6",
    ),
    pytest.param(
        ("twelve dollars",),
        {},
        MoneyError,
        None,
        id="case-7",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0477(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            parse_money(*args, **kwargs)
    else:
        assert parse_money(*args, **kwargs) == expected
    if after is not None:
        assert args == after
