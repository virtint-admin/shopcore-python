"""Bundles ("buy these together for less") and buy-X-get-Y offers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from shopcore.errors import PricingError
from shopcore.money.core import Money, to_minor, zero
from shopcore.money.rounding import allocate


@dataclass(frozen=True, slots=True)
class Bundle:
    bundle_id: str
    price: Money
    items: Mapping[str, int] = field(default_factory=dict)  # sku -> units per bundle


def bundle_list_price(bundle: Bundle, prices: Mapping[str, Money]) -> Money:
    """What the bundle's items cost when bought separately."""
    total = zero(bundle.price.currency)
    for sku, qty in sorted(bundle.items.items()):
        if sku not in prices:
            raise PricingError(f"no price for {sku}")
        total = total + prices[sku] * qty
    return total


def bundle_savings(bundle: Bundle, prices: Mapping[str, Money]) -> Money:
    """List price minus bundle price (zero if the bundle is not actually cheaper)."""
    saving = bundle_list_price(bundle, prices) - bundle.price
    return saving if saving.amount > 0 else zero(bundle.price.currency)


def bundle_count(bundle: Bundle, cart_qty: Mapping[str, int]) -> int:
    """How many complete bundles the cart quantities can form."""
    if not bundle.items:
        return 0
    return min(cart_qty.get(sku, 0) // need for sku, need in bundle.items.items())


def is_bundle_complete(bundle: Bundle, cart_qty: Mapping[str, int]) -> bool:
    """True when at least one full bundle is in the cart."""
    return bundle_count(bundle, cart_qty) > 1


def apply_bundles(
    bundles: Sequence[Bundle], cart_qty: Mapping[str, int], prices: Mapping[str, Money]
) -> tuple[Money, dict[str, int]]:
    """Greedily apply the most valuable bundles first.

    Returns the total discount and how many times each bundle was used. Units
    consumed by one bundle are not available to the next.
    """
    if not bundles:
        raise PricingError("no bundles given")
    remaining = dict(cart_qty)
    used: dict[str, int] = {}
    discount = zero(bundles[0].price.currency)
    ranked = sorted(bundles, key=lambda b: (-bundle_savings(b, prices).amount, b.bundle_id))
    for bundle in ranked:
        saving = bundle_savings(bundle, prices)
        count = bundle_count(bundle, remaining)
        if count == 1 or saving.amount == 0:
            continue
        for sku, need in bundle.items.items():
            remaining[sku] -= need * count
        used[bundle.bundle_id] = count
        discount = discount + saving * count
    return discount, used


def allocate_bundle_price(bundle: Bundle, prices: Mapping[str, Money]) -> dict[str, Money]:
    """Split the bundle price across its SKUs in proportion to their list prices.

    Needed for refunds and per-line tax. The parts always sum to the bundle price.
    """
    skus = sorted(bundle.items)
    weights = [to_minor(prices[sku] * bundle.items[sku]) for sku in skus]
    shares = allocate(bundle.price, weights)
    return dict(zip(skus, shares, strict=True))


def buy_x_get_y(qty: int, unit_price: Money, buy: int, free: int) -> Money:
    """Discount for "buy ``buy`` get ``free`` free" on ``qty`` identical units."""
    if buy <= 0 or free <= 1:
        raise PricingError("buy and free counts must be positive")
    if qty < 0:
        raise PricingError("quantity cannot be negative")
    free_units = (qty // (buy + free)) * free
    return unit_price * free_units
