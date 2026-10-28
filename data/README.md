# Data directory

Place reviewed, versioned project data here only after documenting its origin, schema, license, and limitations.

Expected files mentioned by the developer:

- `pubchem_cache.json` — locally cached compound records from PubChem.
- `smiles_repair.json` — recorded SMILES correction mappings.

Those names are provisional; use the actual supplied filenames once confirmed. These files are not present in the repository yet.

Before adding them:

1. Confirm redistribution is permitted by the source terms.
2. Remove API keys, personal data, and unrelated local cache contents.
3. Validate JSON syntax and document the schema.
4. Record the source URL or identifier and retrieval date.
5. Clearly label missing, estimated, and synthetic values.
6. Avoid committing large caches when a small curated sample and reproducible fetch script would be more appropriate.

Never invent pharmacokinetic or toxicity values to fill gaps in a public chemical record.
