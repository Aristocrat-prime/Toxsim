## Requirements for every data file

Each data source should document:

- File name and purpose.
- Original source and retrieval date.
- Source identifiers, such as PubChem Compound IDs, where applicable.
- Units for every numeric field.
- Whether each value is measured, curated, estimated, assumed, or missing.
- Schema/version and any transformations performed.
- Known limitations and a contact or issue link for corrections.

## Chemical identifiers are not clinical evidence

A compound name, CID, molecular formula, or SMILES string does not establish human bioavailability, clearance, half-life, organ sensitivity, toxicity threshold, or an outcome for a mixture. A structure retrieved from a public chemical database should not silently acquire invented pharmacokinetic values.

If a field is unknown, preserve it as unknown rather than filling it with a plausible-looking default. If an educational demonstration requires synthetic data, label it explicitly as synthetic and keep it separate from real compound records.

## SMILES repair file

A repair mapping should preserve the original input, proposed corrected string, reason for the correction, source or review status, and a validation result from a chemistry toolkit. Do not overwrite the original string without retaining provenance. A string that parses successfully is not, by itself, proof that the intended molecule was represented correctly.

## Validation checklist

- [ ] JSON parses successfully.
- [ ] Required keys and value types are checked against a documented schema.
- [ ] Duplicate identifiers and conflicting records are reported.
- [ ] Numeric values have units and valid ranges.
- [ ] Missing values remain missing rather than being silently imputed.
- [ ] Source and retrieval date are retained.
- [ ] SMILES parse checks are recorded separately from identity verification.
- [ ] Data updates can be reproduced and reviewed.

## Handling and licensing

Check the applicable source terms before redistributing data. Do not commit API keys, private data, local caches containing sensitive information, or large generated files. Store secrets in environment variables or GitHub Actions secrets, never in tracked JSON files.
