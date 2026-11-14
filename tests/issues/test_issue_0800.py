"""Issue 0800. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.reports.export import daily_sales_csv

CASES = [
    pytest.param(
        (
            {
                datetime.date(2026, 11, 10): Money("2997.00", "INR"),
                datetime.date(2026, 11, 9): Money("4397.00", "INR"),
            },
        ),
        {},
        "date,revenue,currency\n2026-11-09,4397.00,INR\n2026-11-10,2997.00,INR\n",
        None,
        id="case-1",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 10): Money("2997.00", "INR"),
                datetime.date(2026, 11, 9): Money("4396.99", "INR"),
            },
        ),
        {},
        "date,revenue,currency\n2026-11-09,4396.99,INR\n2026-11-10,2997.00,INR\n",
        None,
        id="case-2",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 10): Money("2996.99", "INR"),
                datetime.date(2026, 11, 9): Money("4397.00", "INR"),
            },
        ),
        {},
        "date,revenue,currency\n2026-11-09,4397.00,INR\n2026-11-10,2996.99,INR\n",
        None,
        id="case-3",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 10): Money("2997.00", "INR"),
                datetime.date(2026, 11, 9): Money("4397.01", "INR"),
            },
        ),
        {},
        "date,revenue,currency\n2026-11-09,4397.01,INR\n2026-11-10,2997.00,INR\n",
        None,
        id="case-4",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 10): Money("2997.00", "INR"),
                datetime.date(2026, 11, 9): Money("8794.00", "INR"),
            },
        ),
        {},
        "date,revenue,currency\n2026-11-09,8794.00,INR\n2026-11-10,2997.00,INR\n",
        None,
        id="case-5",
    ),
    pytest.param(
        (
            {
                datetime.date(2026, 11, 10): Money("2997.01", "INR"),
                datetime.date(2026, 11, 9): Money("4397.00", "INR"),
            },
        ),
        {},
        "date,revenue,currency\n2026-11-09,4397.00,INR\n2026-11-10,2997.01,INR\n",
        None,
        id="case-6",
    ),
    pytest.param(
        ({},),
        {},
        "date,revenue,currency\n",
        None,
        id="case-7",
    ),
    pytest.param(
        ({datetime.date(2026, 11, 9): Money("1500", "JPY")},),
        {},
        "date,revenue,currency\n2026-11-09,1500,JPY\n",
        None,
        id="case-8",
    ),
    pytest.param(
        ({datetime.date(2026, 11, 9): Money("1499", "JPY")},),
        {},
        "date,revenue,currency\n2026-11-09,1499,JPY\n",
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0800(args, kwargs, expected, after):
    assert daily_sales_csv(*args, **kwargs) == expected
    if after is not None:
        assert args == after
