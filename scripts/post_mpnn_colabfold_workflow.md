# Post-ProteinMPNN → ColabFold Workflow for 100 RFdiffusion Models

This guide gives a clean first-pass workflow for your 100 RFdiffusion models after ProteinMPNN.

The overall workflow is:

1. Parse all ProteinMPNN FASTA files  
2. Keep the best few sequences per model  
3. Make ColabFold complex input as `binder:target`  
4. Run ColabFold batch on GPU  
5. Collect `ipTM`, `pTM`, `pLDDT`  
6. Rank and filter finalists  

Because you likely have many sequences per model, do **not** run everything at once first.

Start with **top 3 sequences per model**.

That gives about:

- 100 models  
- × 3 sequences/model  
- = about **300 ColabFold predictions**

That is a good first-pass screen.

---

## 1. Organize folders

Run:

```bash
mkdir -p /global/project/hpcg6049/protein/post_mpnn/{scripts,parsed,cf_input,cf_output,logs}
mkdir -p /global/project/hpcg6049/protein/mpnn_fastas
```

Put your ProteinMPNN FASTA files here:

```bash
/global/project/hpcg6049/protein/mpnn_fastas/
```

---

## 2. Parse all ProteinMPNN FASTAs and keep top 3 per model

Save this as:

```bash
/global/project/hpcg6049/protein/post_mpnn/scripts/parse_mpnn_fastas.py
```

```python
#!/usr/bin/env python3
from pathlib import Path
import re
import csv

INPUT_DIR = Path("/global/project/hpcg6049/protein/mpnn_fastas")
OUT_CSV = Path("/global/project/hpcg6049/protein/post_mpnn/parsed/mpnn_selected.csv")
TOP_K_PER_MODEL = 3

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

    sample_rows.sort(key=lambda x: (x["score"], x["global_score"], -x["seq_recovery"]))

    kept = sample_rows[:TOP_K_PER_MODEL]
    for rank_in_model, row in enumerate(kept, start=1):
        row["rank_in_model"] = rank_in_model
        row["candidate_id"] = f"{row['model_id']}__T{str(row['temperature']).replace('.', 'p')}__s{row['sample']}"
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
```

Run:

```bash
python /global/project/hpcg6049/protein/post_mpnn/scripts/parse_mpnn_fastas.py
```

---

## 3. Make ColabFold input CSV

Now each complex should be:

```text
binder_sequence:target_sequence
```

Save this as:

```bash
/global/project/hpcg6049/protein/post_mpnn/scripts/make_colabfold_csv.py
```

```python
#!/usr/bin/env python3
from pathlib import Path
import csv

SELECTED_CSV = Path("/global/project/hpcg6049/protein/post_mpnn/parsed/mpnn_selected.csv")
OUT_CSV = Path("/global/project/hpcg6049/protein/post_mpnn/cf_input/colabfold_complexes.csv")

# Replace with your actual target sequence
TARGET_SEQUENCE = "PASTE_YOUR_TARGET_CHAIN_SEQUENCE_HERE"

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

print(f"Wrote {count} complexes to: {OUT_CSV}")
```

Run:

```bash
python /global/project/hpcg6049/protein/post_mpnn/scripts/make_colabfold_csv.py
```

---

## 4. Run ColabFold on GPU

Save this as:

```bash
/global/project/hpcg6049/protein/post_mpnn/scripts/run_colabfold.slurm
```

Use this **corrected** version. It avoids the bash startup error you hit before.

```bash
#!/usr/bin/env bash
#SBATCH -J cf_rank
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH -t 24:00:00
#SBATCH -o /global/project/hpcg6049/protein/post_mpnn/logs/cf_%j.out
#SBATCH -e /global/project/hpcg6049/protein/post_mpnn/logs/cf_%j.err

set -eo pipefail

eval "$(conda shell.bash hook)"
conda activate colabfold

INPUT_CSV=/global/project/hpcg6049/protein/post_mpnn/cf_input/colabfold_complexes.csv
OUT_DIR=/global/project/hpcg6049/protein/post_mpnn/cf_output/run1

mkdir -p "$OUT_DIR"

echo "HOSTNAME: $(hostname)"
echo "DATE: $(date)"
echo "PWD: $(pwd)"
echo "PYTHON: $(which python)"
python --version
nvidia-smi

# First make MSA
colabfold_batch "$INPUT_CSV" "$OUT_DIR" --msa-only

# Then predict structures
colabfold_batch "$INPUT_CSV" "$OUT_DIR"

echo "DONE: $(date)"
```

