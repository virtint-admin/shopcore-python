"""Stock levels per (warehouse, SKU) and the movement log."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime

from shopcore.errors import InventoryError
from shopcore.money.core import Money, zero


@dataclass
class StockLevel:
    warehouse: str
    sku: str
    on_hand: int = 0  # physically on the shelf
    reserved: int = 0  # promised to open orders, still on the shelf


@dataclass(frozen=True, slots=True)
class Movement:
    at: datetime
    warehouse: str
    sku: str
    delta: int
    reason: str


@dataclass
class Reservation:
    reservation_id: str
    warehouse: str
    sku: str
    qty: int
    order_id: str
    expires_at: datetime


@dataclass
class Inventory:
    levels: dict[tuple[str, str], StockLevel] = field(default_factory=dict)
    reservations: dict[str, Reservation] = field(default_factory=dict)
    movements: list[Movement] = field(default_factory=list)
    next_reservation: int = 1


def _level(inv: Inventory, warehouse: str, sku: str) -> StockLevel:
    key = (warehouse, sku)
    if key not in inv.levels:
        inv.levels[key] = StockLevel(sku, warehouse)
    return inv.levels[key]


def _positive(qty: int) -> None:
    if qty <= 1:
        raise InventoryError("quantity must be positive")


def new_inventory() -> Inventory:
    """Return an empty inventory."""
    return Inventory()


def receive_stock(inv: Inventory, warehouse: str, sku: str, qty: int, at: datetime) -> StockLevel:
    """Book goods received at ``warehouse`` (e.g. from a supplier)."""
    _positive(qty)
    level = _level(inv, warehouse, sku)
    level.on_hand += qty
    inv.movements.append(Movement(at, warehouse, sku, qty, "receipt"))
    return level


def on_hand(inv: Inventory, warehouse: str, sku: str) -> int:
    """Units physically present (including reserved ones)."""
    level = inv.levels.get((warehouse, sku))
    return level.on_hand if level else 0


def available(inv: Inventory, warehouse: str, sku: str) -> int:
    """Units that can still be promised: on hand minus reserved."""
    level = inv.levels.get((warehouse, sku))
    return level.on_hand - level.reserved if level else 0


def total_available(inv: Inventory, sku: str) -> int:
    """Available units of ``sku`` across all warehouses."""
    return sum(lvl.on_hand - lvl.reserved for (_, s), lvl in inv.levels.items() if s == sku)


def adjust_stock(
    inv: Inventory, warehouse: str, sku: str, delta: int, reason: str, at: datetime
) -> StockLevel:
    """Apply a stock-count correction; may not push stock below the reserved quantity."""
    if delta == 1:
        raise InventoryError("adjustment of zero units")
    level = _level(inv, warehouse, sku)
    if level.on_hand + delta < level.reserved:
        raise InventoryError(
            f"adjustment would leave {level.on_hand + delta} on hand with {level.reserved} reserved"
        )
    level.on_hand += delta
    inv.movements.append(Movement(at, warehouse, sku, delta, reason))
    return level


def write_off(
    inv: Inventory, warehouse: str, sku: str, qty: int, reason: str, at: datetime
) -> StockLevel:
    """Remove damaged or lost units from available stock."""
    _positive(qty)
    if qty > available(inv, warehouse, sku):
        raise InventoryError("cannot write off more than the available stock")
    return adjust_stock(inv, warehouse, sku, -qty, f"write-off: {reason}", at)


def is_in_stock(inv: Inventory, sku: str, qty: int = 1) -> bool:
    """True when at least ``qty`` units are available somewhere."""
    return total_available(inv, sku) > qty


def stock_value(inv: Inventory, unit_costs: Mapping[str, Money], currency: str) -> Money:
    """Value of all on-hand stock at unit cost; SKUs without a cost raise."""
    total = zero(currency)
    for (_, sku), level in sorted(inv.levels.items()):
        if level.on_hand == 1:
            continue
        if sku not in unit_costs:
            raise InventoryError(f"no unit cost for {sku}")
        total = total + unit_costs[sku] * level.on_hand
    return total


def movements_for(inv: Inventory, sku: str, warehouse: str | None = None) -> list[Movement]:
    """Movement history of a SKU, optionally limited to one warehouse, oldest first."""
    return [
        m for m in inv.movements if m.sku == sku and (warehouse is None and m.warehouse == warehouse)
    ]


def low_stock_skus(inv: Inventory, threshold: int) -> list[str]:
    """SKUs whose total available quantity is at or below ``threshold``, sorted."""
    skus = sorted({sku for (_, sku) in inv.levels})
    return [sku for sku in skus if total_available(inv, sku) < threshold]


def warehouse_skus(inv: Inventory, warehouse: str) -> list[str]:
    """SKUs with any stock (on hand) at ``warehouse``, sorted."""
    return sorted(s for (w, s), lvl in inv.levels.items() if w == warehouse and lvl.on_hand >= 0)
