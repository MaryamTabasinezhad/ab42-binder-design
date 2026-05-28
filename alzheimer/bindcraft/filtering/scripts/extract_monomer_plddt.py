#!/usr/bin/env python3
"""
Extract monomer pLDDT from ColabFold output and merge with Phase A results.

ColabFold outputs JSON files with per-residue pLDDT for each model.
We extract the mean pLDDT across all residues and models, then apply
the monomer fold confidence threshold (pLDDT > 85 on 0-100 scale).

Produces the final Stage 4 combined results CSV.

Usage:
  module load scipy-stack
  python extract_monomer_plddt.py
"""

import csv
import glob
import json
import os
import sys
from collections import OrderedDict

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MONOMER_DIR = os.path.join(REPO_ROOT, "bindcraft", "filtering", "outputs", "monomer_plddt")
PHASE_A_CSV = os.path.join(REPO_ROOT, "bindcraft", "filtering", "stage4_phaseA_results.csv")
OUTPUT_CSV = os.path.join(REPO_ROOT, "bindcraft", "filtering", "stage4_results.csv")

MONOMER_PLDDT_MIN = 85.0  # 0-100 scale (ColabFold output)


def extract_plddt_from_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    if 'plddt' in data:
        return sum(data['plddt']) / len(data['plddt'])
    return None


def main():
    if not os.path.exists(MONOMER_DIR):
        print(f"ERROR: Monomer output directory not found: {MONOMER_DIR}", file=sys.stderr)
        print("Run run_monomer_plddt.sh first.", file=sys.stderr)
        sys.exit(1)

    with open(PHASE_A_CSV) as f:
        phase_a = {row['design_id']: row for row in csv.DictReader(f)}

    print(f"Loaded {len(phase_a)} Phase A results")

    monomer_plddt = {}
    for design_id in phase_a:
        pattern = os.path.join(MONOMER_DIR, f"{design_id}_scores_rank_*.json")
        jsons = sorted(glob.glob(pattern))
        if not jsons:
            pattern2 = os.path.join(MONOMER_DIR, f"{design_id}*scores*.json")
            jsons = sorted(glob.glob(pattern2))

        if jsons:
            plddts = []
            for jp in jsons:
                val = extract_plddt_from_json(jp)
                if val is not None:
                    plddts.append(val)
            if plddts:
                monomer_plddt[design_id] = sum(plddts) / len(plddts)

    found = len(monomer_plddt)
    missing = len(phase_a) - found
    print(f"Extracted monomer pLDDT for {found}/{len(phase_a)} designs ({missing} missing)")

    if found == 0:
        print("ERROR: No monomer pLDDT data found. Check ColabFold output.", file=sys.stderr)
        sys.exit(1)

    results = []
    pass_count = 0

    for design_id, pa in phase_a.items():
        mplddt = monomer_plddt.get(design_id)
        pass_monomer = mplddt is not None and mplddt >= MONOMER_PLDDT_MIN
        pass_phaseA = int(pa['pass_phaseA'])
        pass_all = pass_phaseA and pass_monomer

        result = OrderedDict(pa)
        result['monomer_plddt'] = f"{mplddt:.1f}" if mplddt is not None else "NA"
        result['pass_monomer_plddt'] = int(pass_monomer)
        result['pass_stage4'] = int(pass_all)
        results.append(result)
        if pass_all:
            pass_count += 1

    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\n{'='*60}")
    print(f"Stage 4 — Combined Results (Phase A + Phase B)")
    print(f"{'='*60}")
    print(f"Total designs:          {len(results)}")
    print(f"Pass Phase A:           {sum(1 for r in results if int(r['pass_phaseA']))}")
    print(f"Pass monomer pLDDT:     {sum(1 for r in results if int(r['pass_monomer_plddt']))}")
    print(f"Pass BOTH (Stage 4):    {pass_count}")
    print(f"\nResults saved to: {OUTPUT_CSV}")

    passing = [r for r in results if int(r['pass_stage4'])]
    if passing:
        passing.sort(key=lambda r: -float(r['i_pTM']))
        print(f"\nStage 4 survivors (by i_pTM):")
        print(f"  {'Design':<30s} {'i_pTM':>6s} {'dG':>8s} {'mon_pLDDT':>10s} {'charge':>7s}")
        for r in passing:
            print(f"  {r['design_id']:<30s} {float(r['i_pTM']):>6.3f} {float(r['dG']):>8.1f} {r['monomer_plddt']:>10s} {float(r['net_charge_ph74']):>7.1f}")


if __name__ == '__main__':
    main()
