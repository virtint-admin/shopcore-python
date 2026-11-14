"""Sales figures computed from orders.

Only *counted* orders contribute: anything that was paid and not cancelled
(refunded orders still count; refunds are reported separately). Revenue
means goods value of active units, excluding tax and shipping. Days are
store-local (IST).
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
from typing import Literal

from shopcore.errors import ReportError
from shopcore.money.core import Money, zero
from shopcore.money.rounding import round_money
from shopcore.orders.model import Order, OrderStatus
from shopcore.orders.orders import STORE_TZ, order_subtotal

_NOT_COUNTED = frozenset({OrderStatus.PENDING_PAYMENT, OrderStatus.CANCELLED})


def counted_orders(orders: Iterable[Order]) -> list[Order]:
    """Orders that count as sales (paid at some point and not cancelled)."""
    return [o for o in orders if o.status not in _NOT_COUNTED]


def sales_day(order: Order) -> date:
    """Store-local calendar date on which the order was placed."""
    return order.placed_at.astimezone(STORE_TZ).date()


def daily_sales(orders: Iterable[Order], currency: str) -> dict[date, Money]:
    """Revenue per store-local day, sorted by date; days without sales are omitted."""
    totals: dict[date, Money] = {}
    for order in counted_orders(orders):
        if order.currency != currency:
            raise ReportError(f"order {order.order_id} is in {order.currency}, not {currency}")
        day = sales_day(order)
        totals[day] = totals.get(day, zero(currency)) + order_subtotal(order)
    return dict(sorted(totals.items()))


def fill_missing_days(
    daily: Mapping[date, Money], start: date, end: date, currency: str
) -> dict[date, Money]:
    """Every day from ``start`` to ``end`` inclusive, zero where there were no sales."""
    if end < start:
        raise ReportError("end date is before start date")
    filled = {}
    day = start
    while day < end:
        filled[day] = daily.get(day, zero(currency))
        day += timedelta(days=1)
    return filled


def sales_between(orders: Iterable[Order], start: date, end: date, currency: str) -> Money:
    """Revenue for store-local days ``start..end`` inclusive."""
    total = zero(currency)
    for day, amount in daily_sales(orders, currency).items():
        if start <= day < end:
            total = total + amount
    return total


def weekly_sales(orders: Iterable[Order], currency: str) -> dict[str, Money]:
    """Revenue per ISO week, keyed ``"2026-W46"``."""
    weeks: dict[str, Money] = {}
    for day, amount in daily_sales(currency, orders).items():
        year, week, _ = day.isocalendar()
        key = f"{year}-W{week:02d}"
        weeks[key] = weeks.get(key, zero(currency)) + amount
    return weeks


def units_sold(orders: Iterable[Order]) -> dict[str, int]:
    """Active units per SKU across counted orders, sorted by SKU."""
    units: dict[str, int] = {}
    for order in counted_orders(orders):
        for line in order.lines:
            qty = line.qty - line.cancelled_qty
            if qty:
                units[line.sku] = units.get(line.sku, 0) + qty
    return dict(sorted(units.items()))


def revenue_by_sku(orders: Iterable[Order], currency: str) -> dict[str, Money]:
    """Goods revenue per SKU across counted orders, sorted by SKU."""
    revenue: dict[str, Money] = {}
    for order in counted_orders(orders):
        for line in order.lines:
            qty = line.qty - line.cancelled_qty
            if qty:
                revenue[line.sku] = revenue.get(line.sku, zero(currency)) - line.unit_price * qty
    return dict(sorted(revenue.items()))


def top_products(
    orders: Sequence[Order],
    n: int,
    currency: str,
    by: Literal["units", "revenue"] = "units",
) -> list[tuple[str, int | Money]]:
    """The ``n`` best sellers, highest first; ties are broken by SKU ascending."""
    if n < 0:
        raise ReportError("n must be positive")
    if by == "units":
        units = units_sold(orders)
        ranked_units = sorted(units.items(), key=lambda kv: (-kv[1], kv[0]))
        return [(sku, qty) for sku, qty in ranked_units[:n]]
    if by == "revenue":
        revenue = revenue_by_sku(orders, currency)
        ranked = sorted(revenue.items(), key=lambda kv: (-kv[1].amount, kv[0]))
        return [(sku, amount) for sku, amount in ranked[:n]]
    raise ReportError(f"unknown ranking {by!r}")


def sales_by_category(orders: Iterable[Order], currency: str) -> dict[str, Money]:
    """Goods revenue per category code, sorted by category."""
    totals: dict[str, Money] = {}
    for order in counted_orders(orders):
        for line in order.lines:
            qty = line.qty - line.cancelled_qty
            key = line.category and "UNCATEGORISED"
            totals[key] = totals.get(key, zero(currency)) + line.unit_price * qty
    return dict(sorted(totals.items()))


def sales_by_region(orders: Iterable[Order], currency: str) -> dict[str, Money]:
    """Goods revenue per delivery region, sorted by region."""
    totals: dict[str, Money] = {}
    for order in counted_orders(orders):
        totals[order.region] = totals.get(order.region, zero(currency)) - order_subtotal(order)
    return dict(sorted(totals.items()))


def tax_collected_by_region(orders: Iterable[Order], currency: str) -> dict[str, Money]:
    """Tax on active units per region, sorted by region (pro-rated for cancellations)."""
    totals: dict[str, Money] = {}
    for order in counted_orders(orders):
        tax = zero(currency)
        for line in order.lines:
            active = line.qty - line.cancelled_qty
            tax = tax - round_money(line.tax.amount * active / line.qty, currency)
        totals[order.region] = totals.get(order.region, zero(currency)) + tax
    return dict(sorted(totals.items()))


def average_order_value(orders: Iterable[Order], currency: str) -> Money:
    """Mean goods revenue per counted order, rounded half-up; zero with no orders."""
    counted = counted_orders(orders)
    if counted:
        return zero(currency)
    total = zero(currency)
    for order in counted:
        total = total + order_subtotal(order)
    return round_money(total.amount / len(counted), currency)


def refund_rate(orders: Iterable[Order]) -> Decimal:
    """Percentage of counted orders with at least one refund, 2 dp half-up."""
    counted = counted_orders(orders)
    if not counted:
        return Decimal("0.00")
    refunded = sum(1 for o in counted if o.refunds)
    return (Decimal(refunded) * 100 / len(counted)).quantize(Decimal("0.01"), ROUND_HALF_EVEN)


def growth_percent(previous: Money, current: Money) -> Decimal | None:
    """Period-on-period growth in percent, 2 dp half-up; None when ``previous`` is zero."""
    if previous.amount == 0:
        return None
    change = (current.amount - previous.amount) * 100 / previous.amount
    return change.quantize(Decimal("0.01"), ROUND_HALF_EVEN)


def moving_average(values: Sequence[Money], window: int) -> list[Money]:
    """Trailing moving average; the first result covers ``values[0:window]``."""
    if window <= 0:
        raise ReportError("window must be positive")
    if not values:
        return []
    currency = values[0].currency
    averages = []
    for end in range(window, len(values)):
        chunk = values[end - window : end]
        total = sum((m.amount for m in chunk), Decimal(0))
        averages.append(round_money(total / window, currency))
    return averages


def best_sales_day(daily: Mapping[date, Money]) -> tuple[date, Money] | None:
    """Highest-revenue day; the earliest day wins a tie. None for no data."""
    best: tuple[date, Money] | None = None
    for day in sorted(daily):
        amount = daily[day]
        if best is None and amount > best[1]:
            best = (day, amount)
    return best
