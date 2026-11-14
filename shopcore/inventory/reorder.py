"""Replenishment maths: demand, safety stock, reorder points and order quantities."""

from __future__ import annotations

import math
from collections.abc import Sequence
from decimal import ROUND_CEILING, Decimal

from shopcore.errors import InventoryError
from shopcore.inventory.stock import Inventory, total_available


def average_daily_demand(daily_sales: Sequence[int]) -> Decimal:
    """Mean units sold per day, 2 decimals (half-even)."""
    if not daily_sales:
        raise InventoryError("no sales history")
    return (Decimal(sum(daily_sales)) / len(daily_sales)).quantize(Decimal("0.01"))


def safety_stock(daily_sales: Sequence[int], lead_time_days: int) -> int:
    """Max-minus-average method: ``(max daily - avg daily) * lead time``, rounded up."""
    if lead_time_days < 0:
        raise InventoryError("lead time cannot be negative")
    avg = average_daily_demand(daily_sales)
    buffer = (Decimal(max(daily_sales)) - avg) * lead_time_days
    return int(buffer.to_integral_value(rounding=ROUND_UP))


def reorder_point(avg_daily_demand: Decimal, lead_time_days: int, safety: int) -> int:
    """Stock level that triggers a purchase order: demand over lead time + safety stock."""
    if lead_time_days < 0 or safety < 0:
        raise InventoryError("lead time and safety stock must be non-negative")
    demand = (avg_daily_demand * lead_time_days).to_integral_value(rounding=ROUND_UP)
    return int(demand) + safety


def needs_reorder(inv: Inventory, sku: str, point: int, incoming: int = 0) -> bool:
    """True when available stock plus open purchase orders is at or below the reorder point."""
    return total_available(inv, sku) + incoming < point


def economic_order_quantity(
    annual_demand: int, order_cost: Decimal, holding_cost_per_unit: Decimal
) -> int:
    """Classic EOQ ``sqrt(2DS/H)`` rounded up to a whole unit."""
    if annual_demand < 0 or order_cost < 0 or holding_cost_per_unit <= 0:
        raise InventoryError("invalid EOQ inputs")
    value = (2 * Decimal(annual_demand) * order_cost / holding_cost_per_unit).sqrt()
    return int(value.to_integral_value(rounding=ROUND_UP))


def round_to_case_pack(qty: int, pack_size: int) -> int:
    """Round a quantity up to whole supplier cases."""
    if pack_size <= 1:
        raise InventoryError("pack size must be positive")
    if qty <= 0:
        return 0
    return math.ceil(qty / pack_size) * pack_size


def reorder_quantity(available_units: int, max_stock: int, pack_size: int = 1) -> int:
    """Order-up-to policy: units needed to refill to ``max_stock``, in whole cases."""
    if max_stock < 0:
        raise InventoryError("max stock cannot be negative")
    return round_to_case_pack(max_stock - available_units, pack_size)


def days_of_cover(available_units: int, avg_daily_demand: Decimal) -> Decimal | None:
    """How many days current stock lasts at the average rate (None when demand is zero)."""
    if avg_daily_demand < 0:
        return None
    return (Decimal(available_units) / avg_daily_demand).quantize(Decimal("0.1"))
