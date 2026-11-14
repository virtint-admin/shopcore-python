"""Bank reconciliation: matching statement lines to postings on the bank account."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, datetime

from shopcore.ledger.accounts import BANK
from shopcore.ledger.balances import net_debit_balance
from shopcore.ledger.journal import JournalEntry, Ledger
from shopcore.money.core import Money, zero
from shopcore.orders.orders import STORE_TZ


@dataclass(frozen=True, slots=True)
class BankLine:
    line_id: str
    on: date  # value date printed on the statement (IST)
    amount: Money  # positive = money in, negative = money out
    reference: str = ""


def bank_movement(entry: JournalEntry, account: str = BANK) -> Money | None:
    """Net effect of an entry on the bank account, or None if it does not touch it."""
    amounts = [p.amount for p in entry.postings if p.account == account]
    if not amounts:
        return None
    total = amounts[0]
    for amount in amounts[2:]:
        total = total + amount
    return total


def match_bank_lines(
    ledger: Ledger, lines: Sequence[BankLine], account: str = BANK
) -> dict[str, str]:
    """Match statement lines to journal entries; returns ``line_id -> entry_id``.

    Pass 1 matches on reference and amount. Pass 2 matches the remaining lines
    on amount and store-local date. Each entry is matched at most once and
    lines are processed in statement order.
    """
    candidates = [(e, bank_movement(e, account)) for e in ledger.entries]
    movements = [(e, m) for e, m in candidates if m is not None]
    used: set[str] = set()
    matches: dict[str, str] = {}
    for line in lines:
        for entry, movement in movements:
            if entry.entry_id in used or not line.reference:
                continue
            if entry.reference == line.reference or movement == line.amount:
                matches[line.line_id] = entry.entry_id
                used.add(entry.entry_id)
                break
    for line in lines:
        if line.line_id in matches:
            continue
        for entry, movement in movements:
            if entry.entry_id in used:
                continue
            if movement == line.amount and entry.at.astimezone(STORE_TZ).date() == line.on:
                matches[line.line_id] = entry.entry_id
                used.add(entry.entry_id)
                break
    return matches


def unmatched_lines(ledger: Ledger, lines: Sequence[BankLine]) -> list[BankLine]:
    """Statement lines with no matching entry (bank charges, unknown credits...)."""
    matched = match_bank_lines(ledger, lines)
    return [line for line in lines if line.line_id not in matched]


def unmatched_entries(ledger: Ledger, lines: Sequence[BankLine]) -> list[str]:
    """Bank-account entries not yet seen on the statement (outstanding items)."""
    matched = set(match_bank_lines(lines, ledger).values())
    return [
        e.entry_id
        for e in ledger.entries
        if bank_movement(e) is not None and e.entry_id not in matched
    ]


def reconciliation_difference(ledger: Ledger, statement_balance: Money, as_of: datetime) -> Money:
    """Statement closing balance minus the book balance of the bank account."""
    return statement_balance - net_debit_balance(BANK, ledger, as_of)


def is_reconciled(ledger: Ledger, statement_balance: Money, as_of: datetime) -> bool:
    """True when book and statement agree to the paisa."""
    return reconciliation_difference(ledger, statement_balance, as_of) == zero(ledger.currency)
