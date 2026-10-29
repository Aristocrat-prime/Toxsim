"""
poison_database.py — Real compound database with mechanisms
Sources: PubChem (bulk cache + live PUG-View), curated literature entries
"""

import json
import os
import re

import requests

try:
    import pubchempy as pcp
    PUBCHEM_AVAILABLE = True
except ImportError:
    PUBCHEM_AVAILABLE = False

HERE = os.path.dirname(os.path.abspath(__file__))
PUBCHEM_CACHE = os.path.join(HERE, "pubchem_cache.json")
REPAIRS_FILE = os.path.join(HERE, "smiles_repairs.json")

CAS_PATTERN = re.compile(r"\b\d{2,7}-\d{2}-\d\b")

PUG_VIEW_URL = (
    "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/"
    "{cid}/JSON?heading=Pharmacology+and+Biochemistry"
)

POISONS = {
    "gamma-HCH (Lindane)": {
        "cas": "58-89-9",
        "formula": "C6H6Cl6",
        "mw": 290.83,
        "type": "Organochlorine pesticide",
        "structure": "C1(C(C(C(C(C1Cl)Cl)Cl)Cl)Cl)Cl",
        "mechanism": "GABA-A receptor antagonist (picrotoxin site), Na+/K+ ATPase inhibitor, oxidative stress inducer",
        "targets": ["GABA-A receptor", "Na+/K+ ATPase", "Mg2+ ATPase"],
        "organs": {"liver": 0.8, "cns": 0.9, "kidney": 0.4},
        "cyp_substrate": ["CYP2A6", "CYP3A4"],
        "cyp_inhibitor": ["CYP2A6"],
        "half_life_hr": 24.0,
        "vd_l_kg": 1.5,
        "clearance_ml_min": 10.0,
        "bioavailability": 0.85,
        "ld50_mg_kg": 88.0,
        "tox_threshold_mg_L": 0.5,
        "effects": {"cns": "seizures, hyperexcitation", "liver": "hepatotoxicity, oxidative damage"},
        "interactions": {
            "Dieldrin": {"type": "synergistic", "mechanism": "shared GABA antagonism", "multiplier": 1.8},
            "Selenium": {"type": "antagonistic", "mechanism": "competing oxidative pathways", "multiplier": 0.7},
        }
    },
    "Selenium": {
        "cas": "7782-49-2",
        "formula": "Se",
        "mw": 78.96,
        "type": "Inorganic element / toxin",
        "structure": "C1C2C3C(C1C4C2O4)C5(C(=C(C3(C5(Cl)Cl)Cl)Cl)Cl)Cl",
        "mechanism": "Sulfur substitution in proteins, sulfhydryl enzyme inactivation, mitochondrial electron transport disruption, ROS generation",
        "targets": ["Sulfhydryl enzymes", "Mitochondrial ETC", "Glutathione peroxidase"],
        "organs": {"liver": 0.7, "kidney": 0.8, "heart": 0.5},
        "cyp_substrate": [],
        "cyp_inhibitor": ["CYP1A2", "CYP3A4"],
        "half_life_hr": 120.0,
        "vd_l_kg": 0.6,
        "clearance_ml_min": 2.0,
        "bioavailability": 0.70,
        "ld50_mg_kg": 6.7,
        "tox_threshold_mg_L": 0.1,
        "effects": {"liver": "hepatotoxicity", "cns": "neurotoxicity", "gi": "garlic breath, GI distress"},
        "interactions": {
            "gamma-HCH (Lindane)": {"type": "antagonistic", "mechanism": "competing oxidative pathways", "multiplier": 0.7},
            "Digoxin": {"type": "synergistic", "mechanism": "additive cardiac stress", "multiplier": 1.4},
        }
    },
    "MBOCA": {
        "cas": "101-14-4",
        "formula": "C13H12Cl2N2",
        "mw": 267.15,
        "type": "Aromatic amine / carcinogen",
        "structure": "CC1C(C(CC(O1)OC2C(OC(CC2O)OC3C(OC(CC3O)OC4CCC5(C(C4)CCC6C5CC(C7(C6(CCC7C8=CC(=O)OC8)O)C)O)C)C)C)O)O",
        "mechanism": "DNA adduct formation, hemoglobin binding, N-hydroxy metabolite activation",
        "targets": ["DNA", "Hemoglobin", "CYP1A2"],
        "organs": {"liver": 0.9, "bladder": 0.8, "kidney": 0.5},
        "cyp_substrate": ["CYP1A2", "CYP3A4"],
        "cyp_inhibitor": [],
        "half_life_hr": 8.0,
        "vd_l_kg": 1.2,
        "clearance_ml_min": 15.0,
        "bioavailability": 0.75,
        "ld50_mg_kg": 500.0,
        "tox_threshold_mg_L": 2.0,
        "effects": {"liver": "hepatocarcinogenesis", "bladder": "bladder cancer risk"},
        "interactions": {
            "Acenaphthene": {"type": "synergistic", "mechanism": "CYP1A2 induction increases MBOCA activation", "multiplier": 1.6},
        }
    },
    "Acenaphthene": {
        "cas": "83-32-9",
        "formula": "C12H10",
        "mw": 154.21,
        "type": "Polycyclic aromatic hydrocarbon",
        "structure": "C1CC2=CC=CC3=C2C1=CC=C3",
        "mechanism": "AhR binding → CYP1A1/1A2 induction, reactive epoxide metabolites, DNA adducts",
        "targets": ["AhR receptor", "CYP1A1", "CYP1A2", "CYP1B1"],
        "organs": {"liver": 0.8, "lung": 0.6, "skin": 0.5},
        "cyp_substrate": ["CYP1A1", "CYP1A2", "CYP1B1"],
        "cyp_inhibitor": [],
        "cyp_inducer": ["CYP1A1", "CYP1A2", "CYP1B1"],
        "half_life_hr": 6.0,
        "vd_l_kg": 2.0,
        "clearance_ml_min": 25.0,
        "bioavailability": 0.60,
        "ld50_mg_kg": 1000.0,
        "tox_threshold_mg_L": 5.0,
        "effects": {"liver": "tumor promotion", "lung": "carcinogenesis"},
        "interactions": {
            "MBOCA": {"type": "synergistic", "mechanism": "CYP1A2 induction increases MBOCA activation", "multiplier": 1.6},
            "Dieldrin": {"type": "antagonistic", "mechanism": "competing CYP resources", "multiplier": 0.8},
        }
    },
    "Dieldrin": {
        "cas": "60-57-1",
        "formula": "C12H8Cl6O",
        "mw": 380.91,
        "type": "Organochlorine insecticide",
        "structure": "C1C2C3C4C1C5C6C(Cl)C(Cl)C(Cl)C5C2C3(Cl)C(Cl)C4(Cl)O6",
        "mechanism": "GABA-A antagonist, Na+/K+ ATPase inhibition, intracellular Ca2+ accumulation, alpha-synuclein binding",
        "targets": ["GABA-A receptor", "Na+/K+ ATPase", "Ca2+ ATPase", "alpha-synuclein"],
        "organs": {"cns": 0.9, "liver": 0.7, "kidney": 0.4},
        "cyp_substrate": ["CYP3A4", "CYP2C9"],
        "cyp_inhibitor": [],
        "half_life_hr": 48.0,
        "vd_l_kg": 3.0,
        "clearance_ml_min": 5.0,
        "bioavailability": 0.90,
        "ld50_mg_kg": 46.0,
        "tox_threshold_mg_L": 0.3,
        "effects": {"cns": "seizures, tremors", "liver": "hepatotoxicity", "parkinsonism": "alpha-synuclein fibrils"},
        "interactions": {
            "gamma-HCH (Lindane)": {"type": "synergistic", "mechanism": "shared GABA antagonism", "multiplier": 1.8},
            "Acenaphthene": {"type": "antagonistic", "mechanism": "competing CYP resources", "multiplier": 0.8},
        }
    },
    "Ricinine": {
        "cas": "524-40-3",
        "formula": "C8H8N2O2",
        "mw": 164.16,
        "type": "Pyridine alkaloid",
        "structure": "CN1C=CC(=C(C1=O)C#N)OC",
        "mechanism": "Goitrogenic (cyanide release), CNS depressant, metabolic interference",
        "targets": ["Thyroid peroxidase", "CNS receptors"],
        "organs": {"thyroid": 0.8, "cns": 0.6, "liver": 0.4},
        "cyp_substrate": ["CYP2D6"],
        "cyp_inhibitor": [],
        "half_life_hr": 4.0,
        "vd_l_kg": 1.0,
        "clearance_ml_min": 20.0,
        "bioavailability": 0.65,
        "ld50_mg_kg": 300.0,
        "tox_threshold_mg_L": 1.5,
        "effects": {"thyroid": "goiter", "cns": "depression, weakness"},
        "interactions": {
            "Amygdalin": {"type": "synergistic", "mechanism": "additive cyanide burden", "multiplier": 1.5},
        }
    },
    "Tetrodotoxin": {
        "cas": "4368-28-9",
        "formula": "C11H17N3O8",
        "mw": 319.27,
        "type": "Neurotoxin (alkaloid)",
        "structure": "C1=CC=C(C=C1)C(C#N)OC2C(C(C(C(O2)COC3C(C(C(C(O3)CO)O)O)O)O)O)O",
        "mechanism": "Voltage-gated sodium channel blocker (site 1), prevents action potential propagation",
        "targets": ["Nav1.1-1.9 sodium channels"],
        "organs": {"cns": 0.9, "pns": 0.9, "heart": 0.6},
        "cyp_substrate": [],
        "cyp_inhibitor": [],
        "half_life_hr": 1.5,
        "vd_l_kg": 0.4,
        "clearance_ml_min": 30.0,
        "bioavailability": 0.30,
        "ld50_mg_kg": 0.01,
        "tox_threshold_mg_L": 0.005,
        "effects": {"cns": "paresthesia, paralysis", "respiratory": "respiratory failure", "cardiac": "arrhythmia"},
        "interactions": {
            "Aconitine": {"type": "antagonistic", "mechanism": "opposing ion channel effects", "multiplier": 0.6},
        }
    },
    "Aconitine": {
        "cas": "302-27-2",
        "formula": "C34H47NO11",
        "mw": 645.7,
        "type": "Diterpenoid alkaloid",
        "structure": "CCN1CC2(C(CC(C34C2C(C(C31)C5(C6C4CC(C6OC(=O)C7=CC=CC=C7)(C(C5O)OC)O)OC(=O)C)OC)OC)O)COC",
        "mechanism": "Voltage-gated sodium channel activator (persistent activation), neurotoxin, cardiotoxin",
        "targets": ["Nav sodium channels", "Ca2+ channels", "K+ channels"],
        "organs": {"heart": 0.9, "cns": 0.8, "pns": 0.7},
        "cyp_substrate": ["CYP3A4", "CYP2C9"],
        "cyp_inhibitor": [],
        "half_life_hr": 2.0,
        "vd_l_kg": 0.8,
        "clearance_ml_min": 12.0,
        "bioavailability": 0.50,
        "ld50_mg_kg": 0.12,
        "tox_threshold_mg_L": 0.02,
        "effects": {"cardiac": "arrhythmia, ventricular tachycardia", "cns": "paresthesia, seizures", "gi": "nausea, vomiting"},
        "interactions": {
            "Tetrodotoxin": {"type": "antagonistic", "mechanism": "opposing sodium channel effects", "multiplier": 0.6},
            "Digoxin": {"type": "synergistic", "mechanism": "additive cardiac Na+/K+ ATPase stress", "multiplier": 1.7},
        }
    },
    "Digoxin": {
        "cas": "20830-75-5",
        "formula": "C41H64O14",
        "mw": 780.9,
        "type": "Cardiac glycoside",
        "structure": "C[C@H]1[C@@H]([C@H]([C@H]([C@@H](O1)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O)O)O",
        "mechanism": "Na+/K+ ATPase inhibition → intracellular Ca2+ overload → cardiac arrhythmia, positive inotropy",
        "targets": ["Na+/K+ ATPase"],
        "organs": {"heart": 0.9, "cns": 0.4, "kidney": 0.6},
        "cyp_substrate": ["CYP3A4"],
        "cyp_inhibitor": [],
        "half_life_hr": 36.0,
        "vd_l_kg": 7.0,
        "clearance_ml_min": 3.0,
        "bioavailability": 0.75,
        "ld50_mg_kg": 3.0,
        "tox_threshold_mg_L": 0.002,
        "effects": {"cardiac": "arrhythmia, AV block", "cns": "visual disturbances, confusion", "gi": "nausea"},
        "interactions": {
            "Aconitine": {"type": "synergistic", "mechanism": "additive cardiac Na+/K+ ATPase stress", "multiplier": 1.7},
            "Selenium": {"type": "synergistic", "mechanism": "additive cardiac stress", "multiplier": 1.4},
        }
    },
    "Amygdalin": {
        "cas": "29883-15-6",
        "formula": "C20H27NO11",
        "mw": 457.4,
        "type": "Cyanogenic glycoside",
        "structure": "OC[C@H]1O[C@H](O[C@H]2[C@H](O)[C@@H](O)[C@H](O[C@@H]3[C@@H](O)[C@H](O)[C@@H](O)O[C@H]3CO)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@@H]1O",
        "mechanism": "Hydrolysis releases cyanide → mitochondrial cytochrome c oxidase inhibition → cellular hypoxia",
        "targets": ["Cytochrome c oxidase (Complex IV)", "Rhodanese"],
        "organs": {"cns": 0.9, "heart": 0.7, "liver": 0.5},
        "cyp_substrate": ["CYP3A4"],
        "cyp_inhibitor": [],
        "half_life_hr": 1.0,
        "vd_l_kg": 0.5,
        "clearance_ml_min": 15.0,
        "bioavailability": 0.40,
        "ld50_mg_kg": 50.0,
        "tox_threshold_mg_L": 0.1,
        "effects": {"cns": "seizures, coma", "cardiac": "cardiac arrest", "metabolic": "lactic acidosis"},
        "interactions": {
            "Ricinine": {"type": "synergistic", "mechanism": "additive cyanide burden", "multiplier": 1.5},
        }
    },
}


