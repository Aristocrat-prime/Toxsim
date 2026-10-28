# Implementation status

This page distinguishes source that has been shared for review from files actually committed to this repository.

## Shared source snippet

The developer supplied a Python module defining `PoisonPK`, `PoisonSimulator`, and `create_poison_pk`. It imports NumPy and SciPy and calls a local `poison_database` module in its script entry point. The snippet has not yet been committed as a runnable application, and the database and UI modules are not included in the repository.

## Known limitations in the supplied snippet

These are review findings, not claims that the model has been validated.

- The function named `_competitive_inhibition` accepts `substrate_km` but does not use it.
- The inhibition constant is derived from a toxicity threshold. These are different concepts, and the code provides no scientific basis for equating them.
- Absorption rate is changed using the activity of the same enzymes listed as metabolic substrates. This is an assumption in the code, not a generally established PK relationship.
- The `half_life` field is stored but is not used to constrain the differential equations. The absorption rate is selected from a crude rule based on half-life.
- The default central and peripheral volumes, bioavailability, clearance, and intercompartmental clearance may be guesses rather than substance-specific estimates.
- The central-compartment concentration, peripheral-compartment concentration, and amounts need explicit unit checks. The code converts clearance to L/hr/kg, multiplies by body weight, and uses compartment volumes in litres; these relationships require careful dimensional verification.
- The final CYP activity reported is the mutable simulator state left after the numerical solver's last internal evaluation, not a time series and not necessarily the activity at the final requested time.
- The reported maximum organ accumulator is named `lethality_score`, but no validated relationship between that accumulator and mortality is defined. It must not be interpreted as a probability or a prediction of death.
- Organ damage uses a hand-defined threshold rule and recovery term without a documented empirical basis or validation data.
- The code does not demonstrate that multiple substances are chemically reacting. Adding substances to one simulation is not evidence of chemical compatibility or mixture chemistry.
- Input validation for duplicate names, negative doses, invalid parameter ranges, zero or negative thresholds, and empty inputs is not shown.

## Safe next milestones

1. Commit the complete source tree and record the Python version.
2. Document the origin and schema of each JSON data file.
3. Separate measured data, estimated values, and illustrative placeholders.
4. Add unit-aware parameter validation and tests using non-toxic synthetic examples.
5. Review equations and assumptions with a qualified pharmacometrics or toxicology specialist.
6. Remove or rename any output that implies validated injury or lethality unless a defensible validation protocol exists.
7. Add a reproducible test workflow and publish validation results before describing the software as predictive.

## Validation status

**Not validated for clinical, toxicological, or real-world exposure prediction.** No validation dataset, calibration report, uncertainty analysis, or independent review was supplied with the snippet.
