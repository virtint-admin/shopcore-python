"""Issue 0203. Make this test pass by fixing the application code, not the test."""

import datetime
import zoneinfo

import pytest

from shopcore.inventory.reservations import expire_reservations
from shopcore.inventory.stock import Inventory, Movement, Reservation, StockLevel

CASES = [
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=1
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
                        qty=1,
                        order_id="O1",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 10, tzinfo=datetime.timezone.utc
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
            datetime.datetime(2026, 11, 9, 9, 10, tzinfo=datetime.timezone.utc),
        ),
        {},
        ["R000001"],
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
                next_reservation=2,
            ),
            datetime.datetime(2026, 11, 9, 9, 10, tzinfo=datetime.timezone.utc),
        ),
        id="case-1",
    ),
    pytest.param(
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
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=1,
                        order_id="O1",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 10, tzinfo=datetime.timezone.utc
                        ),
                    ),
                    "R000002": Reservation(
                        reservation_id="R000002",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=1,
                        order_id="O2",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc
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
            datetime.datetime(2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc),
        ),
        {},
        ["R000001"],
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=1
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000002": Reservation(
                        reservation_id="R000002",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=1,
                        order_id="O2",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc
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
                next_reservation=3,
            ),
            datetime.datetime(2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc),
        ),
        id="case-2",
    ),
    pytest.param(
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
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000001": Reservation(
                        reservation_id="R000001",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=1,
                        order_id="O1",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 10, tzinfo=datetime.timezone.utc
                        ),
                    ),
                    "R000002": Reservation(
                        reservation_id="R000002",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=1,
                        order_id="O2",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc
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
                        delta=5,
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
            datetime.datetime(2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc),
        ),
        {},
        ["R000001"],
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=1
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=4, reserved=0
                    ),
                    ("DEL", "ELC-0101"): StockLevel(
                        warehouse="DEL", sku="ELC-0101", on_hand=5, reserved=0
                    ),
                },
                reservations={
                    "R000002": Reservation(
                        reservation_id="R000002",
                        warehouse="BLR",
                        sku="ELC-0101",
                        qty=1,
                        order_id="O2",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc
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
                        delta=5,
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
            datetime.datetime(2026, 11, 9, 9, 30, tzinfo=datetime.timezone.utc),
        ),
        id="case-3",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=1
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
                        qty=1,
                        order_id="O1",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 10, tzinfo=datetime.timezone.utc
                        ),
                    )
                },
                movements=[
                    Movement(
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        warehouse="BLR",
                        sku="ELC-0101",
                        delta=4,
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
            datetime.datetime(2026, 11, 9, 9, 10, tzinfo=datetime.timezone.utc),
        ),
        {},
        ["R000001"],
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
                        delta=4,
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
            datetime.datetime(2026, 11, 9, 9, 10, tzinfo=datetime.timezone.utc),
        ),
        id="case-4",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=1
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
                        qty=1,
                        order_id="O1",
                        expires_at=datetime.datetime(
                            2026, 11, 9, 9, 10, tzinfo=datetime.timezone.utc
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
                        at=datetime.datetime(2026, 11, 9, 8, 0, tzinfo=datetime.timezone.utc),
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
            datetime.datetime(2026, 11, 9, 9, 10, tzinfo=datetime.timezone.utc),
        ),
        {},
        ["R000001"],
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
                        at=datetime.datetime(2026, 11, 9, 8, 0, tzinfo=datetime.timezone.utc),
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
            datetime.datetime(2026, 11, 9, 9, 10, tzinfo=datetime.timezone.utc),
        ),
        id="case-5",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=1
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=5, reserved=0
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
                        qty=1,
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
            datetime.datetime(2026, 11, 9, 15, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        ["R000001"],
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=0
                    ),
                    ("BOM", "ELC-0101"): StockLevel(
                        warehouse="BOM", sku="ELC-0101", on_hand=5, reserved=0
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
                next_reservation=2,
            ),
            datetime.datetime(2026, 11, 9, 15, 0, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        id="case-6",
    ),
    pytest.param(
        (
            Inventory(
                levels={
                    ("BLR", "ELC-0101"): StockLevel(
                        warehouse="BLR", sku="ELC-0101", on_hand=4, reserved=1
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
                        qty=1,
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
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
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
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=1
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
                        qty=1,
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
                ],
                next_reservation=2,
            ),
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
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
                        warehouse="BLR", sku="ELC-0101", on_hand=3, reserved=1
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
                        qty=1,
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
            datetime.datetime(2026, 11, 9, 14, 59, tzinfo=zoneinfo.ZoneInfo(key="Asia/Kolkata")),
        ),
        {},
        [],
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0203(args, kwargs, expected, after):
    assert expire_reservations(*args, **kwargs) == expected
    if after is not None:
        assert args == after
