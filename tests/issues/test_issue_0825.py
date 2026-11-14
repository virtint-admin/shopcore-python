"""Issue 0825. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.reports.sales import moving_average

CASES = [
    pytest.param(
        ([Money("0.01", "INR"), Money("0.02", "INR")], 2),
        {},
        [Money("0.02", "INR")],
        None,
        id="case-1",
    ),
    pytest.param(
        (
            [
                Money("10.00", "INR"),
                Money("40.00", "INR"),
                Money("30.00", "INR"),
                Money("40.00", "INR"),
            ],
            2,
        ),
        {},
        [Money("25.00", "INR"), Money("35.00", "INR"), Money("35.00", "INR")],
        None,
        id="case-2",
    ),
    pytest.param(
        (
            [
                Money("10.00", "INR"),
                Money("19.99", "INR"),
                Money("30.00", "INR"),
                Money("40.00", "INR"),
            ],
            2,
        ),
        {},
        [Money("15.00", "INR"), Money("25.00", "INR"), Money("35.00", "INR")],
        None,
        id="case-3",
    ),
    pytest.param(
        (
            [
                Money("10.00", "INR"),
                Money("20.00", "INR"),
                Money("30.01", "INR"),
                Money("40.00", "INR"),
            ],
            2,
        ),
        {},
        [Money("15.00", "INR"), Money("25.01", "INR"), Money("35.01", "INR")],
        None,
        id="case-4",
    ),
    pytest.param(
        ([Money("0.02", "INR"), Money("0.02", "INR")], 2),
        {},
        [Money("0.02", "INR")],
        None,
        id="case-5",
    ),
    pytest.param(
        ([Money("0.01", "INR"), Money("0.01", "INR")], 2),
        {},
        [Money("0.01", "INR")],
        None,
        id="case-6",
    ),
    pytest.param(
        ([], 3),
        {},
        [],
        None,
        id="case-7",
    ),
    pytest.param(
        ([Money("0.01", "INR")], 2),
        {},
        [],
        None,
        id="case-8",
    ),
    pytest.param(
        ([Money("1", "JPY")], 2),
        {},
        [],
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0825(args, kwargs, expected, after):
    assert moving_average(*args, **kwargs) == expected
    if after is not None:
        assert args == after
