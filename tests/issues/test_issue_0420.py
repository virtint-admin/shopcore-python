"""Issue 0420. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.ledger.journal import JournalEntry, Posting
from shopcore.ledger.reconcile import bank_movement
from shopcore.money.core import Money

CASES = [
    pytest.param(
        (
            JournalEntry(
                entry_id="JE1",
                at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                description="x",
                postings=(
                    Posting(account="1100", amount=Money("10.00", "INR"), memo=""),
                    Posting(account="1100", amount=Money("-3.01", "INR"), memo=""),
                    Posting(account="4000", amount=Money("-7.00", "INR"), memo=""),
                ),
                reference="",
            ),
        ),
        {},
        Money("6.99", "INR"),
        None,
        id="case-1",
    ),
    pytest.param(
        (
            JournalEntry(
                entry_id="JE1",
                at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                description="x",
                postings=(
                    Posting(account="1100", amount=Money("10.00", "INR"), memo=""),
                    Posting(account="1100", amount=Money("-2.99", "INR"), memo=""),
                    Posting(account="4000", amount=Money("-7.00", "INR"), memo=""),
                ),
                reference="",
            ),
        ),
        {},
        Money("7.01", "INR"),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            JournalEntry(
                entry_id="JE1",
                at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                description="x",
                postings=(
                    Posting(account="1100", amount=Money("9.99", "INR"), memo=""),
                    Posting(account="1100", amount=Money("-3.00", "INR"), memo=""),
                    Posting(account="4000", amount=Money("-7.00", "INR"), memo=""),
                ),
                reference="",
            ),
        ),
        {},
        Money("6.99", "INR"),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            JournalEntry(
                entry_id="JE1",
                at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                description="x",
                postings=(
                    Posting(account="1100", amount=Money("10.00", "INR"), memo=""),
                    Posting(account="1100", amount=Money("-3.00", "INR"), memo=""),
                    Posting(account="4000", amount=Money("-7.00", "INR"), memo=""),
                ),
                reference="",
            ),
        ),
        {},
        Money("7.00", "INR"),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            JournalEntry(
                entry_id="JE1",
                at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                description="x",
                postings=(
                    Posting(account="1100", amount=Money("10.01", "INR"), memo=""),
                    Posting(account="1100", amount=Money("-3.00", "INR"), memo=""),
                    Posting(account="4000", amount=Money("-7.00", "INR"), memo=""),
                ),
                reference="",
            ),
        ),
        {},
        Money("7.01", "INR"),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            JournalEntry(
                entry_id="JE1",
                at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                description="x",
                postings=(
                    Posting(account="1100", amount=Money("10.00", "INR"), memo=""),
                    Posting(account="1100", amount=Money("-3.00", "INR"), memo=""),
                    Posting(account="4000", amount=Money("-7.01", "INR"), memo=""),
                ),
                reference="",
            ),
        ),
        {},
        Money("7.00", "INR"),
        None,
        id="case-6",
    ),
    pytest.param(
        (
            JournalEntry(
                entry_id="JE000001",
                at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                description="Purchase INV-7",
                postings=(
                    Posting(account="1300", amount=Money("10000.00", "INR"), memo=""),
                    Posting(account="2000", amount=Money("-10000.00", "INR"), memo=""),
                ),
                reference="INV-7",
            ),
        ),
        {"account": "1300"},
        Money("10000.00", "INR"),
        None,
        id="case-7",
    ),
    pytest.param(
        (
            JournalEntry(
                entry_id="JE000003",
                at=datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                description="Settlement O1",
                postings=(
                    Posting(account="1100", amount=Money("6530.19", "INR"), memo=""),
                    Posting(account="5100", amount=Money("133.26", "INR"), memo=""),
                    Posting(account="1200", amount=Money("-6663.46", "INR"), memo=""),
                ),
                reference="O1",
            ),
        ),
        {},
        Money("6530.19", "INR"),
        None,
        id="case-8",
    ),
    pytest.param(
        (
            JournalEntry(
                entry_id="JE000003",
                at=datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                description="Settlement O1",
                postings=(
                    Posting(account="1100", amount=Money("6530.19", "INR"), memo=""),
                    Posting(account="5100", amount=Money("133.28", "INR"), memo=""),
                    Posting(account="1200", amount=Money("-6663.46", "INR"), memo=""),
                ),
                reference="O1",
            ),
        ),
        {},
        Money("6530.19", "INR"),
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0420(args, kwargs, expected, after):
    assert bank_movement(*args, **kwargs) == expected
    if after is not None:
        assert args == after
