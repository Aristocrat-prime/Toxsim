# Model scope, assumptions, and limitations

A simulation is only as useful as its question, data, assumptions, and validation. This page sets out the minimum standard for interpreting or extending Toxsim as a research project.

## Intended scope

The repository is intended to support learning about general pharmacokinetic and toxicological concepts, including how ADME processes shape concentration over time; why model structure and parameter choices affect results; how variability, missing data, and uncertainty should be described; and how to document a scientific model so another researcher can review it.

## Out of scope

Toxsim documentation and future contributions should not be used to calculate or recommend a lethal, incapacitating, or otherwise harmful dose; plan poisoning or optimise toxic exposure; recommend combinations of toxic substances or provide mixture-planning instructions; predict a specific person's outcome from an unverified exposure; or replace emergency services, a poison centre, a clinician, or a qualified toxicologist.

## Questions every model should answer

**Purpose.** What specific research or teaching question does the model address?

**Model structure.** Is it a one-compartment or multi-compartment representation? Which biological processes are represented, and which are omitted?

**Data provenance.** Where did the parameter values come from? Were they measured in humans, animals, in vitro systems, or inferred from another model? Are the units and population clearly specified?

**Assumptions.** Does the model assume constant parameters, linear behaviour, complete mixing, or a particular route? What evidence supports those choices?

**Uncertainty.** Which inputs are uncertain? Are outputs sensitive to those inputs? Is uncertainty reported honestly?

**Validation.** Has the implementation been checked against published datasets or an independent reference implementation? Are the validation data separate from the data used to build or tune the model?

**Reproducibility.** Can another researcher inspect the code, reproduce the analysis, and understand the version of the data and dependencies used?

## Interpretation cautions

A model output is an estimate conditional on its assumptions. It is not direct evidence of what will happen in a real person. Model fit in one dataset does not guarantee performance in another population, route, formulation, or clinical setting.

Toxicity also cannot be inferred from pharmacokinetics alone. Effects may depend on the mechanism of action, active metabolites, tissue-specific exposure, timing, co-exposures, and individual susceptibility. Pharmacodynamics, clinical evidence, and context may be needed to interpret a concentration profile.

## Review checklist

- [ ] The research question and intended audience are stated.
- [ ] Every parameter has a definition, unit, source, and rationale.
- [ ] The model's structure and assumptions are documented.
- [ ] Missing values and data-quality issues are disclosed.
- [ ] Outputs include appropriate uncertainty or caveats.
- [ ] Validation methods and limitations are reported.
- [ ] No output is presented as individual medical advice.
- [ ] Safety and ethical review requirements have been considered.

## Handling real-world exposure concerns

If exposure is suspected, do not use a simulation to decide whether the situation is safe or whether care is needed. Contact local emergency services or a poison information service and follow qualified professional guidance.
