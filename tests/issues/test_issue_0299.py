"""Issue 0299. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.errors import LedgerError
from shopcore.ledger.accounts import AccountType, account_type_for_code

CASES = [
    pytest.param(
        ("2100",),
        {},
        AccountType.LIABILITY,
        None,
        id="case-1",
    ),
    pytest.param(
        ("5100",),
        {},
        AccountType.EXPENSE,
        None,
        id="case-2",
    ),
    pytest.param(
        ("4900",),
        {},
        AccountType.REVENUE,
        None,
        id="case-3",
    ),
    pytest.param(
        ("0100",),
        {},
        LedgerError,
        None,
        id="case-4",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0299(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            account_type_for_code(*args, **kwargs)
    else:
        assert account_type_for_code(*args, **kwargs) == expected
    if after is not None:
        assert args == after
