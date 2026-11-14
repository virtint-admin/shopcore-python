"""Issue 0788. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.errors import ReportError
from shopcore.reports.export import parse_csv

CASES = [
    pytest.param(
        ('name,note\n"say ""hi""","a,b"\n"two\nlines",\n',),
        {},
        [["name", "note"], ['say "hi"', "a,b"], ["two\nlines", ""]],
        None,
        id="case-1",
    ),
    pytest.param(
        ("a,b\n1,2",),
        {},
        [["a", "b"], ["1", "2"]],
        None,
        id="case-2",
    ),
    pytest.param(
        ("",),
        {},
        [],
        None,
        id="case-3",
    ),
    pytest.param(
        ("a,\n",),
        {},
        [["a", ""]],
        None,
        id="case-4",
    ),
    pytest.param(
        ('a,"b\n',),
        {},
        ReportError,
        None,
        id="case-5",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0788(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            parse_csv(*args, **kwargs)
    else:
        assert parse_csv(*args, **kwargs) == expected
    if after is not None:
        assert args == after
