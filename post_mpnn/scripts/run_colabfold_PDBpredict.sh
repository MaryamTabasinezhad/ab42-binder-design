#!/usr/bin/env bash
#SBATCH -J cf_predict
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH -t 24:00:00
#SBATCH -o /global/project/hpcg6049/protein/post_mpnn/logs/cf_predict_%j.out
#SBATCH -e /global/project/hpcg6049/protein/post_mpnn/logs/cf_predict_%j.err

set -eo pipefail

eval "$(conda shell.bash hook)"
conda activate colabfold

INPUT_CSV=/global/project/hpcg6049/protein/post_mpnn/cf_input/colabfold_complexes.csv
OUT_DIR=/global/project/hpcg6049/protein/post_mpnn/cf_output/run1

mkdir -p "$OUT_DIR"

echo "Starting ColabFold prediction..."
colabfold_batch "$INPUT_CSV" "$OUT_DIR"

echo "DONE: $(date)"
