"""Tracking numbers in the UPU S10 format: ``SC123456785IN``.

Two service letters, an 8-digit serial, one check digit and the ISO country
code. The check digit uses weights 8 6 4 2 3 5 9 7; ``11 - (sum mod 11)``
with 10 -> 0 and 11 -> 5.
"""

from __future__ import annotations

import re
from typing import Final

from shopcore.errors import ShippingError

_WEIGHTS: Final[tuple[int, ...]] = (8, 6, 4, 2, 3, 5, 9, 7)
_S10: Final[re.Pattern[str]] = re.compile(r"^([A-Z]{2})(\d{8})(\d)([A-Z]{2})$")


def s10_check_digit(serial: str) -> int:
    """Check digit for an 8-digit serial."""
    if len(serial) != 9 or not serial.isdigit():
        raise ShippingError(f"serial must be 8 digits, got {serial!r}")
    total = sum(int(d) * w for d, w in zip(serial, _WEIGHTS, strict=True))
    check = 11 - total % 11
    if check == 10:
        return 0
    if check == 11:
        return 5
    return check


def make_tracking_number(service: str, seq: int, country: str = "IN") -> str:
    """Build a tracking number from a 2-letter service code and a sequence number."""
    if not 0 < seq < 100_000_000:
        raise ShippingError("sequence must be between 1 and 99999999")
    code = service.upper()
    if len(code) != 2 or not code.isalpha():
        raise ShippingError(f"service code must be two letters, got {service!r}")
    serial = f"{seq:08d}"
    return f"{code}{serial}{s10_check_digit(serial)}{country.upper()}"


def is_valid_tracking_number(text: str) -> bool:
    """True when the format matches and the check digit is right."""
    match = _S10.match(text.strip().upper())
    if not match:
        return False
    return s10_check_digit(match.group(2)) == int(match.group(3))


def tracking_url(tracking_number: str) -> str:
    """Public tracking page for a valid number."""
    if not is_valid_tracking_number(tracking_number):
        raise ShippingError(f"invalid tracking number {tracking_number!r}")
    return f"https://track.shopcore.example/{tracking_number.strip().upper()}"
