"""Issue 0159. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import InventoryError
from shopcore.inventory.reorder import reorder_point

CASES = [
    pytest.param(
        (Decimal("5.00"), 8, 21),
        {},
        61,
        None,
        id="case-1",
    ),
    pytest.param(
        (Decimal("5.00"), 7, 0),
        {},
        35,
        None,
        id="case-2",
    ),
    pytest.param(
        (Decimal("4.99"), 7, 21),
        {},
        56,
        None,
        id="case-3",
    ),
    pytest.param(
        (Decimal("9.5"), 0, 2),
        {},
        2,
        None,
        id="case-4",
    ),
    pytest.param(
        (Decimal("19.0"), 0, 3),
        {},
        3,
        None,
        id="case-5",
    ),
    pytest.param(
        (Decimal("1"), 1, 0),
        {},
        1,
        None,
        id="case-6",
    ),
    pytest.param(
        (Decimal("1"), 0, -1),
        {},
        InventoryError,
        None,
        id="case-7",
    ),
    pytest.param(
        (Decimal("1"), 2, -1),
        {},
        InventoryError,
        None,
        id="case-8",
    ),
    pytest.param(
        (Decimal("0"), 1, -1),
        {},
        InventoryError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0159(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            reorder_point(*args, **kwargs)
    else:
        assert reorder_point(*args, **kwargs) == expected
    if after is not None:
        assert args == after
