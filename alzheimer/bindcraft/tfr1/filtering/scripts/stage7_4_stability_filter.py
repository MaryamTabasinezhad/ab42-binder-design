#!/usr/bin/env python3
"""Stage 7.4 — TfR1 stability and developability filtering.

Applies sequential pass/fail filters to accepted BindCraft designs,
then ranks survivors by composite score with affinity-window penalty.

Filters adapted from DEVELOPMENT_PLAN.md Stage 4, with TfR1-specific
affinity-window constraint (target 50-200 nM, not maximum affinity).

Usage:
    python stage7_4_stability_filter.py
"""

import csv
import sys
from pathlib import Path

import numpy as np

DESIGNS_CSV = Path("/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/tfr1/designs/final_design_stats.csv")
OUTPUT_DIR = Path("/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/tfr1/filtering")

# Amino acid charges at pH 7.4
POS_CHARGED = set("RK")
NEG_CHARGED = set("DE")

# ── Pass/fail filters ──────────────────────────────────────────────────
# Each tuple: (column, operator, threshold, description)
# operator: "ge" (>=), "le" (<=), "eq" (==), "func" (custom function)
FILTERS = [
    ("Average_i_pTM",               "ge", 0.70, "i_pTM >= 0.70"),
    ("Average_pLDDT",               "ge", 0.80, "pLDDT >= 0.80"),
    ("Average_Binder_pLDDT",        "ge", 0.85, "Binder pLDDT >= 0.85"),
    ("Average_Relaxed_Clashes",     "le", 0.0,  "No relaxed clashes"),
    ("Average_ShapeComplementarity", "ge", 0.55, "SC >= 0.55"),
    ("Average_PackStat",            "ge", 0.55, "PackStat >= 0.55"),
    ("Average_Binder_RMSD",         "le", 2.5,  "Binder RMSD <= 2.5 Å"),
    ("Average_Target_RMSD",         "le", 0.5,  "Target RMSD <= 0.5 Å"),
    ("Average_Surface_Hydrophobicity", "le", 0.35, "Surface hydrophobicity <= 0.35"),
    ("Average_dG",                  "le", -30.0, "dG <= -30 kcal/mol"),
    ("Average_n_InterfaceResidues", "ge", 7.0,  "Interface residues >= 7"),
    ("Average_n_InterfaceHbonds",   "ge", 3.0,  "Interface H-bonds >= 3"),
]


def check_no_cysteine(seq):
    return "C" not in seq


def check_net_charge(seq, low=-6, high=2):
    charge = sum(1 for aa in seq if aa in POS_CHARGED) - sum(1 for aa in seq if aa in NEG_CHARGED)
    return low <= charge <= high


def net_charge(seq):
    return sum(1 for aa in seq if aa in POS_CHARGED) - sum(1 for aa in seq if aa in NEG_CHARGED)


def passes_filter(row, col, op, threshold):
    try:
        val = float(row[col])
    except (ValueError, KeyError):
        return None
    if op == "ge":
        return val >= threshold
    elif op == "le":
        return val <= threshold
    elif op == "eq":
        return val == threshold
    return None


def affinity_window_score(i_ptm, dg):
    """Score based on distance from moderate-affinity sweet spot.

    For TfR1 brain-shuttle, moderate affinity (50-200 nM) is optimal.
    Very tight binders (high i_pTM, very negative dG) are penalised.

    Returns 0-1 score (1 = optimal window).
    """
    # i_pTM sweet spot: 0.72-0.82 (moderate, not maximum)
    if 0.72 <= i_ptm <= 0.82:
        iptm_score = 1.0
    elif i_ptm < 0.72:
        iptm_score = max(0, 1.0 - (0.72 - i_ptm) / 0.10)
    else:
        iptm_score = max(0, 1.0 - (i_ptm - 0.82) / 0.10)

    # dG sweet spot: -35 to -55 kcal/mol
    if -55 <= dg <= -35:
        dg_score = 1.0
    elif dg > -35:
        dg_score = max(0, 1.0 - (-35 - dg) / 15)
    else:
        dg_score = max(0, 1.0 - (dg + 55) / (-20))

    return 0.5 * iptm_score + 0.5 * dg_score


def composite_rank_score(row):
    """Composite score for ranking Stage 7.4 survivors.

    Higher = better. Balances binding quality with affinity window.
    """
    try:
        i_ptm = float(row["Average_i_pTM"])
        dg = float(row["Average_dG"])
        sc = float(row["Average_ShapeComplementarity"])
        binder_plddt = float(row["Average_Binder_pLDDT"])
        binder_rmsd = float(row["Average_Binder_RMSD"])
        packstat = float(row["Average_PackStat"])
    except (ValueError, KeyError):
        return 0.0

    affinity_score = affinity_window_score(i_ptm, dg)

    score = (
        0.30 * affinity_score
        + 0.20 * min(sc / 0.80, 1.0)
        + 0.15 * min(binder_plddt / 0.95, 1.0)
        + 0.15 * max(0, 1.0 - binder_rmsd / 3.0)
        + 0.10 * min(packstat / 0.70, 1.0)
        + 0.10 * min(i_ptm / 0.85, 1.0)
    )
    return round(score, 4)


