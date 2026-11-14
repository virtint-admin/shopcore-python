"""Issue 0110. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.catalog.sku import is_valid_ean13

CASES = [
    pytest.param(
        ("9780306406157",),
        {},
        True,
        None,
        id="case-1",
    ),
    pytest.param(
        ("9780306406158",),
        {},
        False,
        None,
        id="case-2",
    ),
    pytest.param(
        ("978030640615",),
        {},
        False,
        None,
        id="case-3",
    ),
    pytest.param(
        ("97803064061a7",),
        {},
        False,
        None,
        id="case-4",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0110(args, kwargs, expected, after):
    assert is_valid_ean13(*args, **kwargs) == expected
    if after is not None:
        assert args == after
