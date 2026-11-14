"""Issue 0487. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import MoneyError
from shopcore.money.core import Money
from shopcore.money.rounding import RoundingMode, round_to_increment

CASES = [
    pytest.param(
        (Money("1.02", "SGD"), Decimal("0.05")),
        {},
        Money("1.00", "SGD"),
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("1.01", "SGD"), Decimal("0.05")),
        {},
        Money("1.00", "SGD"),
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("117.49", "INR"), Decimal("1")),
        {},
        Money("117.00", "INR"),
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("117.51", "INR"), Decimal("1")),
        {},
        Money("118.00", "INR"),
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("1.01", "SGD"), Decimal("0.10"), RoundingMode.UP),
        {},
        Money("1.10", "SGD"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("2.02", "SGD"), Decimal("0.05"), RoundingMode.UP),
        {},
        Money("2.05", "SGD"),
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("117.50", "INR"), Decimal("0")),
        {},
        MoneyError,
        None,
        id="case-7",
    ),
    pytest.param(
        (Money("0.99", "INR"), Decimal("0")),
        {},
        MoneyError,
        None,
        id="case-8",
    ),
    pytest.param(
        (Money("1.01", "INR"), Decimal("0")),
        {},
        MoneyError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0487(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            round_to_increment(*args, **kwargs)
    else:
        assert round_to_increment(*args, **kwargs) == expected
    if after is not None:
        assert args == after
