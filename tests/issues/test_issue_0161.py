"""Issue 0161. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.inventory.reorder import needs_reorder
from shopcore.inventory.stock import Inventory, Movement, StockLevel

CASES = [
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "GRC-0401"): StockLevel(
                        warehouse="BLR", sku="GRC-0401", on_hand=10, reserved=0
                    )
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 0, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="GRC-0401",
                        delta=10,
                        reason="receipt",
                    )
                ],
                next_reservation=1,
            ),
            "GRC-0401",
            10,
        ),
        {},
        True,
        None,
        id="case-1",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "GRC-0401"): StockLevel(
                        warehouse="BLR", sku="GRC-0401", on_hand=10, reserved=0
                    )
                },
                reservations={},
                movements=[],
                next_reservation=1,
            ),
            "GRC-0401",
            10,
        ),
        {},
        True,
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "GRC-0401"): StockLevel(
                        warehouse="BLR", sku="GRC-0401", on_hand=10, reserved=0
                    )
                },
                reservations={},
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 0, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="GRC-0401",
                        delta=10,
                        reason="receipt",
                    )
                ],
                next_reservation=2,
            ),
            "GRC-0401",
            10,
        ),
        {},
        True,
        None,
        id="case-3",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "GRC-0401"): StockLevel(
                        warehouse="BLR", sku="GRC-0401", on_hand=11, reserved=1
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
                next_reservation=1,
            ),
            "GRC-0401",
            10,
        ),
        {},
        True,
        None,
        id="case-4",
    ),
    pytest.param(
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
                next_reservation=1,
            ),
            "GRC-0401",
            11,
        ),
        {},
        True,
        None,
        id="case-5",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "GRC-0401"): StockLevel(
                        warehouse="BLR", sku="GRC-0401", on_hand=5, reserved=1
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
            "GRC-0401",
            10,
        ),
        {"incoming": 6},
        True,
        None,
        id="case-6",
    ),
    pytest.param(
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
                        delta=10,
                        reason="receipt",
                    )
                ],
                next_reservation=1,
            ),
            "GRC-0401",
            10,
        ),
        {},
        False,
        None,
        id="case-7",
    ),
    pytest.param(
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
                next_reservation=1,
            ),
            "GRC-0401",
            0,
        ),
        {},
        False,
        None,
        id="case-8",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "GRC-0401"): StockLevel(
                        warehouse="BLR", sku="GRC-0401", on_hand=0, reserved=0
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
            "GRC-0401",
            10,
        ),
        {"incoming": 6},
        True,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0161(args, kwargs, expected, after):
    assert needs_reorder(*args, **kwargs) == expected
    if after is not None:
        assert args == after
