#!/usr/bin/env python3
"""
Stage 4 — Stability and developability filtering (Phase A: sequence + CSV metrics).

Filters applied:
  1. Unpaired cysteines == 0             (hard pass/fail)
  2. Net charge at pH 7.4 in [-5, +5]   (relaxed from dev plan's [-2, +4] — flagged for PI)
  3. Average_ss_pLDDT >= 0.85            (BindCraft's secondary-structure pLDDT)
  4. Average_Binder_pLDDT >= 80          (binder-only pLDDT from BindCraft AF2)

Continuous metrics recorded for ranking (Stage 5):
  - Average_Surface_Hydrophobicity       (lower = less aggregation-prone)
  - Average_Binder_Energy_Score          (more negative = more stable)
  - Average_PackStat                     (higher = better packed)
  - Average_ShapeComplementarity         (higher = better interface fit)
  - Average_n_InterfaceUnsatHbonds       (lower = fewer unsatisfied H-bonds)
  - Average_InterfaceUnsatHbondsPercentage
  - Average_dG                           (more negative = stronger binding)
  - Average_i_pTM                        (higher = better interface confidence)
  - Average_pAE, Average_i_pAE           (lower = better)

Deferred to Phase B (ColabFold monomer on GPU):
  - AF2 monomer pLDDT > 85 (binder folds independently)

Deferred to Phase C (PyRosetta on Frontenac or PDB transfer):
  - SAP score < 0.10
  - Buried unsatisfied H-bonds == 0
  - Polar contact molecular surface > 40%
  - Predicted Tm > 60°C

Usage:
  module load scipy-stack    # on Narval — provides numpy/pandas
  python stage4_sequence_filters.py
"""

import csv
import os
import sys
from collections import OrderedDict

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STATS_CSV = os.path.join(REPO_ROOT, "bindcraft", "designs", "final_design_stats.csv")
OUTPUT_CSV = os.path.join(REPO_ROOT, "bindcraft", "filtering", "stage4_phaseA_results.csv")

CHARGE_TABLE = {
    'D': -1, 'E': -1,
    'K': +1, 'R': +1,
    'H': +0.1,  # ~10% protonated at pH 7.4 (pKa ~6.0)
}

NET_CHARGE_MIN = -5
NET_CHARGE_MAX = +5
SS_PLDDT_MIN = 0.85
BINDER_PLDDT_MIN = 0.80  # BindCraft reports on 0-1 scale, not 0-100


def count_unpaired_cys(seq):
    return seq.count('C') % 2


def net_charge_ph74(seq):
    charge = 0.0
    for aa in seq:
        charge += CHARGE_TABLE.get(aa, 0.0)
    return round(charge, 1)