Submit:

```bash
sbatch /global/project/hpcg6049/protein/post_mpnn/scripts/run_colabfold.slurm
```

Check logs:

```bash
cat /global/project/hpcg6049/protein/post_mpnn/logs/cf_JOBID.out
cat /global/project/hpcg6049/protein/post_mpnn/logs/cf_JOBID.err
```

---

## 5. Collect ColabFold scores

Save this as:

```bash
/global/project/hpcg6049/protein/post_mpnn/scripts/collect_cf_scores.py
```

```python
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
```

Run:

```bash
python /global/project/hpcg6049/protein/post_mpnn/scripts/collect_cf_scores.py
```

---

## 6. Filter best hits

Save this as:

```bash
/global/project/hpcg6049/protein/post_mpnn/scripts/filter_final_hits.py
```

```python
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
```

Run:

```bash
python /global/project/hpcg6049/protein/post_mpnn/scripts/filter_final_hits.py
```

---

## 7. Exact command order

Run everything in this order:

```bash
pip uninstall -y jax-cuda12-pjrt

python /global/project/hpcg6049/protein/post_mpnn/scripts/parse_mpnn_fastas.py
python /global/project/hpcg6049/protein/post_mpnn/scripts/make_colabfold_csv.py
sbatch /global/project/hpcg6049/protein/post_mpnn/scripts/run_colabfold.slurm
python /global/project/hpcg6049/protein/post_mpnn/scripts/collect_cf_scores.py
python /global/project/hpcg6049/protein/post_mpnn/scripts/filter_final_hits.py
```

---

## Recommendation

Do this in **two rounds**.

### Round 1
- top 3 sequences per model  
- run ColabFold  
- get top 20 models  

### Round 2
- only for the best backbones, test more MPNN sequences from those models  

That is much smarter than sending every sequence immediately.

---

## Optional next step

If you want, the next refinement is to replace the placeholder target sequence with your real target chain sequence and hard-code your exact filenames so the workflow becomes fully copy-paste ready.
# Post-ProteinMPNN → ColabFold Workflow for 100 RFdiffusion Models

This guide gives a clean first-pass workflow for your 100 RFdiffusion models after ProteinMPNN.

The overall workflow is:

1. Parse all ProteinMPNN FASTA files  
2. Keep the best few sequences per model  
3. Make ColabFold complex input as `binder:target`  
4. Run ColabFold batch on GPU  
5. Collect `ipTM`, `pTM`, `pLDDT`  
6. Rank and filter finalists  

Because you likely have many sequences per model, do **not** run everything at once first.

Start with **top 3 sequences per model**.

That gives about:

- 100 models  
- × 3 sequences/model  
- = about **300 ColabFold predictions**

That is a good first-pass screen.

---

## 1. Organize folders

Run:

```bash
mkdir -p /global/project/hpcg6049/protein/post_mpnn/{scripts,parsed,cf_input,cf_output,logs}
mkdir -p /global/project/hpcg6049/protein/mpnn_fastas
```

Put your ProteinMPNN FASTA files here:

```bash
/global/project/hpcg6049/protein/mpnn_fastas/
```

---

## 2. Parse all ProteinMPNN FASTAs and keep top 3 per model

Save this as:

```bash
/global/project/hpcg6049/protein/post_mpnn/scripts/parse_mpnn_fastas.py
```

```python
#!/usr/bin/env python3
from pathlib import Path
import re
import csv

INPUT_DIR = Path("/global/project/hpcg6049/protein/mpnn_fastas")
OUT_CSV = Path("/global/project/hpcg6049/protein/post_mpnn/parsed/mpnn_selected.csv")
TOP_K_PER_MODEL = 3

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

    sample_rows.sort(key=lambda x: (x["score"], x["global_score"], -x["seq_recovery"]))

    kept = sample_rows[:TOP_K_PER_MODEL]
    for rank_in_model, row in enumerate(kept, start=1):
        row["rank_in_model"] = rank_in_model
        row["candidate_id"] = f"{row['model_id']}__T{str(row['temperature']).replace('.', 'p')}__s{row['sample']}"
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
```

Run:

