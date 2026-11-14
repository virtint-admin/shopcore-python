"""Issue 0609. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.orders.model import OrderStatus
from shopcore.orders.state import is_terminal

CASES = [
    pytest.param(
        (OrderStatus.CANCELLED,),
        {},
        True,
        None,
        id="case-1",
    ),
    pytest.param(
        (OrderStatus.REFUNDED,),
        {},
        True,
        None,
        id="case-2",
    ),
    pytest.param(
        (OrderStatus.DELIVERED,),
        {},
        False,
        None,
        id="case-3",
    ),
    pytest.param(
        (OrderStatus.PENDING_PAYMENT,),
        {},
        False,
        None,
        id="case-4",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0609(args, kwargs, expected, after):
    assert is_terminal(*args, **kwargs) == expected
    if after is not None:
        assert args == after
