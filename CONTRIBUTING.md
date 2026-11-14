# Contributing

1. Branch from `main`; one fix per pull request.
2. Change code under `shopcore/` only. Tests, build files and CI are protected
   (`.virtint/protected.txt`); a PR that touches them is rejected automatically.
3. Before pushing run `make build lint` and the tests of your issue
   (`make test TESTS="<id>;<id>"`). Do not add new ruff findings.
   `main` carries every open issue, so in a full `make test` run the tests named in
   other open issues fail. That is expected; your change must not break any other test.
4. Keep functions pure: pass time in, return values out, raise the module's
   `ShopCoreError` subclass on bad input.
5. Describe the customer-visible effect in the PR description, not just the code change.
