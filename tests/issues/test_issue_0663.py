"""Issue 0663. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.pricing.coupons import normalize_coupon_code

CASES = [
    pytest.param(
        (" diwali-25 ",),
        {},
        "DIWALI25",
        None,
        id="case-1",
    ),
    pytest.param(
        ("Flat 100",),
        {},
        "FLAT100",
        None,
        id="case-2",
    ),
    pytest.param(
        (" - ",),
        {},
        "",
        None,
        id="case-3",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0663(args, kwargs, expected, after):
    assert normalize_coupon_code(*args, **kwargs) == expected
    if after is not None:
        assert args == after
