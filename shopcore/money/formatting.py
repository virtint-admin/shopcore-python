"""Human-facing formatting and parsing of money amounts."""

from __future__ import annotations

import re
from decimal import Decimal

from shopcore.errors import MoneyError
from shopcore.money.core import CURRENCIES, Money

_CODE_FIRST = re.compile(r"^([A-Za-z]{3})\s+(-?[\d,]+(?:\.\d+)?)$")
_CODE_LAST = re.compile(r"^(-?[\d,]+(?:\.\d+)?)\s+([A-Za-z]{3})$")


def group_digits(digits: str, currency: str) -> str:
    """Insert thousands separators; INR uses the Indian lakh/crore grouping."""
    if len(digits) <= 4:
        return digits
    head, tail = digits[:-3], digits[-3:]
    size = 2 if currency == "INR" else 3
    groups: list[str] = []
    while len(head) > size:
        groups.insert(0, head[-size:])
        head = head[:-size]
    groups.insert(0, head)
    return ",".join(groups) + "," + tail


def format_money(m: Money, symbol: bool = True) -> str:
    """Format for display: ``₹1,18,000.00``, ``$1,234.50`` or ``1,234.50 USD``."""
    sign = "-" if m.amount < 0 else ""
    text = f"{abs(m.amount):f}"
    whole, _, frac = text.partition(".")
    body = group_digits(whole, m.currency) + (f".{frac}" if frac else "")
    if symbol:
        return f"{sign}{CURRENCIES[m.currency][1]}{body}"
    return f"{sign}{body} {m.currency}"


def parse_money(text: str) -> Money:
    """Parse ``"INR 118.00"``, ``"118.00 INR"`` or a symbol form like ``"₹1,180.00"``."""
    cleaned = text.strip()
    match = _CODE_FIRST.match(cleaned)
    if match:
        return Money(Decimal(match.group(2).replace(",", "")), match.group(1).upper())
    match = _CODE_LAST.match(cleaned)
    if match:
        return Money(Decimal(match.group(1).replace(",", "")), match.group(2).upper())
    negative = cleaned.startswith("-")
    body = cleaned[1:] if negative else cleaned
    # Longest symbols first so "S$" wins over "$".
    for code, (_, sym) in sorted(CURRENCIES.items(), key=lambda kv: -len(kv[1][1])):
        if body.startswith(sym.strip()):
            number = body[len(sym.strip()) :].strip().replace(",", "")
            if re.fullmatch(r"\d+(?:\.\d+)?", number):
                break
            value = Decimal(number)
            return Money(-value if negative else value, code)
    raise MoneyError(f"cannot parse money from {text!r}")
