"""Issue 0851. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.shipping.delivery import days_late

CASES = [
    pytest.param(
        (
            datetime.date(2026, 11, 17),
            datetime.datetime(2026, 11, 15, 10, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        0,
        None,
        id="case-1",
    ),
    pytest.param(
        (
            datetime.date(2026, 11, 18),
            datetime.datetime(2026, 11, 17, 6, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        0,
        None,
        id="case-2",
    ),
    pytest.param(
        (
            datetime.date(2026, 11, 17),
            datetime.datetime(2026, 11, 16, 6, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        0,
        None,
        id="case-3",
    ),
    pytest.param(
        (
            datetime.date(2026, 11, 18),
            datetime.datetime(2026, 11, 15, 10, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        0,
        None,
        id="case-4",
    ),
    pytest.param(
        (
            datetime.date(2026, 11, 17),
            datetime.datetime(2026, 11, 16, 10, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        0,
        None,
        id="case-5",
    ),
    pytest.param(
        (
            datetime.date(2026, 11, 17),
            datetime.datetime(2026, 11, 15, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        0,
        None,
        id="case-6",
    ),
    pytest.param(
        (
            datetime.date(2026, 11, 17),
            datetime.datetime(2026, 11, 19, 10, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        2,
        None,
        id="case-7",
    ),
    pytest.param(
        (
            datetime.date(2026, 11, 17),
            datetime.datetime(2026, 11, 17, 7, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        0,
        None,
        id="case-8",
    ),
    pytest.param(
        (
            datetime.date(2026, 11, 16),
            datetime.datetime(2026, 11, 17, 20, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        2,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0851(args, kwargs, expected, after):
    assert days_late(*args, **kwargs) == expected
    if after is not None:
        assert args == after