def main():
    if not os.path.exists(STATS_CSV):
        print(f"ERROR: Stats CSV not found: {STATS_CSV}", file=sys.stderr)
        sys.exit(1)

    with open(STATS_CSV) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Loaded {len(rows)} designs from {STATS_CSV}")

    results = []
    pass_count = 0
    filter_fails = {'cys': 0, 'charge': 0, 'ss_plddt': 0, 'binder_plddt': 0}

    for row in rows:
        design = row['Design']
        seq = row['Sequence']
        length = int(row['Length'])

        unpaired_cys = count_unpaired_cys(seq)
        charge = net_charge_ph74(seq)
        ss_plddt = float(row['Average_ss_pLDDT'])
        binder_plddt = float(row['Average_Binder_pLDDT'])

        pass_cys = unpaired_cys == 0
        pass_charge = NET_CHARGE_MIN <= charge <= NET_CHARGE_MAX
        pass_ss = ss_plddt >= SS_PLDDT_MIN
        pass_bplddt = binder_plddt >= BINDER_PLDDT_MIN
        pass_all = pass_cys and pass_charge and pass_ss and pass_bplddt

        if not pass_cys: filter_fails['cys'] += 1
        if not pass_charge: filter_fails['charge'] += 1
        if not pass_ss: filter_fails['ss_plddt'] += 1
        if not pass_bplddt: filter_fails['binder_plddt'] += 1
        if pass_all: pass_count += 1

        result = OrderedDict([
            ('design_id', design),
            ('length', length),
            ('sequence', seq),
            ('n_cys', seq.count('C')),
            ('unpaired_cys', unpaired_cys),
            ('pass_cys', int(pass_cys)),
            ('net_charge_ph74', charge),
            ('pass_charge', int(pass_charge)),
            ('ss_plddt', ss_plddt),
            ('pass_ss_plddt', int(pass_ss)),
            ('binder_plddt', binder_plddt),
            ('pass_binder_plddt', int(pass_bplddt)),
            ('pass_phaseA', int(pass_all)),
            ('i_pTM', float(row['Average_i_pTM'])),
            ('pAE', float(row['Average_pAE'])),
            ('i_pAE', float(row['Average_i_pAE'])),
            ('dG', float(row['Average_dG'])),
            ('surface_hydrophobicity', float(row['Average_Surface_Hydrophobicity'])),
            ('binder_energy', float(row['Average_Binder_Energy_Score'])),
            ('packstat', float(row['Average_PackStat'])),
            ('shape_complementarity', float(row['Average_ShapeComplementarity'])),
            ('n_interface_unsat_hbonds', float(row['Average_n_InterfaceUnsatHbonds'])),
            ('interface_unsat_hbonds_pct', float(row['Average_InterfaceUnsatHbondsPercentage'])),
            ('dG_per_dSASA', float(row['Average_dG/dSASA'])),
            ('interface_hydrophobicity', float(row['Average_Interface_Hydrophobicity'])),
            ('n_interface_residues', float(row['Average_n_InterfaceResidues'])),
            ('n_interface_hbonds', float(row['Average_n_InterfaceHbonds'])),
        ])
        results.append(result)

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\n{'='*60}")
    print(f"Stage 4 Phase A — Sequence + CSV Filters")
    print(f"{'='*60}")
    print(f"Total designs:      {len(rows)}")
    print(f"")
    print(f"Filter results (individual):")
    print(f"  Unpaired Cys == 0:           {len(rows) - filter_fails['cys']}/{len(rows)} pass  ({filter_fails['cys']} fail)")
    print(f"  Net charge [{NET_CHARGE_MIN}, +{NET_CHARGE_MAX}]:       {len(rows) - filter_fails['charge']}/{len(rows)} pass  ({filter_fails['charge']} fail)")
    print(f"  ss_pLDDT >= {SS_PLDDT_MIN}:           {len(rows) - filter_fails['ss_plddt']}/{len(rows)} pass  ({filter_fails['ss_plddt']} fail)")
    print(f"  Binder pLDDT >= {BINDER_PLDDT_MIN}:        {len(rows) - filter_fails['binder_plddt']}/{len(rows)} pass  ({filter_fails['binder_plddt']} fail)")
    print(f"")
    print(f"  Pass ALL Phase A:            {pass_count}/{len(rows)} ({100*pass_count/len(rows):.1f}%)")
    print(f"")

    passing = [r for r in results if r['pass_phaseA']]
    if passing:
        print(f"Top 10 Phase A survivors (by i_pTM):")
        passing.sort(key=lambda r: -r['i_pTM'])
        print(f"  {'Design':<30s} {'i_pTM':>6s} {'dG':>8s} {'charge':>7s} {'ss_pLDDT':>9s} {'binder_pLDDT':>13s}")
        for r in passing[:10]:
            print(f"  {r['design_id']:<30s} {r['i_pTM']:>6.3f} {r['dG']:>8.1f} {r['net_charge_ph74']:>7.1f} {r['ss_plddt']:>9.3f} {r['binder_plddt']:>13.1f}")

    print(f"\nResults saved to: {OUTPUT_CSV}")

    charges = [r['net_charge_ph74'] for r in results]
    print(f"\n--- Net charge distribution ---")
    print(f"  Range: [{min(charges)}, {max(charges)}]")
    print(f"  Mean:  {sum(charges)/len(charges):.1f}")
    bins = [(-99, -7), (-7, -5), (-5, -2), (-2, 0), (0, 4), (4, 7), (7, 99)]
    for lo, hi in bins:
        ct = sum(1 for c in charges if lo <= c < hi)
        label = f"[{lo}, {hi})" if hi < 99 else f"[{lo}, ...)"
        print(f"  {label:<12s}: {ct}")

    if pass_count < 20:
        print(f"\n*** WARNING: Only {pass_count} designs pass Phase A. ***")
        print(f"*** The net charge filter is the main bottleneck. ***")
        print(f"*** Relaxing to [-7, +7] would yield: ", end="")
        relaxed = sum(1 for r in results
                      if r['pass_cys'] and -7 <= r['net_charge_ph74'] <= 7
                      and r['ss_plddt'] >= SS_PLDDT_MIN
                      and r['binder_plddt'] >= BINDER_PLDDT_MIN)
        print(f"{relaxed}/{len(rows)} ***")

    print(f"\nPhase B (ColabFold monomer pLDDT) pending — run prepare_monomer_inputs.py next.")


if __name__ == '__main__':
    main()
