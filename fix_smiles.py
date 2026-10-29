"""
fix_smiles.py — Repair curated SMILES via PubChem.
Run once:  py fix_smiles.py
"""

import re
import sys

try:
    import pubchempy as pcp
except ImportError:
    print("py -m pip install pubchempy")
    sys.exit(1)

try:
    from rdkit import Chem, RDLogger
    RDLogger.DisableLog("rdApp.*")
    RDKIT = True
except ImportError:
    RDKIT = False
    print("RDKit missing — validation skipped.")

DB_FILE = "poison_database.py"

CURATED = [
    "gamma-HCH (Lindane)",
    "Selenium",
    "MBOCA",
    "Acenaphthene",
    "Dieldrin",
    "Ricinine",
    "Tetrodotoxin",
    "Aconitine",
    "Digoxin",
    "Amygdalin",
]


def fetch_smiles(query):
    try:
        compounds = pcp.get_compounds(query, "name")
        if not compounds:
            return None
        c = compounds[0]
        return c.connectivity_smiles or c.canonical_smiles
    except Exception as e:
        print(f"  [{query}] pubchem error: {e}")
        return None


def validate(smiles):
    if not RDKIT or not smiles:
        return True
    return Chem.MolFromSmiles(smiles) is not None


def patch_db(name, new_smiles):
    with open(DB_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    escaped = re.escape(f'"{name}"')
    pattern = re.compile(
        escaped + r':\s*\{.*?"structure":\s*"[^"]*"',
        re.DOTALL
    )
    m = pattern.search(text)
    if not m:
        print(f"  [{name}] block not found")
        return False

    old = m.group(0)
    new = re.sub(
        r'"structure":\s*"[^"]*"',
        f'"structure": "{new_smiles}"',
        old
    )
    text = text[:m.start()] + new + text[m.end():]
    with open(DB_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    return True


def main():
    print("Verifying curated SMILES against PubChem...\n")
    fixed = 0

    for db_key in CURATED:
        query = db_key
        if "(" in db_key:
            query = db_key.split("(")[0].strip()

        smiles = fetch_smiles(query)
        if not smiles:
            print(f"  [{db_key}] no PubChem match — leaving as-is")
            continue

        if not validate(smiles):
            print(f"  [{db_key}] fetched SMILES invalid — skipping")
            continue

        if patch_db(db_key, smiles):
            print(f"  [{db_key}] UPDATED")
            fixed += 1

    print(f"\nDone. {fixed} compounds fixed.")
    print("Restart the dashboard to see the fix.")


if __name__ == "__main__":
    main()