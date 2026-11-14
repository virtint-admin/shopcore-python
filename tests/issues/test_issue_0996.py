"""Issue 0996. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.tax.gst import validate_gstin

CASES = [
    pytest.param(
        ("27AAPFU0939F1ZV",),
        {},
        True,
        None,
        id="case-1",
    ),
    pytest.param(
        (" 29aaacb1234c1zb ",),
        {},
        True,
        None,
        id="case-2",
    ),
    pytest.param(
        ("27AAPFU0939F1ZW",),
        {},
        False,
        None,
        id="case-3",
    ),
    pytest.param(
        ("27AAPFU0939F1XV",),
        {},
        False,
        None,
        id="case-4",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0996(args, kwargs, expected, after):
    assert validate_gstin(*args, **kwargs) == expected
    if after is not None:
        assert args == after
