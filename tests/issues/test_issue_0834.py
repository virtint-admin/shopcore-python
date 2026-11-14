"""Issue 0834. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.errors import ReportError
from shopcore.money.core import Money
from shopcore.reports.sales import fill_missing_days

CASES = [
    pytest.param(
        (
            {
                datetime.date(2026, 11, 9): Money("4397.00", "INR"),
                datetime.date(2026, 11, 10): Money("2997.00", "INR"),
                datetime.date(2026, 11, 12): Money("5998.00", "INR"),
            },
            datetime.date(2026, 11, 10),
            datetime.date(2026, 11, 11),
            "INR",
        ),
        {},
        {
            datetime.date(2026, 11, 10): Money("2997.00", "INR"),
            datetime.date(2026, 11, 11): Money("0.00", "INR"),
        },
        None,
        id="case-1",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 9): Money("4397.01", "INR"),
                datetime.date(2026, 11, 10): Money("2997.00", "INR"),
                datetime.date(2026, 11, 12): Money("5998.00", "INR"),
            },
            datetime.date(2026, 11, 9),
            datetime.date(2026, 11, 12),
            "INR",
        ),
        {},
        {
            datetime.date(2026, 11, 9): Money("4397.01", "INR"),
            datetime.date(2026, 11, 10): Money("2997.00", "INR"),
            datetime.date(2026, 11, 11): Money("0.00", "INR"),
            datetime.date(2026, 11, 12): Money("5998.00", "INR"),
        },
        None,
        id="case-2",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 9): Money("4397.00", "INR"),
                datetime.date(2026, 11, 10): Money("2997.01", "INR"),
                datetime.date(2026, 11, 12): Money("5998.00", "INR"),
            },
            datetime.date(2026, 11, 10),
            datetime.date(2026, 11, 11),
            "INR",
        ),
        {},
        {
            datetime.date(2026, 11, 10): Money("2997.01", "INR"),
            datetime.date(2026, 11, 11): Money("0.00", "INR"),
        },
        None,
        id="case-3",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 9): Money("4397.01", "INR"),
                datetime.date(2026, 11, 10): Money("2997.00", "INR"),
                datetime.date(2026, 11, 12): Money("5998.00", "INR"),
            },
            datetime.date(2026, 11, 10),
            datetime.date(2026, 11, 11),
            "INR",
        ),
        {},
        {
            datetime.date(2026, 11, 10): Money("2997.00", "INR"),
            datetime.date(2026, 11, 11): Money("0.00", "INR"),
        },
        None,
        id="case-4",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 9): Money("4397.00", "INR"),
                datetime.date(2026, 11, 10): Money("2997.00", "INR"),
                datetime.date(2026, 11, 12): Money("5997.99", "INR"),
            },
            datetime.date(2026, 11, 10),
            datetime.date(2026, 11, 11),
            "INR",
        ),
        {},
        {
            datetime.date(2026, 11, 10): Money("2997.00", "INR"),
            datetime.date(2026, 11, 11): Money("0.00", "INR"),
        },
        None,
        id="case-5",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 9): Money("4396.99", "INR"),
                datetime.date(2026, 11, 10): Money("2997.00", "INR"),
                datetime.date(2026, 11, 12): Money("5998.00", "INR"),
            },
            datetime.date(2026, 11, 10),
            datetime.date(2026, 11, 11),
            "INR",
        ),
        {},
        {
            datetime.date(2026, 11, 10): Money("2997.00", "INR"),
            datetime.date(2026, 11, 11): Money("0.00", "INR"),
        },
        None,
        id="case-6",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 9): Money("4397.00", "INR"),
                datetime.date(2026, 11, 10): Money("2996.99", "INR"),
                datetime.date(2026, 11, 12): Money("5998.00", "INR"),
            },
            datetime.date(2026, 11, 12),
            datetime.date(2026, 11, 9),
            "INR",
        ),
        {},
        ReportError,
        None,
        id="case-7",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 9): Money("8794.00", "INR"),
                datetime.date(2026, 11, 10): Money("2997.00", "INR"),
                datetime.date(2026, 11, 12): Money("5998.00", "INR"),
            },
            datetime.date(2026, 11, 12),
            datetime.date(2026, 11, 9),
            "INR",
        ),
        {},
        ReportError,
        None,
        id="case-8",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 9): Money("4397.00", "INR"),
                datetime.date(2026, 11, 10): Money("2997.00", "INR"),
                datetime.date(2026, 11, 12): Money("5998.00", "INR"),
            },
            datetime.date(2026, 11, 13),
            datetime.date(2026, 11, 9),
            "INR",
        ),
        {},
        ReportError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0834(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            fill_missing_days(*args, **kwargs)
    else:
        assert fill_missing_days(*args, **kwargs) == expected
    if after is not None:
        assert args == after
