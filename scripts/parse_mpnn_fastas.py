#!/usr/bin/env python3
from pathlib import Path
import re
import csv

# =========================
# EDIT THESE PATHS
# =========================
INPUT_DIR = Path("/global/project/hpcg6049/protein/mpnn_fastas")
OUT_CSV = Path("/global/project/hpcg6049/protein/post_mpnn/parsed/mpnn_selected.csv")
TOP_K_PER_MODEL = 3
# =========================

header_original_re = re.compile(
    r'^(?P<model_id>[^,]+),\s*score=(?P<score>[-0-9.]+),\s*global_score=(?P<global_score>[-0-9.]+)'
)

header_sample_re = re.compile(
    r'^T=(?P<T>[-0-9.]+),\s*sample=(?P<sample>\d+),\s*score=(?P<score>[-0-9.]+),\s*global_score=(?P<global_score>[-0-9.]+),\s*seq_recovery=(?P<seq_recovery>[-0-9.]+)'
)

def read_fasta(path):
    records = []
    header = None
    seq_lines = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    records.append((header, "".join(seq_lines)))
                header = line[1:].strip()
                seq_lines = []
            else:
                seq_lines.append(line)
        if header is not None:
            records.append((header, "".join(seq_lines)))
    return records

def is_valid_protein(seq):
    allowed = set("ACDEFGHIKLMNPQRSTVWY")
    return set(seq).issubset(allowed)

all_rows = []

for fasta_path in sorted(INPUT_DIR.glob("*")):
    if fasta_path.suffix.lower() not in {".fa", ".fasta", ".faa"}:
        continue

    records = read_fasta(fasta_path)
    if len(records) < 2:
        continue

    # first record = original RFdiffusion/backbone record
    first_header, first_seq = records[0]
    m0 = header_original_re.match(first_header)
    if not m0:
        print(f"WARNING: could not parse original header in {fasta_path.name}")
        continue

    model_id = m0.group("model_id")

    sample_rows = []
    seen_sequences = set()

    for header, seq in records[1:]:
        ms = header_sample_re.match(header)
        if not ms:
            continue

        if not is_valid_protein(seq):
            continue

        # remove exact duplicates within the same model
        if seq in seen_sequences:
            continue
        seen_sequences.add(seq)

        sample_rows.append({
            "model_id": model_id,
            "source_fasta": fasta_path.name,
            "temperature": float(ms.group("T")),
            "sample": int(ms.group("sample")),
            "score": float(ms.group("score")),
            "global_score": float(ms.group("global_score")),
            "seq_recovery": float(ms.group("seq_recovery")),
            "sequence": seq,
            "length": len(seq),
        })

    # lower ProteinMPNN score is better as a first-pass internal ranking
    sample_rows.sort(key=lambda x: (x["score"], x["global_score"], -x["seq_recovery"]))

    kept = sample_rows[:TOP_K_PER_MODEL]
    for rank_in_model, row in enumerate(kept, start=1):
        row["rank_in_model"] = rank_in_model
        row["candidate_id"] = (
            f"{row['model_id']}__T{str(row['temperature']).replace('.', 'p')}__s{row['sample']}"
        )
        all_rows.append(row)

OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

fieldnames = [
    "candidate_id",
    "model_id",
    "source_fasta",
    "rank_in_model",
    "temperature",
    "sample",
    "score",
    "global_score",
    "seq_recovery",
    "length",
    "sequence",
]

with open(OUT_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_rows)

print(f"Wrote {len(all_rows)} selected candidates to: {OUT_CSV}")
