# Final project handoff and release gates

**Last reviewed:** 2026-10-28

This page closes out the repository-maintenance work completed so far and separates verified repository checks from unfinished application and release work.

## What is complete in this repository

- Repository structure, README, contribution guidance, security reporting guidance, and technical documentation are in place.
- Python packaging metadata and dependency declarations are present for the scaffold.
- Automated checks run on Python 3.11 and 3.12.
- CI checks Python syntax, local documentation links, and the test suite.
- JSON checks validate that the tracked cache and repair-map files parse and have the expected basic shape.
- The supplied archive has been audited for missing integration pieces, dependency mismatches, data-provenance gaps, and release risks.
- The repository no longer claims a licence that the owner has not selected.

## What has been verified

The latest checked-in `main` commit has successful GitHub Actions checks for Python 3.11 and Python 3.12. The tests cover repository scaffolding and basic data-file integrity.

These checks establish only that the tested repository-maintenance code passes in CI. They do not establish that the original desktop interface launches, that the archive has been fully integrated, or that any pharmacokinetic or toxicological model is scientifically valid.

## What is not complete

- The original desktop UI, full database module, and simulation engine are not integrated as a runnable app in this repository.
- The original simulation's toxic-compound dose-to-lethality calculations have not been wired into the public repository.
- Scientific fields and repair mappings have not received a full field-by-field provenance and identity review.
- No independent scientific validation report has been supplied.
- The project licence has not been selected, and rights to bundled assets and third-party materials still require confirmation.
- A clean Windows installation and desktop launch have not been verified.

## Owner decisions and release gates

Before describing or distributing a runnable product:

- [ ] Decide the intended audience, use, and distribution model.
- [ ] Confirm rights to contributed source, generated images, data, and third-party materials.
- [ ] Select a project licence deliberately and add the corresponding licence file and notices.
- [ ] Have a qualified safety/scientific reviewer assess the proposed functionality and data.
- [ ] Preserve field-level provenance and clearly distinguish measured, estimated, synthetic, and unknown values.
- [ ] Review dependency licences, bundled binaries, secrets, and external network calls.
- [ ] Test the intended installation target from a clean environment.
- [ ] Publish accurate release notes and state explicitly what has and has not been validated.

## Recommended final verification

From the repository root, in an environment with the declared development dependencies installed:

```bash
python scripts/check_repository.py
python scripts/check_data_files.py
python -m pytest -q
python -m build
```

The first three commands are covered by the existing CI workflow (build verification is a local release check, not currently a CI job). If `python -m build` is used, install the `build` package first. A successful package build is still not a desktop-app build.

## Release and legal caution

This handoff is not legal advice, scientific certification, or a guarantee against claims or regulatory action. Applicability depends on actual code, claims, data, distribution, users, and jurisdictions. Obtain qualified legal and scientific review before public or commercial release.

## Bottom line

The repository-maintenance scaffold is in a substantially better documented and automatically checked state. **The original desktop product is not yet ready to be called runnable or validated from this repository.** The remaining work is not something that can responsibly be represented as finished by documentation or passing scaffold tests alone.
