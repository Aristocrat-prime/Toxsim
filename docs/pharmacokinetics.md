# Pharmacokinetics: the basics

Pharmacokinetics is the study of how the body handles a substance over time. It is often introduced through four connected processes: absorption, distribution, metabolism, and excretion (ADME). The framework is useful, but it is a simplification. Real biological systems are variable, and the same substance may behave differently across people and circumstances.

This page is a conceptual introduction for study and research. It is not a guide to dosing, exposure planning, or treating poisoning.

## 1. Absorption

Absorption is the movement of a substance from its entry point into the body's circulation. How much is absorbed, and how quickly, can depend on the route of exposure, the substance's physical and chemical properties, the formulation, and the condition of the exposed tissue.

Bioavailability is the fraction of an administered amount that reaches systemic circulation in an unchanged form. It is not the same as the amount initially encountered, and it can vary substantially by route.

The timing of absorption matters. Two exposures that produce similar overall systemic availability may still have different concentration-time profiles. A simple model may represent absorption as a single process, while real absorption can be delayed, incomplete, or affected by several mechanisms.

## 2. Distribution

Once in circulation, a substance may move into tissues and organs. Distribution depends on factors such as blood flow, tissue composition, binding to proteins, membrane permeability, and the substance's affinity for particular tissues.

Volume of distribution is a model-derived parameter relating the amount of substance in the body to its measured concentration in blood or plasma. It is not a literal anatomical volume. It helps describe how extensively a substance appears to distribute beyond the sampled circulation, but it cannot by itself identify where the substance is located or predict an individual outcome.

Distribution can change over time. Some substances enter certain tissues slowly, bind to tissue components, or move back into circulation later. A one-compartment model may not represent these patterns adequately.

## 3. Metabolism

Metabolism is the chemical transformation of a substance by the body. Enzymes in the liver are often important, although metabolism can also occur in the gut, blood, kidneys, lungs, and other tissues.

Transformation does not always mean detoxification. A metabolite may be less active, more readily eliminated, still biologically active, or more harmful than the original compound. The direction and extent of these changes depend on the specific substance and biological context.

Metabolism can vary because of genetics, age, health, enzyme activity, other medicines or substances, and prior exposure. Models that use a single fixed metabolic rate may hide this variability.

## 4. Excretion

Excretion is the removal of a substance or its metabolites from the body. The kidneys and urine are common routes, while bile and feces, exhaled air, and other pathways can also contribute.

Clearance describes the body's apparent efficiency in removing a substance from a defined fluid, usually plasma. It is a rate-like parameter with units of volume per time. Clearance is not the same thing as the amount removed at one moment, and it may not remain constant under every condition.

Impaired organ function, changes in blood flow, transporter activity, and interactions with other substances can alter elimination. A model should state which elimination pathways it represents and which it leaves out.

## Concentration over time

A concentration-time profile describes how the measured concentration changes after an exposure or administration. Its shape reflects the combined effects of absorption, distribution, metabolism, and excretion.

- Cmax: the highest observed or modelled concentration in a specified profile.
- Tmax: the time at which that maximum occurs.
- Area under the curve (AUC): a measure of total concentration over a defined period.
- Elimination half-life: the time required for concentration to fall by half during a phase where the relevant elimination process behaves accordingly.

These terms are useful for comparing research observations, but they do not independently establish toxicity, safety, or clinical outcome. Interpretation depends on the substance, the measured biological compartment, the sampling window, the model, and the question being asked.

## Linear and nonlinear behaviour

Some pharmacokinetic models assume approximately linear behaviour over the range being studied: the relationship between exposure and measured concentration follows a consistent pattern, and parameters remain reasonably stable. Other substances or conditions show nonlinear behaviour, for example when enzymes or transporters become saturated, binding changes, or physiological systems are altered.

A linear assumption should therefore be treated as a modelling choice, not a universal biological rule. The assumptions need to be visible and justified for the research question.

## Inter-individual variability

People do not share identical pharmacokinetic parameters. Age, body composition, genetics, pregnancy, disease, hydration, nutrition, organ function, environmental factors, and co-exposures may all matter. Measurement error and differences in sampling can add further uncertainty.

Population averages are useful for research, but an average is not a reliable prediction for every individual. A responsible report should distinguish measured findings from estimates and should describe uncertainty rather than presenting a single output as a certainty.

## What this means for Toxsim

For any simulation, documentation should make clear what scientific question the model is designed to explore; which processes and compartments are represented; which assumptions are fixed and which parameters vary; where input data came from and whether they apply to the intended context; how outputs were checked against independent evidence; and what the model cannot infer.

Without source code, data provenance, and validation evidence, a simulation's internal calculations cannot be independently assessed. The presence of a numerical result is not proof that the result is accurate.

## Further reading

See docs/references.md for authoritative starting points. This overview is educational and intentionally does not provide substance-specific dose calculations, harmful exposure scenarios, or treatment instructions.