def main():
    with open(DESIGNS_CSV) as f:
        designs = list(csv.DictReader(f))

    print(f"Stage 7.4 TfR1 Stability & Developability Filtering")
    print(f"{'=' * 55}")
    print(f"Input: {len(designs)} accepted designs")
    print()

    # ── Sequential filtering ──
    survivors = designs[:]
    filter_log = []

    for col, op, threshold, desc in FILTERS:
        before = len(survivors)
        survivors = [r for r in survivors if passes_filter(r, col, op, threshold) is True]
        after = len(survivors)
        filter_log.append((desc, before, after, before - after))
        print(f"  {desc:<45} {before:>4} → {after:>4} (cut {before - after})")

    # Sequence-based filters
    before = len(survivors)
    survivors = [r for r in survivors if check_no_cysteine(r["Sequence"])]
    after = len(survivors)
    filter_log.append(("No unpaired cysteines", before, after, before - after))
    print(f"  {'No unpaired cysteines':<45} {before:>4} → {after:>4} (cut {before - after})")

    before = len(survivors)
    survivors = [r for r in survivors if check_net_charge(r["Sequence"])]
    after = len(survivors)
    filter_log.append(("Net charge -6 to +2", before, after, before - after))
    print(f"  {'Net charge -6 to +2':<45} {before:>4} → {after:>4} (cut {before - after})")

    print(f"\n  Survivors after all filters: {len(survivors)} / {len(designs)}")

    # ── Rank survivors ──
    for r in survivors:
        r["composite_score"] = composite_rank_score(r)
        r["affinity_window_score"] = affinity_window_score(
            float(r["Average_i_pTM"]), float(r["Average_dG"])
        )
        r["net_charge"] = net_charge(r["Sequence"])

    survivors.sort(key=lambda r: r["composite_score"], reverse=True)

    # ── Output detailed results ──
    out_fields = [
        "rank", "Design", "Length", "Sequence",
        "Average_i_pTM", "Average_pLDDT", "Average_Binder_pLDDT",
        "Average_dG", "Average_ShapeComplementarity", "Average_PackStat",
        "Average_Binder_RMSD", "Average_Target_RMSD",
        "Average_Surface_Hydrophobicity", "Average_n_InterfaceResidues",
        "Average_n_InterfaceHbonds",
        "net_charge", "affinity_window_score", "composite_score",
    ]

    results_path = OUTPUT_DIR / "stage7_4_results.csv"
    with open(results_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields, extrasaction="ignore")
        writer.writeheader()
        for i, r in enumerate(survivors, 1):
            r["rank"] = i
            writer.writerow(r)

    # ── Print top 20 ──
    print(f"\nTop 20 designs (ranked by composite score):")
    print(f"{'Rank':<5} {'Design':<30} {'i_pTM':>6} {'dG':>7} {'SC':>5} {'B_pLDDT':>8} {'B_RMSD':>7} {'Affin':>6} {'Score':>6}")
    print("-" * 85)
    for i, r in enumerate(survivors[:20], 1):
        print(f"{i:<5} {r['Design']:<30} {float(r['Average_i_pTM']):>6.3f} {float(r['Average_dG']):>7.1f} "
              f"{float(r['Average_ShapeComplementarity']):>5.2f} {float(r['Average_Binder_pLDDT']):>8.3f} "
              f"{float(r['Average_Binder_RMSD']):>7.2f} {r['affinity_window_score']:>6.3f} {r['composite_score']:>6.4f}")

    # ── Summary stats ──
    if survivors:
        iptms = [float(r["Average_i_pTM"]) for r in survivors]
        dgs = [float(r["Average_dG"]) for r in survivors]
        print(f"\nSurvivors summary:")
        print(f"  i_pTM: {np.min(iptms):.3f} – {np.max(iptms):.3f} (median {np.median(iptms):.3f})")
        print(f"  dG:    {np.min(dgs):.1f} – {np.max(dgs):.1f} (median {np.median(dgs):.1f})")

    # ── Filter log ──
    log_path = OUTPUT_DIR / "stage7_4_filter_log.csv"
    with open(log_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filter", "input", "output", "removed"])
        for desc, before, after, removed in filter_log:
            writer.writerow([desc, before, after, removed])

    print(f"\nOutput files:")
    print(f"  Results: {results_path}")
    print(f"  Filter log: {log_path}")


if __name__ == "__main__":
    main()
