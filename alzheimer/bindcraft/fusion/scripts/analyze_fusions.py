#!/usr/bin/env python3
"""
Analyze Stage 8 fusion ColabFold predictions.

Extracts per-arm pLDDT, inter-domain PAE, and pTM from ColabFold outputs,
applies filters, and ranks fusions for the synthesis panel.

Filter scheme (updated 2026-06-10):
  Tandem fusions are TWO independent binder domains joined by a flexible/rigid
  linker. Global pTM is the WRONG quality gate here — it scores whole-chain
  confidence and is necessarily low when the two domains have no fixed relative
  orientation (which is exactly what we designed for, and what a high
  inter-domain PAE confirms). So pTM is kept as an informational column and a
  soft tiebreaker only — it is NOT a hard gate.

  Hard gates (pass_all):
    - arm1 pLDDT > ARM_PLDDT_MIN   (Aβ42 arm folds)
    - arm2 pLDDT > ARM_PLDDT_MIN   (TfR1 arm folds)
    - inter-domain PAE > INTER_PAE_MIN  (domains independent, as designed)

  Ranking (among pass_all survivors):
    mean per-arm pLDDT (primary) -> min per-arm pLDDT (penalize lopsided folds)
    -> pTM (soft tiebreaker) -> inter-domain PAE

  Diversity cap: at most MAX_PER_PAIR designs per (ab42_design, tfr1_design)
  arm pair are flagged for the panel, up to PANEL_SIZE total, so the panel
  isn't dominated by many linker variants of one arm pair.

Usage:
  python analyze_fusions.py \
    --manifest <fusion_manifest.csv> \
    --output-dirs <split_A/> <split_B/> \
    --output <stage8_results.csv> \
    [--panel-size 20] [--max-per-pair 2] \
    [--arm-plddt-min 80] [--inter-pae-min 15]
"""

import argparse
import csv
import json
import numpy as np
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True, help="fusion_manifest.csv")
    p.add_argument("--output-dirs", nargs='+', required=True, help="ColabFold output directories")
    p.add_argument("--output", required=True, help="Output results CSV (ranked)")
    p.add_argument("--panel-size", type=int, default=20, help="Max designs flagged for the synthesis panel")
    p.add_argument("--max-per-pair", type=int, default=2, help="Max designs per (ab42,tfr1) arm pair in the panel")
    p.add_argument("--arm-plddt-min", type=float, default=80.0, help="Per-arm pLDDT hard gate")
    p.add_argument("--inter-pae-min", type=float, default=15.0, help="Inter-domain PAE hard gate (domain independence)")
    return p.parse_args()


def find_scores_json(fusion_id, output_dirs):
    for d in output_dirs:
        candidates = list(Path(d).glob(f"{fusion_id}_scores_rank_001_*.json"))
        if candidates:
            return candidates[0]
    return None


def analyze_fusion(scores_path, arm1_len, arm2_len, linker_len):
    with open(scores_path) as f:
        data = json.load(f)

    plddt = data['plddt']
    pae = np.array(data['pae'])
    ptm = data.get('ptm', 0)
    total_len = len(plddt)

    arm1_end = arm1_len
    linker_end = arm1_len + linker_len
    arm2_end = total_len

    arm1_plddt = np.mean(plddt[:arm1_end])
    arm2_plddt = np.mean(plddt[linker_end:arm2_end])
    linker_plddt = np.mean(plddt[arm1_end:linker_end]) if linker_len > 0 else 0

    arm1_range = slice(0, arm1_end)
    arm2_range = slice(linker_end, arm2_end)
    inter_pae_12 = np.mean(pae[arm1_range, arm2_range])
    inter_pae_21 = np.mean(pae[arm2_range, arm1_range])
    inter_pae = (inter_pae_12 + inter_pae_21) / 2

    return {
        'arm1_plddt': round(float(arm1_plddt), 2),
        'arm2_plddt': round(float(arm2_plddt), 2),
        'linker_plddt': round(float(linker_plddt), 2),
        'inter_domain_pae': round(float(inter_pae), 2),
        'ptm': round(float(ptm), 4),
    }


