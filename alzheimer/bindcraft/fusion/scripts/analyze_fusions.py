#!/usr/bin/env python3
"""
Analyze Stage 8 fusion ColabFold predictions.

Extracts per-arm pLDDT, inter-domain PAE, and pTM from ColabFold outputs.
Filters and ranks fusions for synthesis panel.

Usage:
  python analyze_fusions.py \
    --manifest <fusion_manifest.csv> \
    --output-dirs <split_A/> <split_B/> \
    --output <stage8_results.csv>
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
    p.add_argument("--output", required=True, help="Output results CSV")
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
                'inter_domain_pae': '', 'ptm': '',
                'pass_arm1_plddt': False, 'pass_arm2_plddt': False,
                'pass_inter_pae': False, 'pass_ptm': False, 'pass_all': False,
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

        result['pass_arm1_plddt'] = metrics['arm1_plddt'] > 80
        result['pass_arm2_plddt'] = metrics['arm2_plddt'] > 80
        result['pass_inter_pae'] = metrics['inter_domain_pae'] > 15
        result['pass_ptm'] = metrics['ptm'] > 0.6
        result['pass_all'] = all([
            result['pass_arm1_plddt'], result['pass_arm2_plddt'],
            result['pass_inter_pae'], result['pass_ptm'],
        ])

        results.append(result)

    out_fields = [
        'id', 'ab42_design', 'tfr1_design', 'domain_order',
        'linker_id', 'linker_name', 'linker_len', 'total_len',
        'arm1_plddt', 'arm2_plddt', 'linker_plddt',
        'inter_domain_pae', 'ptm',
        'pass_arm1_plddt', 'pass_arm2_plddt', 'pass_inter_pae', 'pass_ptm', 'pass_all',
    ]

    with open(args.output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=out_fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)

    n_pass = sum(1 for r in results if r.get('pass_all'))
    print(f"Analyzed {found}/{len(manifest)} fusions ({missing} missing)")
    print(f"Pass all filters: {n_pass}/{found}")
    print(f"Results: {args.output}")

    if n_pass > 0:
        survivors = [r for r in results if r.get('pass_all')]
        survivors.sort(key=lambda r: -(float(r['arm1_plddt']) + float(r['arm2_plddt'])) / 2)
        print(f"\nTop 10 fusions:")
        for i, r in enumerate(survivors[:10]):
            mean_plddt = (float(r['arm1_plddt']) + float(r['arm2_plddt'])) / 2
            print(f"  {i+1}. {r['id']}: arm1={r['arm1_plddt']}, arm2={r['arm2_plddt']}, "
                  f"iPAE={r['inter_domain_pae']}, pTM={r['ptm']}, "
                  f"mean_pLDDT={mean_plddt:.1f}, order={r['domain_order']}, "
                  f"linker={r['linker_name']}")


if __name__ == "__main__":
    main()
