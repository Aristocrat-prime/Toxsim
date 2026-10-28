# Development and quality checks

This guide covers the checks that can run while the repository is still being prepared. It does not imply that the desktop application is ready to launch.

## Development tools

Use Python 3.11 or 3.12 and create a virtual environment from the repository root:

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**
```bat
.venv\Scripts\activate.bat
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install the lightweight development-check dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

## Run the checks

From the repository root, run:

```bash
python scripts/check_repository.py
python -m compileall -q scripts tests
python -m pytest -q
```

The repository checker verifies that local Markdown links and embedded local assets point to files that exist inside the repository. The tests exercise the checker with valid links, missing targets, and paths that attempt to escape the repository root.

These are repository-integrity checks only. Passing them does not validate pharmacokinetic equations, clinical performance, or scientific assumptions.

## Runtime dependencies

`requirements.txt` is retained for the project's intended application dependencies. The repository-only CI workflow deliberately does not install those dependencies while the desktop entry point and data files are absent. This keeps documentation and basic tests fast and avoids mistaking a successful dependency install for a functional application.

See the [installation guide](installation.md) and [implementation status](implementation-status.md) for the current application limitations.
