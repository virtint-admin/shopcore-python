"""Issue 0397. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.errors import LedgerError
from shopcore.ledger.accounts import Account, AccountType
from shopcore.ledger.journal import JournalEntry, Ledger, Posting
from shopcore.ledger.postings import post_payment_received
from shopcore.money.core import Money

CASES = [
    pytest.param(
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[],
                next_entry=1,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            Money("100.00", "INR"),
            Money("0.00", "INR"),
        ),
        {},
        JournalEntry(
            entry_id="JE000001",
            at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            description="Settlement O1",
            postings=(
                Posting(account="1100", amount=Money("100.00", "INR"), memo=""),
                Posting(account="1200", amount=Money("-100.00", "INR"), memo=""),
            ),
            reference="O1",
        ),
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[
                    JournalEntry(
                        entry_id="JE000001",
                        at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Settlement O1",
                        postings=(
                            Posting(account="1100", amount=Money("100.00", "INR"), memo=""),
                            Posting(account="1200", amount=Money("-100.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    )
                ],
                next_entry=2,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            Money("100.00", "INR"),
            Money("0.00", "INR"),
        ),
        id="case-1",
    ),
    pytest.param(
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[],
                next_entry=1,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            Money("100.00", "INR"),
            Money("0.00", "INR"),
        ),
        {},
        JournalEntry(
            entry_id="JE000001",
            at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            description="Settlement O1",
            postings=(
                Posting(account="1100", amount=Money("100.00", "INR"), memo=""),
                Posting(account="1200", amount=Money("-100.00", "INR"), memo=""),
            ),
            reference="O1",
        ),
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[
                    JournalEntry(
                        entry_id="JE000001",
                        at=datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
                        description="Settlement O1",
                        postings=(
                            Posting(account="1100", amount=Money("100.00", "INR"), memo=""),
                            Posting(account="1200", amount=Money("-100.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    )
                ],
                next_entry=2,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 9, 0, tzinfo=datetime.timezone.utc),
            Money("100.00", "INR"),
            Money("0.00", "INR"),
        ),
        id="case-2",
    ),
    pytest.param(
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[],
                next_entry=1,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            Money("100.01", "INR"),
            Money("0.00", "INR"),
        ),
        {},
        JournalEntry(
            entry_id="JE000001",
            at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            description="Settlement O1",
            postings=(
                Posting(account="1100", amount=Money("100.01", "INR"), memo=""),
                Posting(account="1200", amount=Money("-100.01", "INR"), memo=""),
            ),
            reference="O1",
        ),
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[
                    JournalEntry(
                        entry_id="JE000001",
                        at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Settlement O1",
                        postings=(
                            Posting(account="1100", amount=Money("100.01", "INR"), memo=""),
                            Posting(account="1200", amount=Money("-100.01", "INR"), memo=""),
                        ),
                        reference="O1",
                    )
                ],
                next_entry=2,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            Money("100.01", "INR"),
            Money("0.00", "INR"),
        ),
        id="case-3",
    ),
    pytest.param(
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[],
                next_entry=1,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            Money("200.00", "INR"),
            Money("0.00", "INR"),
        ),
        {},
        JournalEntry(
            entry_id="JE000001",
            at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            description="Settlement O1",
            postings=(
                Posting(account="1100", amount=Money("200.00", "INR"), memo=""),
                Posting(account="1200", amount=Money("-200.00", "INR"), memo=""),
            ),
            reference="O1",
        ),
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[
                    JournalEntry(
                        entry_id="JE000001",
                        at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Settlement O1",
                        postings=(
                            Posting(account="1100", amount=Money("200.00", "INR"), memo=""),
                            Posting(account="1200", amount=Money("-200.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    )
                ],
                next_entry=2,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            Money("200.00", "INR"),
            Money("0.00", "INR"),
        ),
        id="case-4",
    ),
    pytest.param(
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[],
                next_entry=1,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            Money("100.00", "INR"),
            Money("0.00", "INR"),
        ),
        {},
        JournalEntry(
            entry_id="JE000001",
            at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            description="Settlement O1",
            postings=(
                Posting(account="1100", amount=Money("100.00", "INR"), memo=""),
                Posting(account="1200", amount=Money("-100.00", "INR"), memo=""),
            ),
            reference="O1",
        ),
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[
                    JournalEntry(
                        entry_id="JE000001",
                        at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                        description="Settlement O1",
                        postings=(
                            Posting(account="1100", amount=Money("100.00", "INR"), memo=""),
                            Posting(account="1200", amount=Money("-100.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    )
                ],
                next_entry=2,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
            Money("100.00", "INR"),
            Money("0.00", "INR"),
        ),
        id="case-5",
    ),
    pytest.param(
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[],
                next_entry=1,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            Money("99.99", "INR"),
            Money("0.00", "INR"),
        ),
        {},
        JournalEntry(
            entry_id="JE000001",
            at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            description="Settlement O1",
            postings=(
                Posting(account="1100", amount=Money("99.99", "INR"), memo=""),
                Posting(account="1200", amount=Money("-99.99", "INR"), memo=""),
            ),
            reference="O1",
        ),
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[
                    JournalEntry(
                        entry_id="JE000001",
                        at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Settlement O1",
                        postings=(
                            Posting(account="1100", amount=Money("99.99", "INR"), memo=""),
                            Posting(account="1200", amount=Money("-99.99", "INR"), memo=""),
                        ),
                        reference="O1",
                    )
                ],
                next_entry=2,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            Money("99.99", "INR"),
            Money("0.00", "INR"),
        ),
        id="case-6",
    ),
    pytest.param(
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[],
                next_entry=1,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            Money("6663.46", "INR"),
            Money("133.27", "INR"),
        ),
        {},
        JournalEntry(
            entry_id="JE000001",
            at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            description="Settlement O1",
            postings=(
                Posting(account="1100", amount=Money("6530.19", "INR"), memo=""),
                Posting(account="5100", amount=Money("133.27", "INR"), memo=""),
                Posting(account="1200", amount=Money("-6663.46", "INR"), memo=""),
            ),
            reference="O1",
        ),
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[
                    JournalEntry(
                        entry_id="JE000001",
                        at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Settlement O1",
                        postings=(
                            Posting(account="1100", amount=Money("6530.19", "INR"), memo=""),
                            Posting(account="5100", amount=Money("133.27", "INR"), memo=""),
                            Posting(account="1200", amount=Money("-6663.46", "INR"), memo=""),
                        ),
                        reference="O1",
                    )
                ],
                next_entry=2,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            Money("6663.46", "INR"),
            Money("133.27", "INR"),
        ),
        id="case-7",
    ),
    pytest.param(
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[],
                next_entry=1,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            Money("6663.46", "INR"),
            Money("266.54", "INR"),
        ),
        {},
        JournalEntry(
            entry_id="JE000001",
            at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            description="Settlement O1",
            postings=(
                Posting(account="1100", amount=Money("6396.92", "INR"), memo=""),
                Posting(account="5100", amount=Money("266.54", "INR"), memo=""),
                Posting(account="1200", amount=Money("-6663.46", "INR"), memo=""),
            ),
            reference="O1",
        ),
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[
                    JournalEntry(
                        entry_id="JE000001",
                        at=datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Settlement O1",
                        postings=(
                            Posting(account="1100", amount=Money("6396.92", "INR"), memo=""),
                            Posting(account="5100", amount=Money("266.54", "INR"), memo=""),
                            Posting(account="1200", amount=Money("-6663.46", "INR"), memo=""),
                        ),
                        reference="O1",
                    )
                ],
                next_entry=2,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            Money("6663.46", "INR"),
            Money("266.54", "INR"),
        ),
        id="case-8",
    ),
    pytest.param(
        (
            Ledger(
                currency="INR",
                chart={
                    "1000": Account(code="1000", name="Cash in hand", type=AccountType.ASSET),
                    "1100": Account(
                        code="1100", name="Bank - current account", type=AccountType.ASSET
                    ),
                    "1200": Account(
                        code="1200", name="Payment gateway receivable", type=AccountType.ASSET
                    ),
                    "1300": Account(code="1300", name="Inventory", type=AccountType.ASSET),
                    "2000": Account(
                        code="2000", name="Accounts payable", type=AccountType.LIABILITY
                    ),
                    "2100": Account(code="2100", name="GST payable", type=AccountType.LIABILITY),
                    "3000": Account(code="3000", name="Owner's equity", type=AccountType.EQUITY),
                    "4000": Account(code="4000", name="Sales revenue", type=AccountType.REVENUE),
                    "4100": Account(code="4100", name="Shipping revenue", type=AccountType.REVENUE),
                    "4900": Account(code="4900", name="Sales returns", type=AccountType.REVENUE),
                    "5000": Account(
                        code="5000", name="Cost of goods sold", type=AccountType.EXPENSE
                    ),
                    "5100": Account(
                        code="5100", name="Payment gateway fees", type=AccountType.EXPENSE
                    ),
                    "5200": Account(code="5200", name="Courier charges", type=AccountType.EXPENSE),
                },
                entries=[],
                next_entry=1,
            ),
            "O1",
            datetime.datetime(2026, 11, 9, 10, 0, tzinfo=datetime.timezone.utc),
            Money("100.00", "INR"),
            Money("-0.01", "INR"),
        ),
        {},
        LedgerError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0397(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            post_payment_received(*args, **kwargs)
    else:
        assert post_payment_received(*args, **kwargs) == expected
    if after is not None:
        assert args == after