def main():
    args = parse_args()

    with open(args.manifest) as f:
        manifest = list(csv.DictReader(f))

    results = []
    found = 0
    missing = 0

    for row in manifest:
        fid = row['id']
        scores_path = find_scores_json(fid, args.output_dirs)

        result = {**row}

        if scores_path is None:
            missing += 1
            result.update({
                'arm1_plddt': '', 'arm2_plddt': '', 'linker_plddt': '',
                'inter_domain_pae': '', 'ptm': '', 'mean_arm_plddt': '', 'min_arm_plddt': '',
                'pass_arm1_plddt': False, 'pass_arm2_plddt': False,
                'pass_inter_pae': False, 'pass_ptm_soft': False, 'pass_all': False,
                'rank': '', 'panel_selected': False,
            })
            results.append(result)
            continue

        found += 1
        metrics = analyze_fusion(
            scores_path,
            arm1_len=int(row['arm1_len']),
            arm2_len=int(row['arm2_len']),
            linker_len=int(row['linker_len']),
        )
        result.update(metrics)

        mean_arm = (metrics['arm1_plddt'] + metrics['arm2_plddt']) / 2
        min_arm = min(metrics['arm1_plddt'], metrics['arm2_plddt'])
        result['mean_arm_plddt'] = round(mean_arm, 2)
        result['min_arm_plddt'] = round(min_arm, 2)

        result['pass_arm1_plddt'] = metrics['arm1_plddt'] > args.arm_plddt_min
        result['pass_arm2_plddt'] = metrics['arm2_plddt'] > args.arm_plddt_min
        result['pass_inter_pae'] = metrics['inter_domain_pae'] > args.inter_pae_min
        # pTM is informational/soft only — NOT part of pass_all (see module docstring)
        result['pass_ptm_soft'] = metrics['ptm'] > 0.6
        result['pass_all'] = all([
            result['pass_arm1_plddt'], result['pass_arm2_plddt'], result['pass_inter_pae'],
        ])

        result['rank'] = ''
        result['panel_selected'] = False
        results.append(result)

    # Rank survivors: mean arm pLDDT -> min arm pLDDT -> pTM -> inter-domain PAE
    survivors = [r for r in results if r.get('pass_all')]
    survivors.sort(key=lambda r: (
        -float(r['mean_arm_plddt']),
        -float(r['min_arm_plddt']),
        -float(r['ptm']),
        -float(r['inter_domain_pae']),
    ))

    # Diversity-capped panel selection over the (ab42, tfr1) arm pair
    pair_count = {}
    n_selected = 0
    for i, r in enumerate(survivors):
        r['rank'] = i + 1
        pair = (r.get('ab42_design', ''), r.get('tfr1_design', ''))
        if n_selected < args.panel_size and pair_count.get(pair, 0) < args.max_per_pair:
            r['panel_selected'] = True
            pair_count[pair] = pair_count.get(pair, 0) + 1
            n_selected += 1

    out_fields = [
        'id', 'ab42_design', 'tfr1_design', 'domain_order',
        'linker_id', 'linker_name', 'linker_len', 'total_len',
        'arm1_plddt', 'arm2_plddt', 'mean_arm_plddt', 'min_arm_plddt',
        'linker_plddt', 'inter_domain_pae', 'ptm',
        'pass_arm1_plddt', 'pass_arm2_plddt', 'pass_inter_pae', 'pass_ptm_soft', 'pass_all',
        'rank', 'panel_selected',
    ]

    # Write ranked: survivors first (by rank), then non-survivors, then missing
    def sort_key(r):
        if r.get('pass_all'):
            return (0, int(r['rank']))
        if r.get('arm1_plddt') != '':
            return (1, -float(r['mean_arm_plddt']))
        return (2, 0)
    results.sort(key=sort_key)

    with open(args.output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=out_fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)

    print(f"Analyzed {found}/{len(manifest)} fusions ({missing} missing)")
    print(f"Pass hard gates (arm1>{args.arm_plddt_min}, arm2>{args.arm_plddt_min}, "
          f"interPAE>{args.inter_pae_min}): {len(survivors)}/{found}")
    print(f"Panel selected (<= {args.max_per_pair}/pair, <= {args.panel_size} total): {n_selected}")
    print(f"Results: {args.output}")

    if survivors:
        print(f"\nTop {min(args.panel_size, len(survivors))} panel candidates:")
        shown = [r for r in survivors if r['panel_selected']]
        for r in shown:
            print(f"  {r['rank']:>2}. {r['id']:<44} "
                  f"arm1={r['arm1_plddt']:>5} arm2={r['arm2_plddt']:>5} "
                  f"mean={r['mean_arm_plddt']:>5} iPAE={r['inter_domain_pae']:>5} "
                  f"pTM={r['ptm']} linker={r['linker_name']}")


if __name__ == "__main__":
    main()
