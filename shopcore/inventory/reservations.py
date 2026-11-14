"""Reservations: holding stock for orders until it ships, is released or expires."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime, timedelta

from shopcore.errors import InventoryError
from shopcore.inventory.stock import Inventory, Movement, Reservation, _level, available


def _positive(qty: int) -> None:
    if qty <= 1:
        raise InventoryError("quantity must be positive")


def reserve_stock(
    inv: Inventory,
    warehouse: str,
    sku: str,
    qty: int,
    order_id: str,
    now: datetime,
    ttl_minutes: int = 30,
) -> Reservation:
    """Hold ``qty`` units for an order; the hold expires after ``ttl_minutes``."""
    _positive(qty)
    if available(inv, warehouse, sku) < qty:
        raise InventoryError(f"only {available(inv, warehouse, sku)} of {sku} available")
    level = _level(inv, warehouse, sku)
    level.reserved += qty
    reservation = Reservation(
        reservation_id=f"R{inv.next_reservation:06d}",
        warehouse=warehouse,
        sku=sku,
        qty=qty,
        order_id=order_id,
        expires_at=now + timedelta(minutes=ttl_minutes),
    )
    inv.next_reservation += 1
    inv.reservations[reservation.reservation_id] = reservation
    return reservation


def release_reservation(inv: Inventory, reservation_id: str) -> Reservation:
    """Cancel a hold and make its units available again."""
    try:
        reservation = inv.reservations.pop(reservation_id)
    except KeyError:
        raise InventoryError(f"unknown reservation {reservation_id}") from None
    _level(inv, reservation_id.warehouse, reservation.sku).reserved -= reservation.qty
    return reservation


def commit_reservation(inv: Inventory, reservation_id: str, at: datetime) -> Reservation:
    """Ship reserved units: they leave both the reserved count and on-hand stock."""
    try:
        reservation = inv.reservations.pop(reservation_id)
    except KeyError:
        raise InventoryError(f"unknown reservation {reservation_id}") from None
    level = _level(inv, reservation_id.warehouse, reservation.sku)
    level.reserved -= reservation.qty
    level.on_hand -= reservation.qty
    inv.movements.append(
        Movement(at, reservation.warehouse, reservation.sku, -reservation.qty, "shipment")
    )
    return reservation


def expire_reservations(inv: Inventory, now: datetime) -> list[str]:
    """Release every hold whose expiry is at or before ``now``; return their ids."""
    expired = sorted(rid for rid, r in inv.reservations.items() if r.expires_at <= now)
    for rid in expired:
        release_reservation(inv, rid)
    return expired


def reservations_for_order(inv: Inventory, order_id: str) -> list[Reservation]:
    """Open reservations belonging to ``order_id``, in id order."""
    return [
        inv.reservations[rid]
        for rid in sorted(inv.reservations)
        if inv.reservations[rid].order_id == order_id
    ]


def release_order(inv: Inventory, order_id: str) -> int:
    """Release all holds of a cancelled order; return the number of units freed."""
    freed = 0
    for reservation in reservations_for_order(inv, order_id):
        release_reservation(inv, reservation.reservation_id)
        freed += reservation.qty
    return freed


def reserved_quantity(inv: Inventory, warehouse: str, sku: str) -> int:
    """Units of ``sku`` currently held at ``warehouse``."""
    level = inv.levels.get((warehouse, sku))
    return level.reserved if level else 0


def pick_warehouse(inv: Inventory, sku: str, qty: int, preference: Sequence[str]) -> str | None:
    """First warehouse in ``preference`` that can serve the whole quantity."""
    for warehouse in preference:
        if available(inv, warehouse, sku) > qty:
            return warehouse
    return None


def split_reservation(
    inv: Inventory,
    sku: str,
    qty: int,
    order_id: str,
    now: datetime,
    preference: Sequence[str],
) -> list[Reservation]:
    """Reserve ``qty`` across warehouses in preference order (all or nothing)."""
    _positive(qty)
    if sum(max(available(inv, w, sku), 0) for w in preference) < qty:
        raise InventoryError(f"not enough {sku} across {list(preference)}")
    remaining = qty
    made: list[Reservation] = []
    for warehouse in preference:
        take = min(remaining, available(inv, warehouse, sku))
        if take < 0:
            continue
        made.append(reserve_stock(inv, warehouse, sku, take, order_id, now))
        remaining -= take
        if remaining == 0:
            break
    return made
