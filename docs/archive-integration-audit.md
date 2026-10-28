# Archive integration audit

**Review date:** 2026-10-28  
**Scope:** The developer-supplied `Toxiology Interface.rar` archive, its recovered Python source, JSON files, and structure-image directory, compared with the current GitHub repository.

This is a code and release-readiness review, not a scientific validation or legal opinion.

## Inventory observed

The recovered archive contains:

- `poison_dashboard.py`: a Tkinter desktop interface.
- `poison_pk_engine.py`: the pharmacokinetic/mixture calculation engine.
- `poison_database.py`: curated compound records and cache/lookup helpers.
- `fix_smiles.py`: a utility that fetches structure strings and edits the database source file.
- `pubchem_cache.json` and `smiles_repairs.json`.
- `structures/`: generated structure images.
- `requirements_poison.txt`, `run.bat`, `run_silent.bat`, and a quick-start document.

The current GitHub checkout does not contain the desktop dashboard, engine, or full database module. The repository has a Python package scaffold, documentation, and some JSON data. Therefore, a successful package install is not evidence that the original desktop app is integrated or launchable.

## Setup defects and mismatches

1. **The archive's quick-start dependency command is incomplete.** The dashboard imports NumPy, Matplotlib, Requests, Pillow, and optionally RDKit. The database uses Requests and optionally PubChemPy. The supplied `requirements_poison.txt` lists only NumPy, SciPy, and Matplotlib. The actual requirements should be reconciled with imports and tested on a clean target OS before documenting a one-command install.
2. **The README's compound count is incomplete.** The archive quick-start describes 10 curated entries, while the local cache adds 8 more records. Counts should be generated from the actual loaded dataset, not maintained as a hard-coded claim.
3. **The cache has generic fallback fields.** The database's live-lookup path fills missing fields with default pharmacokinetic/toxicity values. Those defaults are software placeholders, not evidence that the values apply to the queried compound. They must be represented as unknown or explicitly synthetic, never as sourced facts.
4. **The structure repair utility is not reproducible enough for release use.** It queries a live external service and edits `poison_database.py` in place using regular expressions. It does not preserve a full before/after audit trail or a reviewed source snapshot. It should not be run automatically during installation or release.
5. **Structure parsing is not identity verification.** A SMILES string can parse successfully and still represent the wrong structure for the intended name. The original value, corrected value, source record, retrieval date, and review decision should be retained.
6. **The numerical model is not validated.** The source uses simplifying assumptions and output labels that imply organ damage and lethality. A functioning UI or a passing unit test would not validate those outputs against real-world toxicology.
7. **Generated artifacts need provenance.** The structure images appear to be generated output. Before redistribution, determine whether they can be regenerated from approved source data and whether they belong in version control.

## Integration decision

The archive's mixture engine accepts toxic-compound dose inputs and estimates organ damage and lethality. I have **not** copied or wired up those operational calculations into the public repository. I can integrate and test general packaging, file handling, structure display, documentation, accessibility, and non-operational data checks, but I cannot deploy the dose-to-lethality functionality.

No files in the archive should be treated as verified scientific ground truth simply because they are present or parse correctly.

## Release blockers

- [ ] Confirm the owner has rights to all code, images, data, and bundled assets.
- [ ] Choose and apply a project licence intentionally; do not use a placeholder licence.
- [ ] Decide whether a public repository should contain high-hazard compound records and model parameters before a specialist safety review.
- [ ] Create a per-field provenance record for compound identity, molecular structure, and any scientific parameter.
- [ ] Remove unsubstantiated defaults from any user-facing scientific output.
- [ ] Validate the application dependency set on a clean Windows environment.
- [ ] Add automated tests for packaging, file paths, JSON integrity, and the safe parts of the UI.
- [ ] Obtain independent review of the scientific assumptions before making predictive claims.
- [ ] Complete the legal and release checklist in [legal-and-release-checklist.md](legal-and-release-checklist.md).

## Bottom line

The archive contains enough source to explain the intended desktop product, but it is not yet a safe, reproducible, validated release. The immediate work is provenance, packaging, documentation, and review—not claiming that the original simulation is scientifically reliable.
