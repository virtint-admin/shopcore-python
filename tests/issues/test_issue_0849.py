"""Issue 0849. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.shipping.delivery import is_late

CASES = [
    pytest.param(
        (
            datetime.date(2026, 11, 17),
            datetime.datetime(2026, 11, 17, 18, 29, tzinfo=datetime.timezone.utc),
        ),
        {},
        False,
        None,
        id="case-1",
    ),
    pytest.param(
        (
            datetime.date(2026, 11, 17),
            datetime.datetime(2026, 11, 17, 17, 29, tzinfo=datetime.timezone.utc),
        ),
        {},
        False,
        None,
        id="case-2",
    ),
    pytest.param(
        (
            datetime.date(2026, 11, 17),
            datetime.datetime(2026, 11, 16, 18, 30, tzinfo=datetime.timezone.utc),
        ),
        {},
        False,
        None,
        id="case-3",
    ),
    pytest.param(
        (
            datetime.date(2026, 11, 18),
            datetime.datetime(2026, 11, 17, 18, 30, tzinfo=datetime.timezone.utc),
        ),
        {},
        False,
        None,
        id="case-4",
    ),
    pytest.param(
        (
            datetime.date(2026, 11, 17),
            datetime.datetime(2026, 11, 17, 17, 30, tzinfo=datetime.timezone.utc),
        ),
        {},
        False,
        None,
        id="case-5",
    ),
    pytest.param(
        (
            datetime.date(2026, 11, 17),
            datetime.datetime(2026, 11, 17, 18, 30, tzinfo=datetime.timezone.utc),
        ),
        {},
        True,
        None,
        id="case-6",
    ),
    pytest.param(
        (
            datetime.date(2026, 11, 17),
            datetime.datetime(2026, 11, 18, 18, 30, tzinfo=datetime.timezone.utc),
        ),
        {},
        True,
        None,
        id="case-7",
    ),
    pytest.param(
        (
            datetime.date(2026, 11, 18),
            datetime.datetime(2026, 11, 12, 6, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        False,
        None,
        id="case-8",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0849(args, kwargs, expected, after):
    assert is_late(*args, **kwargs) == expected
    if after is not None:
        assert args == after
