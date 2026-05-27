#!/usr/bin/env python3
from pathlib import Path
import csv

IN_CSV = Path("/global/project/hpcg6049/protein/post_mpnn/parsed/final_ranked_candidates.csv")
OUT_CSV = Path("/global/project/hpcg6049/protein/post_mpnn/parsed/final_hits_strong.csv")

MIN_IPTM = 0.60
MIN_PLDDT = 75.0

kept = []
with open(IN_CSV) as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            iptm = float(row["iptm"]) if row["iptm"] not in ("", "None", None) else None
            plddt = float(row["mean_plddt"]) if row["mean_plddt"] not in ("", "None", None) else None
        except ValueError:
            continue

        if iptm is not None and plddt is not None:
            if iptm >= MIN_IPTM and plddt >= MIN_PLDDT:
                kept.append(row)

with open(OUT_CSV, "w", newline="") as f:
    if kept:
        writer = csv.DictWriter(f, fieldnames=kept[0].keys())
        writer.writeheader()
        writer.writerows(kept)

print(f"Kept {len(kept)} hits -> {OUT_CSV}")
