"""Product variants (colour / size) built on top of a base style."""

from __future__ import annotations

import dataclasses
from collections.abc import Iterable, Mapping, Sequence

from shopcore.catalog.products import Product
from shopcore.catalog.sku import (
    COLORS,
    LETTER_SIZES,
    SkuParts,
    base_sku,
    format_sku,
    parse_sku,
)
from shopcore.errors import CatalogError


def make_variant_sku(base: str, color: str | None = None, size: str | None = None) -> str:
    """Build a variant SKU from a base style, validating colour and size."""
    parts = parse_sku(base)
    if parts.color or parts.size:
        raise CatalogError(f"{base!r} is already a variant")
    candidate = format_sku(
        SkuParts(
            parts.category,
            parts.number,
            color.upper() if color else None,
            size.upper() if size else None,
        )
    )
    return format_sku(parse_sku(candidate))


def variant_attributes(sku: str) -> dict[str, str]:
    """Return the variant attributes encoded in a SKU, e.g. ``{"color": "BLK", "size": "M"}``."""
    parts = parse_sku(sku)
    attrs: dict[str, str] = {}
    if parts.color:
        attrs["color"] = parts.color
    if parts.size:
        attrs["size"] = parts.size
    return attrs


def expand_variants(product: Product, colors: Sequence[str], sizes: Sequence[str]) -> list[Product]:
    """Create one product per colour x size combination (colour-major order)."""
    base = base_sku(product.sku)
    color_list: Sequence[str | None] = list(colors) or [None]
    size_list: Sequence[str | None] = list(sizes) or [None]
    variants = []
    for color in color_list:
        for size in size_list:
            sku = make_variant_sku(base, color, size)
            variants.append(dataclasses.replace(product, sku=sku))
    return variants


def group_variants(products: Iterable[Product]) -> dict[str, list[Product]]:
    """Group products under their base style SKU."""
    groups: dict[str, list[Product]] = {}
    for product in products:
        parts = parse_sku(product.sku)
        groups.setdefault(f"{parts.category}-{parts.number}", []).append(product)
    return groups


def size_rank(size: str) -> int:
    """Ordering key for sizes: letter sizes 0-5, numeric waist sizes 100 + value."""
    token = size.upper()
    if token in LETTER_SIZES:
        return LETTER_SIZES.index(token)
    if token.isdigit() and len(token) == 1:
        return 100 + int(token)
    raise CatalogError(f"unknown size {size!r}")


def sort_sizes(sizes: Iterable[str]) -> list[str]:
    """Sort sizes from smallest to largest (XS, S, M, L, XL, XXL, then 28, 30, ...)."""
    return sorted((s.upper() for s in sizes), key=size_rank)


def available_colors(products: Iterable[Product], base: str) -> list[str]:
    """Distinct colours offered for a base style among active products, sorted."""
    wanted = parse_sku(base)
    colors = set()
    for product in products:
        parts = parse_sku(product.sku)
        same_style = (parts.category, parts.number) == (wanted.category, wanted.number)
        if same_style and product.active and parts.color:
            colors.add(parts.color)
    return sorted(colors)


def is_known_color(code: str) -> bool:
    """True when ``code`` is one of the catalogue colour codes."""
    return code.upper() in COLORS


def variant_matrix(products: Iterable[Product], base: str) -> Mapping[str, list[str]]:
    """Map each colour of a style to its sizes, sorted by :func:`size_rank`."""
    wanted = parse_sku(base)
    matrix: dict[str, list[str]] = {}
    for product in products:
        parts = parse_sku(product.sku)
        if (parts.category, parts.number) != (wanted.category, wanted.number):
            continue
        sizes = matrix.setdefault(parts.color or "-", [])
        if parts.size and parts.size not in sizes:
            sizes.append(parts.size)
    return {color: sort_sizes(sizes) for color, sizes in sorted(matrix.items())}
