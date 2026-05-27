"""Diagnostic metrics for the minimized chain-A+B+C-with-N-terminus structure.

Outputs JSON to nterm_md/docs/starting_structure_diagnostics.json with:
  1. bond/angle stereochemistry (max deviations from ideal)
  2. N-terminus clash check (residues 1-8 vs the rest of the system)
  3. N-terminus orientation (Rg, centroid vector, angle to filament axis)
  4. Buried surface area between residues 1-8 and the rest

Reads:
  starting_structure/chainA_B_C_with_nterm_minimized.pdb
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from Bio.PDB import PDBParser
from Bio.PDB.SASA import ShrakeRupley

ROOT = Path(__file__).parent.parent
PDB = ROOT / "starting_structure" / "chainA_B_C_with_nterm_minimized.pdb"
OUT = ROOT / "docs" / "starting_structure_diagnostics.json"

# Approximate ideal bond lengths (Å) for backbone & common heavy-atom bonds.
# Within-residue bonds only — the C-N peptide bond is handled in the
# inter-residue loop.
IDEAL_BONDS_INTRA = {
    ("N", "CA"): 1.458,
    ("CA", "C"): 1.525,
    ("C", "O"): 1.231,
    ("CA", "CB"): 1.530,
}
IDEAL_PEPTIDE_BOND_A = 1.329  # C(i) - N(i+1)

# Standard backbone bond angles (degrees) — within-residue (centred on a real bond).
IDEAL_ANGLES_INTRA = {
    ("N", "CA", "C"): 111.2,
    ("CA", "C", "O"): 120.8,
    ("N", "CA", "CB"): 110.5,
}
# Inter-residue angles around the peptide bond C(i)-N(i+1).
# These need atoms from both residues and are checked separately.
IDEAL_PEPTIDE_ANGLES = {
    "CA(i)-C(i)-N(i+1)": 116.2,
    "C(i)-N(i+1)-CA(i+1)": 121.7,
    "O(i)-C(i)-N(i+1)": 122.7,
}

THREE_TO_ONE = {
    "ALA":"A","ARG":"R","ASN":"N","ASP":"D","CYS":"C","GLU":"E","GLN":"Q",
    "GLY":"G","HIS":"H","ILE":"I","LEU":"L","LYS":"K","MET":"M","PHE":"F",
    "PRO":"P","SER":"S","THR":"T","TRP":"W","TYR":"Y","VAL":"V",
}


def angle_deg(a, b, c):
    v1 = a - b
    v2 = c - b
    cos = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return float(np.degrees(np.arccos(np.clip(cos, -1.0, 1.0))))


def stereochemistry_check(structure) -> dict:
    """Backbone bond and angle deviations across all chains."""
    bond_violations = []
    angle_violations = []
    bond_max = {"pair": None, "dev": 0.0, "value": 0.0, "ideal": 0.0, "loc": None}
    angle_max = {"triplet": None, "dev": 0.0, "value": 0.0, "ideal": 0.0, "loc": None}

    for chain in structure[0]:
        residues = [r for r in chain if r.id[0] == " "]
        # Within-residue backbone bonds.
        for r in residues:
            for (a1, a2), ideal in IDEAL_BONDS_INTRA.items():
                if a1 in r and a2 in r:
                    d = float(np.linalg.norm(r[a1].coord - r[a2].coord))
                    dev = abs(d - ideal)
                    if dev > 0.05:
                        bond_violations.append(
                            {"chain": chain.id, "resid": r.id[1], "atoms": f"{a1}-{a2}",
                             "value": d, "ideal": ideal, "dev": dev}
                        )
                    if dev > bond_max["dev"]:
                        bond_max = {"pair": f"{a1}-{a2}", "dev": dev, "value": d,
                                    "ideal": ideal, "loc": f"{chain.id}:{r.id[1]}"}
            # Within-residue backbone angles.
            for (a1, a2, a3), ideal in IDEAL_ANGLES_INTRA.items():
                if a1 in r and a2 in r and a3 in r:
                    ang = angle_deg(r[a1].coord, r[a2].coord, r[a3].coord)
                    dev = abs(ang - ideal)
                    if dev > 5.0:
                        angle_violations.append(
                            {"chain": chain.id, "resid": r.id[1],
                             "atoms": f"{a1}-{a2}-{a3}", "value": ang, "ideal": ideal,
                             "dev": dev}
                        )
                    if dev > angle_max["dev"]:
                        angle_max = {"triplet": f"{a1}-{a2}-{a3}", "dev": dev,
                                     "value": ang, "ideal": ideal,
                                     "loc": f"{chain.id}:{r.id[1]}"}

        # Peptide bonds and surrounding angles between consecutive residues.
        for r1, r2 in zip(residues, residues[1:]):
            if "C" in r1 and "N" in r2:
                d = float(np.linalg.norm(r1["C"].coord - r2["N"].coord))
                dev = abs(d - IDEAL_PEPTIDE_BOND_A)
                if dev > 0.05:
                    bond_violations.append(
                        {"chain": chain.id, "resid": f"{r1.id[1]}-{r2.id[1]}",
                         "atoms": "C-N(peptide)", "value": d,
                         "ideal": IDEAL_PEPTIDE_BOND_A, "dev": dev}
                    )
                if dev > bond_max["dev"]:
                    bond_max = {"pair": "C-N(peptide)", "dev": dev, "value": d,
                                "ideal": IDEAL_PEPTIDE_BOND_A,
                                "loc": f"{chain.id}:{r1.id[1]}-{r2.id[1]}"}
            # Peptide-bond surrounding angles.
            checks = [
                ("CA(i)-C(i)-N(i+1)", "CA", "C", "N", r1, r1, r2, 116.2),
                ("C(i)-N(i+1)-CA(i+1)", "C", "N", "CA", r1, r2, r2, 121.7),
                ("O(i)-C(i)-N(i+1)", "O", "C", "N", r1, r1, r2, 122.7),
            ]
            for label, a, b, c, ra, rb, rc, ideal in checks:
                if a in ra and b in rb and c in rc:
                    ang = angle_deg(ra[a].coord, rb[b].coord, rc[c].coord)
                    dev = abs(ang - ideal)
                    if dev > 5.0:
                        angle_violations.append(
                            {"chain": chain.id, "resid": f"{r1.id[1]}-{r2.id[1]}",
                             "atoms": label, "value": ang, "ideal": ideal, "dev": dev}
                        )
                    if dev > angle_max["dev"]:
                        angle_max = {"triplet": label, "dev": dev, "value": ang,
                                     "ideal": ideal,
                                     "loc": f"{chain.id}:{r1.id[1]}-{r2.id[1]}"}

    return {
        "max_bond_deviation_A": bond_max,
        "max_angle_deviation_deg": angle_max,
        "bond_violations_count_gt_0p05A": len(bond_violations),
        "angle_violations_count_gt_5deg": len(angle_violations),
        "bond_violations_top10": sorted(bond_violations, key=lambda x: -x["dev"])[:10],
        "angle_violations_top10": sorted(angle_violations, key=lambda x: -x["dev"])[:10],
    }


def heavy_atoms_of_chain_residues(structure, chain_id, resid_lo, resid_hi):
    out = []
    chain = structure[0][chain_id]
    for r in chain:
        if r.id[0] != " ": continue
        if resid_lo <= r.id[1] <= resid_hi:
            for a in r:
                if a.element != "H":
                    out.append(a)
    return out


def all_other_heavy_atoms(structure, exclude_chain, exclude_resids):
    """All heavy atoms NOT in (exclude_chain, exclude_resids)."""
    out = []
    for chain in structure[0]:
        for r in chain:
            if r.id[0] != " ": continue
            if chain.id == exclude_chain and r.id[1] in exclude_resids:
                continue
            for a in r:
                if a.element != "H":
                    out.append(a)
    return out


def clash_check(structure) -> dict:
    """For each heavy atom in chain A residues 1-8, find the minimum distance
    to any heavy atom NOT in residues 1-8 of chain A."""
    nterm = heavy_atoms_of_chain_residues(structure, "A", 1, 8)
    other = all_other_heavy_atoms(structure, "A", set(range(1, 9)))
    if not nterm or not other:
        return {"error": "no atoms found"}
    nterm_coords = np.array([a.coord for a in nterm])
    other_coords = np.array([a.coord for a in other])
    # Pairwise min distance per nterm atom.
    diffs = nterm_coords[:, None, :] - other_coords[None, :, :]
    d2 = (diffs ** 2).sum(-1)
    mins = np.sqrt(d2.min(axis=1))
    argmins = d2.argmin(axis=1)

    clashes = []
    bonded_peptide = []  # the legitimate residue-8 C → residue-9 N peptide bond
    nonbonded_min = float("inf")
    for atom, mn, am in zip(nterm, mins, argmins):
        partner = other[am]
        atom_res = atom.get_parent()
        partner_res = partner.get_parent()
        atom_chain = atom_res.get_parent().id
        partner_chain = partner_res.get_parent().id
        is_peptide_bond = (
            atom_chain == "A" and partner_chain == "A"
            and atom_res.id[1] == 8 and partner_res.id[1] == 9
            and atom.name == "C" and partner.name == "N"
        )
        if not is_peptide_bond and mn < nonbonded_min:
            nonbonded_min = float(mn)
        if mn < 2.0:
            entry = {
                "nterm_atom": f"{atom_chain}:{atom_res.id[1]}{atom_res.resname}:{atom.name}",
                "partner": f"{partner_chain}:{partner_res.id[1]}{partner_res.resname}:{partner.name}",
                "distance_A": float(mn),
            }
            if is_peptide_bond:
                bonded_peptide.append(entry)
            else:
                clashes.append(entry)
    return {
        "min_distance_A_including_peptide_bond": float(mins.min()),
        "min_distance_A_nonbonded_only": nonbonded_min,
        "mean_min_distance_A": float(mins.mean()),
        "n_nterm_heavy_atoms": len(nterm),
        "n_clashes_lt_2A": len(clashes),
        "clashes": sorted(clashes, key=lambda x: x["distance_A"]),
        "bonded_peptide_pairs_excluded": bonded_peptide,
    }


def orientation(structure) -> dict:
    """Rg of residues 1-8 (heavy atoms), centroid vector relative to chain A core,
    angle to the filament helical axis."""
    nterm = heavy_atoms_of_chain_residues(structure, "A", 1, 8)
    core = heavy_atoms_of_chain_residues(structure, "A", 9, 42)
    nterm_coords = np.array([a.coord for a in nterm])
    core_coords = np.array([a.coord for a in core])

    nterm_centroid = nterm_coords.mean(axis=0)
    core_centroid = core_coords.mean(axis=0)
    rg = float(np.sqrt(((nterm_coords - nterm_centroid) ** 2).sum(axis=1).mean()))
    vec = nterm_centroid - core_centroid

    # Filament axis: vector from chain B centroid to chain C centroid (intra-PF stacking).
    b_atoms = heavy_atoms_of_chain_residues(structure, "B", 9, 42)
    c_atoms = heavy_atoms_of_chain_residues(structure, "C", 9, 42)
    b_centroid = np.array([a.coord for a in b_atoms]).mean(axis=0)
    c_centroid = np.array([a.coord for a in c_atoms]).mean(axis=0)
    axis = c_centroid - b_centroid
    axis_unit = axis / np.linalg.norm(axis)

    vec_norm = np.linalg.norm(vec)
    cos = float(np.dot(vec, axis_unit) / vec_norm) if vec_norm > 0 else 0.0
    angle = float(np.degrees(np.arccos(np.clip(cos, -1.0, 1.0))))

    return {
        "nterm_radius_of_gyration_A": rg,
        "nterm_centroid_xyz_A": nterm_centroid.tolist(),
        "chainA_core_centroid_xyz_A": core_centroid.tolist(),
        "vector_core_to_nterm_xyz_A": vec.tolist(),
        "vector_length_A": float(vec_norm),
        "filament_axis_unit_vec": axis_unit.tolist(),
        "angle_to_filament_axis_deg": angle,
    }


def bsa(structure) -> dict:
    """Buried surface area between residues 1-8 of chain A and the rest of A+B+C.

    BSA = (SASA of nterm alone) + (SASA of rest alone) - (SASA of full system).
    Uses Bio.PDB.SASA.ShrakeRupley with default 1.4 Å probe.
    """
    sr = ShrakeRupley()

    # SASA in the full context: keep all chains and residues.
    sr.compute(structure[0], level="A")
    nterm_atoms_full = []
    for atom in structure[0]["A"].get_atoms():
        r = atom.get_parent()
        if r.id[0] != " " or atom.element == "H": continue
        if 1 <= r.id[1] <= 8:
            nterm_atoms_full.append(atom)
    rest_atoms_full = []
    for chain in structure[0]:
        for r in chain:
            if r.id[0] != " ": continue
            if chain.id == "A" and 1 <= r.id[1] <= 8:
                continue
            for atom in r:
                if atom.element == "H": continue
                rest_atoms_full.append(atom)
    nterm_sasa_in_context = sum(a.sasa for a in nterm_atoms_full)
    rest_sasa_in_context = sum(a.sasa for a in rest_atoms_full)

    # SASA of N-terminus alone (without rest).
    from Bio.PDB import Structure, Model, Chain
    s_nterm = Structure.Structure("nterm")
    m = Model.Model(0); s_nterm.add(m)
    new_a = Chain.Chain("A"); m.add(new_a)
    for r in structure[0]["A"]:
        if r.id[0] != " ": continue
        if 1 <= r.id[1] <= 8:
            new_a.add(r.copy())
    sr.compute(s_nterm[0], level="A")
    nterm_sasa_alone = sum(a.sasa for a in s_nterm[0]["A"].get_atoms() if a.element != "H")

    # SASA of rest alone.
    s_rest = Structure.Structure("rest")
    m2 = Model.Model(0); s_rest.add(m2)
    for chain in structure[0]:
        new_c = Chain.Chain(chain.id); m2.add(new_c)
        for r in chain:
            if r.id[0] != " ": continue
            if chain.id == "A" and 1 <= r.id[1] <= 8:
                continue
            new_c.add(r.copy())
    sr.compute(s_rest[0], level="A")
    rest_sasa_alone = sum(a.sasa for a in s_rest[0].get_atoms() if a.element != "H")

    full_sasa = nterm_sasa_in_context + rest_sasa_in_context
    bsa_val = (nterm_sasa_alone + rest_sasa_alone) - full_sasa

    return {
        "nterm_sasa_alone_A2": float(nterm_sasa_alone),
        "rest_sasa_alone_A2": float(rest_sasa_alone),
        "full_system_sasa_A2": float(full_sasa),
        "buried_surface_area_A2": float(bsa_val),
    }


def main():
    if not PDB.exists():
        sys.exit(f"missing input PDB: {PDB}")
    print(f"Reading {PDB}")
    structure = PDBParser(QUIET=True).get_structure("min", str(PDB))

    # Quick sanity check.
    chain_a = structure[0]["A"]
    nterm_seq = "".join(
        THREE_TO_ONE.get(r.resname, "?")
        for r in chain_a if r.id[0] == " " and 1 <= r.id[1] <= 8
    )
    print(f"chain A residues 1-8: {nterm_seq} (expected DAEFRHDS)")

    print("\n[1/4] stereochemistry...")
    stereo = stereochemistry_check(structure)
    print("  max bond dev:", stereo["max_bond_deviation_A"])
    print("  max angle dev:", stereo["max_angle_deviation_deg"])

    print("\n[2/4] clashes...")
    clashes = clash_check(structure)
    print(f"  min distance (peptide-bond included): "
          f"{clashes['min_distance_A_including_peptide_bond']:.3f} Å")
    print(f"  min distance (non-bonded only):       "
          f"{clashes['min_distance_A_nonbonded_only']:.3f} Å")
    print(f"  clashes < 2.0 Å (excl. peptide bond): {clashes['n_clashes_lt_2A']}")

    print("\n[3/4] orientation...")
    orient = orientation(structure)
    print(f"  Rg(N-term): {orient['nterm_radius_of_gyration_A']:.2f} Å")
    print(f"  vector length core→Nterm: {orient['vector_length_A']:.2f} Å")
    print(f"  angle to filament axis: {orient['angle_to_filament_axis_deg']:.1f}°")

    print("\n[4/4] buried surface area...")
    bsa_d = bsa(structure)
    print(f"  BSA: {bsa_d['buried_surface_area_A2']:.1f} Å²")

    out = {
        "input_pdb": str(PDB),
        "nterm_sequence_observed": nterm_seq,
        "stereochemistry": stereo,
        "clash_check": clashes,
        "orientation": orient,
        "buried_surface_area": bsa_d,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
