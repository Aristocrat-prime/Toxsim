<p align="center">
  <img src="assets/toxsim-banner.svg" alt="Toxsim — pharmacokinetics, molecular data, and model transparency" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Aristocrat-prime/Toxsim/actions/workflows/checks.yml"><img alt="Python checks" src="https://github.com/Aristocrat-prime/Toxsim/actions/workflows/checks.yml/badge.svg"></a>
  <img alt="Python 3.11–3.12" src="https://img.shields.io/badge/python-3.11%20%7C%203.12-3776AB?logo=python&logoColor=white">
  <img alt="Status: desktop data-review console" src="https://img.shields.io/badge/status-desktop%20data%20review-0f766e">
  <img alt="Research and education" src="https://img.shields.io/badge/focus-research%20%26%20education-0f766e">
</p>

<h1 align="center">Toxsim</h1>

<p align="center">
  <strong>Explore the model. Inspect the assumptions. Keep the evidence visible.</strong><br>
  An educational research project for pharmacokinetics, molecular information, and model transparency.
</p>

---

## About the project

Toxsim is a transparent, reviewable codebase for learning about pharmacokinetic concepts, molecular data, scientific assumptions, and the limits of simplified models. The project emphasises traceable data, explicit units, reproducible checks, and honest communication of uncertainty.

> [!IMPORTANT]
> **Research notice:** Toxsim is not a medical device or clinical decision-support system. The desktop console currently included in this repository checks JSON readability and aggregate metadata coverage; it does not run the archived toxicology simulation engine or provide predictions of injury or death. Do not use this project to plan exposures or make treatment decisions.

## Current application status

The repository includes a runnable Python desktop **data-review console**. It opens a native window, checks the tracked JSON cache, and displays aggregate file and metadata-coverage checks. This is an actual launchable desktop component, but it is **not the complete original desktop application from the supplied archive**.

| Area | Current status |
| --- | --- |
| Desktop data-review console | Included; launch instructions below |
| Windows launcher | `scripts/run_desktop.bat` |
| JSON integrity and metadata coverage | Included and unit-tested |
| Original archived dashboard and simulation engine | Not integrated into this console |
| Scientific or toxicological model validation | Not complete |
| Release licence and asset-rights review | Owner decision and review still required |

## Launch the desktop console

Requirements: Python 3.11 or 3.12 and a Python distribution with Tkinter.

Clone and prepare the repository:

```powershell
git clone https://github.com/Aristocrat-prime/Toxsim.git
cd Toxsim
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e . --no-deps
```

Then launch either by double-clicking `scripts/run_desktop.bat` or running:

```powershell
python -m toxsim
```

After editable installation, this command is also available:

```powershell
toxsim-desktop
```

The desktop console uses Python's standard library and does not require the scientific dependencies merely to open the data-review window.

## Run repository checks

Install test dependencies and run:

```powershell
python -m pip install -r requirements-dev.txt
python scripts/check_repository.py
python scripts/check_data_files.py
python -m pytest -q
```

These checks validate repository integrity and the data-review code; they do not validate scientific predictions.

## Documentation

- [Desktop launch and scope](docs/desktop-app.md)
- [Installation and troubleshooting](docs/installation.md)
- [Implementation status](docs/implementation-status.md)
- [Data policy](docs/data-policy.md)
- [Model scope and limitations](docs/model-scope.md)
- [Final handoff and release gates](docs/release-handoff.md)
- [Contribution guide](CONTRIBUTING.md)
- [References](docs/references.md)

## Scientific integrity

- Keep provenance attached to each value.
- Do not disguise uncertainty with plausible-looking defaults.
- A chemical identifier or structure string does not establish human pharmacokinetics, mixture compatibility, toxicity, or clinical outcome.
- Software tests check code behaviour; they do not establish that a model predicts real-world biology accurately.

## Disclaimer

This project is provided for educational and research discussion only, without warranty of accuracy or fitness for a particular purpose. It does not provide medical advice.
