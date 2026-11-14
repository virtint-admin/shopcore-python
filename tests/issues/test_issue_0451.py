"""Issue 0451. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money, is_negative

CASES = [
    pytest.param(
        (Money("0.00", "USD"),),
        {},
        False,
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("0.01", "USD"),),
        {},
        False,
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("-0.01", "USD"),),
        {},
        True,
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("3.00", "USD"),),
        {},
        False,
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("6.00", "USD"),),
        {},
        False,
        None,
        id="case-5",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0451(args, kwargs, expected, after):
    assert is_negative(*args, **kwargs) == expected
    if after is not None:
        assert args == after
