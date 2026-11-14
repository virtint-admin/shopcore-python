"""Regional tax rules: which rate applies where, and whether shipping is taxed.

Regions use ISO 3166-2 style codes: ``IN-KA`` (Karnataka), ``IN-MH``
(Maharashtra), ``US-NY``, or a bare country code for VAT countries (``DE``,
``GB``). Seed rules live in ``shopcore/data/tax_rules.json``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Final

from shopcore._seed import _read_seed_json
from shopcore.errors import TaxError
from shopcore.money.core import Money, zero
from shopcore.money.rounding import round_money


@dataclass(frozen=True, slots=True)
class TaxRule:
    region: str
    name: str
    rate: Decimal  # percent, e.g. Decimal("18")
    inclusive: bool  # True when shelf prices already contain the tax (EU VAT)
    taxes_shipping: bool
    category_rates: Mapping[str, Decimal] = field(default_factory=dict)


REGION_ALIASES: Final[dict[str, str]] = {
    "KARNATAKA": "IN-KA",
    "MAHARASHTRA": "IN-MH",
    "DELHI": "IN-DL",
    "TAMIL NADU": "IN-TN",
    "NEW YORK": "US-NY",
    "OREGON": "US-OR",
    "GERMANY": "DE",
    "UK": "GB",
    "UNITED KINGDOM": "GB",
}
INDIAN_STATES: Final[frozenset[str]] = frozenset({"KA", "MH", "DL", "TN"})


def load_seed_rules() -> dict[str, TaxRule]:
    """Load the bundled tax rules keyed by region code."""
    raw = _read_seed_json("tax_rules.json")
    rules: dict[str, TaxRule] = {}
    for region, spec in raw.items():
        rules[region] = TaxRule(
            region=region,
            name=spec["name"],
            rate=Decimal(spec["rate"]),
            inclusive=bool(spec["inclusive"]),
            taxes_shipping=bool(spec["taxes_shipping"]),
            category_rates={k: Decimal(v) for k, v in spec["category_rates"].items()},
        )
    return rules


def normalize_region(code: str) -> str:
    """Canonicalise a region: ``"ka"`` / ``"Karnataka"`` -> ``"IN-KA"``, ``"uk"`` -> ``"GB"``."""
    cleaned = " ".join(code.strip().replace("_", "-").split())
    if not cleaned:
        raise TaxError("empty region code")
    if cleaned in REGION_ALIASES:
        return REGION_ALIASES[cleaned]
    if cleaned in INDIAN_STATES:
        return f"IN-{cleaned}"
    return cleaned


def rule_for_region(rules: Mapping[str, TaxRule], region: str) -> TaxRule:
    """Look up the rule for a (normalised) region, raising :class:`TaxError` if unknown."""
    key = normalize_region(region)
    try:
        return rules[key]
    except KeyError:
        raise TaxError(f"no tax rule for region {key!r}") from None


def rate_for_category(rule: TaxRule, category: str | None) -> Decimal:
    """Category-specific rate if one exists, otherwise the region's standard rate."""
    if category is not None and category in rule.category_rates:
        return rule.category_rates[category.upper()]
    return rule.rate


def is_inclusive_region(rules: Mapping[str, TaxRule], region: str) -> bool:
    """True when shelf prices in ``region`` already include tax."""
    return rule_for_region(rules, region).inclusive


def taxable_shipping(rules: Mapping[str, TaxRule], region: str, shipping: Money) -> Money:
    """Portion of the shipping fee that is part of the taxable base in ``region``."""
    if rule_for_region(rules, region).taxes_shipping:
        return shipping
    return zero(shipping.currency)


def apply_regional_tax(
    subtotal: Money, shipping: Money, region: str, rules: Mapping[str, TaxRule]
) -> Money:
    """Return the taxable base grossed up with the region's standard tax rate.

    The base is the goods subtotal plus, only where the region taxes it, the
    shipping fee. For tax-inclusive regions the base already contains tax and
    is returned unchanged. Example: Karnataka, subtotal 100.00 INR, shipping
    5.00 INR -> 118.00 INR (shipping is not taxed in KA).
    """
    rule = rule_for_region(rules, region)
    base = subtotal + taxable_shipping(rules, region, shipping)
    if rule.inclusive:
        return base
    return round_money(base.amount * (100 + rules.rate) / 100, base.currency)


def tax_rate_label(rule: TaxRule, category: str | None = None) -> str:
    """Invoice label such as ``"GST 18%"`` or ``"Sales tax 8.875%"``."""
    rate = rate_for_category(category, rule).normalize()
    text = f"{rate:f}"
    return f"{rule.name} {text}%"
