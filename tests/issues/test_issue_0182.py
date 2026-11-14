"""Issue 0182. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.errors import InventoryError
from shopcore.inventory.reservations import split_reservation
from shopcore.inventory.stock import Inventory, Movement, Reservation, StockLevel

CASES = [
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=3
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=3,
                        order_id="O0",
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
                next_reservation=2,
            ),
            "ELC-0101",
            4,
            "O1",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM", "DEL"],
        ),
        {},
        [
            Reservation(
                reservation_id="R000002",
                warehouse="BOM",
                sku="ELC-0101",
                qty=4,
                order_id="O1",
                expires_at=datetime.datetime(2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc),
            )
        ],
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=3
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=4
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=3,
                        order_id="O0",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc
                        ),
                    ),
                    "R000002": Reservation(
                        reservation_id="R000002",
                        warehouse="BOM",
                        sku="ELC-0101",
                        qty=4,
                        order_id="O1",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc
                        ),
                    ),
                },
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
                next_reservation=3,
            ),
            "ELC-0101",
            4,
            "O1",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM", "DEL"],
        ),
        id="case-1",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=3
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=-1
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=3,
                        order_id="O0",
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
                next_reservation=2,
            ),
            "ELC-0101",
            4,
            "O1",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM", "DEL"],
        ),
        {},
        [
            Reservation(
                reservation_id="R000002",
                warehouse="BOM",
                sku="ELC-0101",
                qty=4,
                order_id="O1",
                expires_at=datetime.datetime(2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc),
            )
        ],
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=3
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=3
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=3,
                        order_id="O0",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc
                        ),
                    ),
                    "R000002": Reservation(
                        reservation_id="R000002",
                        warehouse="BOM",
                        sku="ELC-0101",
                        qty=4,
                        order_id="O1",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc
                        ),
                    ),
                },
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
                next_reservation=3,
            ),
            "ELC-0101",
            4,
            "O1",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM", "DEL"],
        ),
        id="case-2",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=3
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=3,
                        order_id="O0",
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
                next_reservation=2,
            ),
            "ELC-0101",
            4,
            "O1",
            datetime.datetime(2026, 11, 10, 9, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM", "DEL"],
        ),
        {},
        [
            Reservation(
                reservation_id="R000002",
                warehouse="BOM",
                sku="ELC-0101",
                qty=4,
                order_id="O1",
                expires_at=datetime.datetime(2026, 11, 10, 9, 30, tzinfo=datetime.timezone.utc),
            )
        ],
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=3
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=4
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=3,
                        order_id="O0",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc
                        ),
                    ),
                    "R000002": Reservation(
                        reservation_id="R000002",
                        warehouse="BOM",
                        sku="ELC-0101",
                        qty=4,
                        order_id="O1",
                        expires_at=datetime.datetime(
                            2026, 11, 10, 9, 30, tzinfo=datetime.timezone.utc
                        ),
                    ),
                },
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
                next_reservation=3,
            ),
            "ELC-0101",
            4,
            "O1",
            datetime.datetime(2026, 11, 10, 9, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM", "DEL"],
        ),
        id="case-3",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=3
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=3,
                        order_id="O0",
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
                next_reservation=2,
            ),
            "ELC-0101",
            4,
            "O1",
            datetime.datetime(2026, 11, 9, 8, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM", "DEL"],
        ),
        {},
        [
            Reservation(
                reservation_id="R000002",
                warehouse="BOM",
                sku="ELC-0101",
                qty=4,
                order_id="O1",
                expires_at=datetime.datetime(2026, 11, 9, 8, 30, tzinfo=datetime.timezone.utc),
            )
        ],
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=3
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=4
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=3,
                        order_id="O0",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc
                        ),
                    ),
                    "R000002": Reservation(
                        reservation_id="R000002",
                        warehouse="BOM",
                        sku="ELC-0101",
                        qty=4,
                        order_id="O1",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 8, 30, tzinfo=datetime.timezone.utc
                        ),
                    ),
                },
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
                next_reservation=3,
            ),
            "ELC-0101",
            4,
            "O1",
            datetime.datetime(2026, 11, 9, 8, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM", "DEL"],
        ),
        id="case-4",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=3
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=3,
                        order_id="O0",
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
                        delta=3,
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
                        delta=5,
                        reason="receipt",
                    ),
                ],
                next_reservation=2,
            ),
            "ELC-0101",
            4,
            "O1",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM", "DEL"],
        ),
        {},
        [
            Reservation(
                reservation_id="R000002",
                warehouse="BOM",
                sku="ELC-0101",
                qty=4,
                order_id="O1",
                expires_at=datetime.datetime(2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc),
            )
        ],
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=3
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=4
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=3,
                        order_id="O0",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc
                        ),
                    ),
                    "R000002": Reservation(
                        reservation_id="R000002",
                        warehouse="BOM",
                        sku="ELC-0101",
                        qty=4,
                        order_id="O1",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc
                        ),
                    ),
                },
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
                        delta=0,
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
                next_reservation=3,
            ),
            "ELC-0101",
            4,
            "O1",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM", "DEL"],
        ),
        id="case-5",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=3
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=3,
                        order_id="O0",
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
                next_reservation=2,
            ),
            "ELC-0101",
            4,
            "O1",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM"],
        ),
        {},
        [
            Reservation(
                reservation_id="R000002",
                warehouse="BOM",
                sku="ELC-0101",
                qty=4,
                order_id="O1",
                expires_at=datetime.datetime(2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc),
            )
        ],
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=3
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=4
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=3,
                        order_id="O0",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc
                        ),
                    ),
                    "R000002": Reservation(
                        reservation_id="R000002",
                        warehouse="BOM",
                        sku="ELC-0101",
                        qty=4,
                        order_id="O1",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc
                        ),
                    ),
                },
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
                next_reservation=3,
            ),
            "ELC-0101",
            4,
            "O1",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM"],
        ),
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
                        at=datetime.datetime(2026, 11, 8, 9, 0, tzinfo=datetime.timezone.utc),
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
            5,
            "O1",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM", "DEL"],
        ),
        {},
        [
            Reservation(
                reservation_id="R000001",
                warehouse="BLR",
                sku="ELC-0101",
                qty=3,
                order_id="O1",
                expires_at=datetime.datetime(2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc),
            ),
            Reservation(
                reservation_id="R000002",
                warehouse="BOM",
                sku="ELC-0101",
                qty=2,
                order_id="O1",
                expires_at=datetime.datetime(2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc),
            ),
        ],
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=3
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=2
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=3,
                        order_id="O1",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc
                        ),
                    ),
                    "R000002": Reservation(
                        reservation_id="R000002",
                        warehouse="BOM",
                        sku="ELC-0101",
                        qty=2,
                        order_id="O1",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc
                        ),
                    ),
                },
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=3,
                        reason="receipt",
                    ),
                    Movement(
                        at=datetime.datetime(2026, 11, 8, 9, 0, tzinfo=datetime.timezone.utc),
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
                next_reservation=3,
            ),
            "ELC-0101",
            5,
            "O1",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM", "DEL"],
        ),
        id="case-7",
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
            2,
            "O1",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM", "DEL"],
        ),
        {},
        [
            Reservation(
                reservation_id="R000001",
                warehouse="BLR",
                sku="ELC-0101",
                qty=2,
                order_id="O1",
                expires_at=datetime.datetime(2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc),
            )
        ],
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=2
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
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
                next_reservation=2,
            ),
            "ELC-0101",
            2,
            "O1",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM", "DEL"],
        ),
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
                        at=datetime.datetime(2026, 11, 10, 9, 0, tzinfo=datetime.timezone.utc),
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
            0,
            "O1",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            ["BLR", "BOM", "DEL"],
        ),
        {},
        InventoryError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0182(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            split_reservation(*args, **kwargs)
    else:
        assert split_reservation(*args, **kwargs) == expected
    if after is not None:
        assert args == after
