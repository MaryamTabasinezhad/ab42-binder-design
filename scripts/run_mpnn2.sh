#!/usr/bin/env bash
#SBATCH -J mpnn_run
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH -t 12:00:00
#SBATCH --output=logs/mpnn_%j.out
#SBATCH --error=logs/mpnn_%j.err

set -eo pipefail

cd /global/project/hpcg6049/protein/ProteinMPNN

echo "HOSTNAME: $(hostname)"
echo "PWD: $(pwd)"
echo "Starting at: $(date)"

eval "$(conda shell.bash hook)"
conda activate mpnn

echo "PYTHON: $(which python)"
python --version

echo "Checking input files..."
ls -l outputs/tfr1_binders/parsed_pdbs.jsonl
ls -l outputs/tfr1_binders/assigned_pdbs.jsonl

echo "Running ProteinMPNN..."
python protein_mpnn_run.py \
  --jsonl_path outputs/tfr1_binders/parsed_pdbs.jsonl \
  --chain_id_jsonl outputs/tfr1_binders/assigned_pdbs.jsonl \
  --out_folder outputs/tfr1_binders/results \
  --num_seq_per_target 8 \
  --sampling_temp "0.1 0.15 0.2" \
  --seed 37 \
  --batch_size 1 \
  --use_soluble_model

echo "Finished at: $(date)"
