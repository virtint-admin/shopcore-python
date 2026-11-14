"""Issue 0866. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.shipping.delivery import business_days_between

CASES = [
    pytest.param(
        (
            datetime.date(2026, 12, 24),
            datetime.date(2026, 12, 28),
            frozenset({datetime.date(2026, 12, 25)}),
        ),
        {},
        2,
        None,
        id="case-1",
    ),
    pytest.param(
        (datetime.date(2026, 11, 10), datetime.date(2026, 11, 16)),
        {},
        5,
        None,
        id="case-2",
    ),
    pytest.param(
        (datetime.date(2026, 11, 8), datetime.date(2026, 11, 16)),
        {},
        7,
        None,
        id="case-3",
    ),
    pytest.param(
        (
            datetime.date(2026, 12, 25),
            datetime.date(2026, 12, 28),
            frozenset({datetime.date(2026, 12, 25)}),
        ),
        {},
        2,
        None,
        id="case-4",
    ),
    pytest.param(
        (
            datetime.date(2026, 12, 23),
            datetime.date(2026, 12, 28),
            frozenset({datetime.date(2026, 12, 25)}),
        ),
        {},
        3,
        None,
        id="case-5",
    ),
    pytest.param(
        (datetime.date(2026, 11, 8), datetime.date(2026, 11, 9)),
        {},
        1,
        None,
        id="case-6",
    ),
    pytest.param(
        (datetime.date(2026, 11, 16), datetime.date(2026, 11, 9)),
        {},
        0,
        None,
        id="case-7",
    ),
    pytest.param(
        (datetime.date(2026, 11, 15), datetime.date(2026, 11, 9)),
        {},
        0,
        None,
        id="case-8",
    ),
    pytest.param(
        (datetime.date(2026, 11, 9), datetime.date(2026, 11, 8)),
        {},
        0,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0866(args, kwargs, expected, after):
    assert business_days_between(*args, **kwargs) == expected
    if after is not None:
        assert args == after
