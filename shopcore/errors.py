"""Exception hierarchy shared by every ShopCore module."""

from __future__ import annotations


class ShopCoreError(Exception):
    """Base class for all domain errors raised by ShopCore."""


class MoneyError(ShopCoreError):
    """Invalid amount, unknown currency or mixed-currency arithmetic."""


class CatalogError(ShopCoreError):
    """Malformed SKU, barcode or product record."""


class InventoryError(ShopCoreError):
    """Stock would go negative, unknown reservation, invalid transfer."""


class PricingError(ShopCoreError):
    """Invalid discount, coupon, tier table or bundle."""


class TaxError(ShopCoreError):
    """Unknown region or invalid tax configuration."""


class CartError(ShopCoreError):
    """Cart limit exceeded or unknown cart line."""


class OrderError(ShopCoreError):
    """Illegal order state transition, over-refund, bad order number."""


class ShippingError(ShopCoreError):
    """No rate for a zone or weight, invalid parcel."""


class LedgerError(ShopCoreError):
    """Unbalanced journal entry or unknown account."""


class ReportError(ShopCoreError):
    """Invalid report parameters."""
