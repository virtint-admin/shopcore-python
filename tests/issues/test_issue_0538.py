"""Issue 0538. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.errors import OrderError
from shopcore.orders.orders import order_number

CASES = [
    pytest.param(
        (0, datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc)),
        {},
        OrderError,
        None,
        id="case-1",
    ),
    pytest.param(
        (0, datetime.datetime(2026, 11, 9, 20, 0, tzinfo=datetime.timezone.utc)),
        {},
        OrderError,
        None,
        id="case-2",
    ),
    pytest.param(
        (
            0,
            datetime.datetime(
                2026,
                11,
                8,
                23,
                0,
                tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400)),
            ),
        ),
        {},
        OrderError,
        None,
        id="case-3",
    ),
    pytest.param(
        (0, datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc)),
        {},
        OrderError,
        None,
        id="case-4",
    ),
    pytest.param(
        (0, datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc)),
        {},
        OrderError,
        None,
        id="case-5",
    ),
    pytest.param(
        (0, datetime.datetime(2026, 11, 9, 0, 0)),
        {},
        OrderError,
        None,
        id="case-6",
    ),
    pytest.param(
        (7, datetime.datetime(2026, 11, 9, 20, 0, tzinfo=datetime.timezone.utc)),
        {},
        "SC-20261110-000007",
        None,
        id="case-7",
    ),
    pytest.param(
        (42, datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc)),
        {},
        "SC-20261109-000042",
        None,
        id="case-8",
    ),
    pytest.param(
        (
            1,
            datetime.datetime(
                2026,
                11,
                9,
                0,
                0,
                tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400)),
            ),
        ),
        {},
        "SC-20261109-000001",
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0538(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            order_number(*args, **kwargs)
    else:
        assert order_number(*args, **kwargs) == expected
    if after is not None:
        assert args == after
