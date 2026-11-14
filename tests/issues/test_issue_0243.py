"""Issue 0243. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.errors import InventoryError
from shopcore.inventory.stock import Inventory, Movement, StockLevel, receive_stock

CASES = [
    pytest.param(
        (
            Inventory(levels={}, reservations={}, movements=[], next_reservation=1),
            "BLR",
            "GRC-0401",
            5,
            datetime.datetime(2026, 11, 9, 0, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        StockLevel(warehouse="BLR", sku="GRC-0401", on_hand=5, reserved=0),
        (
            Inventory(
                levels={
                    ("BLR", "GRC-0401"): StockLevel(
                        warehouse="BLR", sku="GRC-0401", on_hand=5, reserved=0
                    )
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 0, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="GRC-0401",
                        delta=5,
                        reason="receipt",
                    )
                ],
                next_reservation=1,
            ),
            "BLR",
            "GRC-0401",
            5,
            datetime.datetime(2026, 11, 9, 0, 0, tzinfo=datetime.timezone.utc),
        ),
        id="case-1",
    ),
    pytest.param(
        (
            Inventory(levels={}, reservations={}, movements=[], next_reservation=1),
            "BLR",
            "ELC-0101",
            5,
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        StockLevel(warehouse="BLR", sku="ELC-0101", on_hand=5, reserved=0),
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=5, reserved=0
                    )
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=5,
                        reason="receipt",
                    )
                ],
                next_reservation=1,
            ),
            "BLR",
            "ELC-0101",
            5,
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        id="case-2",
    ),
    pytest.param(
        (
            Inventory(levels={}, reservations={}, movements=[], next_reservation=2),
            "BLR",
            "GRC-0401",
            11,
            datetime.datetime(2026, 11, 9, 0, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        StockLevel(warehouse="BLR", sku="GRC-0401", on_hand=11, reserved=0),
        (
            Inventory(
                levels={
                    ("BLR", "GRC-0401"): StockLevel(
                        warehouse="BLR", sku="GRC-0401", on_hand=11, reserved=0
                    )
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 0, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="GRC-0401",
                        delta=11,
                        reason="receipt",
                    )
                ],
                next_reservation=2,
            ),
            "BLR",
            "GRC-0401",
            11,
            datetime.datetime(2026, 11, 9, 0, 0, tzinfo=datetime.timezone.utc),
        ),
        id="case-3",
    ),
    pytest.param(
        (
            Inventory(levels={}, reservations={}, movements=[], next_reservation=1),
            "BLR",
            "GRC-0401",
            11,
            datetime.datetime(2026, 11, 10, 0, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        StockLevel(warehouse="BLR", sku="GRC-0401", on_hand=11, reserved=0),
        (
            Inventory(
                levels={
                    ("BLR", "GRC-0401"): StockLevel(
                        warehouse="BLR", sku="GRC-0401", on_hand=11, reserved=0
                    )
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 10, 0, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="GRC-0401",
                        delta=11,
                        reason="receipt",
                    )
                ],
                next_reservation=1,
            ),
            "BLR",
            "GRC-0401",
            11,
            datetime.datetime(2026, 11, 10, 0, 0, tzinfo=datetime.timezone.utc),
        ),
        id="case-4",
    ),
    pytest.param(
        (
            Inventory(levels={}, reservations={}, movements=[], next_reservation=1),
            "BLR",
            "ELC-0101",
            10,
            datetime.datetime(2026, 11, 10, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        StockLevel(warehouse="BLR", sku="ELC-0101", on_hand=10, reserved=0),
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=10, reserved=0
                    )
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 10, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=10,
                        reason="receipt",
                    )
                ],
                next_reservation=1,
            ),
            "BLR",
            "ELC-0101",
            10,
            datetime.datetime(2026, 11, 10, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        id="case-5",
    ),
    pytest.param(
        (
            Inventory(
                levels={("BLR", "X"): StockLevel(warehouse="BLR", sku="X", on_hand=2, reserved=0)},
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 8, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="X",
                        delta=2,
                        reason="receipt",
                    )
                ],
                next_reservation=1,
            ),
            "BOM",
            "X",
            2,
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        StockLevel(warehouse="BOM", sku="X", on_hand=2, reserved=0),
        (
            Inventory(
                levels={
                    ("BLR", "X"): StockLevel(warehouse="BLR", sku="X", on_hand=2, reserved=0),
                    ("BOM", "X"): StockLevel(warehouse="BOM", sku="X", on_hand=2, reserved=0),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 8, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="X",
                        delta=2,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BOM",
                        sku="X",
                        delta=2,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "BOM",
            "X",
            2,
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        id="case-6",
    ),
    pytest.param(
        (
            Inventory(levels={}, reservations={}, movements=[], next_reservation=1),
            "BLR",
            "X",
            0,
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        InventoryError,
        None,
        id="case-7",
    ),
    pytest.param(
        (
            Inventory(levels={}, reservations={}, movements=[], next_reservation=2),
            "BLR",
            "X",
            0,
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        InventoryError,
        None,
        id="case-8",
    ),
    pytest.param(
        (
            Inventory(
                levels={("BLR", "X"): StockLevel(warehouse="BLR", sku="X", on_hand=2, reserved=0)},
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="X",
                        delta=2,
                        reason="receipt",
                    )
                ],
                next_reservation=1,
            ),
            "BOM",
            "X",
            0,
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        InventoryError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0243(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            receive_stock(*args, **kwargs)
    else:
        assert receive_stock(*args, **kwargs) == expected
    if after is not None:
        assert args == after
