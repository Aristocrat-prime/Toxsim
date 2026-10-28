# Tests

Automated tests will be added when the full application modules and data schemas are committed. There are no executable project tests in this scaffold yet.

Recommended initial coverage:

- JSON syntax and schema validation for the PubChem cache and SMILES repair mapping.
- Required-field, type, unit, and range validation.
- Handling of missing or malformed records.
- Deterministic tests using clearly labelled synthetic values.
- Numerical sanity checks for a simple, non-toxic educational one-compartment example.
- Plot creation and UI smoke tests that do not require external API access.
- Regression tests for any previously corrected defects.

Tests must not use real toxic mixtures or harmful dose scenarios as their fixtures. Passing software tests demonstrates that code behaves as specified; it does not validate the model against real human outcomes.
