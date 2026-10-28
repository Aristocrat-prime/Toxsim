# Tests

This repository currently includes automated tests for its documentation-integrity helper. Run them from the repository root:

```bash
python -m pip install -r requirements-dev.txt
python scripts/check_repository.py
python -m pytest -q
```

The checks cover extracting local Markdown/HTML links, accepting valid local targets, detecting missing targets, and rejecting paths that escape the repository root.

## Future test coverage

When the complete application modules and data schemas are reviewed and included, additional tests may cover:

- JSON syntax and schema validation using synthetic fixtures.
- Required-field and type validation.
- Handling of missing or malformed records.
- Deterministic tests using clearly labelled synthetic examples.
- Plot creation and interface smoke tests that do not require external network access.
- Regression tests for confirmed defects.

Tests must not use real toxic mixtures or harmful dose scenarios as fixtures. Passing software tests demonstrates that code behaves as specified; it does not validate a model against real human outcomes.
