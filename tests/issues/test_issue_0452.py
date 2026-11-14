"""Issue 0452. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import MoneyError
from shopcore.money.core import Money, sum_money

CASES = [
    pytest.param(
        ([Money("1.10", "USD"), Money("2.21", "USD"), Money("3.30", "USD")], "USD"),
        {},
        Money("6.61", "USD"),
        None,
        id="case-1",
    ),
    pytest.param(
        ([Money("1.11", "USD"), Money("2.20", "USD"), Money("3.30", "USD")], "USD"),
        {},
        Money("6.61", "USD"),
        None,
        id="case-2",
    ),
    pytest.param(
        ([Money("1.10", "USD"), Money("4.40", "USD"), Money("3.30", "USD")], "USD"),
        {},
        Money("8.80", "USD"),
        None,
        id="case-3",
    ),
    pytest.param(
        ([Money("3.30", "USD"), Money("2.20", "USD"), Money("1.10", "USD")], "USD"),
        {},
        Money("6.60", "USD"),
        None,
        id="case-4",
    ),
    pytest.param(
        ([Money("1.10", "USD"), Money("2.20", "USD"), Money("6.60", "USD")], "USD"),
        {},
        Money("9.90", "USD"),
        None,
        id="case-5",
    ),
    pytest.param(
        ([Money("1.09", "USD"), Money("2.20", "USD"), Money("3.30", "USD")], "USD"),
        {},
        Money("6.59", "USD"),
        None,
        id="case-6",
    ),
    pytest.param(
        ([], "INR"),
        {},
        Money("0.00", "INR"),
        None,
        id="case-7",
    ),
    pytest.param(
        ([Money("1.00", "INR"), Money("0.99", "USD")], "INR"),
        {},
        MoneyError,
        None,
        id="case-8",
    ),
    pytest.param(
        ([Money("1.01", "USD")], "INR"),
        {},
        MoneyError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0452(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            sum_money(*args, **kwargs)
    else:
        assert sum_money(*args, **kwargs) == expected
    if after is not None:
        assert args == after
