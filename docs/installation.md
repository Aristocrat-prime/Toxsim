# Installation and troubleshooting

## Status first

The repository includes a runnable desktop **data-review console**. It checks the tracked JSON cache and displays aggregate file and metadata-coverage results. It is not the complete original desktop application from the supplied archive; the archived dashboard and simulation engine are not integrated into this console.

The tracked JSON files' presence and successful parsing do not verify chemical identity, provenance, or toxicological accuracy.

## Recommended environment

- Python 3.11 or 3.12
- Windows 10/11 for the supplied double-click launcher
- A Python distribution that includes Tkinter

## Launch on Windows

For the quickest launch, open the repository folder and double-click:

```text
scripts/run_desktop.bat
```

The launcher sets the source path so an editable package installation is not required. Or, from the repository root, run:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m toxsim
```

To register the command in a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e . --no-deps
toxsim-desktop
```

The console uses the Python standard library and tracked `pubchem_cache.json`; it does not need the project's scientific dependencies merely to open.

## Build a Windows executable

The GitHub Actions workflow named **Build Windows desktop console** builds a single-file Windows executable and publishes it as an Actions artifact. Open the workflow's latest successful run and download the `Toxsim-Data-Review-Windows` artifact. The artifact is a ZIP containing `Toxsim-Data-Review.exe`; it is not the archived original application.

## Run repository checks

```powershell
python -m pip install -r requirements-dev.txt
python scripts/check_repository.py
python scripts/check_data_files.py
python -m pytest -q
```

These checks validate repository integrity and the data-review code; they do not validate scientific predictions.

## RDKit note

RDKit installation support differs by Python version and operating system. If pip cannot find a compatible wheel, use the official RDKit installation instructions or a Conda environment.

Official project: https://www.rdkit.org/docs/Install.html

## Original archive status

The original archived dashboard and simulation engine are not restored by this console. Their dependencies, assets, application integration, scientific assumptions, and distribution suitability remain separate review tasks. This repository does not claim that the original simulation model is scientifically validated.
