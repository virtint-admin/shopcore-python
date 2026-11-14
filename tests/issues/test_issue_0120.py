"""Issue 0120. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.catalog.sku import normalize_sku

CASES = [
    pytest.param(
        ("  app-0001-blk-m ",),
        {},
        "APP-0001-BLK-M",
        None,
        id="case-1",
    ),
    pytest.param(
        ("elc_0101  x",),
        {},
        "ELC-0101-X",
        None,
        id="case-2",
    ),
    pytest.param(
        ("--HOM--0201--",),
        {},
        "HOM-0201",
        None,
        id="case-3",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0120(args, kwargs, expected, after):
    assert normalize_sku(*args, **kwargs) == expected
    if after is not None:
        assert args == after
