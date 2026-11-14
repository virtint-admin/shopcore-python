"""Issue 0245. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.errors import InventoryError
from shopcore.inventory.stock import Inventory, Movement, Reservation, StockLevel, write_off

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
            "BLR",
            "HOM-0201",
            1,
            "dented",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        StockLevel(warehouse="BLR", sku="HOM-0201", on_hand=1, reserved=0),
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
                        warehouse="BLR", sku="HOM-0201", on_hand=1, reserved=0
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
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=-1,
                        reason="write-off: dented",
                    ),
                ],
                next_reservation=1,
            ),
            "BLR",
            "HOM-0201",
            1,
            "dented",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
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
                        delta=3,
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
            "BLR",
            "HOM-0201",
            1,
            "dented",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        StockLevel(warehouse="BLR", sku="HOM-0201", on_hand=1, reserved=0),
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
                        warehouse="BLR", sku="HOM-0201", on_hand=1, reserved=0
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
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=2,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=-1,
                        reason="write-off: dented",
                    ),
                ],
                next_reservation=1,
            ),
            "BLR",
            "HOM-0201",
            1,
            "dented",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
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
                        at=datetime.datetime(2026, 11, 10, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=2,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            "BLR",
            "HOM-0201",
            1,
            "dented",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        StockLevel(warehouse="BLR", sku="HOM-0201", on_hand=1, reserved=0),
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
                        warehouse="BLR", sku="HOM-0201", on_hand=1, reserved=0
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
                        at=datetime.datetime(2026, 11, 10, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=2,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=-1,
                        reason="write-off: dented",
                    ),
                ],
                next_reservation=1,
            ),
            "BLR",
            "HOM-0201",
            1,
            "dented",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
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
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=2,
                        reason="receipt",
                    ),
                ],
                next_reservation=2,
            ),
            "BLR",
            "HOM-0201",
            1,
            "dented",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        StockLevel(warehouse="BLR", sku="HOM-0201", on_hand=1, reserved=0),
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
                        warehouse="BLR", sku="HOM-0201", on_hand=1, reserved=0
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
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=-1,
                        reason="write-off: dented",
                    ),
                ],
                next_reservation=2,
            ),
            "BLR",
            "HOM-0201",
            1,
            "dented",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        id="case-4",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=0, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("BLR", "HOM-0201"): StockLevel(
                        warehouse="BLR", sku="HOM-0201", on_hand=2, reserved=2
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="HOM-0201",
                        qty=2,
                        order_id="O1",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc
                        ),
                    )
                },
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
                next_reservation=2,
            ),
            "BLR",
            "HOM-0201",
            1,
            "dented",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        InventoryError,
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
                        warehouse="BLR", sku="HOM-0201", on_hand=2, reserved=2
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="HOM-0201",
                        qty=2,
                        order_id="O1",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc
                        ),
                    )
                },
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
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=2,
                        reason="receipt",
                    ),
                ],
                next_reservation=2,
            ),
            "BLR",
            "HOM-0201",
            1,
            "dented",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        InventoryError,
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
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=1
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
            "BLR",
            "HOM-0201",
            2,
            "dented",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        StockLevel(warehouse="BLR", sku="HOM-0201", on_hand=0, reserved=0),
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=10, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=1
                    ),
                    ("BLR", "HOM-0201"): StockLevel(
                        warehouse="BLR", sku="HOM-0201", on_hand=0, reserved=0
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
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=-2,
                        reason="write-off: dented",
                    ),
                ],
                next_reservation=1,
            ),
            "BLR",
            "HOM-0201",
            2,
            "dented",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
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
                    ("BLR", "HOM-0201"): StockLevel(
                        warehouse="BLR", sku="HOM-0201", on_hand=2, reserved=1
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
            "BLR",
            "HOM-0201",
            2,
            "dented",
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
                        at=datetime.datetime(2026, 11, 10, 9, 0, tzinfo=datetime.timezone.utc),
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
            "BLR",
            "HOM-0201",
            -1,
            "x",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
        ),
        {},
        InventoryError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0245(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            write_off(*args, **kwargs)
    else:
        assert write_off(*args, **kwargs) == expected
    if after is not None:
        assert args == after
