"""Issue 0828. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.reports.sales import best_sales_day

CASES = [
    pytest.param(
        (
            {
                datetime.date(2026, 11, 9): Money("4397.00", "INR"),
                datetime.date(2026, 11, 10): Money("2997.00", "INR"),
                datetime.date(2026, 11, 12): Money("5998.00", "INR"),
            },
        ),
        {},
        (datetime.date(2026, 11, 12), Money("5998.00", "INR")),
        None,
        id="case-1",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 9): Money("4397.00", "INR"),
                datetime.date(2026, 11, 10): Money("2997.01", "INR"),
                datetime.date(2026, 11, 12): Money("5998.00", "INR"),
            },
        ),
        {},
        (datetime.date(2026, 11, 12), Money("5998.00", "INR")),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 12): Money("10.00", "INR"),
                datetime.date(2026, 11, 9): Money("5.00", "INR"),
            },
        ),
        {},
        (datetime.date(2026, 11, 12), Money("10.00", "INR")),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 12): Money("4.99", "INR"),
                datetime.date(2026, 11, 9): Money("5.00", "INR"),
            },
        ),
        {},
        (datetime.date(2026, 11, 9), Money("5.00", "INR")),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 12): Money("5.00", "INR"),
                datetime.date(2026, 11, 9): Money("10.00", "INR"),
            },
        ),
        {},
        (datetime.date(2026, 11, 9), Money("10.00", "INR")),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 12): Money("5.00", "INR"),
                datetime.date(2026, 11, 9): Money("5.01", "INR"),
            },
        ),
        {},
        (datetime.date(2026, 11, 9), Money("5.01", "INR")),
        None,
        id="case-6",
    ),
    pytest.param(
        ({},),
        {},
        None,
        None,
        id="case-7",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0828(args, kwargs, expected, after):
    assert best_sales_day(*args, **kwargs) == expected
    if after is not None:
        assert args == after
