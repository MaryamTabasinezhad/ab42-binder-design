#!/usr/bin/env bash
#SBATCH -J proteinmpnn_binders
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH -t 48:00:00
#SBATCH --output=/global/project/hpcg6049/protein/ProteinMPNN/logs/proteinmpnn_%j.out
#SBATCH --error=/global/project/hpcg6049/protein/ProteinMPNN/logs/proteinmpnn_%j.err

source ~/.bashrc
conda activate mpnn

set -euo pipefail

cd /global/project/hpcg6049/protein/ProteinMPNN

INPUT_DIR=/global/project/hpcg6049/protein/rfdiffusion_test/output/set1/top100_pdbs
mkdir -p outputs/tfr1_binders outputs/mtfr1_binders/results

python helper_scripts/parse_multiple_chains.py \
  --input_path "$INPUT_DIR" \
  --output_path outputs/tfr1_binders/parsed_pdbs.jsonl

python helper_scripts/assign_fixed_chains.py \
  --input_path outputs/tfr1_binders/parsed_pdbs.jsonl \
  --output_path outputs/tfr1_binders/assigned_pdbs.jsonl \
  --chain_list "A"

python protein_mpnn_run.py \
  --jsonl_path outputs/tfr1_binders/parsed_pdbs.jsonl \
  --chain_id_jsonl outputs/tfr1_binders/assigned_pdbs.jsonl \
  --out_folder outputs/mtfr1_binders/results \
  --num_seq_per_target 8 \
  --sampling_temp "0.1 0.15 0.2" \
  --seed 37 \
  --batch_size 1 \
  --use_soluble_model

echo "Job finished successfully."
