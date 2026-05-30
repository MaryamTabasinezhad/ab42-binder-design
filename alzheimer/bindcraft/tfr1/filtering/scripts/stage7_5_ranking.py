#!/usr/bin/env python3
"""Stage 7.5 — TfR1 ranking and selection for fusion panel.

Ranks Stage 7.4 survivors by weighted composite score with structural
diversity bonus, caps per-scaffold representation, and selects top 50.

Usage:
    python stage7_5_ranking.py
"""

import csv
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

INPUT_CSV = Path("/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/tfr1/filtering/stage7_4_results.csv")
OUTPUT_DIR = Path("/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/tfr1/filtering")

MAX_PER_SCAFFOLD = 5
TOP_N = 50

SCAFFOLD_RE = re.compile(r"_(s\d+)_")


def extract_scaffold(design_name):
    m = SCAFFOLD_RE.search(design_name)
    return m.group(1) if m else design_name


def normalize(values, higher_is_better=True):
    arr = np.array(values, dtype=float)
    lo, hi = arr.min(), arr.max()
    if hi == lo:
        return np.full_like(arr, 0.5)
    normed = (arr - lo) / (hi - lo)
    return normed if higher_is_better else 1.0 - normed


def structural_diversity_bonus(scaffold_counts, total_designs):
    """Reward under-represented scaffolds. Rarer scaffold → higher bonus."""
    bonuses = {}
    max_count = max(scaffold_counts.values())
    for scaffold, count in scaffold_counts.items():
        bonuses[scaffold] = 1.0 - (count / max_count)
    return bonuses


def main():
    with open(INPUT_CSV) as f:
        designs = list(csv.DictReader(f))

    print(f"Stage 7.5 TfR1 Ranking & Selection")
    print(f"{'=' * 50}")
    print(f"Input: {len(designs)} Stage 7.4 survivors")

    for r in designs:
        r["scaffold"] = extract_scaffold(r["Design"])

    scaffold_counts = Counter(r["scaffold"] for r in designs)
    diversity_bonuses = structural_diversity_bonus(scaffold_counts, len(designs))

    print(f"Unique scaffolds: {len(scaffold_counts)}")
    print(f"Scaffolds with >{MAX_PER_SCAFFOLD} designs: {sum(1 for c in scaffold_counts.values() if c > MAX_PER_SCAFFOLD)}")

    i_ptms = [float(r["Average_i_pTM"]) for r in designs]
    dgs = [float(r["Average_dG"]) for r in designs]
    binder_plddts = [float(r["Average_Binder_pLDDT"]) for r in designs]
    scs = [float(r["Average_ShapeComplementarity"]) for r in designs]
    packstats = [float(r["Average_PackStat"]) for r in designs]

    norm_iptm = normalize(i_ptms, higher_is_better=True)
    norm_dg = normalize(dgs, higher_is_better=False)
    norm_plddt = normalize(binder_plddts, higher_is_better=True)
    norm_sc = normalize(scs, higher_is_better=True)
    norm_pack = normalize(packstats, higher_is_better=True)

    for i, r in enumerate(designs):
        div_bonus = diversity_bonuses[r["scaffold"]]
        score = (
            0.25 * norm_iptm[i]
            + 0.20 * norm_dg[i]
            + 0.15 * norm_plddt[i]
            + 0.15 * norm_sc[i]
            + 0.10 * norm_pack[i]
            + 0.15 * div_bonus
        )
        r["stage7_5_score"] = round(float(score), 4)
        r["diversity_bonus"] = round(div_bonus, 4)

    designs.sort(key=lambda r: r["stage7_5_score"], reverse=True)

    selected = []
    scaffold_selected = Counter()
    skipped_by_cap = 0

    for r in designs:
        if len(selected) >= TOP_N:
            break
        if scaffold_selected[r["scaffold"]] >= MAX_PER_SCAFFOLD:
            skipped_by_cap += 1
            continue
        scaffold_selected[r["scaffold"]] += 1
        selected.append(r)

    print(f"\nSelection: top {TOP_N} with max {MAX_PER_SCAFFOLD}/scaffold")
    print(f"  Selected: {len(selected)}")
    print(f"  Skipped by scaffold cap: {skipped_by_cap}")
    print(f"  Scaffolds represented: {len(scaffold_selected)}")

    out_fields = [
        "fusion_rank", "Design", "scaffold", "Length", "Sequence",
        "Average_i_pTM", "Average_pLDDT", "Average_Binder_pLDDT",
        "Average_dG", "Average_ShapeComplementarity", "Average_PackStat",
        "Average_Binder_RMSD", "Average_Target_RMSD",
        "Average_Surface_Hydrophobicity", "Average_n_InterfaceResidues",
        "Average_n_InterfaceHbonds",
        "net_charge", "affinity_window_score", "diversity_bonus", "stage7_5_score",
    ]

    results_path = OUTPUT_DIR / "stage7_5_ranked.csv"
    with open(results_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields, extrasaction="ignore")
        writer.writeheader()
        for i, r in enumerate(selected, 1):
            r["fusion_rank"] = i
            writer.writerow(r)

    full_path = OUTPUT_DIR / "stage7_5_full_ranking.csv"
    with open(full_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields, extrasaction="ignore")
        writer.writeheader()
        for i, r in enumerate(designs, 1):
            r["fusion_rank"] = i
            writer.writerow(r)

    print(f"\nTop 20 (fusion panel):")
    print(f"{'Rank':<5} {'Design':<32} {'Scaffold':<10} {'i_pTM':>6} {'dG':>7} {'SC':>5} {'B_pLDDT':>8} {'DivB':>5} {'Score':>6}")
    print("-" * 95)
    for i, r in enumerate(selected[:20], 1):
        print(f"{i:<5} {r['Design']:<32} {r['scaffold']:<10} "
              f"{float(r['Average_i_pTM']):>6.3f} {float(r['Average_dG']):>7.1f} "
              f"{float(r['Average_ShapeComplementarity']):>5.2f} "
              f"{float(r['Average_Binder_pLDDT']):>8.3f} "
              f"{r['diversity_bonus']:>5.3f} {r['stage7_5_score']:>6.4f}")

    print(f"\nScaffold representation in top {TOP_N}:")
    for scaffold, count in scaffold_selected.most_common():
        print(f"  {scaffold}: {count}")

    if selected:
        sel_iptms = [float(r["Average_i_pTM"]) for r in selected]
        sel_dgs = [float(r["Average_dG"]) for r in selected]
        print(f"\nSelected pool summary:")
        print(f"  i_pTM: {np.min(sel_iptms):.3f} – {np.max(sel_iptms):.3f} (median {np.median(sel_iptms):.3f})")
        print(f"  dG:    {np.min(sel_dgs):.1f} – {np.max(sel_dgs):.1f} (median {np.median(sel_dgs):.1f})")
        lengths = [int(r["Length"]) for r in selected]
        print(f"  Length: {min(lengths)} – {max(lengths)} (median {int(np.median(lengths))})")

    print(f"\nOutput files:")
    print(f"  Fusion panel (top {TOP_N}): {results_path}")
    print(f"  Full ranking (all {len(designs)}): {full_path}")


if __name__ == "__main__":
    main()
