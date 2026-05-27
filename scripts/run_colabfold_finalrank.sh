#!/usr/bin/env bash
#SBATCH -J cf_rank
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH -t 01:00:00
#SBATCH -o /global/project/hpcg6049/protein/post_mpnn/logs/cf_rank_%j.out
#SBATCH -e /global/project/hpcg6049/protein/post_mpnn/logs/cf_rank_%j.err

set -eo pipefail

eval "$(conda shell.bash hook)"
conda activate colabfold

OUT_DIR=/global/project/hpcg6049/protein/post_mpnn/cf_output/run1

echo "Running ranking..."

python <<EOF
import json, glob, os, csv

out_dir = "$OUT_DIR"
results = []

for f in glob.glob(os.path.join(out_dir, "*.json")):
    with open(f) as fh:
        data = json.load(fh)

    iptm = data.get("iptm", 0)
    ptm = data.get("ptm", 0)
    plddt = data.get("plddt", [])

    mean_plddt = sum(plddt)/len(plddt) if isinstance(plddt, list) and len(plddt)>0 else 0
    score = 0.8 * iptm + 0.2 * ptm

    results.append((f, iptm, ptm, mean_plddt, score))

results.sort(key=lambda x: x[4], reverse=True)

out_csv = os.path.join(out_dir, "ranking_results.csv")

with open(out_csv, "w") as f:
    f.write("file,iptm,ptm,plddt,score\n")
    for r in results:
        f.write(",".join(map(str, r)) + "\n")

print("Top 20:")
for r in results[:20]:
    print(r)

print("Saved:", out_csv)
EOF

echo "DONE: $(date)"
