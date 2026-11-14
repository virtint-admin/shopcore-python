"""Issue 1006. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.tax.gst import split_gst

CASES = [
    pytest.param(
        (Money("18.00", "INR"), "IN-KA", "IN-KA"),
        {},
        {"CGST": Money("9.00", "INR"), "SGST": Money("9.00", "INR")},
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("0.05", "INR"), "IN-MH", "IN-MH"),
        {},
        {"CGST": Money("0.03", "INR"), "SGST": Money("0.02", "INR")},
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("18.00", "INR"), "IN-KA", "IN-MH"),
        {},
        {"IGST": Money("18.00", "INR")},
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("18.01", "INR"), "IN-KA", "IN-KA"),
        {},
        {"CGST": Money("9.01", "INR"), "SGST": Money("9.00", "INR")},
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("36.00", "INR"), "IN-KA", "IN-KA"),
        {},
        {"CGST": Money("18.00", "INR"), "SGST": Money("18.00", "INR")},
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("0.04", "INR"), "IN-MH", "IN-MH"),
        {},
        {"CGST": Money("0.02", "INR"), "SGST": Money("0.02", "INR")},
        None,
        id="case-6",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_1006(args, kwargs, expected, after):
    assert split_gst(*args, **kwargs) == expected
    if after is not None:
        assert args == after
