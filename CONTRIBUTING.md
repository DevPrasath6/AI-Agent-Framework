# Contributing to AI Agent Framework

Thank you for your interest in contributing! We welcome contributions of all
kinds: bug reports, feature requests, documentation improvements, tests, and
code.

## How to contribute

1. Fork the repository and create a branch for your change:

   - Use a descriptive branch name, e.g. `fix/auth-bug` or `feat/metrics`.

2. Follow the coding standards

   - Python: follow PEP8. We recommend using ruff/black for formatting.
   - Add or update unit tests for your change under `tests/`.

3. Run tests locally

   - Create a virtual environment and install dependencies from
     `requirements.txt` and `requirements-dev.txt`.
   - Run the test suite: see `pytest.ini` for configuration.

4. Open a pull request

   - Provide a clear title and description of your change.
   - Link related issues and include screenshots or logs if applicable.
   - The maintainers will review your PR. Address review comments as needed.

## Development setup (quick)

- Python 3.10+ recommended.
- Create a virtualenv: `python -m venv .venv` ; then activate it.
- Install dependencies: `pip install -r requirements.txt -r requirements-dev.txt`
- Run tests: `pytest -q`

## Branching and releases

- We use `main` as the primary development branch. Create feature branches
  from `main` and open PRs against `main`.
- Release branches/tags will be created by maintainers.

## Code reviews and CI

- All PRs should pass automated checks (lint, tests) before merging.
- Maintain a clear commit history; use small, focused commits.

If you'd like help getting started, please open an issue and we'll point you to
good first issues.
