#!/usr/bin/env python3
from pathlib import Path
import csv
import json

CF_DIR = Path("/global/project/hpcg6049/protein/post_mpnn/cf_output/run1")
OUT_CSV = Path("/global/project/hpcg6049/protein/post_mpnn/parsed/final_ranked_candidates.csv")

def mean_of_nested(x):
    vals = []
    if isinstance(x, list):
        for item in x:
            if isinstance(item, list):
                vals.extend([v for v in item if isinstance(v, (int, float))])
            elif isinstance(item, (int, float)):
                vals.append(item)
    return sum(vals) / len(vals) if vals else None

rows = []

for jf in sorted(CF_DIR.rglob("*.json")):
    try:
        with open(jf) as f:
            data = json.load(f)
    except Exception:
        continue

    keys = set(data.keys())
    if not ({"ptm", "iptm"} & keys or {"plddt", "pae"} & keys):
        continue

    row = {
        "json_file": str(jf),
        "design_id": jf.stem,
        "ptm": data.get("ptm"),
        "iptm": data.get("iptm"),
        "mean_plddt": None,
        "mean_pae": None,
        "ranking_score": data.get("ranking_score"),
        "has_clash": data.get("has_clash"),
    }

    if "plddt" in data:
        if isinstance(data["plddt"], list):
            vals = [v for v in data["plddt"] if isinstance(v, (int, float))]
            if vals:
                row["mean_plddt"] = sum(vals) / len(vals)
        elif isinstance(data["plddt"], (int, float)):
            row["mean_plddt"] = data["plddt"]

    if "atom_plddts" in data and row["mean_plddt"] is None:
        vals = [v for v in data["atom_plddts"] if isinstance(v, (int, float))]
        if vals:
            row["mean_plddt"] = sum(vals) / len(vals)

    if "pae" in data:
        row["mean_pae"] = mean_of_nested(data["pae"])

    rows.append(row)

rows.sort(
    key=lambda r: (
        -(r["iptm"] if isinstance(r["iptm"], (int, float)) else -999),
        -(r["ptm"] if isinstance(r["ptm"], (int, float)) else -999),
        -(r["mean_plddt"] if isinstance(r["mean_plddt"], (int, float)) else -999),
        (r["mean_pae"] if isinstance(r["mean_pae"], (int, float)) else 999),
    )
)

OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

with open(OUT_CSV, "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "design_id", "iptm", "ptm", "mean_plddt",
            "mean_pae", "ranking_score", "has_clash", "json_file"
        ]
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote ranked table to: {OUT_CSV}")
print("\nTop 20:")
for i, r in enumerate(rows[:20], start=1):
    print(
        i,
        r["design_id"],
        "ipTM=", r["iptm"],
        "pTM=", r["ptm"],
        "pLDDT=", r["mean_plddt"],
        "PAE=", r["mean_pae"]
    )
