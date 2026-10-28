# Installation and troubleshooting

## Status first

The repository is currently a documentation and setup scaffold. The desktop interface, complete Python modules, and JSON data files described by the developer have not yet been committed here. Installing dependencies alone will not launch Toxsim.

## Recommended environment

- Python 3.11 or 3.12
- Git
- A virtual environment dedicated to this project
- Windows 10/11, macOS, or Linux

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

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## RDKit note

RDKit installation support differs by Python version and operating system. If pip cannot find a compatible wheel, use the official RDKit installation instructions or a Conda environment. Do not download unofficial binary builds from untrusted sites.

Official project: https://www.rdkit.org/docs/Install.html

## Still required before launch

1. Add the actual application entry point and UI modules.
2. Add or document every imported local module, including `poison_pk_engine.py`, `poison_database.py`, and any interface modules.
3. Add the PubChem cache and SMILES repair JSON files, with provenance and schema documentation.
4. Confirm the correct dependency versions against all imports.
5. Add tests and run them on a clean environment.
6. Document the command used to launch the app only after the actual entry point is confirmed.

Do not guess the launch command from a partial code snippet.
