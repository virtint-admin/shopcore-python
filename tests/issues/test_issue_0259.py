"""Issue 0259. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.inventory.stock import Inventory, Movement, StockLevel
from shopcore.inventory.transfers import Transfer, rebalance

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
                        delta=3,
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
            "ELC-0101",
            ["BLR", "BOM", "DEL"],
        ),
        {},
        [
            Transfer(
                transfer_id="T001",
                sku="ELC-0101",
                source="BLR",
                destination="DEL",
                qty=4,
                status="planned",
                received_qty=0,
            ),
            Transfer(
                transfer_id="T002",
                sku="ELC-0101",
                source="BLR",
                destination="BOM",
                qty=1,
                status="planned",
                received_qty=0,
            ),
        ],
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
                        warehouse="DEL", sku="ELC-0101", on_hand=1, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=9,
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
            "ELC-0101",
            ["BLR", "BOM", "DEL"],
        ),
        {},
        [
            Transfer(
                transfer_id="T001",
                sku="ELC-0101",
                source="BLR",
                destination="DEL",
                qty=4,
                status="planned",
                received_qty=0,
            ),
            Transfer(
                transfer_id="T002",
                sku="ELC-0101",
                source="BLR",
                destination="BOM",
                qty=1,
                status="planned",
                received_qty=0,
            ),
        ],
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
                        warehouse="BOM", sku="ELC-0101", on_hand=3, reserved=0
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
            "ELC-0101",
            ["BLR", "BOM", "DEL"],
        ),
        {},
        [
            Transfer(
                transfer_id="T001",
                sku="ELC-0101",
                source="BLR",
                destination="DEL",
                qty=3,
                status="planned",
                received_qty=0,
            ),
            Transfer(
                transfer_id="T002",
                sku="ELC-0101",
                source="BLR",
                destination="BOM",
                qty=2,
                status="planned",
                received_qty=0,
            ),
        ],
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
                        delta=2,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
            ["BLR", "BOM", "DEL"],
        ),
        {},
        [
            Transfer(
                transfer_id="T001",
                sku="ELC-0101",
                source="BLR",
                destination="DEL",
                qty=4,
                status="planned",
                received_qty=0,
            ),
            Transfer(
                transfer_id="T002",
                sku="ELC-0101",
                source="BLR",
                destination="BOM",
                qty=1,
                status="planned",
                received_qty=0,
            ),
        ],
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
            "ELC-0101",
            ["BLR", "BOM", "DEL"],
        ),
        {},
        [
            Transfer(
                transfer_id="T001",
                sku="ELC-0101",
                source="BLR",
                destination="DEL",
                qty=4,
                status="planned",
                received_qty=0,
            ),
            Transfer(
                transfer_id="T002",
                sku="ELC-0101",
                source="BLR",
                destination="BOM",
                qty=1,
                status="planned",
                received_qty=0,
            ),
        ],
        None,
        id="case-5",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "X"): StockLevel(warehouse="BLR", sku="X", on_hand=2, reserved=1),
                    ("BOM", "X"): StockLevel(warehouse="BOM", sku="X", on_hand=2, reserved=0),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
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
            "X",
            ["BLR", "BOM"],
        ),
        {},
        [
            Transfer(
                transfer_id="T001",
                sku="X",
                source="BOM",
                destination="BLR",
                qty=1,
                status="planned",
                received_qty=0,
            )
        ],
        None,
        id="case-6",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "X"): StockLevel(warehouse="BLR", sku="X", on_hand=2, reserved=0),
                    ("BOM", "X"): StockLevel(warehouse="BOM", sku="X", on_hand=2, reserved=0),
                },
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
            "X",
            ["BLR", "BOM"],
        ),
        {},
        [],
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
                        warehouse="DEL", sku="ELC-0101", on_hand=1, reserved=-1
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
            "ELC-0101",
            ["BLR"],
        ),
        {},
        [],
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
                        delta=2,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
            ["BLR"],
        ),
        {},
        [],
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0259(args, kwargs, expected, after):
    assert rebalance(*args, **kwargs) == expected
    if after is not None:
        assert args == after
