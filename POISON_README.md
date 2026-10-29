# Poison Mixing Simulator — Quick Start

## 1. Install Dependencies
```bash
py -m pip install numpy scipy matplotlib
```

## 2. Run Dashboard
```bash
py poison_dashboard.py
```

## 3. Use
- Search and select poisons from left panel
- Set dose (mg/kg)
- Click "Add to Mixture"
- Repeat for multiple poisons
- Click "RUN SIMULATION"
- View tabs: PK Curves | Organ Damage | Interactions | Summary
- Save/load mixtures as JSON

## Files
- `poison_database.py` — 10 real poisons from T3DB/PubChem
- `poison_pk_engine.py` — PK simulation with CYP competition
- `poison_dashboard.py` — GUI dashboard
