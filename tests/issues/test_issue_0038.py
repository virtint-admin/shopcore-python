"""Issue 0038. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.cart.cart import CartLimits
from shopcore.cart.maintenance import clamp_quantity

CASES = [
    pytest.param(
        (-3,),
        {},
        0,
        None,
        id="case-1",
    ),
    pytest.param(
        (-2,),
        {},
        0,
        None,
        id="case-2",
    ),
    pytest.param(
        (-4,),
        {},
        0,
        None,
        id="case-3",
    ),
    pytest.param(
        (0,),
        {},
        0,
        None,
        id="case-4",
    ),
    pytest.param(
        (0, CartLimits(max_lines=50, max_qty_per_line=6, max_total_qty=100)),
        {},
        0,
        None,
        id="case-5",
    ),
    pytest.param(
        (25, CartLimits(max_lines=50, max_qty_per_line=7, max_total_qty=100)),
        {},
        7,
        None,
        id="case-6",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0038(args, kwargs, expected, after):
    assert clamp_quantity(*args, **kwargs) == expected
    if after is not None:
        assert args == after
