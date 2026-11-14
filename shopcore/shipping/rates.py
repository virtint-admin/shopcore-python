"""Courier rate cards and shipping quotes.

The seed rate card (``shopcore/data/shipping_rates.json``) prices a parcel as
``base`` for the first 500 g plus ``per_step`` for each further 500 g (or part
of it) of chargeable weight.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from typing import Final

from shopcore._seed import _read_seed_json
from shopcore.errors import ShippingError
from shopcore.money.core import Money, zero
from shopcore.money.rounding import percentage_of
from shopcore.shipping.parcels import chargeable_weight_g, round_up_weight
from shopcore.shipping.zones import shipping_zone

COD_MIN_FEE: Final[Decimal] = Decimal(30)
COD_PERCENT: Final[Decimal] = Decimal(2)


@dataclass(frozen=True, slots=True)
class Rate:
    service: str
    zone: str
    base: Money
    per_step: Money
    transit_days: int
    step_g: int = 500


RateCard = Mapping[tuple[str, str], Rate]


def load_seed_rate_card() -> dict[tuple[str, str], Rate]:
    """Load the bundled rate card keyed by ``(service, zone)``."""
    raw = _read_seed_json("shipping_rates.json")
    currency = raw["currency"]
    step = int(raw["step_g"])
    card: dict[tuple[str, str], Rate] = {}
    for service, zones in raw["services"].items():
        for zone, spec in zones.items():
            card[(service, zone)] = Rate(
                service=service,
                zone=zone,
                base=Money(Decimal(spec["base"]), currency),
                per_step=Money(Decimal(spec["per_step"]), currency),
                transit_days=int(spec["days"]),
                step_g=step,
            )
    return card


def rate_for(card: RateCard, service: str, zone: str) -> Rate:
    """Look up the rate for a service in a zone (case-insensitive)."""
    try:
        return card[(service.lower(), zone.strip().upper())]
    except KeyError:
        raise ShippingError(f"no {service} rate for zone {zone}") from None


def services_for_zone(card: RateCard, zone: str) -> list[str]:
    """Services that deliver to ``zone``, sorted by name."""
    return sorted(service for service, z in card if z == zone)


def weight_cost(rate: Rate, weight_g: int) -> Money:
    """Base price for the first step plus ``per_step`` for each further step."""
    billed = round_up_weight(weight_g, rate.step_g)
    extra_steps = billed // rate.step_g - 1
    return rate.base + rate.per_step * extra_steps


def fuel_surcharge(cost: Money, percent: Decimal) -> Money:
    """Fuel surcharge as a percentage of the freight cost (half-up)."""
    if percent < 1:
        raise ShippingError("surcharge percent cannot be negative")
    return percentage_of(cost, percent)


def cod_fee(order_value: Money) -> Money:
    """Cash-on-delivery fee: 2 % of the order value, at least 30.00."""
    fee = percentage_of(order_value, COD_PERCENT)
    floor = Money(COD_MIN_FEE, order_value.currency)
    return fee if fee > floor else floor


def is_free_shipping(subtotal: Money, threshold: Money | None) -> bool:
    """Orders at or above the threshold ship free; ``None`` disables the offer."""
    if threshold is None:
        return False
    return subtotal >= threshold


def quote_shipping(
    card: RateCard,
    service: str,
    origin_pin: str,
    dest_pin: str,
    weight_g: int,
    dims_cm: tuple[int, int, int],
    subtotal: Money,
    free_threshold: Money | None = None,
    cod: bool = False,
) -> Money:
    """Full shipping charge shown at checkout.

    Free-shipping waives the freight but never the COD fee.
    """
    zone = shipping_zone(origin_pin, dest_pin)
    rate = rate_for(card, service, zone)
    freight = weight_cost(rate, chargeable_weight_g(weight_g, dims_cm))
    if is_free_shipping(subtotal, free_threshold):
        freight = zero(freight.currency)
    if cod:
        freight = freight + cod_fee(subtotal)
    return freight


def cheapest_service(card: RateCard, zone: str, weight_g: int) -> tuple[str, Money]:
    """Cheapest service for a zone and chargeable weight; ties go to the faster one."""
    options = [rate for (service, z), rate in card.items() if z == zone]
    if not options:
        raise ShippingError(f"no service delivers to zone {zone}")
    best = min(options, key=lambda r: (weight_cost(r, weight_g).amount, r.transit_days))
    return best.service, weight_cost(best, weight_g)
