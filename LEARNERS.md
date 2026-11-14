# Learner guide

Welcome! This repository is a practice codebase: **Python ShopCore**, the back-office
engine of a fictional online store. It works like a real product with real bug reports.
Each open issue is a bug that customers noticed. Your job is to find what causes it,
fix it, and prove the fix with the issue's test.

This guide covers everything from picking an issue to getting a green check.

---

## 1. What you need

- A GitHub account
- `git` and `make`
- Python 3.12

## 2. Pick an issue

Open the **Issues** tab. Every issue has:

| Part | What it tells you |
|---|---|
| Title and "What's happening" | What a user sees going wrong. It never names a file or a function; finding the cause is the exercise. |
| Labels | `difficulty:easy` means the cause is close to where the symptom shows. `difficulty:medium` means it's further away, or only some inputs trigger it. `module:<name>` is the area of the shop where the symptom shows. |
| Example | One concrete wrong result, when there is one. |
| Test to make pass | The test that checks your fix, plus the command to run it. |

New here? Start with a `difficulty:easy` issue.

## 3. Fork, clone and set up

1. Click **Fork** at the top of this page.
2. Clone **your fork** and set it up:

```sh
git clone https://github.com/<your-username>/shopcore-python-s1.git
cd shopcore-python-s1
python3.12 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
```

## 4. Reproduce the bug

Run the issue's test. The command is in the issue; it looks like this:

```sh
make test TESTS="tests/issues/test_issue_0009.py::test_issue_0009"
```

It should **fail**. Read the output: which inputs fail, what was expected, and what
came back. That's your first clue.

> `main` contains **every** open bug at once. If you run the full `make test`, the
> tests of all other open issues fail too. That's expected; only your issue's test
> matters.

## 5. Find the cause

- **Start where the symptom shows.** Find the code behind the behaviour the issue
  describes (`ARCHITECTURE.md` maps the modules), then follow the calls inward.
- **Read the test.** It shows the exact inputs that fail and the ones that must keep
  working. The difference between them points at the bug.
- **Compare with similar code.** Bugs are small: a boundary off by one, a flipped
  condition, a value not updated, a missing step. Similar code nearby usually shows
  how it should look.
- **Medium issues** often start in a different module from where the symptom shows.
  Keep following the data.

## 6. Fix it

- Change the application code only, under `shopcore/`.
- **Don't edit tests or build files.** Tests, `.github/`, `.virtint/`, the build files
  and everything in `.virtint/protected.txt` are reset to `main`'s version before your
  fix is checked. Editing them has no effect.
- Fix the cause, not the test inputs. The test checks several inputs, including some
  that must keep working, so special-casing one value won't pass.
- Keep the change small: usually a line or two.

Before pushing, check your issue's test passes and you haven't broken anything else:

```sh
make test TESTS="<your issue's test>"   # must pass now
make test                               # only other issues' tests may fail
make lint
```

## 7. Open a pull request

1. Commit on a branch and push it to your fork.
2. Open a pull request from your fork to **this repository's `main`**.
3. In the description, write **`Fixes #<issue number>`**, for example `Fixes #12`.
   This is how the check knows which issue you're fixing. `Closes #12` and
   `Resolves #12` also work.

One issue per pull request. To fix another issue, open another pull request from a
separate branch.

## 8. Read the result

A check called **check-fix** runs on your pull request automatically, and again every
time you push or edit the description.

- ✅ **Green:** your issue's test passes. Done!
- ❌ **Red:** click **Details** next to check-fix, then open the step
  **"Run the issue's test"** to see the test output. Fix, push again, and the check
  reruns.

Common messages:

| Message | What to do |
|---|---|
| `Say which issue this pull request fixes` | Add `Fixes #<number>` to the pull request description. |
| `#N is not an issue of this repository` / `That issue is not a task of this repository` | Check the number. It must be one of this repository's open issues, not a pull request. |
| `These files are tests or build files and were reset` | You changed protected files. That's only a warning: they were put back, and your fix was checked without them. |
| `FAIL: <test>` | The test still fails. Read the output above it. |

If the check doesn't start at all, GitHub may be waiting for a maintainer to approve
workflows for a brand-new GitHub account. It runs once approved.

## 9. Good habits

- In the pull request, explain the **root cause** in a sentence or two: what was wrong
  and why your change fixes it.
- Don't copy other learners' pull requests. They're public, but you only learn by
  tracing the bug yourself.
- Stuck? Re-read the test, add a print or log near the suspect code, and run the one
  test again. It's fast.

If you joined through **VirtInt**, your dashboard assigns you one issue at a time and
records a pass when your pull request goes green. A passing pull request is closed
**without merging**, so the bug stays in place for other learners. That's normal.
