"""Run ruff on the package and write ``reports/lint.json`` in the grader's format.

Output: ``{"tool": "ruff", "errors": [{"path", "line", "code", "message"}]}``
with repo-relative POSIX paths, sorted by (path, line, code). Exit status is 0
unless ruff itself crashes (ruff exit code >= 2), in which case it is passed on.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    out = Path(argv[1]) if len(argv) > 1 else ROOT / "reports" / "lint.json"
    targets = argv[2:] or ["shopcore"]
    proc = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "--no-cache", "--output-format", "json", *targets],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode >= 2:
        sys.stderr.write(proc.stderr)
        return proc.returncode
    errors = []
    for item in json.loads(proc.stdout or "[]"):
        path = Path(item["filename"]).resolve()
        try:
            rel = path.relative_to(ROOT).as_posix()
        except ValueError:
            rel = path.as_posix()
        errors.append(
            {
                "path": rel,
                "line": item["location"]["row"],
                "code": item["code"] or "E999",
                "message": item["message"],
            }
        )
    errors.sort(key=lambda e: (e["path"], e["line"], e["code"]))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"tool": "ruff", "errors": errors}, indent=2) + "\n", "utf-8")
    print(f"lint: {len(errors)} error(s) -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
