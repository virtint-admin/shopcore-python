"""Order data types shared by the orders sub-modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from shopcore.money.core import Money


class OrderStatus(StrEnum):
    PENDING_PAYMENT = "pending_payment"
    PAID = "paid"
    PACKED = "packed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"
    REFUNDED = "refunded"


@dataclass
class OrderLine:
    sku: str
    qty: int
    unit_price: Money
    tax: Money  # tax for the whole line (all ``qty`` units)
    category: str = ""
    cancelled_qty: int = 0


@dataclass(frozen=True, slots=True)
class Refund:
    refund_id: str
    amount: Money
    at: datetime
    reason: str


@dataclass
class Order:
    order_id: str
    customer_id: str
    currency: str
    region: str
    lines: list[OrderLine]
    shipping: Money
    placed_at: datetime
    status: OrderStatus = OrderStatus.PENDING_PAYMENT
    history: list[tuple[OrderStatus, datetime]] = field(default_factory=list)
    paid: Money | None = None
    refunds: list[Refund] = field(default_factory=list)
