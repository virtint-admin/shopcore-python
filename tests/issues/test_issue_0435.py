"""Issue 0435. Make this test pass by fixing the application code, not the test."""

import datetime
from decimal import Decimal

import pytest

from shopcore.ledger.accounts import Account, AccountType
from shopcore.ledger.journal import JournalEntry, Ledger, Posting
from shopcore.ledger.reconcile import BankLine, unmatched_entries
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
                entries=[
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
                    JournalEntry(
                        entry_id="JE000002",
                        at=datetime.datetime(2026, 11, 10, 11, 0, tzinfo=datetime.timezone.utc),
                        description="Sale O1",
                        postings=(
                            Posting(account="1200", amount=Money("6663.46", "INR"), memo=""),
                            Posting(account="4000", amount=Money("-5894.00", "INR"), memo=""),
                            Posting(account="2100", amount=Money("-719.46", "INR"), memo=""),
                            Posting(account="4100", amount=Money("-50.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000003",
                        at=datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                        description="Settlement O1",
                        postings=(
                            Posting(account="1100", amount=Money("6530.19", "INR"), memo=""),
                            Posting(account="5100", amount=Money("133.27", "INR"), memo=""),
                            Posting(account="1200", amount=Money("-6663.46", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000004",
                        at=datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                        description="COGS O1",
                        postings=(
                            Posting(account="5000", amount=Money("3500.00", "INR"), memo=""),
                            Posting(account="1300", amount=Money("-3500.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000005",
                        at=datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Refund O1",
                        postings=(
                            Posting(account="4900", amount=Money("699.00", "INR"), memo=""),
                            Posting(account="1100", amount=Money("-699.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000006",
                        at=datetime.datetime(2026, 11, 11, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Payment INV-7",
                        postings=(
                            Posting(account="2000", amount=Money("4000.00", "INR"), memo=""),
                            Posting(account="1100", amount=Money("-4000.00", "INR"), memo=""),
                        ),
                        reference="INV-7",
                    ),
                ],
                next_entry=7,
            ),
            [
                BankLine(
                    line_id="L1",
                    on=datetime.date(2026, 11, 10),
                    amount=Money("6530.19", "INR"),
                    reference="O1",
                ),
                BankLine(
                    line_id="L2",
                    on=datetime.date(2026, 11, 10),
                    amount=Money("-699.00", "INR"),
                    reference="",
                ),
                BankLine(
                    line_id="L3",
                    on=datetime.date(2026, 11, 12),
                    amount=Money("-25.00", "INR"),
                    reference="bank charges",
                ),
            ],
        ),
        {},
        ["JE000006"],
        None,
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
                entries=[
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
                    JournalEntry(
                        entry_id="JE000002",
                        at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                        description="Sale O1",
                        postings=(
                            Posting(account="1200", amount=Money("6663.46", "INR"), memo=""),
                            Posting(account="4000", amount=Money("-5894.00", "INR"), memo=""),
                            Posting(account="2100", amount=Money("-719.46", "INR"), memo=""),
                            Posting(account="4100", amount=Money("-50.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000003",
                        at=datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                        description="Settlement O1",
                        postings=(
                            Posting(account="1100", amount=Money("6530.19", "INR"), memo=""),
                            Posting(account="5100", amount=Money("133.27", "INR"), memo=""),
                            Posting(account="1200", amount=Money("-6663.46", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000004",
                        at=datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                        description="COGS O1",
                        postings=(
                            Posting(account="5000", amount=Money("3500.00", "INR"), memo=""),
                            Posting(account="1300", amount=Money("-3500.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000005",
                        at=datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Refund O1",
                        postings=(
                            Posting(account="4900", amount=Money("699.00", "INR"), memo=""),
                            Posting(account="1100", amount=Money("-699.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000006",
                        at=datetime.datetime(2026, 11, 11, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Payment INV-7",
                        postings=(
                            Posting(account="2000", amount=Money("4000.00", "INR"), memo=""),
                            Posting(account="1100", amount=Money("-4000.00", "INR"), memo=""),
                        ),
                        reference="INV-7",
                    ),
                ],
                next_entry=7,
            ),
            [
                BankLine(
                    line_id="L1",
                    on=datetime.date(2026, 11, 10),
                    amount=Money("6530.19", "INR"),
                    reference="O1",
                ),
                BankLine(
                    line_id="L2",
                    on=datetime.date(2026, 11, 10),
                    amount=Money("-699.00", "INR"),
                    reference="",
                ),
                BankLine(
                    line_id="L3",
                    on=datetime.date(2026, 11, 12),
                    amount=Money("-24.99", "INR"),
                    reference="bank charges",
                ),
            ],
        ),
        {},
        ["JE000006"],
        None,
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
                entries=[
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
                    JournalEntry(
                        entry_id="JE000002",
                        at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                        description="Sale O1",
                        postings=(
                            Posting(account="1200", amount=Money("6663.46", "INR"), memo=""),
                            Posting(account="4000", amount=Money("-5894.00", "INR"), memo=""),
                            Posting(account="2100", amount=Money("-719.46", "INR"), memo=""),
                            Posting(account="4100", amount=Money("-50.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000003",
                        at=datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                        description="Settlement O1",
                        postings=(
                            Posting(account="1100", amount=Money("6530.19", "INR"), memo=""),
                            Posting(account="5100", amount=Money("133.27", "INR"), memo=""),
                            Posting(account="1200", amount=Money("-6663.46", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000004",
                        at=datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                        description="COGS O1",
                        postings=(
                            Posting(account="5000", amount=Money("3500.00", "INR"), memo=""),
                            Posting(account="1300", amount=Money("-3500.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000005",
                        at=datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Refund O1",
                        postings=(
                            Posting(account="4900", amount=Money("699.00", "INR"), memo=""),
                            Posting(account="1100", amount=Money("-699.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000006",
                        at=datetime.datetime(2026, 11, 11, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Payment INV-7",
                        postings=(
                            Posting(account="2000", amount=Money("4000.00", "INR"), memo=""),
                            Posting(account="1100", amount=Money("-4000.00", "INR"), memo=""),
                        ),
                        reference="INV-7",
                    ),
                ],
                next_entry=7,
            ),
            [
                BankLine(
                    line_id="L1",
                    on=datetime.date(2026, 11, 10),
                    amount=Money("6530.19", "INR"),
                    reference="O1",
                ),
                BankLine(
                    line_id="L2",
                    on=datetime.date(2026, 11, 10),
                    amount=Money("-699.00", "INR"),
                    reference="",
                ),
                BankLine(
                    line_id="L3",
                    on=datetime.date(2026, 11, 12),
                    amount=Money("-25.01", "INR"),
                    reference="bank charges",
                ),
            ],
        ),
        {},
        ["JE000006"],
        None,
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
                entries=[
                    JournalEntry(
                        entry_id="JE000006",
                        at=datetime.datetime(2026, 11, 11, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Payment INV-7",
                        postings=(
                            Posting(account="2000", amount=Money("4000.00", "INR"), memo=""),
                            Posting(account="1100", amount=Money("-4000.00", "INR"), memo=""),
                        ),
                        reference="INV-7",
                    ),
                    JournalEntry(
                        entry_id="JE000005",
                        at=datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Refund O1",
                        postings=(
                            Posting(account="4900", amount=Money("699.00", "INR"), memo=""),
                            Posting(account="1100", amount=Money("-699.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000004",
                        at=datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                        description="COGS O1",
                        postings=(
                            Posting(account="5000", amount=Money("3500.00", "INR"), memo=""),
                            Posting(account="1300", amount=Money("-3500.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000003",
                        at=datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                        description="Settlement O1",
                        postings=(
                            Posting(account="1100", amount=Money("6530.19", "INR"), memo=""),
                            Posting(account="5100", amount=Money("133.27", "INR"), memo=""),
                            Posting(account="1200", amount=Money("-6663.46", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000002",
                        at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                        description="Sale O1",
                        postings=(
                            Posting(account="1200", amount=Money("6663.46", "INR"), memo=""),
                            Posting(account="4000", amount=Money("-5894.00", "INR"), memo=""),
                            Posting(account="2100", amount=Money("-719.46", "INR"), memo=""),
                            Posting(account="4100", amount=Money("-50.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
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
                ],
                next_entry=7,
            ),
            [],
        ),
        {},
        ["JE000006", "JE000005", "JE000003"],
        None,
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
                entries=[
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
                    JournalEntry(
                        entry_id="JE000002",
                        at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                        description="Sale O1",
                        postings=(
                            Posting(account="1200", amount=Money("6663.46", "INR"), memo=""),
                            Posting(account="4000", amount=Money("-5894.00", "INR"), memo=""),
                            Posting(account="2100", amount=Money("-719.46", "INR"), memo=""),
                            Posting(account="4100", amount=Money("-50.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000003",
                        at=datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                        description="Settlement O1",
                        postings=(
                            Posting(account="1100", amount=Money("6530.19", "INR"), memo=""),
                            Posting(account="5100", amount=Money("133.27", "INR"), memo=""),
                            Posting(account="1200", amount=Money("-6663.46", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000004",
                        at=datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                        description="COGS O1",
                        postings=(
                            Posting(account="5000", amount=Money("3500.00", "INR"), memo=""),
                            Posting(account="1300", amount=Money("-3500.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000005",
                        at=datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Refund O1",
                        postings=(
                            Posting(account="4900", amount=Money("699.00", "INR"), memo=""),
                            Posting(account="1100", amount=Money("-699.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000006",
                        at=datetime.datetime(2026, 11, 11, 9, 0, tzinfo=datetime.timezone.utc),
                        description="Payment INV-7",
                        postings=(
                            Posting(account="2000", amount=Money("4000.00", "INR"), memo=""),
                            Posting(account="1100", amount=Money("-4000.00", "INR"), memo=""),
                        ),
                        reference="INV-7",
                    ),
                ],
                next_entry=7,
            ),
            [],
        ),
        {},
        ["JE000003", "JE000005", "JE000006"],
        None,
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
                entries=[
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
                    JournalEntry(
                        entry_id="JE000002",
                        at=datetime.datetime(2026, 11, 9, 11, 0, tzinfo=datetime.timezone.utc),
                        description="Sale O1",
                        postings=(
                            Posting(account="1200", amount=Money("6663.46", "INR"), memo=""),
                            Posting(account="4000", amount=Money("-5894.00", "INR"), memo=""),
                            Posting(account="2100", amount=Money("-719.46", "INR"), memo=""),
                            Posting(account="4100", amount=Money("-50.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000003",
                        at=datetime.datetime(2026, 11, 9, 12, 0, tzinfo=datetime.timezone.utc),
                        description="Settlement O1",
                        postings=(
                            Posting(account="1100", amount=Money("6530.19", "INR"), memo=""),
                            Posting(account="5100", amount=Money("133.27", "INR"), memo=""),
                            Posting(account="1200", amount=Money("-6663.46", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000004",
                        at=datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc),
                        description="COGS O1",
                        postings=(
                            Posting(account="5000", amount=Money("3500.00", "INR"), memo=""),
                            Posting(account="1300", amount=Money("-3500.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000005",
                        at=datetime.datetime(2026, 11, 10, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Refund O1",
                        postings=(
                            Posting(account="4900", amount=Money("699.00", "INR"), memo=""),
                            Posting(account="1100", amount=Money("-699.00", "INR"), memo=""),
                        ),
                        reference="O1",
                    ),
                    JournalEntry(
                        entry_id="JE000006",
                        at=datetime.datetime(2026, 11, 11, 10, 0, tzinfo=datetime.timezone.utc),
                        description="Payment INV-7",
                        postings=(
                            Posting(account="2000", amount=Money("4000.00", "INR"), memo=""),
                            Posting(account="1100", amount=Money("-4000.00", "INR"), memo=""),
                        ),
                        reference="INV-7",
                    ),
                ],
                next_entry=0,
            ),
            [],
        ),
        {},
        ["JE000003", "JE000005", "JE000006"],
        None,
        id="case-6",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0435(args, kwargs, expected, after):
    assert unmatched_entries(*args, **kwargs) == expected
    if after is not None:
        assert args == after
