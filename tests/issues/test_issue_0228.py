"""Issue 0228. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.errors import InventoryError
from shopcore.inventory.stock import Inventory, Movement, StockLevel, stock_value
from shopcore.money.core import Money

CASES = [
    pytest.param(
        (
            Inventory(
                levels={("BLR", "X"): StockLevel(warehouse="BLR", sku="X", on_hand=0, reserved=0)},
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="X",
                        delta=1,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 8, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="X",
                        delta=-1,
                        reason="lost",
                    ),
                ],
                next_reservation=1,
            ),
            {},
            "INR",
        ),
        {},
        Money("0.00", "INR"),
        None,
        id="case-1",
    ),
    pytest.param(
        (
            Inventory(
                levels={("BLR", "X"): StockLevel(warehouse="BLR", sku="X", on_hand=0, reserved=0)},
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="X",
                        delta=1,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="X",
                        delta=-1,
                        reason="lost",
                    ),
                ],
                next_reservation=1,
            ),
            {},
            "INR",
        ),
        {},
        Money("0.00", "INR"),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Inventory(
                levels={("BLR", "X"): StockLevel(warehouse="BLR", sku="X", on_hand=0, reserved=0)},
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="X",
                        delta=0,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="X",
                        delta=-1,
                        reason="lost",
                    ),
                ],
                next_reservation=1,
            ),
            {},
            "INR",
        ),
        {},
        Money("0.00", "INR"),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            Inventory(
                levels={("BLR", "X"): StockLevel(warehouse="BLR", sku="X", on_hand=0, reserved=1)},
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="X",
                        delta=1,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="X",
                        delta=-1,
                        reason="lost",
                    ),
                ],
                next_reservation=1,
            ),
            {},
            "INR",
        ),
        {},
        Money("0.00", "INR"),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            Inventory(
                levels={("BLR", "X"): StockLevel(warehouse="BLR", sku="X", on_hand=0, reserved=0)},
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 8, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="X",
                        delta=1,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="X",
                        delta=-1,
                        reason="lost",
                    ),
                ],
                next_reservation=1,
            ),
            {},
            "INR",
        ),
        {},
        Money("0.00", "INR"),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            Inventory(
                levels={("BLR", "X"): StockLevel(warehouse="BLR", sku="X", on_hand=0, reserved=0)},
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 10, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="X",
                        delta=1,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="X",
                        delta=-1,
                        reason="lost",
                    ),
                ],
                next_reservation=1,
            ),
            {},
            "INR",
        ),
        {},
        Money("0.00", "INR"),
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
                        at=datetime.datetime(2026, 11, 9, 8, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="HOM-0201",
                        delta=2,
                        reason="receipt",
                    ),
                ],
                next_reservation=1,
            ),
            {"ELC-0101": Money("1800.00", "INR"), "HOM-0201": Money("300.00", "INR")},
            "INR",
        ),
        {},
        Money("25800.00", "INR"),
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
                ],
                next_reservation=1,
            ),
            {"ELC-0101": Money("1.00", "INR")},
            "INR",
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
                        delta=5,
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
            {"ELC-0101": Money("1.00", "INR")},
            "INR",
        ),
        {},
        InventoryError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0228(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            stock_value(*args, **kwargs)
    else:
        assert stock_value(*args, **kwargs) == expected
    if after is not None:
        assert args == after
