"""Issue 0175. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.inventory.reorder import days_of_cover

CASES = [
    pytest.param(
        (10, Decimal("0")),
        {},
        None,
        None,
        id="case-1",
    ),
    pytest.param(
        (9, Decimal("0")),
        {},
        None,
        None,
        id="case-2",
    ),
    pytest.param(
        (0, Decimal("0")),
        {},
        None,
        None,
        id="case-3",
    ),
    pytest.param(
        (11, Decimal("0")),
        {},
        None,
        None,
        id="case-4",
    ),
    pytest.param(
        (10, Decimal("3")),
        {},
        Decimal("3.3"),
        None,
        id="case-5",
    ),
    pytest.param(
        (0, Decimal("3")),
        {},
        Decimal("0.0"),
        None,
        id="case-6",
    ),
    pytest.param(
        (-1, Decimal("5")),
        {},
        Decimal("-0.2"),
        None,
        id="case-7",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0175(args, kwargs, expected, after):
    assert days_of_cover(*args, **kwargs) == expected
    if after is not None:
        assert args == after
