"""Issue 0540. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.errors import OrderError
from shopcore.orders.orders import parse_order_number

CASES = [
    pytest.param(
        ("SC-20261109-000042",),
        {},
        (datetime.date(2026, 11, 9), 42),
        None,
        id="case-1",
    ),
    pytest.param(
        ("  sc-20261231-000001 ",),
        {},
        (datetime.date(2026, 12, 31), 1),
        None,
        id="case-2",
    ),
    pytest.param(
        ("SC-2026119-000042",),
        {},
        OrderError,
        None,
        id="case-3",
    ),
    pytest.param(
        ("SC-20261131-000042",),
        {},
        OrderError,
        None,
        id="case-4",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0540(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            parse_order_number(*args, **kwargs)
    else:
        assert parse_order_number(*args, **kwargs) == expected
    if after is not None:
        assert args == after
