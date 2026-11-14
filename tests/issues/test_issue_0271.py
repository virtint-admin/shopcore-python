"""Issue 0271. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.errors import InventoryError
from shopcore.inventory.stock import Inventory, Movement, StockLevel
from shopcore.inventory.transfers import Transfer, plan_transfer

CASES = [
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=10, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=1, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=10,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BOM",
                        sku="ELC-0101",
                        delta=4,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="DEL",
                        sku="ELC-0101",
                        delta=1,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "T1",
            "ELC-0101",
            "BLR",
            "BLR",
            1,
        ),
        {},
        InventoryError,
        None,
        id="case-1",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=10, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=2, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=10,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BOM",
                        sku="ELC-0101",
                        delta=4,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="DEL",
                        sku="ELC-0101",
                        delta=1,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "T1",
            "ELC-0101",
            "BLR",
            "BLR",
            1,
        ),
        {},
        InventoryError,
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=10, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=-1
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=1, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=10,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BOM",
                        sku="ELC-0101",
                        delta=4,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="DEL",
                        sku="ELC-0101",
                        delta=1,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "T1",
            "ELC-0101",
            "BLR",
            "BLR",
            1,
        ),
        {},
        InventoryError,
        None,
        id="case-3",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=10, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=1, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=10,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BOM",
                        sku="ELC-0101",
                        delta=4,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="DEL",
                        sku="ELC-0101",
                        delta=1,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "T1",
            "ELC-0101",
            "BLR",
            "DEL",
            1,
        ),
        {},
        Transfer(
            transfer_id="T1",
            sku="ELC-0101",
            source="BLR",
            destination="DEL",
            qty=1,
            status="planned",
            received_qty=0,
        ),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=10, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=1, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 8, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=10,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BOM",
                        sku="ELC-0101",
                        delta=4,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="DEL",
                        sku="ELC-0101",
                        delta=1,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "T1",
            "ELC-0101",
            "BLR",
            "DEL",
            1,
        ),
        {},
        Transfer(
            transfer_id="T1",
            sku="ELC-0101",
            source="BLR",
            destination="DEL",
            qty=1,
            status="planned",
            received_qty=0,
        ),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=10, reserved=-1
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=1, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=10,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BOM",
                        sku="ELC-0101",
                        delta=4,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="DEL",
                        sku="ELC-0101",
                        delta=1,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "T1",
            "ELC-0101",
            "BLR",
            "DEL",
            1,
        ),
        {},
        Transfer(
            transfer_id="T1",
            sku="ELC-0101",
            source="BLR",
            destination="DEL",
            qty=1,
            status="planned",
            received_qty=0,
        ),
        None,
        id="case-6",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=10, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=1, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=10,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BOM",
                        sku="ELC-0101",
                        delta=0,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="DEL",
                        sku="ELC-0101",
                        delta=1,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "T1",
            "ELC-0101",
            "BLR",
            "DEL",
            0,
        ),
        {},
        InventoryError,
        None,
        id="case-7",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=10, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=1, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=10,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 10, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BOM",
                        sku="ELC-0101",
                        delta=4,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="DEL",
                        sku="ELC-0101",
                        delta=1,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "T1",
            "ELC-0101",
            "BOM",
            "DEL",
            4,
        ),
        {},
        Transfer(
            transfer_id="T1",
            sku="ELC-0101",
            source="BOM",
            destination="DEL",
            qty=4,
            status="planned",
            received_qty=0,
        ),
        None,
        id="case-8",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=10, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=1
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=1, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=10,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BOM",
                        sku="ELC-0101",
                        delta=4,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="DEL",
                        sku="ELC-0101",
                        delta=1,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "T1",
            "ELC-0101",
            "BOM",
            "DEL",
            4,
        ),
        {},
        InventoryError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0271(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            plan_transfer(*args, **kwargs)
    else:
        assert plan_transfer(*args, **kwargs) == expected
    if after is not None:
        assert args == after
