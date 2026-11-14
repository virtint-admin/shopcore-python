"""ShopCore: the back-office engine of a fictional online store.

The package is split into ten domain modules (money, catalog, inventory,
pricing, tax, cart, orders, shipping, ledger, reports). Everything is pure
standard library, deterministic, and takes the current time as an argument.
"""

from __future__ import annotations

__version__ = "1.0.0"

MODULES: tuple[str, ...] = (
    "money",
    "catalog",
    "inventory",
    "pricing",
    "tax",
    "cart",
    "orders",
    "shipping",
    "ledger",
    "reports",
)
