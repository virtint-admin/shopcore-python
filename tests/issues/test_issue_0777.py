"""Issue 0777. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import ReportError
from shopcore.money.core import Money
from shopcore.reports.export import to_csv

CASES = [
    pytest.param(
        (["a", "b"], [[None, 1], ["x,y", Money("2.50", "INR")]]),
        {},
        'a,b\n,1\n"x,y",2.50\n',
        None,
        id="case-1",
    ),
    pytest.param(
        (["a", "b"], [[1, None], [Money("2.50", "INR"), "x,y"]]),
        {},
        'a,b\n1,\n2.50,"x,y"\n',
        None,
        id="case-2",
    ),
    pytest.param(
        (["name", "note"], [['say "hi"', "a,b"], ["", "two\nlines"]]),
        {},
        'name,note\n"say ""hi""","a,b"\n,"two\nlines"\n',
        None,
        id="case-3",
    ),
    pytest.param(
        (["name", "note"], [['say "hi"', "a,b"]]),
        {},
        'name,note\n"say ""hi""","a,b"\n',
        None,
        id="case-4",
    ),
    pytest.param(
        (["name", "note"], [["two\nlines", ""], ['say "hi"', "a,b"]]),
        {},
        'name,note\n"two\nlines",\n"say ""hi""","a,b"\n',
        None,
        id="case-5",
    ),
    pytest.param(
        (["note", "name"], [['say "hi"', "a,b"], ["two\nlines", ""]]),
        {},
        'note,name\n"say ""hi""","a,b"\n"two\nlines",\n',
        None,
        id="case-6",
    ),
    pytest.param(
        ([], []),
        {},
        ReportError,
        None,
        id="case-7",
    ),
    pytest.param(
        (["a", "b"], [[2, 2], [3]]),
        {},
        ReportError,
        None,
        id="case-8",
    ),
    pytest.param(
        (["name", "note"], [['say "hi"'], ["two\nlines", ""]]),
        {},
        ReportError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0777(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            to_csv(*args, **kwargs)
    else:
        assert to_csv(*args, **kwargs) == expected
    if after is not None:
        assert args == after
