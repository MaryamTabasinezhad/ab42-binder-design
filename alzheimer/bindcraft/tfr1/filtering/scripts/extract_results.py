#!/usr/bin/env python3
"""Extract pae_interaction and iptm from TfR1 Stage 7.3 counter-screen results.

Pass criteria:
  6WRV_positive:        pae_interaction < 10  (must bind TfR1)
  TfR2_negative:        pae_interaction > 15  (must NOT bind TfR2)
  1SUV_Tf_competition:  pae_interaction < 12  (must still bind TfR1 with Tf present)
"""

import csv
import json
import re
from pathlib import Path

import numpy as np

FILTER_DIR = Path("/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/tfr1/filtering")
OUTPUTS_DIR = FILTER_DIR / "outputs"
DESIGNS_CSV = Path("/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/tfr1/designs/final_design_stats.csv")

TARGETS = ["6WRV_positive", "TfR2_negative", "1SUV_Tf_competition"]

THRESHOLDS = {
    "6WRV_positive": ("lt", 10),
    "TfR2_negative": ("gt", 15),
    "1SUV_Tf_competition": ("lt", 12),
}


def load_design_lengths():
    lengths = {}
    with open(DESIGNS_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            lengths[row["Design"]] = len(row["Sequence"])
    return lengths


def compute_pae_interaction(pae_matrix, binder_length):
    pae = np.array(pae_matrix)
    binder_to_target = pae[:binder_length, binder_length:]
    target_to_binder = pae[binder_length:, :binder_length]
    return float(np.mean(np.concatenate([binder_to_target.flatten(), target_to_binder.flatten()])))


def parse_scores(score_file, binder_length):
    with open(score_file) as f:
        data = json.load(f)

    iptm = data.get("iptm", [None])[0] if isinstance(data.get("iptm"), list) else data.get("iptm")
    ptm = data.get("ptm", [None])[0] if isinstance(data.get("ptm"), list) else data.get("ptm")
    plddt_all = data.get("plddt", [[]])[0] if isinstance(data.get("plddt", [[]])[0], list) else data.get("plddt", [])
    plddt_binder = float(np.mean(plddt_all[:binder_length])) if plddt_all else None

    pae_matrix = data.get("pae", [[]])[0]
    if isinstance(pae_matrix, list) and len(pae_matrix) > 0 and isinstance(pae_matrix[0], list):
        pae_interaction = compute_pae_interaction(pae_matrix, binder_length)
    else:
        pae_raw = data.get("pae")
        pae_interaction = compute_pae_interaction(pae_raw, binder_length) if pae_raw else None

    return {"iptm": iptm, "ptm": ptm, "plddt_binder": plddt_binder, "pae_interaction": pae_interaction}


def check_pass(target, pae_interaction):
    if pae_interaction is None:
        return None
    op, threshold = THRESHOLDS[target]
    if op == "lt":
        return pae_interaction < threshold
    return pae_interaction > threshold


def main():
    design_lengths = load_design_lengths()
    results = []

    for target in TARGETS:
        target_dir = OUTPUTS_DIR / target
        if not target_dir.exists():
            print(f"WARNING: no output dir for {target}")
            continue

        score_files = sorted(target_dir.glob("*_scores_rank_001_*.json"))
        if not score_files:
            score_files = sorted(target_dir.glob("*scores*.json"))

        for sf in score_files:
            name = sf.stem
            match = re.match(r"(tfr1_\w+)_vs_" + re.escape(target), name)
            if not match:
                parts = name.split("_scores_")
                if parts:
                    match2 = re.match(r"(tfr1_\w+)_vs_" + re.escape(target), parts[0])
                    if match2:
                        design_id = match2.group(1)
                    else:
                        continue
                else:
                    continue
            else:
                design_id = match.group(1)

            binder_len = design_lengths.get(design_id)
            if not binder_len:
                print(f"WARNING: no length for {design_id}")
                continue

            try:
                scores = parse_scores(sf, binder_len)
            except Exception as e:
                print(f"ERROR parsing {sf}: {e}")
                continue

            results.append({
                "design_id": design_id,
                "target": target,
                "pae_interaction": scores["pae_interaction"],
                "iptm": scores["iptm"],
                "plddt_binder": scores["plddt_binder"],
            })

    if not results:
        print("No results found. Are the ColabFold jobs complete?")
        return

    detail_path = FILTER_DIR / "stage7_3_results.csv"
    with open(detail_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["design_id", "target", "pae_interaction", "iptm", "plddt_binder", "pass"])
        writer.writeheader()
        for r in results:
            row = {**r, "pass": check_pass(r["target"], r["pae_interaction"])}
            writer.writerow(row)

    design_ids = sorted(set(r["design_id"] for r in results))
    summary_path = FILTER_DIR / "stage7_3_summary.csv"
    with open(summary_path, "w", newline="") as f:
        fields = (["design_id"]
                  + [f"pae_{t}" for t in TARGETS]
                  + [f"iptm_{t}" for t in TARGETS]
                  + ["pass_positive", "pass_tfr2_selectivity", "pass_tf_competition", "pass_stage7_3"])
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for did in design_ids:
            row = {"design_id": did}
            did_results = {r["target"]: r for r in results if r["design_id"] == did}

            passes = {}
            for target in TARGETS:
                r = did_results.get(target)
                pae = r["pae_interaction"] if r else None
                iptm = r["iptm"] if r else None
                row[f"pae_{target}"] = f"{pae:.2f}" if pae is not None else ""
                row[f"iptm_{target}"] = f"{iptm:.4f}" if iptm is not None else ""
                passes[target] = check_pass(target, pae)

            row["pass_positive"] = passes.get("6WRV_positive")
            row["pass_tfr2_selectivity"] = passes.get("TfR2_negative")
            row["pass_tf_competition"] = passes.get("1SUV_Tf_competition")
            row["pass_stage7_3"] = all(v is True for v in passes.values()) if all(v is not None for v in passes.values()) else None
            writer.writerow(row)

    n_pass = sum(1 for did in design_ids
                 if all(check_pass(r["target"], r["pae_interaction"]) is True
                        for r in results if r["design_id"] == did and r["pae_interaction"] is not None)
                 and len([r for r in results if r["design_id"] == did]) == len(TARGETS))

    print(f"\nStage 7.3 TfR1 Counter-Screen Results")
    print(f"{'=' * 45}")
    print(f"Total designs screened: {len(design_ids)}")
    print(f"Designs passing all 3 criteria: {n_pass}")
    print(f"Detail: {detail_path}")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
