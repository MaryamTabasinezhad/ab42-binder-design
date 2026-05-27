#!/bin/bash
#SBATCH --job-name=bc_tfr1_p3
#SBATCH --output=/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/tfr1/logs/bc_tfr1_p3_%j.out
#SBATCH --error=/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/tfr1/logs/bc_tfr1_p3_%j.err
#SBATCH --account=def-ghaedi
#SBATCH --time=6-23:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:h100:1
#SBATCH --mem=42G

set -eo pipefail

echo "Job $SLURM_JOB_ID on $(hostname)"
echo "GPU: CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
nvidia-smi -L | head -1
echo "Started: $(date)"

eval "$(/home/ghaedi/miniconda3/bin/conda shell.bash hook)"
conda activate BindCraft

REPO=/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/repo
SETTINGS=/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/tfr1/settings

python -u "$REPO/bindcraft.py" \
  --settings "$SETTINGS/tfr1_AB_p3.json" \
  --filters "$SETTINGS/tfr1_filters.json" \
  --advanced "$SETTINGS/advanced_tfr1.json"

echo "Finished: $(date)"
