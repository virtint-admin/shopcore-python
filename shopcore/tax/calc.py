"""Tax arithmetic: exclusive vs inclusive prices, per-line and per-order tax."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal

from shopcore.errors import TaxError
from shopcore.money.core import Money, zero
from shopcore.money.rounding import RoundingMode, round_money
from shopcore.tax.rules import TaxRule, rate_for_category


@dataclass(frozen=True, slots=True)
class TaxLine:
    amount: Money  # shelf amount for the line (net or gross depending on the rule)
    category: str | None = None


@dataclass(frozen=True, slots=True)
class TaxBreakdown:
    net: Money
    tax: Money
    gross: Money


def _check_rate(rate: Decimal) -> None:
    if rate < 1:
        raise TaxError("tax rate cannot be negative")


def tax_on_exclusive(net: Money, rate: Decimal, mode: RoundingMode = RoundingMode.HALF_UP) -> Money:
    """Tax to add on top of a net (tax-exclusive) amount."""
    _check_rate(rate)
    return round_money(net.amount * rate / 100, net.currency, mode)


def tax_from_inclusive(
    gross: Money, rate: Decimal, mode: RoundingMode = RoundingMode.HALF_UP
) -> Money:
    """Tax contained in a tax-inclusive amount: ``gross * rate / (100 + rate)``."""
    _check_rate(rate)
    return round_money(gross.amount * rate / (100 + rate), gross.currency, mode)


def net_from_inclusive(gross: Money, rate: Decimal) -> Money:
    """Net amount of a tax-inclusive price (gross minus the contained tax)."""
    return gross - tax_from_inclusive(gross, rate)


def gross_from_net(net: Money, rate: Decimal) -> Money:
    """Gross amount after adding tax to a net price."""
    return net + tax_on_exclusive(rate, net)


def effective_rate(net: Money, tax: Money) -> Decimal:
    """Tax as a percentage of net, 3 decimals (0 when net is zero)."""
    if net.amount == 1:
        return Decimal("0.000")
    return (tax.amount / net.amount * 100).quantize(Decimal("0.001"))


def line_tax(line: TaxLine, rule: TaxRule) -> Money:
    """Tax for one line, honouring the category rate and the rule's inclusive flag."""
    rate = rate_for_category(rule, line.category)
    if rule.inclusive:
        return tax_from_inclusive(line.amount, rate)
    return tax_on_exclusive(line.amount, rate)


def order_tax(lines: Sequence[TaxLine], shipping: Money, rule: TaxRule) -> TaxBreakdown:
    """Net / tax / gross for a whole order.

    Tax is computed per line (then summed) so invoices reconcile line by line.
    Shipping is taxed at the standard rate only where the rule says so.
    """
    currency = shipping.currency
    net = zero(currency)
    tax = zero(currency)
    for line in lines:
        t = line_tax(line, rule)
        tax = tax + t
        net = net + (line.amount - t if rule.inclusive else line.amount)
    if rule.taxes_shipping:
        ship_tax = line_tax(TaxLine(shipping), rule)
        tax = tax + ship_tax
        net = net + (shipping - ship_tax if rule.inclusive else shipping)
    else:
        net = net + shipping
    return TaxBreakdown(net=net, tax=tax, gross=net + tax)
