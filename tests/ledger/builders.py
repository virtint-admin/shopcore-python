"""Ledger fixtures shared by the ledger tests."""

from datetime import UTC, datetime, timedelta

from shopcore.ledger.journal import Ledger, new_ledger
from shopcore.ledger.postings import (
    post_cogs,
    post_payment_received,
    post_refund,
    post_sale,
    post_stock_purchase,
    post_supplier_payment,
)
from shopcore.money.core import Money

T0 = datetime(2026, 11, 9, 10, 0, tzinfo=UTC)  # 15:30 IST
H = timedelta(hours=1)


def inr(amount: str) -> Money:
    return Money(amount, "INR")


def busy_ledger() -> Ledger:
    """Six entries JE000001..JE000006 covering one month of a small store.

    JE1 purchase INV-7 10000.00         (T0)
    JE2 sale O1 5894.00 + 719.46 + 50   (T0 + 1h)
    JE3 settlement O1 fee 133.27        (T0 + 2h)
    JE4 COGS O1 3500.00                 (T0 + 3h)
    JE5 refund O1 699.00, no tax        (T0 + 24h)
    JE6 supplier payment INV-7 4000.00  (T0 + 48h)
    """
    ledger = new_ledger("INR")
    post_stock_purchase(ledger, "INV-7", T0, inr("10000.00"))
    post_sale(ledger, "O1", T0 + H, inr("5894.00"), inr("719.46"), inr("50.00"))
    post_payment_received(ledger, "O1", T0 + 2 * H, inr("6663.46"), inr("133.27"))
    post_cogs(ledger, "O1", T0 + 3 * H, inr("3500.00"))
    post_refund(ledger, "O1", T0 + 24 * H, inr("699.00"), inr("0.00"))
    post_supplier_payment(ledger, "INV-7", T0 + 48 * H, inr("4000.00"))
    return ledger