def _default_organs():
    return {"liver": 0.5, "kidney": 0.5, "cns": 0.5}


def _extract_cas(compound) -> str:
    """Pull a CAS number out of PubChem synonyms via regex."""
    try:
        if not compound.synonyms:
            return "N/A"
        for synonym in compound.synonyms:
            match = CAS_PATTERN.search(synonym)
            if match:
                return match.group(0)
    except Exception:
        pass
    return "N/A"


def _fetch_pharmacology(cid: int):
    """
    Query PubChem PUG-View for pharmacology data.
    Returns (mechanism_str, targets_list). Falls back to (None, None).
    """
    try:
        r = requests.get(PUG_VIEW_URL.format(cid=cid), timeout=20)
        if r.status_code != 200:
            return None, None
        data = r.json()

        mechanism = None
        targets = []

        def walk(node):
            nonlocal mechanism
            if isinstance(node, dict):
                heading = node.get("TOCHeading", "")
                if heading == "Mechanism of Action" and not mechanism:
                    for info in node.get("Information", []):
                        val = info.get("Value", {})
                        for entry in val.get("StringWithMarkup", []):
                            s = entry.get("String", "").strip()
                            if s:
                                mechanism = s
                                break
                        if mechanism:
                            break
                if heading in ("Targets", "Target"):
                    for info in node.get("Information", []):
                        val = info.get("Value", {})
                        for entry in val.get("StringWithMarkup", []):
                            s = entry.get("String", "").strip()
                            if s and s not in targets:
                                targets.append(s)
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for item in node:
                    walk(item)

        walk(data)
        return mechanism, (targets if targets else None)
    except Exception as e:
        print(f"[PUG-View] fetch failed for CID {cid}: {e}")
        return None, None


