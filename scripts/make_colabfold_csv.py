#!/usr/bin/env python3
from pathlib import Path
import csv

# =========================
# EDIT THESE
# =========================
SELECTED_CSV = Path("/global/project/hpcg6049/protein/post_mpnn/parsed/mpnn_selected.csv")
OUT_CSV = Path("/global/project/hpcg6049/protein/post_mpnn/cf_input/colabfold_complexes.csv")

# Put your target chain sequence here
TARGET_SEQUENCE = "IQVKDSAQNSVIIVDKNGRLVYLVENPGGYVAYSKAATVTGKLVHANFGTKKDFEDLYTPVNGSIVIVRAG"
# =========================

OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

with open(SELECTED_CSV) as f_in, open(OUT_CSV, "w", newline="") as f_out:
    reader = csv.DictReader(f_in)
    writer = csv.writer(f_out)
    writer.writerow(["id", "sequence"])
    count = 0
    for row in reader:
        binder_seq = row["sequence"].strip()
        candidate_id = row["candidate_id"].strip()
        complex_seq = f"{binder_seq}:{TARGET_SEQUENCE}"
        writer.writerow([candidate_id, complex_seq])
        count += 1

print(f"Wrote {count} ColabFold complex inputs to: {OUT_CSV}")
