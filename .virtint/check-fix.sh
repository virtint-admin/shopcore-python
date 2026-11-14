#!/usr/bin/env bash
# Grade one pull request of a task repo: does it make the linked issue's test pass?
# Run by .github/workflows/check-fix.yml from the DEFAULT BRANCH's copy (never the PR's).
#
#   check-fix.sh issue-number          PR_BODY, PR_TITLE -> prints N from "Fixes #N"
#   check-fix.sh test-id   BASE        ISSUE_BODY -> prints the issue's test id
#   check-fix.sh restore   BASE PR     put tests/build files of BASE over PR
#   check-fix.sh run       PR TEST_ID  SETUP_COMMAND, then `make test TESTS=<id>`
#
# Trust: BASE is the default branch; ISSUE_BODY is written by the maintainers; PR and
# PR_BODY/PR_TITLE come from the student and are only parsed, never executed (except
# PR's application code, which is what is being tested).
set -euo pipefail

fail() { echo "::error::$1" >&2; exit 1; }

cmd="${1:-}"
case "$cmd" in
issue-number)
  text="${PR_TITLE:-} ${PR_BODY:-}"
  n="$(grep -oiE '\b(fix|fixes|fixed|close|closes|closed|resolve|resolves|resolved)[[:space:]]+#[0-9]{1,9}\b' <<<"$text" | head -n1 | grep -oE '[0-9]+$' || true)"
  [[ -n "$n" ]] || fail "Say which issue this pull request fixes: put \"Fixes #<issue number>\" in its description."
  echo "$n"
  ;;

test-id)
  base="$2"
  id="$(grep -oE '<!--[[:space:]]*virtint-issue:[[:space:]]*[A-Z]+-[0-9]+[[:space:]]*-->' <<<"${ISSUE_BODY:-}" | head -n1 | grep -oE '[A-Z]+-[0-9]+' || true)"
  [[ -n "$id" ]] || fail "That issue is not a task of this repository."
  [[ -f "$base/.virtint/tests.txt" ]] || fail ".virtint/tests.txt is missing on the default branch"
  tid="$(awk -v id="$id" '$1 == id { print $2; exit }' "$base/.virtint/tests.txt")"
  [[ -n "$tid" ]] || fail "Issue $id has no test in .virtint/tests.txt"
  [[ "$tid" =~ ^[A-Za-z0-9_./:#]+$ ]] || fail "bad test id for $id"
  echo "$tid"
  ;;

restore)
  base="$2"; pr="$3"
  # Everything a solution may not change: these, plus base/.virtint/protected.txt.
  PROTECTED_DIRS=(tests src/test .github .virtint)
  PROTECTED_FILES=(conftest.py pytest.ini pyproject.toml setup.cfg tox.ini pom.xml build.gradle build.gradle.kts CMakeLists.txt Makefile)
  EXTRA=()
  if [[ -f "$base/.virtint/protected.txt" ]]; then
    while IFS= read -r line || [[ -n "$line" ]]; do
      line="${line%%#*}"; line="${line//[[:space:]]/}"
      if [[ -n "$line" ]]; then EXTRA+=("${line//\*\*/*}"); fi
    done < "$base/.virtint/protected.txt"
  fi
  matches() {  # matches <path> <pattern>...: exact path, directory prefix or glob
    local rel="$1" p
    shift
    for p in "$@"; do
      p="${p%/}"
      [[ -n "$p" ]] || continue
      # shellcheck disable=SC2053
      if [[ "$rel" == "$p" || "$rel" == "$p"/* || "$rel" == $p ]]; then return 0; fi
    done
    return 1
  }
  protected() {
    local rel="$1" f
    if matches "$rel" "${PROTECTED_DIRS[@]}"; then return 0; fi
    for f in "${PROTECTED_FILES[@]}"; do
      if [[ "${rel##*/}" == "$f" ]]; then return 0; fi
    done
    [[ ${#EXTRA[@]} -gt 0 ]] && matches "$rel" "${EXTRA[@]}"
  }
  list() {  # every file and symlink of a tree, repo-relative, NUL-separated
    ( cd "$1" && find . -path ./.git -prune -o \( -type f -o -type l \) -print0 ) | sed -z 's|^\./||' | sort -z
  }
  pr_root="$(realpath "$pr")"
  changed=()
  while IFS= read -r -d '' rel; do  # 1. drop the PR's copy of every protected path
    if protected "$rel"; then
      if [[ ! -f "$base/$rel" ]] || ! cmp -s "$base/$rel" "$pr/$rel"; then changed+=("$rel"); fi
      rm -f -- "$pr/$rel"
    fi
  done < <(list "$pr")
  while IFS= read -r -d '' rel; do  # 2. copy the default branch's version back in
    protected "$rel" || continue
    dir="$(realpath -m -- "$pr/$(dirname "$rel")")"
    [[ "$dir" == "$pr_root" || "$dir" == "$pr_root"/* ]] || fail "$(dirname "$rel") leaves the repository through a symlink"
    mkdir -p "$dir"
    cp -a -- "$base/$rel" "$pr/$rel"
  done < <(list "$base")
  if [[ ${#changed[@]} -gt 0 ]]; then
    echo "::warning::These files are tests or build files and were reset to the default branch's version: ${changed[*]}"
  fi
  echo "tests and build files restored from the default branch"
  ;;

run)
  pr="$2"; tid="$3"
  cd "$pr"
  if [[ -n "${SETUP_COMMAND:-}" ]]; then bash -euo pipefail -c "$SETUP_COMMAND"; fi
  echo "running $tid"
  set +e
  make test TESTS="$tid"
  code=$?
  set -e
  if [[ $code -eq 0 ]]; then echo "PASS: $tid"; else echo "::error::FAIL: $tid (exit code $code)"; fi
  exit "$code"
  ;;

*)
  fail "usage: check-fix.sh issue-number | test-id BASE | restore BASE PR | run PR TEST_ID"
  ;;
esac
