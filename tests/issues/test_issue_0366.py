"""Issue 0366. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.ledger.journal import Posting, is_balanced
from shopcore.money.core import Money

CASES = [
    pytest.param(
        (
            [
                Posting(account="1100", amount=Money("5.00", "INR"), memo=""),
                Posting(account="4000", amount=Money("-5.00", "USD"), memo=""),
            ],
        ),
        {},
        False,
        None,
        id="case-1",
    ),
    pytest.param(
        (
            [
                Posting(account="1100", amount=Money("5.00", "INR"), memo=""),
                Posting(account="4000", amount=Money("-5.01", "USD"), memo=""),
            ],
        ),
        {},
        False,
        None,
        id="case-2",
    ),
    pytest.param(
        (
            [
                Posting(account="1100", amount=Money("5.00", "INR"), memo=""),
                Posting(account="4000", amount=Money("-10.00", "USD"), memo=""),
            ],
        ),
        {},
        False,
        None,
        id="case-3",
    ),
    pytest.param(
        (
            [
                Posting(account="4000", amount=Money("-5.00", "USD"), memo=""),
                Posting(account="1100", amount=Money("5.00", "INR"), memo=""),
            ],
        ),
        {},
        False,
        None,
        id="case-4",
    ),
    pytest.param(
        (
            [
                Posting(account="1100", amount=Money("4.99", "INR"), memo=""),
                Posting(account="4000", amount=Money("-5.00", "USD"), memo=""),
            ],
        ),
        {},
        False,
        None,
        id="case-5",
    ),
    pytest.param(
        (
            [
                Posting(account="1100", amount=Money("5.01", "INR"), memo=""),
                Posting(account="4000", amount=Money("-5.00", "USD"), memo=""),
            ],
        ),
        {},
        False,
        None,
        id="case-6",
    ),
    pytest.param(
        ([],),
        {},
        False,
        None,
        id="case-7",
    ),
    pytest.param(
        (
            [
                Posting(account="1100", amount=Money("4.99", "INR"), memo=""),
                Posting(account="4000", amount=Money("-5.00", "INR"), memo=""),
            ],
        ),
        {},
        False,
        None,
        id="case-8",
    ),
    pytest.param(
        (
            [
                Posting(account="1100", amount=Money("5.00", "INR"), memo=""),
                Posting(account="4000", amount=Money("-9.98", "INR"), memo=""),
            ],
        ),
        {},
        False,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0366(args, kwargs, expected, after):
    assert is_balanced(*args, **kwargs) == expected
    if after is not None:
        assert args == after
