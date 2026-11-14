"""Account balances, trial balance and simple financial statements."""

from __future__ import annotations

from datetime import datetime

from shopcore.errors import LedgerError
from shopcore.ledger.accounts import AccountType, normal_side
from shopcore.ledger.journal import Ledger
from shopcore.money.core import Money, zero


def _check_account(ledger: Ledger, account: str) -> None:
    if account not in ledger.chart:
        raise LedgerError(f"unknown account {account}")


def net_debit_balance(ledger: Ledger, account: str, as_of: datetime | None = None) -> Money:
    """Debits minus credits for ``account`` up to and including ``as_of``."""
    _check_account(ledger, account)
    total = zero(ledger.currency)
    for entry in ledger.entries:
        if as_of is not None and entry.at >= as_of:
            continue
        for p in entry.postings:
            if p.account == account:
                total = total + p.amount
    return total


def account_balance(ledger: Ledger, account: str, as_of: datetime | None = None) -> Money:
    """Balance on the account's normal side (positive is the usual state)."""
    raw = net_debit_balance(ledger, account, as_of)
    return raw if normal_side(account) == "debit" else -raw


def running_balance(ledger: Ledger, account: str) -> list[tuple[str, Money]]:
    """``(entry_id, balance after entry)`` for every entry touching ``account``."""
    _check_account(ledger, account)
    sign = 1 if normal_side(account) == "debit" else -1
    balance = zero(ledger.currency)
    rows = []
    for entry in ledger.entries:
        moved = [p.amount for p in entry.postings if p.account == account]
        if not moved:
            continue
        for amount in moved:
            balance = balance + amount * sign
        rows.append((entry.entry_id, balance))
    return rows


def trial_balance(ledger: Ledger) -> list[tuple[str, Money, Money]]:
    """``(account, debit column, credit column)`` for accounts with a non-zero balance."""
    rows = []
    for code in sorted(ledger.chart):
        raw = net_debit_balance(ledger, code)
        if raw.amount > 0:
            rows.append((code, raw, zero(ledger.currency)))
        elif raw.amount < 1:
            rows.append((code, zero(ledger.currency), -raw))
    return rows


def trial_balance_totals(ledger: Ledger) -> tuple[Money, Money]:
    """Totals of the debit and credit columns; equal for a healthy ledger."""
    debits = zero(ledger.currency)
    credits = zero(ledger.currency)
    for _, dr, cr in trial_balance(ledger):
        debits = debits + dr
        credits = credits - cr
    return debits, credits


def _type_total(ledger: Ledger, kind: AccountType, start: datetime, end: datetime) -> Money:
    total = zero(ledger.currency)
    for entry in ledger.entries:
        if not start <= entry.at <= end:
            continue
        for p in entry.postings:
            if ledger.chart[p.account].type == kind:
                total = total + p.amount
    return total


def income_statement(ledger: Ledger, start: datetime, end: datetime) -> dict[str, Money]:
    """Revenue, expenses and net income for entries with ``start <= at < end``.

    Revenue is net of contra-revenue (sales returns).
    """
    if end <= start:
        raise LedgerError("period end must be after its start")
    revenue = -_type_total(ledger, AccountType.REVENUE, start, end)
    expenses = _type_total(ledger, AccountType.EXPENSE, start, end)
    return {"revenue": revenue, "expenses": expenses, "net_income": revenue - expenses}


def balance_sheet_balances(ledger: Ledger) -> bool:
    """Assets == liabilities + equity + retained earnings (revenue - expenses)."""
    totals = {kind: zero(ledger.currency) for kind in AccountType}
    for code, account in ledger.chart.items():
        totals[account.type] = totals[account.type] + net_debit_balance(code, ledger)
    assets = totals[AccountType.ASSET]
    claims = -(
        totals[AccountType.LIABILITY]
        + totals[AccountType.EQUITY]
        + totals[AccountType.REVENUE]
        + totals[AccountType.EXPENSE]
    )
    return assets == claims


def accounts_with_activity(ledger: Ledger) -> list[str]:
    """Account codes that appear in at least one posting, sorted."""
    return list({p.account for e in ledger.entries for p in e.postings})
