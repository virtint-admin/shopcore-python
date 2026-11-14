"""Issue 0171. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.errors import InventoryError
from shopcore.inventory.reorder import reorder_quantity

CASES = [
    pytest.param(
        (30, 100),
        {},
        70,
        None,
        id="case-1",
    ),
    pytest.param(
        (30, 0),
        {},
        0,
        None,
        id="case-2",
    ),
    pytest.param(
        (31, 100),
        {},
        69,
        None,
        id="case-3",
    ),
    pytest.param(
        (30, 99),
        {},
        69,
        None,
        id="case-4",
    ),
    pytest.param(
        (30, 101),
        {},
        71,
        None,
        id="case-5",
    ),
    pytest.param(
        (29, 100),
        {},
        71,
        None,
        id="case-6",
    ),
    pytest.param(
        (30, 100, 11),
        {},
        77,
        None,
        id="case-7",
    ),
    pytest.param(
        (30, 0, 12),
        {},
        0,
        None,
        id="case-8",
    ),
    pytest.param(
        (0, -1),
        {},
        InventoryError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0171(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            reorder_quantity(*args, **kwargs)
    else:
        assert reorder_quantity(*args, **kwargs) == expected
    if after is not None:
        assert args == after
