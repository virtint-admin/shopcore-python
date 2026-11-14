"""Issue 0448. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import MoneyError
from shopcore.money.core import Money, add

CASES = [
    pytest.param(
        (Money("10.00", "USD"), Money("-12.50", "USD")),
        {},
        Money("-2.50", "USD"),
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("100.00", "INR"), Money("36.00", "INR")),
        {},
        Money("136.00", "INR"),
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("200.00", "INR"), Money("18.00", "INR")),
        {},
        Money("218.00", "INR"),
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("20.00", "USD"), Money("-12.50", "USD")),
        {},
        Money("7.50", "USD"),
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("10.01", "USD"), Money("-12.50", "USD")),
        {},
        Money("-2.49", "USD"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("10.00", "USD"), Money("-12.49", "USD")),
        {},
        Money("-2.49", "USD"),
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("0.99", "INR"), Money("1.00", "USD")),
        {},
        MoneyError,
        None,
        id="case-7",
    ),
    pytest.param(
        (Money("1.00", "INR"), Money("0.99", "USD")),
        {},
        MoneyError,
        None,
        id="case-8",
    ),
    pytest.param(
        (Money("2.00", "INR"), Money("1.00", "USD")),
        {},
        MoneyError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0448(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            add(*args, **kwargs)
    else:
        assert add(*args, **kwargs) == expected
    if after is not None:
        assert args == after
