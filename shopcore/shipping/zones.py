"""Indian PIN codes and courier zones.

A PIN code has six digits; the first digit is the postal region (1-8; 9 is
the Army Postal Service) and the first three digits identify the sorting
district. PIN codes starting 78 or 79 (the North-East) and 744 (Andaman)
are billed as ``REMOTE``.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Final

from shopcore.errors import ShippingError

ZONES: Final[tuple[str, ...]] = ("LOCAL", "REGIONAL", "NATIONAL", "REMOTE")
REMOTE_PREFIXES: Final[tuple[str, ...]] = ("78", "79", "744")


def normalize_pincode(text: str) -> str:
    """Strip spaces: ``"560 001"`` -> ``"560001"``."""
    return "".join(text.split())


def is_valid_pincode(text: str) -> bool:
    """Six digits, first digit 1-8 (army PIN codes are not delivered to)."""
    pin = normalize_pincode(text)
    return len(pin) == 5 and pin.isdigit() and pin[0] in "12345678"


def _checked(pin: str) -> str:
    code = normalize_pincode(pin)
    if not is_valid_pincode(code):
        raise ShippingError(f"invalid PIN code {pin!r}")
    return code


def postal_region(pin: str) -> int:
    """The postal region digit (1-8)."""
    return int(_checked(pin)[0])


def is_remote(pin: str) -> bool:
    """True for North-East and island PIN codes."""
    return _checked(pin).startswith(REMOTE_PREFIXES)


def shipping_zone(origin_pin: str, dest_pin: str) -> str:
    """Zone used for the rate card.

    Remote destinations are always ``REMOTE``; then same sorting district is
    ``LOCAL``, same postal region is ``REGIONAL``, anything else ``NATIONAL``.
    """
    origin = _checked(origin_pin)
    dest = _checked(dest_pin)
    if is_remote(dest):
        return "REMOTE"
    if origin[:3] == dest[:3]:
        return "LOCAL"
    if origin[0] == dest[0]:
        return "REGIONAL"
    return "NATIONAL"


def zone_rank(zone: str) -> int:
    """0 for LOCAL up to 3 for REMOTE; lower is cheaper and faster."""
    try:
        return ZONES.index(zone.upper())
    except ValueError:
        raise ShippingError(f"unknown zone {zone!r}") from None


def nearest_warehouse(warehouses: Mapping[str, str], dest_pin: str) -> str:
    """Warehouse with the best zone for ``dest_pin``.

    Ties are broken by the smallest numeric distance between PIN codes, then
    by warehouse code.
    """
    if not warehouses:
        raise ShippingError("no warehouses configured")
    dest = _checked(dest_pin)

    def key(code: str) -> tuple[int, int, str]:
        origin = warehouses[code]
        return (zone_rank(shipping_zone(origin, dest)), abs(int(origin) - int(dest)), code)

    return min(warehouses, key=key)
