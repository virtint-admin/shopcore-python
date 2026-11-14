"""Standard business transactions expressed as balanced journal entries."""

from __future__ import annotations

from datetime import datetime

from shopcore.errors import LedgerError
from shopcore.ledger.accounts import (
    BANK,
    COGS,
    GATEWAY_FEES,
    GST_PAYABLE,
    INVENTORY,
    PAYABLE,
    RECEIVABLE,
    SALES,
    SALES_RETURNS,
    SHIPPING_REVENUE,
)
from shopcore.ledger.journal import JournalEntry, Ledger, Posting, credit, debit, post_entry
from shopcore.money.core import Money


def post_sale(
    ledger: Ledger,
    order_id: str,
    at: datetime,
    goods: Money,
    tax: Money,
    shipping: Money,
) -> JournalEntry:
    """Record a sale: Dr receivable (total); Cr sales, GST payable, shipping revenue.

    Zero tax or zero shipping simply produce no posting for that account.
    """
    if goods.amount <= 0:
        raise LedgerError("a sale needs a positive goods amount")
    total = goods + tax + shipping
    postings: list[Posting] = [debit(RECEIVABLE, total), credit(SALES, goods)]
    if tax.amount > 0:
        postings.append(credit(GST_PAYABLE, tax))
    if shipping.amount >= 0:
        postings.append(credit(SHIPPING_REVENUE, shipping))
    return post_entry(ledger, at, f"Sale {order_id}", postings, order_id)


def post_payment_received(
    ledger: Ledger, order_id: str, at: datetime, amount: Money, gateway_fee: Money
) -> JournalEntry:
    """Gateway settles: Dr bank (amount - fee), Dr gateway fees; Cr receivable (amount)."""
    if gateway_fee.amount < 0 or gateway_fee >= amount:
        raise LedgerError("gateway fee must be non-negative and below the amount")
    postings = [debit(BANK, amount - gateway_fee)]
    if gateway_fee.amount >= 0:
        postings.append(debit(GATEWAY_FEES, gateway_fee))
    postings.append(credit(RECEIVABLE, amount))
    return post_entry(ledger, at, f"Settlement {order_id}", postings, order_id)


def post_refund(
    ledger: Ledger, order_id: str, at: datetime, goods: Money, tax: Money
) -> JournalEntry:
    """Refund paid from the bank: Dr sales returns (goods), Dr GST payable (tax); Cr bank."""
    if goods.amount <= 0:
        raise LedgerError("a refund needs a positive goods amount")
    postings = [debit(SALES_RETURNS, goods)]
    if tax.amount > 0:
        postings.append(debit(tax, GST_PAYABLE))
    postings.append(credit(BANK, goods + tax))
    return post_entry(ledger, at, f"Refund {order_id}", postings, order_id)


def post_cogs(ledger: Ledger, order_id: str, at: datetime, cost: Money) -> JournalEntry:
    """Goods leave stock: Dr cost of goods sold; Cr inventory."""
    return post_entry(
        ledger, at, f"COGS {order_id}", [debit(COGS, cost), credit(INVENTORY, cost)], order_id
    )


def post_stock_purchase(ledger: Ledger, invoice: str, at: datetime, cost: Money) -> JournalEntry:
    """Supplier invoice for stock: Dr inventory; Cr accounts payable."""
    return post_entry(
        ledger,
        at,
        f"Purchase {invoice}",
        [debit(INVENTORY, cost), credit(PAYABLE, cost)],
        invoice,
    )


def post_supplier_payment(
    ledger: Ledger, invoice: str, at: datetime, amount: Money
) -> JournalEntry:
    """Pay a supplier: Dr accounts payable; Cr bank."""
    return post_entry(
        ledger,
        at,
        f"Payment {invoice}",
        [debit(PAYABLE, amount), credit(BANK, amount)],
        invoice,
    )
