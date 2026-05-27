#!/usr/bin/env python3
"""Extract pae_interaction and iptm from ColabFold Stage 3 counter-screen results.

Reads ColabFold JSON score files, computes pae_interaction (mean PAE between
binder and target chains), and applies pass/fail filters.

Outputs:
  stage3_results.csv — per-prediction detail
  stage3_summary.csv — per-design summary with pass/fail
"""

import csv
import json
import re
from pathlib import Path

import numpy as np

FILTER_DIR = Path("/lustre07/scratch/ghaedi/ab42-binder-design/alzheimer/bindcraft/filtering")
OUTPUTS_DIR = FILTER_DIR / "outputs"

TARGETS = ["9CO4", "9CKI", "9CK6", "7Q4B", "7Q4M", "6SHS", "1IYT", "Ab40_monomer"]
NEGATIVE_TARGETS = ["9CKI", "9CK6", "7Q4B", "7Q4M", "6SHS", "1IYT", "Ab40_monomer"]

POSITIVE_THRESHOLD = 10
NEGATIVE_THRESHOLD = 15

# Binder lengths from final_design_stats.csv, keyed by design_id
DESIGNS_CSV = Path("/lustre07/scratch/ghaedi/ab42-binder-design/alzheimer/bindcraft/designs/final_design_stats.csv")


def load_design_lengths():
    lengths = {}
    with open(DESIGNS_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            lengths[row["Design"]] = int(row["Length"])
    return lengths


def compute_pae_interaction(pae_matrix, binder_length):
    """Mean PAE between binder residues and target residues."""
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

    pae_matrix = data.get("pae", [[]])[0] if isinstance(data.get("pae", [[]])[0], list) and isinstance(data.get("pae", [[]])[0][0], list) else data.get("pae")
    pae_interaction = compute_pae_interaction(pae_matrix, binder_length) if pae_matrix else None

    return {
        "iptm": iptm,
        "ptm": ptm,
        "plddt_binder": plddt_binder,
        "pae_interaction": pae_interaction,
    }


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
            match = re.match(r"(ab42_\w+)_vs_" + re.escape(target), name)
            if not match:
                parts = name.split("_scores_")
                if parts:
                    job_id = parts[0]
                    match2 = re.match(r"(ab42_\w+)_vs_" + re.escape(target), job_id)
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

    detail_path = FILTER_DIR / "stage3_results.csv"
    with open(detail_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["design_id", "target", "pae_interaction", "iptm", "plddt_binder", "pass"])
        writer.writeheader()
        for r in results:
            is_positive = r["target"] == "9CO4"
            if r["pae_interaction"] is not None:
                if is_positive:
                    passed = r["pae_interaction"] < POSITIVE_THRESHOLD
                else:
                    passed = r["pae_interaction"] > NEGATIVE_THRESHOLD
            else:
                passed = None
            row = {**r, "pass": passed}
            writer.writerow(row)

    design_ids = sorted(set(r["design_id"] for r in results))
    summary_path = FILTER_DIR / "stage3_summary.csv"
    with open(summary_path, "w", newline="") as f:
        fields = ["design_id"] + [f"pae_{t}" for t in TARGETS] + [f"iptm_{t}" for t in TARGETS] + ["pass_positive", "pass_all_negative", "pass_stage3"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for did in design_ids:
            row = {"design_id": did}
            did_results = {r["target"]: r for r in results if r["design_id"] == did}

            pass_positive = None
            pass_all_neg = True
            for target in TARGETS:
                r = did_results.get(target)
                pae = r["pae_interaction"] if r else None
                iptm = r["iptm"] if r else None
                row[f"pae_{target}"] = f"{pae:.2f}" if pae is not None else ""
                row[f"iptm_{target}"] = f"{iptm:.4f}" if iptm is not None else ""

                if target == "9CO4" and pae is not None:
                    pass_positive = pae < POSITIVE_THRESHOLD
                elif target != "9CO4":
                    if pae is None or pae <= NEGATIVE_THRESHOLD:
                        pass_all_neg = False

            row["pass_positive"] = pass_positive
            row["pass_all_negative"] = pass_all_neg if pass_positive is not None else None
            row["pass_stage3"] = (pass_positive and pass_all_neg) if pass_positive is not None else None
            writer.writerow(row)

    n_pass = sum(1 for did in design_ids
                 if all(r["target"] == "9CO4" and r["pae_interaction"] < POSITIVE_THRESHOLD
                        or r["target"] != "9CO4" and r["pae_interaction"] > NEGATIVE_THRESHOLD
                        for r in results if r["design_id"] == did and r["pae_interaction"] is not None)
                 and any(r["target"] == "9CO4" and r["pae_interaction"] < POSITIVE_THRESHOLD
                         for r in results if r["design_id"] == did and r["pae_interaction"] is not None))

    print(f"\nStage 3 Counter-Screen Results")
    print(f"{'='*40}")
    print(f"Total designs: {len(design_ids)}")
    print(f"Designs passing Stage 3: {n_pass}")
    print(f"Detail: {detail_path}")
    print(f"Summary: {summary_path}")

    if n_pass >= 20:
        print(f"\nGATE 1: PASS (>= 20 designs) → proceed to Stage 4")
    elif n_pass >= 5:
        print(f"\nGATE 1: MARGINAL (5-19 designs) → expand campaign")
    else:
        print(f"\nGATE 1: FAIL (< 5 designs) → consider RFdiffusion fallback")


if __name__ == "__main__":
    main()
