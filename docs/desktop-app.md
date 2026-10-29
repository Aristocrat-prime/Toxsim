# Desktop data-review console

The repository now includes a standard-library desktop window for checking the
tracked JSON cache's readability and aggregate metadata coverage. It is a
runnable integration point for the current repository, not a restoration of the
separate desktop application from the supplied archive.

## Requirements

- Python 3.11 or 3.12
- Tkinter, included with most standard Windows Python distributions
- The repository's tracked pubchem_cache.json file

The console does not require the project's scientific Python dependencies.

## Launch on Windows

From the repository folder, double-click scripts/run_desktop.bat, or run:

```powershell
python -m toxsim
```

If running from a fresh clone, first create and activate a virtual environment
using the instructions in [installation.md](installation.md). Install the
package with the following command if you want the toxsim-desktop command
registered from the project metadata:

```powershell
python -m pip install -e . --no-deps
```

## What it does

- Opens a desktop window using Tkinter.
- Reads the tracked JSON file and reports parse errors clearly.
- Displays aggregate record counts and metadata-field coverage.
- Avoids printing individual record values to the window.
- Can be refreshed after the file changes.

## What it does not do

This console does not run the archived dashboard or simulation engine. It does
not calculate or display toxic-compound doses, mixtures, injury, organ damage,
or lethality predictions. It is not evidence that the original archive has been
integrated or that the underlying scientific data are valid.

The original archive's full application remains a separate integration and
review task. Existing source files in this repository are not overwritten by
this console.
