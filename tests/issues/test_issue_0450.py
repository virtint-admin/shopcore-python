"""Issue 0450. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money, is_zero

CASES = [
    pytest.param(
        (Money("0.00", "INR"),),
        {},
        True,
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("0.01", "INR"),),
        {},
        False,
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("-0.01", "INR"),),
        {},
        False,
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("0.02", "INR"),),
        {},
        False,
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("-0.02", "INR"),),
        {},
        False,
        None,
        id="case-5",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0450(args, kwargs, expected, after):
    assert is_zero(*args, **kwargs) == expected
    if after is not None:
        assert args == after
