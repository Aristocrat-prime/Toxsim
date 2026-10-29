"""
poison_pk_engine.py — PK simulation with enzyme competition and organ damage
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple
from scipy.integrate import solve_ivp


@dataclass
class PoisonPK:
    """PK parameters for a single poison."""
    name: str
    ka: float           # absorption rate (1/hr)
    F: float            # bioavailability
    Vc: float           # central volume (L/kg)
    Vp: float           # peripheral volume (L/kg)
    CL: float           # clearance (mL/min/kg)
    Q: float            # intercompartmental clearance (L/hr/kg)
    half_life: float    # half-life (hr)
    tox_threshold: float  # mg/L
    ld50: float         # mg/kg
    cyp_substrate: List[str]
    cyp_inhibitor: List[str]
    organs: Dict[str, float]  # organ sensitivity scores


class PoisonSimulator:
    """Simulates PK and organ damage for poison mixtures."""

    def __init__(self, body_weight_kg: float = 70.0):
        self.bw = body_weight_kg
        self.cyp_activity = {
            "CYP1A1": 1.0, "CYP1A2": 1.0, "CYP1B1": 1.0,
            "CYP2A6": 1.0, "CYP2C9": 1.0, "CYP2D6": 1.0,
            "CYP3A4": 1.0,
        }
        self.organ_damage = {
            "liver": 0.0, "kidney": 0.0, "heart": 0.0,
            "cns": 0.0, "lung": 0.0, "thyroid": 0.0,
            "bladder": 0.0, "pns": 0.0, "parkinsonism": 0.0,
        }

    def _competitive_inhibition(self, inhibitor_ki: float, substrate_km: float, 
                                 inhibitor_conc: float) -> float:
        """Fractional activity remaining under competitive inhibition."""
        return 1.0 / (1.0 + inhibitor_conc / inhibitor_ki)

    def _update_cyp_activity(self, poisons: List[PoisonPK], concentrations: Dict[str, float]):
        """Update CYP activities based on current concentrations."""
        # Reset to baseline
        for cyp in self.cyp_activity:
            self.cyp_activity[cyp] = 1.0

        # Apply inhibition
        for poison in poisons:
            conc = concentrations.get(poison.name, 0.0)
            if conc <= 0:
                continue
            for cyp in poison.cyp_inhibitor:
                if cyp in self.cyp_activity:
                    # Simplified: assume Ki proportional to tox_threshold
                    ki = poison.tox_threshold * 0.5
                    inhibition = self._competitive_inhibition(ki, 1.0, conc)
                    self.cyp_activity[cyp] *= inhibition

    def _get_effective_clearance(self, poison: PoisonPK) -> float:
        """Clearance adjusted for CYP inhibition."""
        base_cl = poison.CL / 1000.0 * 60.0  # mL/min/kg → L/hr/kg

        # If metabolized by CYP, scale by activity
        if poison.cyp_substrate:
            avg_activity = np.mean([self.cyp_activity.get(cyp, 1.0) 
                                   for cyp in poison.cyp_substrate])
            return base_cl * avg_activity

        return base_cl

    def simulate_mixture(
        self,
        poisons: List[PoisonPK],
        doses_mg_kg: Dict[str, float],
        time_end: float = 24.0,
        n_points: int = 241,
    ) -> Dict:
        """
        Simulate mixture PK with enzyme competition and organ damage.

        Returns:
            dict with time, concentrations, organ_damage, lethality_score
        """
        t_eval = np.linspace(0, time_end, n_points)

        # State: [A_gut_i, Cc_i, Cp_i] for each poison + organ damage accumulators
        n_poisons = len(poisons)
        n_organs = len(self.organ_damage)
        n_states = n_poisons * 3 + n_organs

        y0 = np.zeros(n_states)
        # Initialize gut compartments with doses
        for i, p in enumerate(poisons):
            dose_mg = doses_mg_kg.get(p.name, 0.0) * self.bw
            y0[i*3] = dose_mg  # A_gut

        def system(t, y):
            dydt = np.zeros(n_states)
            concentrations = {}

            # Extract concentrations
            for i, p in enumerate(poisons):
                gut = y[i*3]
                cc = y[i*3 + 1]
                cp = y[i*3 + 2]
                concentrations[p.name] = cc

            # Update CYP activity based on current concentrations
            self._update_cyp_activity(poisons, concentrations)

            # PK for each poison
            for i, p in enumerate(poisons):
                gut = y[i*3]
                cc = y[i*3 + 1]
                cp = y[i*3 + 2]

                # Absorption
                ka_eff = p.ka * (1.0 if p.cyp_substrate == [] else 
                                np.mean([self.cyp_activity.get(c, 1.0) for c in p.cyp_substrate]))
                d_gut = -ka_eff * gut

                # Effective clearance with CYP competition
                cl_eff = self._get_effective_clearance(p)

                # Central compartment
                vc_total = p.Vc * self.bw
                vp_total = p.Vp * self.bw
                q_total = p.Q * self.bw

                d_cc = (p.F * ka_eff * gut) / vc_total                        - (cl_eff * cc * self.bw) / vc_total                        - q_total * (cc - cp) / vc_total

                # Peripheral compartment
                d_cp = q_total * (cc - cp) / vp_total

                dydt[i*3] = d_gut
                dydt[i*3 + 1] = d_cc
                dydt[i*3 + 2] = d_cp

            # Organ damage accumulation
            organ_idx = n_poisons * 3
            for j, (organ, baseline) in enumerate(self.organ_damage.items()):
                damage_rate = 0.0
                for i, p in enumerate(poisons):
                    if organ in p.organs:
                        sensitivity = p.organs[organ]
                        conc = y[i*3 + 1]
                        # Damage proportional to concentration above threshold
                        if conc > p.tox_threshold:
                            excess = conc - p.tox_threshold
                            damage_rate += sensitivity * excess / p.tox_threshold
                # Saturation kinetics for damage
                current_damage = y[organ_idx + j]
                max_damage = 10.0
                d_damage = damage_rate * (1.0 - current_damage / max_damage) - 0.1 * current_damage
                dydt[organ_idx + j] = max(d_damage, -current_damage * 0.5)  # prevent negative

            return dydt

        sol = solve_ivp(
            system, (0, time_end), y0,
            t_eval=t_eval, method="LSODA",
            rtol=1e-6, atol=1e-8
        )

        if not sol.success:
            raise RuntimeError(f"Integration failed: {sol.message}")

        # Extract results
        results = {
            "time": sol.t,
            "concentrations": {},
            "organ_damage": {},
            "cyp_activity": self.cyp_activity.copy(),
        }

        for i, p in enumerate(poisons):
            results["concentrations"][p.name] = sol.y[i*3 + 1]

        organ_names = list(self.organ_damage.keys())
        for j, organ in enumerate(organ_names):
            results["organ_damage"][organ] = sol.y[n_poisons*3 + j]

        # Calculate lethality score
        max_damages = [np.max(results["organ_damage"][o]) for o in organ_names]
        results["lethality_score"] = np.max(max_damages)
        results["critical_organ"] = organ_names[np.argmax(max_damages)]

        # Time to threshold crossing
        results["time_to_toxicity"] = {}
        for i, p in enumerate(poisons):
            conc = results["concentrations"][p.name]
            above = np.where(conc > p.tox_threshold)[0]
            if len(above) > 0:
                results["time_to_toxicity"][p.name] = sol.t[above[0]]
            else:
                results["time_to_toxicity"][p.name] = None

        return results


def create_poison_pk(poison_data: dict, name: str) -> PoisonPK:
    """Create PoisonPK from database entry."""
    # Estimate ka from half-life if not available
    half_life = poison_data.get("half_life_hr", 4.0)
    ka = 0.5 if half_life > 2 else 1.5  # crude estimate

    return PoisonPK(
        name=name,
        ka=ka,
        F=poison_data.get("bioavailability", 0.7),
        Vc=poison_data.get("vd_l_kg", 1.0),
        Vp=poison_data.get("vd_l_kg", 1.0) * 2.0,  # assume peripheral 2x central
        CL=poison_data.get("clearance_ml_min", 10.0),
        Q=0.5,  # default intercompartmental clearance
        half_life=half_life,
        tox_threshold=poison_data.get("tox_threshold_mg_L", 1.0),
        ld50=poison_data.get("ld50_mg_kg", 100.0),
        cyp_substrate=poison_data.get("cyp_substrate", []),
        cyp_inhibitor=poison_data.get("cyp_inhibitor", []),
        organs=poison_data.get("organs", {}),
    )


if __name__ == "__main__":
    from poison_database import POISONS, get_interaction

    # Test: mix of Aconitine + Digoxin (synergistic cardiac)
    sim = PoisonSimulator(body_weight_kg=70.0)

    acon = create_poison_pk(POISONS["Aconitine"], "Aconitine")
    dig = create_poison_pk(POISONS["Digoxin"], "Digoxin")

    interaction = get_interaction("Aconitine", "Digoxin")
    print(f"Interaction: {interaction}")

    results = sim.simulate_mixture(
        poisons=[acon, dig],
        doses_mg_kg={"Aconitine": 0.1, "Digoxin": 0.5},
        time_end=12.0,
    )

    print(f"\nLethality score: {results['lethality_score']:.2f}")
    print(f"Critical organ: {results['critical_organ']}")
    print(f"Time to toxicity:")
    for name, t in results["time_to_toxicity"].items():
        print(f"  {name}: {t:.2f} hr" if t else f"  {name}: not reached")
