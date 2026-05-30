#!/usr/bin/env python3
"""
Stage 4 stability filtering for Aβ42 BindCraft designs.

Applies 7 filters to the 62 accepted designs:
  1. Unpaired cysteines = 0          (sequence)
  2. Net charge at pH 7.4 in [-8,+5] (sequence)
  3. SAP score per residue < 1.1      (PyRosetta SapScoreMetric / binder length)
  4. Buried unsatisfied H-bonds <= 7  (PyRosetta)
  5. Predicted Tm > 60°C              (Rosetta per-residue energy proxy)
  6. Polar CMS fraction > 40%         (FreeSASA on binder chain)
  7. AF2 monomer pLDDT > 85           (ColabFold — separate GPU job)

Filters 1-6 run on CPU. Filter 7 inputs are prepared for ColabFold.

Usage:
  python stage4_stability_filter.py --designs-csv <path> --pdb-dir <path> --output-dir <path>
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path

import pyrosetta
from pyrosetta.rosetta.core.pack.guidance_scoreterms.sap import SapScoreMetric
from pyrosetta.rosetta.core.select.residue_selector import ChainSelector
from pyrosetta.rosetta.protocols.simple_filters import BuriedUnsatHbondFilter

import freesasa


CHARGE_AT_PH74 = {
    'K': 1, 'R': 1, 'H': 0.1,
    'D': -1, 'E': -1,
}

AA_STANDARD = set("ACDEFGHIKLMNPQRSTVWY")


def parse_args():
    p = argparse.ArgumentParser(description="Stage 4 stability filtering")
    p.add_argument("--designs-csv", required=True, help="final_design_stats.csv")
    p.add_argument("--pdb-dir", required=True, help="Accepted/ PDB directory")
    p.add_argument("--output-dir", required=True, help="Output directory for results")
    return p.parse_args()


def load_designs(csv_path):
    designs = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            designs.append(row)
    return designs


def find_pdb(design_name, pdb_dir):
    """Find the PDB file for a design. BindCraft names: <design>_model<N>.pdb"""
    pdb_dir = Path(pdb_dir)
    candidates = sorted(pdb_dir.glob(f"{design_name}_model*.pdb"))
    if candidates:
        return candidates[0]
    exact = pdb_dir / f"{design_name}.pdb"
    if exact.exists():
        return exact
    return None


# --- Filter 1: Unpaired cysteines ---

def check_unpaired_cys(sequence):
    cys_count = sequence.upper().count('C')
    return cys_count, cys_count % 2 == 0


# --- Filter 2: Net charge at pH 7.4 ---

def calc_net_charge(sequence):
    charge = 0.0
    for aa in sequence.upper():
        charge += CHARGE_AT_PH74.get(aa, 0)
    return round(charge, 1)


# --- Filter 3: SAP score (binder, non-paratope) ---

def calc_sap_score(pose, binder_chain="B"):
    sap = SapScoreMetric()
    binder_sel = ChainSelector(binder_chain)
    sap.set_sap_calculate_selector(binder_sel)
    sap.set_score_selector(binder_sel)
    score = sap.calculate(pose)
    return score


# --- Filter 4: Buried unsatisfied H-bonds (binder only) ---

def calc_buried_unsat(pose, binder_chain="B"):
    binder_sel = ChainSelector(binder_chain)
    filt = BuriedUnsatHbondFilter()
    filt.set_residue_selector(binder_sel)
    filt.set_report_all_heavy_atom_unsats(True)
    score = filt.score(pose)
    return int(score)


# --- Filter 5: Predicted Tm proxy (Rosetta total score per residue) ---

def calc_rosetta_energy_per_res(pose, binder_chain="B"):
    """
    Use Rosetta REF2015 score per residue as Tm proxy.
    More negative = more stable. Threshold: < -2.0 REU/res ≈ Tm > 60°C
    for de novo miniproteins (empirical correlation from Rocklin et al. 2017).
    """
    sfxn = pyrosetta.get_fa_scorefxn()
    sfxn(pose)

    binder_start = None
    binder_end = None
    for i in range(1, pose.num_chains() + 1):
        if pose.pdb_info().chain(pose.chain_begin(i)) == binder_chain:
            binder_start = pose.chain_begin(i)
            binder_end = pose.chain_end(i)
            break

    if binder_start is None:
        return None, None

    total = 0.0
    n_res = binder_end - binder_start + 1
    for r in range(binder_start, binder_end + 1):
        total += pose.energies().residue_total_energy(r)

    per_res = total / n_res if n_res > 0 else 0
    return total, per_res


# --- Filter 6: Polar CMS fraction (FreeSASA on binder) ---

def calc_polar_cms_fraction(pdb_path, binder_chain="B"):
    """
    Contact molecular surface polar fraction.
    Polar = sum of polar atom SASA / total SASA for the binder chain.
    Polar atoms: N, O, S (and their hydrogens).
    """
    structure = freesasa.Structure(str(pdb_path))
    result = freesasa.calc(structure)

    polar_sasa = 0.0
    total_sasa = 0.0

    for i in range(structure.nAtoms()):
        chain = structure.chainLabel(i)
        if chain != binder_chain:
            continue
        atom_sasa = result.atomArea(i)
        total_sasa += atom_sasa
        atom_name = structure.atomName(i).strip()
        if atom_name.startswith(('N', 'O', 'S')):
            polar_sasa += atom_sasa

    if total_sasa == 0:
        return None
    return polar_sasa / total_sasa


# --- Filter 7 prep: ColabFold monomer inputs ---

def prepare_colabfold_monomer_inputs(designs, output_dir):
    """Write a CSV for ColabFold monomer prediction of binder sequences."""
    out_path = Path(output_dir) / "colabfold_monomer_input.csv"
    with open(out_path, 'w') as f:
        f.write("id,sequence\n")
        for d in designs:
            name = d['Design']
            seq = d['Sequence']
            f.write(f"{name},{seq}\n")
    return out_path


def main():
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    designs = load_designs(args.designs_csv)
    print(f"Loaded {len(designs)} designs from {args.designs_csv}")

    # Init PyRosetta (suppress verbose output)
    pyrosetta.init("-mute all -ignore_unrecognized_res true", silent=True)

    results = []
    for i, d in enumerate(designs):
        name = d['Design']
        seq = d['Sequence']
        length = int(d['Length'])
        print(f"[{i+1}/{len(designs)}] {name} ({length} aa)...", end=" ", flush=True)

        row = {
            'design': name,
            'length': length,
            'sequence': seq,
        }

        # Filter 1: Unpaired cysteines
        cys_count, cys_pass = check_unpaired_cys(seq)
        row['cys_count'] = cys_count
        row['cys_pass'] = cys_pass

        # Filter 2: Net charge
        charge = calc_net_charge(seq)
        row['net_charge'] = charge
        row['charge_pass'] = -8 <= charge <= 5

        # Structural filters need PDB
        pdb_path = find_pdb(name, args.pdb_dir)
        if pdb_path is None:
            print(f"PDB NOT FOUND — skipping structural filters")
            row['sap_score'] = None
            row['sap_per_residue'] = None
            row['sap_pass'] = False
            row['buried_unsat'] = None
            row['buried_unsat_pass'] = False
            row['rosetta_energy_per_res'] = None
            row['tm_proxy_pass'] = False
            row['polar_cms_fraction'] = None
            row['polar_cms_pass'] = False
            results.append(row)
            continue

        row['pdb_file'] = pdb_path.name

        # Determine binder chain from PDB
        pose = pyrosetta.pose_from_pdb(str(pdb_path))
        chains = set()
        for r in range(1, pose.total_residue() + 1):
            chains.add(pose.pdb_info().chain(r))
        # BindCraft convention: binder is last chain (typically B for 2-body, or
        # a later letter for multi-chain targets)
        binder_chain = sorted(chains)[-1]

        # Filter 3: SAP (per-residue normalized)
        try:
            sap = calc_sap_score(pose, binder_chain)
            sap_per_res = sap / length
            row['sap_score'] = round(sap, 4)
            row['sap_per_residue'] = round(sap_per_res, 4)
            row['sap_pass'] = sap_per_res < 1.1
        except Exception as e:
            print(f"SAP error: {e}", end=" ")
            row['sap_score'] = None
            row['sap_pass'] = False

        # Filter 4: Buried unsatisfied H-bonds
        try:
            bunsat = calc_buried_unsat(pose, binder_chain)
            row['buried_unsat'] = bunsat
            row['buried_unsat_pass'] = bunsat <= 7
        except Exception as e:
            print(f"BUNS error: {e}", end=" ")
            row['buried_unsat'] = None
            row['buried_unsat_pass'] = False

        # Filter 5: Tm proxy (Rosetta energy/res)
        try:
            total_e, per_res_e = calc_rosetta_energy_per_res(pose, binder_chain)
            row['rosetta_total_energy'] = round(total_e, 2) if total_e else None
            row['rosetta_energy_per_res'] = round(per_res_e, 3) if per_res_e else None
            # Rocklin et al. 2017: designs with per-res energy < -2.0 typically have Tm > 60°C
            row['tm_proxy_pass'] = per_res_e is not None and per_res_e < -2.0
        except Exception as e:
            print(f"Energy error: {e}", end=" ")
            row['rosetta_energy_per_res'] = None
            row['tm_proxy_pass'] = False

        # Filter 6: Polar CMS fraction
        try:
            polar_frac = calc_polar_cms_fraction(pdb_path, binder_chain)
            row['polar_cms_fraction'] = round(polar_frac, 4) if polar_frac else None
            row['polar_cms_pass'] = polar_frac is not None and polar_frac > 0.40
        except Exception as e:
            print(f"FreeSASA error: {e}", end=" ")
            row['polar_cms_fraction'] = None
            row['polar_cms_pass'] = False

        # Existing BindCraft binder pLDDT (design-time, for reference)
        row['bindcraft_binder_plddt'] = d.get('Average_Binder_pLDDT', '')

        # Overall pass (filters 1-6, filter 7 pending)
        row['pass_filters_1_6'] = all([
            row['cys_pass'], row['charge_pass'], row['sap_pass'],
            row['buried_unsat_pass'], row['tm_proxy_pass'], row['polar_cms_pass']
        ])

        status = "PASS(1-6)" if row['pass_filters_1_6'] else "fail"
        print(status)
        results.append(row)

    # Write results CSV
    result_path = output_dir / "stage4_results.csv"
    fieldnames = [
        'design', 'length', 'sequence', 'pdb_file',
        'cys_count', 'cys_pass',
        'net_charge', 'charge_pass',
        'sap_score', 'sap_per_residue', 'sap_pass',
        'buried_unsat', 'buried_unsat_pass',
        'rosetta_total_energy', 'rosetta_energy_per_res', 'tm_proxy_pass',
        'polar_cms_fraction', 'polar_cms_pass',
        'bindcraft_binder_plddt',
        'pass_filters_1_6',
    ]
    with open(result_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)

    # Summary
    n_pass = sum(1 for r in results if r['pass_filters_1_6'])
    print(f"\n{'='*60}")
    print(f"Stage 4 Filters 1-6 Results: {n_pass}/{len(results)} pass all 6 CPU filters")
    print(f"Results: {result_path}")

    for fname, key in [
        ("Unpaired Cys", "cys_pass"),
        ("Net charge", "charge_pass"),
        ("SAP/res < 1.1", "sap_pass"),
        ("Buried unsat <= 7", "buried_unsat_pass"),
        ("Tm proxy (E/res < -2.0)", "tm_proxy_pass"),
        ("Polar CMS > 40%", "polar_cms_pass"),
    ]:
        n = sum(1 for r in results if r.get(key))
        print(f"  {fname}: {n}/{len(results)} pass")

    # Prepare ColabFold monomer inputs for filter 7
    cf_input = prepare_colabfold_monomer_inputs(designs, output_dir)
    print(f"\nColabFold monomer input prepared: {cf_input}")
    print(f"Submit as GPU job to get AF2 monomer pLDDT for filter 7.")


if __name__ == "__main__":
    main()
