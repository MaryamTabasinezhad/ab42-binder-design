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

Usage (analyze ColabFold outputs):
  python analyze_fusions.py \
    --manifest <fusion_manifest.csv> \
    --output-dirs <split_A/> <split_B/> \
    --output <stage8_results.csv> \
    [--panel-size 20] [--max-per-pair 2] \
    [--arm-plddt-min 80] [--inter-pae-min 15]

Usage (merge per-split result CSVs and re-rank across all of them):
  python analyze_fusions.py \
    --merge-csvs <stage8_results_splitA.csv> <stage8_results_splitB.csv> \
    --output <stage8_results_merged.csv> \
    [--panel-size 20] [--max-per-pair 2] \
    [--arm-plddt-min 80] [--inter-pae-min 15]

  Merge mode pools the rows that carry metrics from each CSV (de-duplicated by
  fusion id, preferring rows with metrics), RECOMPUTES the gates/derived columns
  from the raw metric columns using the threshold args, then applies the same
  ranking + diversity cap over the full pooled set. This lets each cluster
  analyze its own split locally and push only a small CSV — no PDB transfer.
"""

import argparse
import csv
import json
import numpy as np
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser()
    # Analyze-mode inputs (validated in main; not required so merge mode can omit them)
    p.add_argument("--manifest", help="fusion_manifest.csv (analyze mode)")
    p.add_argument("--output-dirs", nargs='+', help="ColabFold output directories (analyze mode)")
    # Merge-mode input
    p.add_argument("--merge-csvs", nargs='+', help="Per-split result CSVs to pool and re-rank (merge mode)")
    # Common
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


def _to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def apply_gates(result, args):
    """(Re)compute derived columns + gates from the raw metric columns in `result`.

    Works whether the metric values are numbers (analyze mode) or strings
    (merge mode, read from CSV). Sets metrics blank + all gates False if the
    row has no arm1 metric (i.e. prediction missing)."""
    a1 = _to_float(result.get('arm1_plddt'))
    a2 = _to_float(result.get('arm2_plddt'))
    ip = _to_float(result.get('inter_domain_pae'))
    pt = _to_float(result.get('ptm'))

    if a1 is None or a2 is None or ip is None:
        result.update({
            'arm1_plddt': '', 'arm2_plddt': '', 'linker_plddt': result.get('linker_plddt', ''),
            'inter_domain_pae': '', 'ptm': '', 'mean_arm_plddt': '', 'min_arm_plddt': '',
            'pass_arm1_plddt': False, 'pass_arm2_plddt': False,
            'pass_inter_pae': False, 'pass_ptm_soft': False, 'pass_all': False,
            'rank': '', 'panel_selected': False,
        })
        return result

    mean_arm = (a1 + a2) / 2
    min_arm = min(a1, a2)
    result['arm1_plddt'] = a1
    result['arm2_plddt'] = a2
    result['inter_domain_pae'] = ip
    result['ptm'] = pt if pt is not None else 0.0
    result['mean_arm_plddt'] = round(mean_arm, 2)
    result['min_arm_plddt'] = round(min_arm, 2)
    result['pass_arm1_plddt'] = a1 > args.arm_plddt_min
    result['pass_arm2_plddt'] = a2 > args.arm_plddt_min
    result['pass_inter_pae'] = ip > args.inter_pae_min
    # pTM is informational/soft only — NOT part of pass_all (see module docstring)
    result['pass_ptm_soft'] = (pt is not None and pt > 0.6)
    result['pass_all'] = all([
        result['pass_arm1_plddt'], result['pass_arm2_plddt'], result['pass_inter_pae'],
    ])
    result.setdefault('rank', '')
    result.setdefault('panel_selected', False)
    return result


OUT_FIELDS = [
    'id', 'ab42_design', 'tfr1_design', 'domain_order',
    'linker_id', 'linker_name', 'linker_len', 'total_len',
    'arm1_plddt', 'arm2_plddt', 'mean_arm_plddt', 'min_arm_plddt',
    'linker_plddt', 'inter_domain_pae', 'ptm',
    'pass_arm1_plddt', 'pass_arm2_plddt', 'pass_inter_pae', 'pass_ptm_soft', 'pass_all',
    'rank', 'panel_selected',
]


def rank_select_write(results, args, found, total, missing, label):
    """Rank survivors, apply the diversity-capped panel selection, sort, write, print."""
    survivors = [r for r in results if r.get('pass_all')]
    survivors.sort(key=lambda r: (
        -float(r['mean_arm_plddt']),
        -float(r['min_arm_plddt']),
        -float(r['ptm']),
        -float(r['inter_domain_pae']),
    ))

    pair_count = {}
    n_selected = 0
    for i, r in enumerate(survivors):
        r['rank'] = i + 1
        pair = (r.get('ab42_design', ''), r.get('tfr1_design', ''))
        if n_selected < args.panel_size and pair_count.get(pair, 0) < args.max_per_pair:
            r['panel_selected'] = True
            pair_count[pair] = pair_count.get(pair, 0) + 1
            n_selected += 1

    def sort_key(r):
        if r.get('pass_all'):
            return (0, int(r['rank']))
        if r.get('arm1_plddt') != '':
            return (1, -float(r['mean_arm_plddt']))
        return (2, 0)
    results.sort(key=sort_key)

    with open(args.output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=OUT_FIELDS, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)

    print(f"[{label}] {found}/{total} fusions have metrics ({missing} missing)")
    print(f"Pass hard gates (arm1>{args.arm_plddt_min}, arm2>{args.arm_plddt_min}, "
          f"interPAE>{args.inter_pae_min}): {len(survivors)}/{found}")
    print(f"Panel selected (<= {args.max_per_pair}/pair, <= {args.panel_size} total): {n_selected}")
    print(f"Results: {args.output}")

    if survivors:
        shown = [r for r in survivors if r['panel_selected']]
        print(f"\nTop {len(shown)} panel candidates:")
        for r in shown:
            print(f"  {r['rank']:>2}. {r['id']:<44} "
                  f"arm1={r['arm1_plddt']:>5} arm2={r['arm2_plddt']:>5} "
                  f"mean={r['mean_arm_plddt']:>5} iPAE={r['inter_domain_pae']:>5} "
                  f"pTM={r['ptm']} linker={r['linker_name']}")


def run_analyze(args):
    with open(args.manifest) as f:
        manifest = list(csv.DictReader(f))

    results = []
    found = 0
    missing = 0
    for row in manifest:
        scores_path = find_scores_json(row['id'], args.output_dirs)
        result = {**row}
        if scores_path is None:
            missing += 1
            apply_gates(result, args)  # marks blanks + all gates False
            results.append(result)
            continue
        found += 1
        result.update(analyze_fusion(
            scores_path,
            arm1_len=int(row['arm1_len']),
            arm2_len=int(row['arm2_len']),
            linker_len=int(row['linker_len']),
        ))
        apply_gates(result, args)
        results.append(result)

    rank_select_write(results, args, found, len(manifest), missing, "analyze")


def run_merge(args):
    # Union rows across CSVs by id, preferring rows that carry metrics.
    pooled = {}            # id -> row dict
    has_metrics = {}       # id -> bool
    for path in args.merge_csvs:
        with open(path) as f:
            for row in csv.DictReader(f):
                fid = row['id']
                row_has = _to_float(row.get('arm1_plddt')) is not None
                if fid not in pooled or (row_has and not has_metrics.get(fid, False)):
                    pooled[fid] = dict(row)
                    has_metrics[fid] = row_has

    results = [apply_gates(dict(r), args) for r in pooled.values()]
    found = sum(1 for r in results if r.get('arm1_plddt') != '')
    missing = len(results) - found
    rank_select_write(results, args, found, len(results), missing, "merge")


def main():
    args = parse_args()
    if args.merge_csvs:
        if args.manifest or args.output_dirs:
            print("Note: --manifest/--output-dirs are ignored in --merge-csvs mode.")
        run_merge(args)
    else:
        if not args.manifest or not args.output_dirs:
            raise SystemExit("Analyze mode requires --manifest and --output-dirs "
                             "(or use --merge-csvs to pool existing result CSVs).")
        run_analyze(args)


if __name__ == "__main__":
    main()
