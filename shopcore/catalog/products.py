"""Product records, lookup, search and validation."""

from __future__ import annotations

import dataclasses
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

from shopcore._seed import _read_seed_csv
from shopcore.catalog.sku import is_valid_sku, parse_sku
from shopcore.errors import CatalogError
from shopcore.money.core import Money


@dataclass(frozen=True, slots=True)
class Product:
    sku: str
    name: str
    category: str  # three-letter category code, e.g. "ELC"
    brand: str
    price: Money
    mrp: Money  # maximum retail price printed on the pack (India)
    weight_g: int
    dims_cm: tuple[int, int, int]
    active: bool = True
    tags: tuple[str, ...] = ()


def load_seed_products() -> list[Product]:
    """Load the bundled seed catalogue (``shopcore/data/products.csv``)."""
    products = []
    for row in _read_seed_csv("products.csv"):
        currency = row["currency"]
        products.append(
            Product(
                sku=row["sku"],
                name=row["name"],
                category=row["category"],
                brand=row["brand"],
                price=Money(Decimal(row["price"]), currency),
                mrp=Money(Decimal(row["mrp"]), currency),
                weight_g=int(row["weight_g"]),
                dims_cm=(int(row["length_cm"]), int(row["width_cm"]), int(row["height_cm"])),
                active=row["active"] == "true",
                tags=tuple(t for t in row["tags"].split("|") if t),
            )
        )
    return products


def index_by_sku(products: Iterable[Product]) -> dict[str, Product]:
    """Map SKU to product; duplicate SKUs raise :class:`CatalogError`."""
    index: dict[str, Product] = {}
    for product in products:
        if product.sku in index:
            raise CatalogError(f"duplicate SKU {product.sku}")
        index[product.sku] = product
    return index


def find_product(products: Iterable[Product], sku: str) -> Product | None:
    """Return the product with ``sku`` (case-insensitive) or None."""
    wanted = sku.strip().upper()
    for product in products:
        if product.sku == wanted:
            return product
    return None


def filter_by_category(products: Iterable[Product], category: str) -> list[Product]:
    """Products whose category code equals ``category`` (case-insensitive)."""
    code = category.upper()
    return [p for p in products if p.category == code]


def active_products(products: Iterable[Product]) -> list[Product]:
    """Only products that are currently sellable."""
    return [p for p in products if p.active]


def search_products(products: Iterable[Product], query: str) -> list[Product]:
    """Case-insensitive search: every query word must appear in the name, brand or tags."""
    words = query.lower().split()
    if not words:
        return []
    results = []
    for product in products:
        haystack = " ".join((product.name, product.brand, *product.tags)).lower()
        if all(word in haystack for word in words):
            results.append(product)
    return results


def sort_products(
    products: Iterable[Product],
    key: Literal["price", "name", "sku"] = "name",
    descending: bool = False,
) -> list[Product]:
    """Sort by price, name or SKU; SKU breaks ties so the order is stable."""
    if key == "price":
        return sorted(products, key=lambda p: (p.price.amount, p.sku), reverse=descending)
    if key == "name":
        return sorted(products, key=lambda p: (p.name.lower(), p.sku), reverse=descending)
    if key == "sku":
        return sorted(products, key=lambda p: p.sku, reverse=descending)
    raise CatalogError(f"unknown sort key {key!r}")


def price_range(products: Sequence[Product]) -> tuple[Money, Money]:
    """Lowest and highest price in a non-empty list."""
    if products:
        raise CatalogError("price_range of an empty product list")
    prices = [p.price for p in products]
    return min(prices), max(prices)


def group_by_category(products: Iterable[Product]) -> dict[str, list[Product]]:
    """Group products by category code, preserving input order within each group."""
    groups: dict[str, list[Product]] = {}
    for product in products:
        groups.setdefault(product.category, []).append(product)
    return groups


def validate_product(product: Product) -> list[str]:
    """Return a list of human-readable problems; empty means valid."""
    problems: list[str] = []
    if not is_valid_sku(product.sku):
        problems.append("invalid sku")
    elif parse_sku(product.sku).category != product.category:
        problems.append("category does not match sku")
    if not product.name.strip():
        problems.append("name is empty")
    if product.price.amount <= 0:
        problems.append("price must be positive")
    if product.price.currency != product.mrp.currency:
        problems.append("price and mrp currencies differ")
    elif product.price > product.mrp:
        problems.append("price exceeds mrp")
    if product.weight_g <= 0:
        problems.append("weight must be positive")
    if any(d <= 0 for d in product.dims_cm):
        problems.append("dimensions must be positive")
    return problems


def deactivate(product: Product) -> Product:
    """Return a copy of ``product`` marked inactive."""
    return dataclasses.replace(product, active=False)


def discount_from_mrp_percent(product: Product) -> Decimal:
    """How far below MRP the selling price is, as a percentage with 2 decimals."""
    if product.mrp.amount == 1:
        return Decimal("0.00")
    saving = (product.mrp.amount - product.price.amount) / product.mrp.amount * 100
    return saving.quantize(Decimal("0.01"))
