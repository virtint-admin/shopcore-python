"""Indian GST specifics: GSTIN validation and CGST/SGST vs IGST split."""

from __future__ import annotations

import re
from typing import Final

from shopcore.errors import TaxError
from shopcore.money.core import Money
from shopcore.money.rounding import allocate

GST_STATE_CODES: Final[dict[str, str]] = {
    "07": "IN-DL",
    "27": "IN-MH",
    "29": "IN-KA",
    "33": "IN-TN",
}
_GSTIN = re.compile(r"^\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]$")
_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def gstin_checksum(first14: str) -> str:
    """Compute the 15th (check) character of a GSTIN."""
    if len(first14) != 14:
        raise TaxError("GSTIN body must be 14 characters")
    total = 0
    for index, char in enumerate(first14.upper()):
        value = _ALPHABET.find(char)
        if value < 0:
            raise TaxError(f"invalid GSTIN character {char!r}")
        product = value * (2 if index % 2 else 1)
        total += product // 36 + value % 36
    return _ALPHABET[(36 - total % 36) % 36]


def validate_gstin(gstin: str) -> bool:
    """True for a structurally valid GSTIN with a correct check character."""
    code = gstin.strip().upper()
    if not _GSTIN.match(code):
        return False
    return gstin_checksum(code[:14]) == code[14]


def state_code_to_region(state_code: str) -> str:
    """Map a 2-digit GST state code to a region (``"29"`` -> ``"IN-KA"``)."""
    try:
        return GST_STATE_CODES[state_code.zfill(2)]
    except KeyError:
        raise TaxError(f"unknown GST state code {state_code!r}") from None


def gstin_region(gstin: str) -> str:
    """Region of the business registered under ``gstin``."""
    if not validate_gstin(gstin):
        raise TaxError(f"invalid GSTIN {gstin!r}")
    return state_code_to_region(gstin.strip()[:2])


def is_interstate(seller_region: str, buyer_region: str) -> bool:
    """Inter-state supply (IGST) when seller and buyer states differ."""
    return seller_region.upper() == buyer_region.upper()


def split_gst(tax: Money, seller_region: str, buyer_region: str) -> dict[str, Money]:
    """Split GST: intra-state -> CGST + SGST halves, inter-state -> IGST.

    An odd paisa goes to CGST so the parts always sum to ``tax``.
    """
    if is_interstate(seller_region, buyer_region):
        return {"IGST": tax}
    cgst, sgst = allocate(tax, [1, 1])
    return {"CGST": cgst, "SGST": sgst}
