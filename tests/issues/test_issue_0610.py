"""Issue 0610. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.errors import OrderError
from shopcore.orders.model import OrderStatus
from shopcore.orders.state import parse_status

CASES = [
    pytest.param(
        ("Pending Payment",),
        {},
        OrderStatus.PENDING_PAYMENT,
        None,
        id="case-1",
    ),
    pytest.param(
        ("  PAID ",),
        {},
        OrderStatus.PAID,
        None,
        id="case-2",
    ),
    pytest.param(
        ("pending-payment",),
        {},
        OrderStatus.PENDING_PAYMENT,
        None,
        id="case-3",
    ),
    pytest.param(
        ("lost",),
        {},
        OrderError,
        None,
        id="case-4",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0610(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            parse_status(*args, **kwargs)
    else:
        assert parse_status(*args, **kwargs) == expected
    if after is not None:
        assert args == after
