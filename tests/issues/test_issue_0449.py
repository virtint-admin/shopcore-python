"""Issue 0449. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import MoneyError
from shopcore.money.core import Money, subtract

CASES = [
    pytest.param(
        (Money("1.00", "EUR"), Money("2.50", "EUR")),
        {},
        Money("-1.50", "EUR"),
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("118.01", "INR"), Money("18.00", "INR")),
        {},
        Money("100.01", "INR"),
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("1.00", "EUR"), Money("2.49", "EUR")),
        {},
        Money("-1.49", "EUR"),
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("2.00", "EUR"), Money("2.50", "EUR")),
        {},
        Money("-0.50", "EUR"),
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("1.00", "EUR"), Money("2.51", "EUR")),
        {},
        Money("-1.51", "EUR"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("1.01", "EUR"), Money("2.50", "EUR")),
        {},
        Money("-1.49", "EUR"),
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("1.00", "EUR"), Money("0.99", "GBP")),
        {},
        MoneyError,
        None,
        id="case-7",
    ),
    pytest.param(
        (Money("1.01", "EUR"), Money("1.00", "GBP")),
        {},
        MoneyError,
        None,
        id="case-8",
    ),
    pytest.param(
        (Money("0.99", "EUR"), Money("1.00", "GBP")),
        {},
        MoneyError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0449(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            subtract(*args, **kwargs)
    else:
        assert subtract(*args, **kwargs) == expected
    if after is not None:
        assert args == after
