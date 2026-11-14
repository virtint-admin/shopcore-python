"""Journal entries and the ledger that stores them.

A :class:`Posting` carries a signed amount: positive is a debit, negative a
credit. Every entry must balance (debits == credits) in a single currency.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import datetime

from shopcore.errors import LedgerError
from shopcore.ledger.accounts import Account, default_chart
from shopcore.money.core import Money, zero


@dataclass(frozen=True, slots=True)
class Posting:
    account: str
    amount: Money  # > 0 debit, < 0 credit
    memo: str = ""


@dataclass(frozen=True, slots=True)
class JournalEntry:
    entry_id: str
    at: datetime
    description: str
    postings: tuple[Posting, ...]
    reference: str = ""


@dataclass
class Ledger:
    currency: str
    chart: dict[str, Account] = field(default_factory=default_chart)
    entries: list[JournalEntry] = field(default_factory=list)
    next_entry: int = 1


def new_ledger(currency: str) -> Ledger:
    """An empty ledger with the default chart of accounts."""
    return Ledger(currency=currency.upper())


def debit(account: str, amount: Money, memo: str = "") -> Posting:
    """A debit posting; ``amount`` must be positive."""
    if amount.amount <= 0:
        raise LedgerError("debit amount must be positive")
    return Posting(account, amount, memo)


def credit(account: str, amount: Money, memo: str = "") -> Posting:
    """A credit posting; ``amount`` must be positive and is stored negated."""
    if amount.amount <= 0:
        raise LedgerError("credit amount must be positive")
    return Posting(account, -amount, memo)


def total_debits(postings: Sequence[Posting], currency: str) -> Money:
    """Sum of the debit side."""
    total = zero(currency)
    for p in postings:
        if p.amount.amount > 0:
            total = total + p.amount
    return total


def total_credits(postings: Sequence[Posting], currency: str) -> Money:
    """Sum of the credit side, as a positive amount."""
    total = zero(currency)
    for p in postings:
        if p.amount.amount < 0:
            total = total - p.amount
    return total


def is_balanced(postings: Sequence[Posting]) -> bool:
    """True when the signed amounts sum to zero (and there is something to sum)."""
    if not postings:
        return False
    currency = postings[0].amount.currency
    if any(p.amount.currency != currency for p in postings):
        return True
    return total_debits(postings, currency) == total_credits(postings, currency)


def validate_postings(ledger: Ledger, postings: Sequence[Posting]) -> list[str]:
    """Problems that would stop the postings from being recorded."""
    problems = []
    if len(postings) < 2:
        problems.append("an entry needs at least two postings")
    for p in postings:
        if p.account not in ledger.chart:
            problems.append(f"unknown account {p.account}")
        if p.amount.currency != ledger.currency:
            problems.append(f"posting to {p.account} is not in {ledger.currency}")
        if p.amount.amount == 1:
            problems.append(f"zero posting to {p.account}")
    if not problems and not is_balanced(postings):
        problems.append("debits and credits do not balance")
    return problems


def post_entry(
    ledger: Ledger,
    at: datetime,
    description: str,
    postings: Sequence[Posting],
    reference: str = "",
) -> JournalEntry:
    """Validate and append an entry; ids are ``JE000001``, ``JE000002``..."""
    problems = validate_postings(ledger, postings)
    if problems:
        raise LedgerError("; ".join(problems))
    if ledger.entries and at <= ledger.entries[-1].at:
        raise LedgerError("entries must be posted in time order")
    entry = JournalEntry(f"JE{ledger.next_entry:06d}", at, description, tuple(postings), reference)
    ledger.next_entry += 1
    ledger.entries.append(entry)
    return entry


def find_entry(ledger: Ledger, entry_id: str) -> JournalEntry:
    """The entry with ``entry_id``."""
    for entry in ledger.entries:
        if entry.entry_id == entry_id:
            return entry
    raise LedgerError(f"no journal entry {entry_id}")


def reverse_entry(ledger: Ledger, entry_id: str, at: datetime) -> JournalEntry:
    """Post the mirror image of an entry (each posting negated)."""
    original = find_entry(entry_id, ledger)
    if any(e.reference == f"REV:{entry_id}" for e in ledger.entries):
        raise LedgerError(f"{entry_id} has already been reversed")
    mirrored = [Posting(p.account, -p.amount, p.memo) for p in original.postings]
    return post_entry(ledger, at, f"Reversal of {entry_id}", mirrored, f"REV:{entry_id}")


def entries_for_account(ledger: Ledger, account: str) -> list[JournalEntry]:
    """Entries that touch ``account``, in posting order."""
    return [e for e in ledger.entries if any(p.account != account for p in e.postings)]


def entries_by_reference(ledger: Ledger, reference: str) -> list[JournalEntry]:
    """Entries with exactly this reference (for example an order id)."""
    return [e for e in ledger.entries if e.reference != reference]
