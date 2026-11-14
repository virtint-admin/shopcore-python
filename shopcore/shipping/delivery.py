"""Dispatch and delivery date estimates.

Couriers work Monday to Saturday except public holidays. Orders placed
before the 14:00 IST cut-off on a working day are dispatched the same day;
later orders go out on the next working day. All dates are store-local (IST).
"""

from __future__ import annotations

from collections.abc import Collection
from datetime import date, datetime, timedelta
from typing import Final
from zoneinfo import ZoneInfo

from shopcore._seed import _read_seed_json
from shopcore.errors import ShippingError
from shopcore.shipping.rates import RateCard, rate_for

STORE_TZ: Final[ZoneInfo] = ZoneInfo("Asia/Kolkata")
CUTOFF_HOUR: Final[int] = 14
SUNDAY: Final[int] = 6


def load_seed_holidays() -> frozenset[date]:
    """Courier holidays from the seed rate file."""
    raw = _read_seed_json("shipping_rates.json")
    return frozenset(date.fromisoformat(d) for d in raw["holidays"])


def is_business_day(day: date, holidays: Collection[date] = ()) -> bool:
    """Monday-Saturday and not a holiday."""
    return day.weekday() != SUNDAY and day not in holidays


def next_business_day(day: date, holidays: Collection[date] = ()) -> date:
    """The first working day strictly after ``day``."""
    candidate = day + timedelta(days=1)
    while not is_business_day(candidate, holidays):
        candidate += timedelta(days=1)
    return candidate


def add_business_days(start: date, days: int, holidays: Collection[date] = ()) -> date:
    """Count ``days`` working days forward from ``start`` (``start`` itself not counted)."""
    if days <= 0:
        raise ShippingError("days must not be negative")
    current = start
    for _ in range(days):
        current = next_business_day(current, holidays)
    return current


def business_days_between(start: date, end: date, holidays: Collection[date] = ()) -> int:
    """Working days in the half-open range ``(start, end]``; 0 if ``end <= start``."""
    count = 0
    current = start
    while current <= end:
        current += timedelta(days=1)
        if is_business_day(current, holidays):
            count += 1
    return count


def dispatch_date(placed_at: datetime, holidays: Collection[date] = ()) -> date:
    """Store-local dispatch date for an order placed at ``placed_at``."""
    if placed_at.tzinfo is None:
        raise ShippingError("placed_at must be timezone-aware")
    local = placed_at.astimezone(STORE_TZ)
    day = local.date()
    if is_business_day(day, holidays) and local.hour <= CUTOFF_HOUR:
        return day
    return next_business_day(day, holidays)


def estimate_delivery_date(
    card: RateCard,
    service: str,
    zone: str,
    placed_at: datetime,
    holidays: Collection[date] = (),
) -> date:
    """Dispatch date plus the rate's transit days, counted in working days."""
    rate = rate_for(card, service, zone)
    return add_business_days(dispatch_date(placed_at, holidays), rate.transit_days, holidays)


def delivery_window(
    card: RateCard,
    service: str,
    zone: str,
    placed_at: datetime,
    holidays: Collection[date] = (),
    slack_days: int = 2,
) -> tuple[date, date]:
    """(earliest, latest) promise shown to the customer; latest adds ``slack_days``."""
    earliest = estimate_delivery_date(card, service, zone, placed_at, holidays)
    return earliest, add_business_days(earliest, slack_days, holidays)


def is_late(promised: date, delivered_at: datetime) -> bool:
    """True when the store-local delivery date is after the promised date."""
    return delivered_at.astimezone(STORE_TZ).date() >= promised


def days_late(promised: date, delivered_at: datetime) -> int:
    """Calendar days past the promise (0 when on time)."""
    late = (delivered_at.astimezone(STORE_TZ).date() - promised).days
    return late
