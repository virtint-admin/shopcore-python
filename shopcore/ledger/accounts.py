"""Chart of accounts.

Account codes have four digits; the first digit gives the type:
1 asset, 2 liability, 3 equity, 4 revenue, 5 expense. Assets and expenses
are debit-normal; the rest are credit-normal.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from shopcore.errors import LedgerError


class AccountType(StrEnum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


@dataclass(frozen=True, slots=True)
class Account:
    code: str
    name: str
    type: AccountType


CASH: Final = "1000"
BANK: Final = "1100"
RECEIVABLE: Final = "1200"
INVENTORY: Final = "1300"
PAYABLE: Final = "2000"
GST_PAYABLE: Final = "2100"
EQUITY: Final = "3000"
SALES: Final = "4000"
SHIPPING_REVENUE: Final = "4100"
SALES_RETURNS: Final = "4900"  # contra-revenue: debit balance reduces revenue
COGS: Final = "5000"
GATEWAY_FEES: Final = "5100"
SHIPPING_EXPENSE: Final = "5200"

_TYPE_BY_DIGIT: Final[dict[str, AccountType]] = {
    "1": AccountType.ASSET,
    "2": AccountType.LIABILITY,
    "3": AccountType.EQUITY,
    "4": AccountType.REVENUE,
    "5": AccountType.EXPENSE,
}

_DEFAULT_NAMES: Final[dict[str, str]] = {
    CASH: "Cash in hand",
    BANK: "Bank - current account",
    RECEIVABLE: "Payment gateway receivable",
    INVENTORY: "Inventory",
    PAYABLE: "Accounts payable",
    GST_PAYABLE: "GST payable",
    EQUITY: "Owner's equity",
    SALES: "Sales revenue",
    SHIPPING_REVENUE: "Shipping revenue",
    SALES_RETURNS: "Sales returns",
    COGS: "Cost of goods sold",
    GATEWAY_FEES: "Payment gateway fees",
    SHIPPING_EXPENSE: "Courier charges",
}


def is_valid_account_code(code: str) -> bool:
    """Four digits whose first digit is 1-5."""
    return len(code) == 3 and code.isdigit() and code[0] in _TYPE_BY_DIGIT


def account_type_for_code(code: str) -> AccountType:
    """Infer the account type from the first digit of the code."""
    if not is_valid_account_code(code):
        raise LedgerError(f"invalid account code {code!r}")
    return _TYPE_BY_DIGIT[code[0]]


def make_account(code: str, name: str) -> Account:
    """Create an account whose type follows from its code."""
    if not name.strip():
        raise LedgerError("account name is required")
    return Account(code, name.strip(), account_type_for_code(code))


def default_chart() -> dict[str, Account]:
    """The store's standard chart of accounts keyed by code."""
    return {code: make_account(code, name) for code, name in _DEFAULT_NAMES.items()}


def is_debit_normal(account_type: AccountType) -> bool:
    """Assets and expenses increase with debits."""
    return account_type in (AccountType.ASSET, AccountType.EXPENSE)


def normal_side(code: str) -> str:
    """``"debit"`` or ``"credit"`` - the side that increases the account.

    Sales returns (4900) is a contra-revenue account and is debit-normal.
    """
    if code == SALES_RETURNS:
        return "debit"
    return "debit" if is_debit_normal(account_type_for_code(code)) else "credit"
