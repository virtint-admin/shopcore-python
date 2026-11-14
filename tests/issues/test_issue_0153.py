"""Issue 0153. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.errors import InventoryError
from shopcore.inventory.reorder import safety_stock

CASES = [
    pytest.param(
        ([3, 5, 4, 8], 7),
        {},
        21,
        None,
        id="case-1",
    ),
    pytest.param(
        ([5, 5, 5], 3),
        {},
        0,
        None,
        id="case-2",
    ),
    pytest.param(
        ([3, 5, 4, 8], 6),
        {},
        18,
        None,
        id="case-3",
    ),
    pytest.param(
        ([3, 0, 4, 8], 7),
        {},
        30,
        None,
        id="case-4",
    ),
    pytest.param(
        ([1, 1], 5),
        {},
        0,
        None,
        id="case-5",
    ),
    pytest.param(
        ([5, 6, 5], 3),
        {},
        3,
        None,
        id="case-6",
    ),
    pytest.param(
        ([1, 3], -1),
        {},
        InventoryError,
        None,
        id="case-7",
    ),
    pytest.param(
        ([1, 1], -1),
        {},
        InventoryError,
        None,
        id="case-8",
    ),
    pytest.param(
        ([0, 2], -1),
        {},
        InventoryError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0153(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            safety_stock(*args, **kwargs)
    else:
        assert safety_stock(*args, **kwargs) == expected
    if after is not None:
        assert args == after