def _load_pubchem_cache():
    if not os.path.exists(PUBCHEM_CACHE):
        return {}
    try:
        with open(PUBCHEM_CACHE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[pubchem] cache load failed: {e}")
        return {}


def _save_pubchem_cache(extra: dict):
    cache = {}
    if os.path.exists(PUBCHEM_CACHE):
        try:
            with open(PUBCHEM_CACHE, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except Exception:
            cache = {}
    for name, data in extra.items():
        if data.get("source") == "PubChem":
            cache[name] = data
    try:
        with open(PUBCHEM_CACHE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print(f"[pubchem] cache save failed: {e}")


_pubchem = _load_pubchem_cache()
for _name, _data in _pubchem.items():
    if _name not in POISONS:
        POISONS[_name] = _data

if _pubchem:
    print(f"[pubchem] loaded {len(_pubchem)} compounds from cache")


def _load_repairs():
    if not os.path.exists(REPAIRS_FILE):
        return {}
    try:
        with open(REPAIRS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_repairs(repairs):
    try:
        with open(REPAIRS_FILE, "w", encoding="utf-8") as f:
            json.dump(repairs, f, indent=2)
    except Exception as e:
        print(f"[repairs] save failed: {e}")


# Apply saved SMILES repairs on top of curated entries
_repairs = _load_repairs()
for _name, _smiles in _repairs.items():
    if _name in POISONS:
        POISONS[_name]["structure"] = _smiles
if _repairs:
    print(f"[repairs] applied {len(_repairs)} saved SMILES fixes")


def repair_smiles_for(name: str) -> str:
    """
    If the DB SMILES for `name` doesn't parse or doesn't match the entry's
    formula, fetch the correct SMILES from PubChem and update the entry in
    place. Returns the new SMILES on success, empty string otherwise.
    """
    if not PUBCHEM_AVAILABLE:
        return ""
    entry = get_poison(name)
    if not entry:
        return ""
    data_formula = entry.get("formula", "")
    current_smiles = entry.get("structure", "")
    if not data_formula or data_formula in ("N/A", "Unknown"):
        return ""

    try:
        from rdkit import Chem, RDLogger
        from rdkit.Chem import rdMolDescriptors
        RDLogger.DisableLog("rdApp.*")
    except ImportError:
        return ""

    # already correct?
    if current_smiles:
        mol = Chem.MolFromSmiles(current_smiles)
        if mol is not None and rdMolDescriptors.CalcMolFormula(mol) == data_formula:
            return ""

    # fetch from PubChem by the compound name
    try:
        compounds = pcp.get_compounds(name, "name")
        if not compounds:
            return ""
        c = compounds[0]
        new_smiles = c.connectivity_smiles or c.canonical_smiles
        if not new_smiles:
            return ""
        mol = Chem.MolFromSmiles(new_smiles)
        if mol is None:
            return ""
        if rdMolDescriptors.CalcMolFormula(mol) != data_formula:
            return ""

        entry["structure"] = new_smiles

        if entry.get("source") == "PubChem":
            _save_pubchem_cache({name: entry})
        else:
            # curated — persist fix to the repairs overlay
            repairs = _load_repairs()
            repairs[name] = new_smiles
            _save_repairs(repairs)

        print(f"[repair] fixed SMILES for {name}")
        return new_smiles
    except Exception as e:
        print(f"[repair] failed for {name}: {e}")
        return ""


def register_compound(name: str, data: dict):
    if name in POISONS:
        return False
    POISONS[name] = data
    _save_pubchem_cache({name: data})
    return True


def _classify_compound(name: str, iupac: str = "", smiles: str = "") -> str:
    n = (name or "").lower()
    i = (iupac or "").lower()
    s = (smiles or "").lower()

    if any(k in n for k in ("toxin", "venom", "ricin", "abrin",
                            "botulinum", "saxitoxin", "tetrodotoxin",
                            "batrachotoxin", "ciguatoxin", "palytoxin")):
        return "Biological toxin"

    if any(k in n for k in ("ine", "idine", "amine", "aine", "onine",
                            "anine", "oline", "osine")) and "ane" not in n[-4:]:
        if any(k in i for k in ("alkaloid", "methyl", "amino", "azan")):
            return "Alkaloid"
        if any(k in s for k in ("n1", "n2", "n3", "c[n]", "[n]", "n(")):
            return "Alkaloid"

    if any(k in n for k in ("in", "oside")) and "gluc" in i:
        return "Glycoside"
    if any(k in n for k in ("amygdalin", "linamarin", "prunasin",
                            "oleandrin", "digoxin", "digitoxin", "ouabain")):
        return "Cardiac / cyanogenic glycoside"

    if any(k in n for k in ("phos", "fos", "parathion", "malathion",
                            "diazinon", "chlorpyrifos", "sarin", "soman",
                            "tabun", "vx")):
        return "Organophosphate"
    if "phosph" in i and any(k in i for k in ("oxy", "thio", "phosphoryl")):
        return "Organophosphate"

    if any(k in n for k in ("ddt", "lindane", "dieldrin", "aldrin",
                            "endrin", "chlordane", "heptachlor",
                            "endosulfan", "toxaphene", "mirex",
                            "pentachlorophenol")):
        return "Organochlorine"

    if any(k in n for k in ("carbaryl", "aldicarb", "carbofuran",
                            "methomyl", "propoxur")):
        return "Carbamate"

    if any(k in n for k in ("arsenic", "arsenite", "arsenate", "mercury",
                            "mercuric", "methylmercury", "lead", "cadmium",
                            "thallium", "chromium", "chromate", "dichromate",
                            "barium", "beryllium", "antimony", "selenium",
                            "selenite", "selenate", "uranium", "plutonium",
                            "polonium", "radium")):
        return "Heavy metal / inorganic toxin"

    if any(k in n for k in ("caine", "azepam", "azolam", "pam", "barbital",
                            "cillin", "mycin", "cycline", "profen",
                            "statin", "sartan", "pril", "olol")):
        return "Pharmaceutical"

    if any(k in n for k in ("methanol", "ethanol", "propanol", "glycol",
                            "benzene", "toluene", "xylene", "phenol",
                            "cresol", "aniline", "nitro", "chloroform",
                            "chloride", "solvent", "ether")):
        return "Industrial solvent"

    if any(k in n for k in ("cide", "furan", "fenthion", "dimethoate",
                            "acephate", "paraquat", "diquat", "atrazine",
                            "simazine", "glyphosate")):
        return "Pesticide"

    if any(k in n for k in ("benzidine", "naphthylamine", "aflatoxin",
                            "benzopyrene", "nitrosamine", "pcb", "dioxin",
                            "tcdd")):
        return "Carcinogen / PAH / dioxin"

    if "cyan" in n:
        return "Cyanide"

    if any(k in n for k in ("myco", "aflatoxin", "ochratoxin", "fumonisin",
                            "zearalenone", "patulin", "citrinin", "ergot")):
        return "Mycotoxin"

    if i:
        return f"Chemical ({i[:40]}...)" if len(i) > 40 else f"Chemical ({i})"
    return "Organic compound"


def search_pubchem(query: str, max_results: int = 10) -> list:
    if not PUBCHEM_AVAILABLE:
        return []
    try:
        compounds = pcp.get_compounds(query, "name")
        results = []
        for c in compounds[:max_results]:
            name = query.title()
            iupac = c.iupac_name or ""
            smiles = c.connectivity_smiles or ""
            cas = _extract_cas(c)
            mech, targets = _fetch_pharmacology(c.cid)
            results.append({
                "name": name,
                "cid": c.cid,
                "cas": cas,
                "formula": c.molecular_formula,
                "mw": float(c.molecular_weight) if c.molecular_weight else 0.0,
                "smiles": smiles,
                "iupac": iupac,
                "type": _classify_compound(name, iupac, smiles),
                "mechanism": mech,
                "targets": targets,
                "source": "PubChem",
            })
        return results
    except Exception as e:
        print(f"[PubChem] search failed: {e}")
        return []


def fetch_pubchem_compound(cid: int) -> dict:
    if not PUBCHEM_AVAILABLE:
        return None
    try:
        c = pcp.Compound.from_cid(cid)
        iupac = c.iupac_name or ""
        smiles = c.connectivity_smiles or ""
        name = iupac or f"CID-{cid}"
        cas = _extract_cas(c)
        mech, targets = _fetch_pharmacology(cid)
        return {
            "cas": cas,
            "formula": c.molecular_formula or "Unknown",
            "mw": float(c.molecular_weight) if c.molecular_weight else 100.0,
            "type": _classify_compound(name, iupac, smiles),
            "structure": smiles,
            "mechanism": mech or f"PubChem CID {cid}. IUPAC: {iupac or 'N/A'}",
            "targets": targets or ["See PubChem bioassay data"],
            "organs": _default_organs(),
            "half_life_hr": 4.0,
            "vd_l_kg": 1.0,
            "clearance_ml_min": 50.0,
            "bioavailability": 0.8,
            "ld50_mg_kg": 50.0,
            "tox_threshold_mg_L": 10.0,
            "cyp_substrate": ["CYP3A4"],
            "cyp_inhibitor": [],
            "cid": cid,
            "source": "PubChem",
        }
    except Exception as e:
        print(f"[PubChem] fetch failed for CID {cid}: {e}")
        return None


def get_poison(name: str) -> dict:
    name_lower = name.lower()
    for key, val in POISONS.items():
        if name_lower in key.lower() or key.lower() in name_lower:
            return val
    return None


def list_poisons() -> list:
    return list(POISONS.keys())


def get_interaction(poison1: str, poison2: str) -> dict:
    p1 = get_poison(poison1)
    p2 = get_poison(poison2)
    if not p1 or not p2:
        return {"type": "unknown", "multiplier": 1.0, "mechanism": "data unavailable"}
    if "interactions" in p1 and poison2 in p1["interactions"]:
        return p1["interactions"][poison2]
    if "interactions" in p2 and poison1 in p2["interactions"]:
        return p2["interactions"][poison1]
    p1_inhibits = set(p1.get("cyp_inhibitor", []))
    p2_substrate = set(p2.get("cyp_substrate", []))
    p2_inhibits = set(p2.get("cyp_inhibitor", []))
    p1_substrate = set(p1.get("cyp_substrate", []))
    if p1_inhibits & p2_substrate:
        shared = p1_inhibits & p2_substrate
        return {"type": "synergistic", "multiplier": 1.5, "mechanism": f"{poison1} inhibits {', '.join(shared)} → {poison2} accumulation"}
    if p2_inhibits & p1_substrate:
        shared = p2_inhibits & p1_substrate
        return {"type": "synergistic", "multiplier": 1.5, "mechanism": f"{poison2} inhibits {', '.join(shared)} → {poison1} accumulation"}
    p1_organs = set(p1.get("organs", {}).keys())
    p2_organs = set(p2.get("organs", {}).keys())
    shared_organs = p1_organs & p2_organs
    if shared_organs:
        return {"type": "additive", "multiplier": 1.2, "mechanism": f"shared organ stress: {', '.join(shared_organs)}"}
    return {"type": "neutral", "multiplier": 1.0, "mechanism": "no significant interaction"}


if __name__ == "__main__":
    print(f"Loaded {len(POISONS)} poisons.")
    if PUBCHEM_AVAILABLE:
        print("PubChem live search: available")
    else:
        print("PubChem live search: NOT available (py -m pip install pubchempy)")
    if os.path.exists(PUBCHEM_CACHE):
        print(f"Local PubChem cache: {PUBCHEM_CACHE}")
    else:
        print("No local cache yet. Run 'py pubchem_builder.py' to build one.")