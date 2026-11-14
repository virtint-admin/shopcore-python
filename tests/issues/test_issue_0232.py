"""Issue 0232. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.inventory.stock import Inventory, Movement, StockLevel, movements_for

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
                    ("BLR", "HOM-0201"): StockLevel(
                        warehouse="BLR", sku="HOM-0201", on_hand=2, reserved=0
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
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=2,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
            "BOM",
        ),
        {},
        [
            Movement(
                at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                warehouse="BOM",
                sku="ELC-0101",
                delta=4,
                reason="receipt",
            )
        ],
        None,
        id="case-1",
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
                    ("BLR", "HOM-0201"): StockLevel(
                        warehouse="BLR", sku="HOM-0201", on_hand=2, reserved=0
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
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=2,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
        ),
        {},
        [
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
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("BLR", "HOM-0201"): StockLevel(
                        warehouse="BLR", sku="HOM-0201", on_hand=2, reserved=0
                    ),
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 8, 9, 0, tzinfo=datetime.timezone.utc),
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
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=2,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
        ),
        {},
        [
            Movement(
                at=datetime.datetime(2026, 11, 8, 9, 0, tzinfo=datetime.timezone.utc),
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
                    ("BLR", "HOM-0201"): StockLevel(
                        warehouse="BLR", sku="HOM-0201", on_hand=2, reserved=0
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
                        at=datetime.datetime(2026, 11, 8, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=2,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
        ),
        {},
        [
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
                    ("BLR", "HOM-0201"): StockLevel(
                        warehouse="BLR", sku="HOM-0201", on_hand=2, reserved=0
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
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=3,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
            "BOM",
        ),
        {},
        [
            Movement(
                at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                warehouse="BOM",
                sku="ELC-0101",
                delta=4,
                reason="receipt",
            )
        ],
        None,
        id="case-5",
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
                    ("BLR", "HOM-0201"): StockLevel(
                        warehouse="BLR", sku="HOM-0201", on_hand=2, reserved=0
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
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=0,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "ELC-0101",
            "BOM",
        ),
        {},
        [
            Movement(
                at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                warehouse="BOM",
                sku="ELC-0101",
                delta=4,
                reason="receipt",
            )
        ],
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
                    ("BLR", "HOM-0201"): StockLevel(
                        warehouse="BLR", sku="HOM-0201", on_hand=2, reserved=0
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
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=2,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "NOPE",
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
                        warehouse="BOM", sku="ELC-0101", on_hand=3, reserved=0
                    ),
                    ("BLR", "HOM-0201"): StockLevel(
                        warehouse="BLR", sku="HOM-0201", on_hand=2, reserved=0
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
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=2,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "NOPE",
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
                        warehouse="BLR", sku="ELC-0101", on_hand=9, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("BLR", "HOM-0201"): StockLevel(
                        warehouse="BLR", sku="HOM-0201", on_hand=2, reserved=0
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
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=2,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "NOPE",
        ),
        {},
        [],
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0232(args, kwargs, expected, after):
    assert movements_for(*args, **kwargs) == expected
    if after is not None:
        assert args == after
