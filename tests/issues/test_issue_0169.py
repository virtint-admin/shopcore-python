"""Issue 0169. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import InventoryError
from shopcore.inventory.reorder import economic_order_quantity

CASES = [
    pytest.param(
        (1200, Decimal("100"), Decimal("7")),
        {},
        186,
        None,
        id="case-1",
    ),
    pytest.param(
        (0, Decimal("100"), Decimal("6")),
        {},
        0,
        None,
        id="case-2",
    ),
    pytest.param(
        (1200, Decimal("200"), Decimal("6")),
        {},
        283,
        None,
        id="case-3",
    ),
    pytest.param(
        (1000, Decimal("51"), Decimal("2")),
        {},
        226,
        None,
        id="case-4",
    ),
    pytest.param(
        (1, Decimal("50"), Decimal("2")),
        {},
        8,
        None,
        id="case-5",
    ),
    pytest.param(
        (10, Decimal("5"), Decimal("1")),
        {},
        10,
        None,
        id="case-6",
    ),
    pytest.param(
        (10, Decimal("5"), Decimal("0")),
        {},
        InventoryError,
        None,
        id="case-7",
    ),
    pytest.param(
        (10, Decimal("4"), Decimal("0")),
        {},
        InventoryError,
        None,
        id="case-8",
    ),
    pytest.param(
        (10, Decimal("10"), Decimal("0")),
        {},
        InventoryError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0169(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            economic_order_quantity(*args, **kwargs)
    else:
        assert economic_order_quantity(*args, **kwargs) == expected
    if after is not None:
        assert args == after
