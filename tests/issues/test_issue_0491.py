"""Issue 0491. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import MoneyError
from shopcore.money.core import Money
from shopcore.money.rounding import split_evenly

CASES = [
    pytest.param(
        (Money("5", "JPY"), 1),
        {},
        [Money("5", "JPY")],
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("6", "JPY"), 1),
        {},
        [Money("6", "JPY")],
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("10", "JPY"), 1),
        {},
        [Money("10", "JPY")],
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("4", "JPY"), 1),
        {},
        [Money("4", "JPY")],
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("0.20", "USD"), 3),
        {},
        [Money("0.07", "USD"), Money("0.07", "USD"), Money("0.06", "USD")],
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("5", "JPY"), 2),
        {},
        [Money("3", "JPY"), Money("2", "JPY")],
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("10", "JPY"), 0),
        {},
        MoneyError,
        None,
        id="case-7",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0491(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            split_evenly(*args, **kwargs)
    else:
        assert split_evenly(*args, **kwargs) == expected
    if after is not None:
        assert args == after
