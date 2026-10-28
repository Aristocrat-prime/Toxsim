# Toxsim

Toxsim is an educational research project for exploring pharmacokinetics (PK), molecular information, and the limits of simplified toxicology models. The repository is being organised so that its code, datasets, scientific assumptions, tests, and user documentation can be reviewed separately.

> **Research and safety notice:** Toxsim is not a medical device or clinical decision-support system. Do not use it to choose doses, plan poisoning, select or combine toxic substances, interpret a real exposure, or make treatment decisions. Model outputs must not be treated as validated predictions of injury or death. For a suspected exposure, contact local emergency services or a poison information service immediately.

## Current status

The repository currently contains background documentation and a project scaffold. Source code for the desktop interface and engine, plus the PubChem cache and SMILES repair data mentioned by the developer, still need to be added and reviewed before the project can be installed or run from this repository.

The supplied engine snippet includes unvalidated assumptions and a so-called lethality score. That score is a model-specific number, not a validated probability of death or a clinical endpoint. The snippet also derives inhibition constants from a toxicity threshold and uses rough default parameters for missing data. Those are substantial scientific limitations. Any implementation intended for education should make assumptions visible and avoid presenting unvalidated injury or lethality outputs as reliable predictions.

## Project goals

- Explain PK concepts such as absorption, distribution, metabolism, and excretion (ADME).
- Keep source code, data files, citations, and documentation organised.
- Record data provenance, units, assumptions, and uncertainty.
- Add reproducible tests for data loading, input validation, numerical behaviour, and user-interface components.
- Make it clear which outputs are illustrative and which, if any, have been independently validated.

## Repository map

```text
Toxsim/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── CONTRIBUTING.md
├── docs/
│   ├── installation.md
│   ├── pharmacokinetics.md
│   ├── model-scope.md
│   ├── data-policy.md
│   ├── glossary.md
│   ├── references.md
│   └── implementation-status.md
├── data/
│   └── README.md
├── src/
│   └── toxsim/                 # planned application package
├── tests/
│   └── README.md
└── .github/
    └── workflows/
        └── checks.yml
```

The `src/` package and automated tests are planned locations; they are not complete merely because the folders appear in this diagram.

## Requirements

- Windows 10/11, macOS, or a current Linux distribution.
- Python 3.11 or 3.12 recommended.
- Git, if you intend to clone the repository.
- The Python libraries listed in [requirements.txt](requirements.txt).
- RDKit is needed only for molecular structure features. Installation can vary by operating system; see [the installation guide](docs/installation.md).

## Quick start

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/Aristocrat-prime/Toxsim.git
cd Toxsim
python -m venv .venv
```

Activate it:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install the baseline dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

This installs the documented baseline libraries only. It does **not** make the application runnable until the actual application modules and required data files have been added. See [Installation](docs/installation.md).

## Data and scientific integrity

Do not treat missing values as measured facts. Each compound record should preserve its source, retrieval date, units, and whether a value is measured, estimated, assumed, or unavailable. PubChem identifiers and SMILES strings describe chemical records; they do not establish human pharmacokinetic parameters, toxicity thresholds, mixture compatibility, or clinical outcomes.

See [Data policy](docs/data-policy.md) and [Implementation status](docs/implementation-status.md).

## Documentation

- [Pharmacokinetics overview](docs/pharmacokinetics.md)
- [Model scope and limitations](docs/model-scope.md)
- [Data provenance and JSON files](docs/data-policy.md)
- [Installation and troubleshooting](docs/installation.md)
- [Implementation status and remaining work](docs/implementation-status.md)
- [Glossary](docs/glossary.md)
- [References](docs/references.md)
- [Contribution guide](CONTRIBUTING.md)

## Disclaimer

This project is provided for educational and research discussion only, without warranty of accuracy or fitness for a particular purpose. It does not provide medical advice. Any future model should be reviewed by qualified domain experts and validated against appropriate, documented reference data before its outputs are used beyond classroom illustration.
