# Toxsim

Toxsim is a research and learning project for exploring toxicology concepts, with a focus on how the body handles substances over time. This repository documents the project's scientific background, assumptions, limitations, and responsible use.

The goal is to make pharmacokinetics easier to understand: what happens to a substance after it enters the body, how it moves between tissues, how it is transformed, and how it is eventually eliminated. These processes are often summarized as ADME: absorption, distribution, metabolism, and excretion.

## What this project is for

Toxsim is intended for classroom discussion and independent study of pharmacokinetics and toxicology; explaining concepts such as bioavailability, volume of distribution, clearance, and elimination half-life; reviewing how assumptions in a model affect outputs; and supporting conversations among students, researchers, and qualified professionals about the limits of simplified simulations.

## What it is not for

This project is not a medical device, clinical decision-support system, or substitute for professional toxicology advice. It must not be used to determine a safe or lethal dose, plan poisoning, select or combine toxic substances, predict the outcome of an exposure in a real person, or guide treatment. It does not validate any real-world exposure scenario.

A research-only label does not make every use safe. For that reason, this repository focuses on general scientific education, model transparency, and safety documentation. It does not provide instructions for preparing harmful mixtures or operational guidance for causing toxic effects.

If a real exposure may have occurred, contact local emergency services or a poison information service immediately. Do not wait for a simulation result.

## Pharmacokinetics at a glance

Pharmacokinetics describes the time course of a substance in the body.

- Absorption: movement from the site of exposure into systemic circulation.
- Distribution: movement between blood and tissues.
- Metabolism: chemical transformation, often involving enzymes in the liver and other tissues.
- Excretion: removal from the body, commonly through the kidneys or bile.

These processes interact. Their importance varies with the substance, route of exposure, formulation, physiology, age, organ function, co-exposures, and many other factors. A simplified model cannot capture every relevant variable.

## Repository guide

- docs/pharmacokinetics.md — introductory overview of ADME and related concepts.
- docs/model-scope.md — assumptions, limitations, and responsible interpretation.
- docs/glossary.md — plain-language definitions of common terms.
- docs/references.md — starting points for further reading.
- CONTRIBUTING.md — expectations for contributions.

## Project status

The repository currently contains scientific background and documentation. The Windows executable supplied separately has not been included or reviewed as source code. Its internal implementation, calculations, data sources, and validation status therefore remain unverified. Do not assume that any output from an executable is scientifically reliable.

## Responsible use

Use the material to learn, ask better research questions, and understand why toxicology is context-dependent. Do not use it to make real-world dosing or exposure decisions. Any future model implementation should document its data sources, units, assumptions, uncertainty, validation method, and intended audience before its results are interpreted.

## Disclaimer

This repository is provided for educational and research discussion only, without warranty of accuracy or fitness for a particular purpose. It does not provide medical advice. Users are responsible for complying with applicable laws, research ethics, and institutional safety requirements.
