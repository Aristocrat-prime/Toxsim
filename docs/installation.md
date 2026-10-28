# Installation and troubleshooting

## Status first

The current GitHub repository is a tested documentation and repository-maintenance scaffold, **not a runnable release of the original desktop application**. The archive audit identified the desktop interface (`poison_dashboard.py`), simulation engine (`poison_pk_engine.py`), and full database module (`poison_database.py`), but these are not integrated as a runnable app in this checkout.

The tracked `pubchem_cache.json` and `smiles_repairs.json` files are present. Their presence and successful JSON parsing do not verify chemical identity, provenance, or toxicological accuracy. Installing dependencies alone will not launch the desktop UI.

## Recommended environment

- Python 3.11 or 3.12
- Git
- A virtual environment dedicated to this project
- Windows 10/11, macOS, or Linux for repository checks

Check your Python version:

```bash
python --version
```

## Clone and create an environment

```bash
git clone https://github.com/Aristocrat-prime/Toxsim.git
cd Toxsim
python -m venv .venv
```

Activate the environment.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install the repository's declared dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run repository checks

These commands validate documentation links, tracked JSON syntax/basic shape, and the current automated tests. They do **not** run the original desktop app or validate toxicological predictions.

```bash
python scripts/check_repository.py
python scripts/check_data_files.py
python -m pytest -q
```

## RDKit note

RDKit installation support differs by Python version and operating system. If pip cannot find a compatible wheel, use the official RDKit installation instructions or a Conda environment. Do not download unofficial binary builds from untrusted sites.

Official project: https://www.rdkit.org/docs/Install.html

## What remains before the original app can be called runnable

1. Decide, with appropriate safety review, what original application components and data are suitable for distribution.
2. Inventory and review the source archive, dependencies, assets, and third-party notices.
3. Integrate non-operational UI and file-handling components only after their source and asset rights are established.
4. Reconcile dependencies against the full application source and test a clean supported environment.
5. Preserve per-field data provenance; do not present unknown or synthetic defaults as verified scientific values.
6. Have qualified reviewers assess scientific assumptions before making predictive claims.
7. Document an application launch command only after the actual entry point has been integrated and tested.

Do not infer a launch command from a partial code snippet or from the presence of packaging metadata. See the [final handoff and release gates](release-handoff.md) for the full remaining checklist.
