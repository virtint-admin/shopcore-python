"""Issue 0176. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.inventory.reservations import pick_warehouse
from shopcore.inventory.stock import Inventory, Movement, StockLevel

CASES = [
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=0,
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
                        delta=5,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
            3,
            ["BLR", "BOM", "DEL"],
        ),
        {},
        "BLR",
        None,
        id="case-1",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=3,
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
                        delta=6,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
            3,
            ["BLR", "BOM", "DEL"],
        ),
        {},
        "BLR",
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=2,
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
                        delta=5,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
            3,
            ["BLR", "BOM", "DEL"],
        ),
        {},
        "BLR",
        None,
        id="case-3",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=3,
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
                        delta=5,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
            3,
            ["BLR", "BOM", "DEL"],
        ),
        {},
        "BLR",
        None,
        id="case-4",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=3,
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
                        at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                        warehouse="DEL",
                        sku="ELC-0101",
                        delta=5,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
            3,
            ["BLR", "BOM", "DEL"],
        ),
        {},
        "BLR",
        None,
        id="case-5",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=3,
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
                        at=datetime.datetime(2026, 11, 10, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="DEL",
                        sku="ELC-0101",
                        delta=5,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
            4,
            ["BLR", "BOM", "DEL"],
        ),
        {},
        "BOM",
        None,
        id="case-6",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=3,
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
                        delta=5,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
            6,
            ["BLR", "BOM", "DEL"],
        ),
        {},
        None,
        None,
        id="case-7",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=2, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=3,
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
                        delta=5,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
            6,
            ["BLR", "BOM", "DEL"],
        ),
        {},
        None,
        None,
        id="case-8",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=3,
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
                        at=datetime.datetime(2026, 11, 9, 8, 0, tzinfo=datetime.timezone.utc),
                        warehouse="DEL",
                        sku="ELC-0101",
                        delta=5,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
            6,
            ["BLR", "BOM", "DEL"],
        ),
        {},
        None,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0176(args, kwargs, expected, after):
    assert pick_warehouse(*args, **kwargs) == expected
    if after is not None:
        assert args == after
