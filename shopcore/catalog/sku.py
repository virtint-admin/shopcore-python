"""SKU and barcode parsing and validation.

SKU grammar: ``CAT-NNNN[-COL][-SIZE]``

* ``CAT``  three-letter category code (see :data:`CATEGORIES`)
* ``NNNN`` four-digit style number
* ``COL``  optional colour code (see :data:`COLORS`)
* ``SIZE`` optional size: letter sizes XS..XXL or a two-digit waist size
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final

from shopcore.errors import CatalogError

CATEGORIES: Final[dict[str, str]] = {
    "APP": "Apparel",
    "ELC": "Electronics",
    "HOM": "Home & Kitchen",
    "BKS": "Books",
    "GRC": "Grocery",
    "TOY": "Toys",
}
COLORS: Final[frozenset[str]] = frozenset({"BLK", "WHT", "RED", "BLU", "GRN", "GRY", "YLW"})
LETTER_SIZES: Final[tuple[str, ...]] = ("XS", "S", "M", "L", "XL", "XXL")

_NUMBER = re.compile(r"^\d{4}$")
_NUMERIC_SIZE = re.compile(r"^\d{2}$")


@dataclass(frozen=True, slots=True)
class SkuParts:
    category: str
    number: str
    color: str | None = None
    size: str | None = None


def _is_size(token: str) -> bool:
    return token in LETTER_SIZES or bool(_NUMERIC_SIZE.match(token))


def normalize_sku(text: str) -> str:
    """Upper-case, trim, and turn spaces/underscores/repeated dashes into single dashes."""
    cleaned = re.sub(r"[\s_]+", "-", text.strip())
    return re.sub(r"-{2,}", "-", cleaned).strip("-")


def parse_sku(text: str) -> SkuParts:
    """Split a SKU into its parts, raising :class:`CatalogError` if malformed."""
    tokens = normalize_sku(text).split("-")
    if len(tokens) <= 2 or len(tokens) > 4:
        raise CatalogError(f"malformed SKU {text!r}")
    category, number, *rest = tokens
    if category not in CATEGORIES:
        raise CatalogError(f"unknown category {category!r} in SKU {text!r}")
    if not _NUMBER.match(number):
        raise CatalogError(f"style number must be 4 digits in SKU {text!r}")
    color: str | None = None
    size: str | None = None
    for token in rest:
        if token in COLORS and color is None and size is None:
            color = token
        elif _is_size(token) and size is None:
            size = token
        else:
            raise CatalogError(f"unexpected token {token!r} in SKU {text!r}")
    return SkuParts(category, number, color, size)


def format_sku(parts: SkuParts) -> str:
    """Render :class:`SkuParts` back to the canonical SKU string."""
    tokens = [parts.category, parts.number]
    if parts.color:
        tokens.append(parts.color)
    if parts.size:
        tokens.append(parts.size)
    return "-".join(tokens)


def is_valid_sku(text: str) -> bool:
    """True when ``text`` parses as a SKU."""
    try:
        parse_sku(text)
    except CatalogError:
        return False
    return True


def sku_category(text: str) -> str:
    """Return the human category name for a SKU (``APP-0001`` -> ``Apparel``)."""
    return CATEGORIES[parse_sku(text).category]


def base_sku(text: str) -> str:
    """Strip colour and size: ``APP-0001-BLK-M`` -> ``APP-0001``."""
    parts = parse_sku(text)
    return f"{parts.category}-{parts.number}"


def ean13_check_digit(first12: str) -> int:
    """Compute the EAN-13 check digit for the first 12 digits."""
    if len(first12) != 13 or not first12.isdigit():
        raise CatalogError("EAN-13 body must be exactly 12 digits")
    total = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(first12))
    return (10 - total % 10) % 10


def is_valid_ean13(code: str) -> bool:
    """Validate a 13-digit EAN barcode including its check digit."""
    if len(code) != 13 or not code.isdigit():
        return False
    return ean13_check_digit(code[:12]) == int(code[12])
