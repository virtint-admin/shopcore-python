"""Index public functions and the tests that pin them.

Writes ``.virtint/functions.json``::

    {"shopcore.tax.rules.apply_regional_tax": {
        "file": "shopcore/tax/rules.py", "start_line": 101, "end_line": 116,
        "tests": ["tests/tax/test_rules.py::test_apply_regional_tax_excludes_shipping", ...]}}

A test belongs to function ``f`` when it lives under ``tests/<module>/`` and
its name is ``test_<f>`` or starts with ``test_<f>_`` (the longest matching
function name wins). ``--check`` exits 1 if any public function has fewer
than ``--min-tests`` tests (default 3) or any test maps to no function.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "shopcore"
TESTS = ROOT / "tests"


def _snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def public_functions() -> dict[str, dict[str, object]]:
    """Public module-level functions, plus public classes that define methods.

    Classes are keyed by their real name (``shopcore.money.core.Money``) and
    matched to tests through the snake-case form (``test_money_...``).
    """
    found: dict[str, dict[str, object]] = {}
    for path in sorted(PACKAGE.rglob("*.py")):
        rel = path.relative_to(ROOT)
        if any(part.startswith("_") and part != "__init__.py" for part in rel.parts):
            continue
        module = ".".join(rel.with_suffix("").parts)
        tree = ast.parse(path.read_text("utf-8"), filename=str(rel))
        for node in tree.body:
            is_function = isinstance(node, ast.FunctionDef)
            is_class_with_methods = isinstance(node, ast.ClassDef) and any(
                isinstance(item, ast.FunctionDef) for item in node.body
            )
            if (is_function or is_class_with_methods) and not node.name.startswith("_"):
                assert isinstance(node, ast.FunctionDef | ast.ClassDef)
                found[f"{module}.{node.name}"] = {
                    "file": rel.as_posix(),
                    "start_line": node.lineno,
                    "end_line": node.end_lineno,
                    "tests": [],
                }
    return found


def test_functions() -> list[tuple[str, str, str]]:
    """(domain module, test id, test name) for every top-level test function."""
    tests = []
    for path in sorted(TESTS.rglob("test_*.py")):
        rel = path.relative_to(ROOT)
        domain = rel.parts[1] if len(rel.parts) > 2 else ""
        tree = ast.parse(path.read_text("utf-8"), filename=str(rel))
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                tests.append((domain, f"{rel.as_posix()}::{node.name}", node.name))
    return tests


def build_index() -> tuple[dict[str, dict[str, object]], list[str]]:
    functions = public_functions()
    by_domain: dict[str, list[str]] = {}
    for qualified in functions:
        by_domain.setdefault(qualified.split(".")[1], []).append(qualified)
    orphans = []
    for domain, test_id, name in test_functions():
        candidates = [
            q
            for q in by_domain.get(domain, [])
            if name == f"test_{_snake(q.rsplit('.', 1)[1])}"
            or name.startswith(f"test_{_snake(q.rsplit('.', 1)[1])}_")
        ]
        if not candidates:
            orphans.append(test_id)
            continue
        # Prefer the longest function name, then a test file mirroring the source file.
        stem = test_id.split("::")[0].rsplit("/", 1)[1].removeprefix("test_").removesuffix(".py")
        best = max(
            candidates,
            key=lambda q: (len(q.rsplit(".", 1)[1]), q.split(".")[-2] == stem),
        )
        tests = functions[best]["tests"]
        assert isinstance(tests, list)
        tests.append(test_id)
    return functions, orphans


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(ROOT / ".virtint" / "functions.json"))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--min-tests", type=int, default=3)
    args = parser.parse_args()
    functions, orphans = build_index()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(functions, indent=2) + "\n", "utf-8")
    thin = {q: len(v["tests"]) for q, v in functions.items() if len(v["tests"]) < args.min_tests}  # type: ignore[arg-type]
    total_tests = sum(len(v["tests"]) for v in functions.values())  # type: ignore[arg-type]
    print(f"{len(functions)} public functions, {total_tests} mapped tests, {len(orphans)} unmapped")
    for q, n in sorted(thin.items()):
        print(f"  too few tests ({n}): {q}")
    for test_id in orphans:
        print(f"  unmapped test: {test_id}")
    if args.check and (thin or orphans):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
