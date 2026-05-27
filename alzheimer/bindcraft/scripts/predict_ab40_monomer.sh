#!/bin/bash
#SBATCH --job-name=ab40_af2
#SBATCH --output=/global/project/hpcg6049/protein/alzheimer/bindcraft/logs/ab40_af2_%j.out
#SBATCH --error=/global/project/hpcg6049/protein/alzheimer/bindcraft/logs/ab40_af2_%j.err
#SBATCH --account=def-hpcg6049_gpu
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --mem=16G

set -eo pipefail

echo "Job $SLURM_JOB_ID on $(hostname), partition=$SLURM_JOB_PARTITION"
nvidia-smi -L | head -1

eval "$(conda shell.bash hook)"
conda activate colabfold

OUTDIR=/global/project/hpcg6049/protein/alzheimer/structures/negative_targets/ab40_colabfold
mkdir -p "$OUTDIR"

# Aβ40 sequence (FASTA format)
FASTA_DIR=/global/project/hpcg6049/protein/alzheimer/structures/negative_targets/ab40_input
mkdir -p "$FASTA_DIR"
echo ">Ab40_monomer
DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVV" > "$FASTA_DIR/ab40.fasta"

colabfold_batch "$FASTA_DIR/ab40.fasta" "$OUTDIR" \
  --num-models 5 \
  --num-recycle 3 \
  --model-type alphafold2_ptm

echo "Done. Best model will be selected by pLDDT."
ls -la "$OUTDIR/"