```bash
python /global/project/hpcg6049/protein/post_mpnn/scripts/parse_mpnn_fastas.py
```

---

## 3. Make ColabFold input CSV

Now each complex should be:

```text
binder_sequence:target_sequence
```

Save this as:

```bash
/global/project/hpcg6049/protein/post_mpnn/scripts/make_colabfold_csv.py
```

```python
#!/usr/bin/env python3
from pathlib import Path
import csv

SELECTED_CSV = Path("/global/project/hpcg6049/protein/post_mpnn/parsed/mpnn_selected.csv")
OUT_CSV = Path("/global/project/hpcg6049/protein/post_mpnn/cf_input/colabfold_complexes.csv")

# Replace with your actual target sequence
TARGET_SEQUENCE = "PASTE_YOUR_TARGET_CHAIN_SEQUENCE_HERE"

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

print(f"Wrote {count} complexes to: {OUT_CSV}")
```

Run:

```bash
python /global/project/hpcg6049/protein/post_mpnn/scripts/make_colabfold_csv.py
```

---

## 4. Run ColabFold on GPU

Save this as:

```bash
/global/project/hpcg6049/protein/post_mpnn/scripts/run_colabfold.slurm
```

Use this **corrected** version. It avoids the bash startup error you hit before.

```bash
#!/usr/bin/env bash
#SBATCH -J cf_rank
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH -t 24:00:00
#SBATCH -o /global/project/hpcg6049/protein/post_mpnn/logs/cf_%j.out
#SBATCH -e /global/project/hpcg6049/protein/post_mpnn/logs/cf_%j.err

set -eo pipefail

eval "$(conda shell.bash hook)"
conda activate colabfold

INPUT_CSV=/global/project/hpcg6049/protein/post_mpnn/cf_input/colabfold_complexes.csv
OUT_DIR=/global/project/hpcg6049/protein/post_mpnn/cf_output/run1

mkdir -p "$OUT_DIR"

echo "HOSTNAME: $(hostname)"
echo "DATE: $(date)"
echo "PWD: $(pwd)"
echo "PYTHON: $(which python)"
python --version
nvidia-smi

# First make MSA
colabfold_batch "$INPUT_CSV" "$OUT_DIR" --msa-only

# Then predict structures
colabfold_batch "$INPUT_CSV" "$OUT_DIR"

echo "DONE: $(date)"
```

Submit:

```bash
sbatch /global/project/hpcg6049/protein/post_mpnn/scripts/run_colabfold.slurm
```

Check logs:

```bash
cat /global/project/hpcg6049/protein/post_mpnn/logs/cf_JOBID.out
cat /global/project/hpcg6049/protein/post_mpnn/logs/cf_JOBID.err
```

---

## 5. Collect ColabFold scores

Save this as:

```bash
/global/project/hpcg6049/protein/post_mpnn/scripts/collect_cf_scores.py
```

```python
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
```

Run:

```bash
python /global/project/hpcg6049/protein/post_mpnn/scripts/collect_cf_scores.py
```

---

## 6. Filter best hits

Save this as:

```bash
/global/project/hpcg6049/protein/post_mpnn/scripts/filter_final_hits.py
```

```python
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
```

Run:

```bash
python /global/project/hpcg6049/protein/post_mpnn/scripts/filter_final_hits.py
```

---

## 7. Exact command order

Run everything in this order:

```bash
pip uninstall -y jax-cuda12-pjrt

python /global/project/hpcg6049/protein/post_mpnn/scripts/parse_mpnn_fastas.py
python /global/project/hpcg6049/protein/post_mpnn/scripts/make_colabfold_csv.py
sbatch /global/project/hpcg6049/protein/post_mpnn/scripts/run_colabfold.slurm
python /global/project/hpcg6049/protein/post_mpnn/scripts/collect_cf_scores.py
python /global/project/hpcg6049/protein/post_mpnn/scripts/filter_final_hits.py
```

---

## Recommendation

Do this in **two rounds**.

### Round 1
- top 3 sequences per model  
- run ColabFold  
- get top 20 models  

### Round 2
- only for the best backbones, test more MPNN sequences from those models  

That is much smarter than sending every sequence immediately.

---

## Optional next step

If you want, the next refinement is to replace the placeholder target sequence with your real target chain sequence and hard-code your exact filenames so the workflow becomes fully copy-paste ready.
