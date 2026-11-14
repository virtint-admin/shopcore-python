"""Issue 0873. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.errors import ShippingError
from shopcore.shipping.delivery import dispatch_date

CASES = [
    pytest.param(
        (datetime.datetime(2026, 11, 9, 8, 30, tzinfo=datetime.timezone.utc),),
        {},
        datetime.date(2026, 11, 10),
        None,
        id="case-1",
    ),
    pytest.param(
        (datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),),
        {},
        datetime.date(2026, 11, 10),
        None,
        id="case-2",
    ),
    pytest.param(
        (datetime.datetime(2026, 11, 10, 8, 30, tzinfo=datetime.timezone.utc),),
        {},
        datetime.date(2026, 11, 11),
        None,
        id="case-3",
    ),
    pytest.param(
        (datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),),
        {},
        datetime.date(2026, 11, 10),
        None,
        id="case-4",
    ),
    pytest.param(
        (datetime.datetime(2026, 11, 9, 10, 0),),
        {},
        ShippingError,
        None,
        id="case-5",
    ),
    pytest.param(
        (datetime.datetime(2026, 11, 16, 5, 0, tzinfo=datetime.timezone.utc),),
        {},
        datetime.date(2026, 11, 16),
        None,
        id="case-6",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0873(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            dispatch_date(*args, **kwargs)
    else:
        assert dispatch_date(*args, **kwargs) == expected
    if after is not None:
        assert args == after
