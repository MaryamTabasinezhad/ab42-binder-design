#!/bin/bash
#SBATCH --job-name=bc_p1
#SBATCH --output=/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/logs/bc_ab42_p1_%j.out
#SBATCH --error=/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/logs/bc_ab42_p1_%j.err
#SBATCH --account=def-ghaedi
#SBATCH --time=05:59:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:h100:1
#SBATCH --mem=48G

set -eo pipefail

echo "Job $SLURM_JOB_ID on $(hostname), partition=$SLURM_JOB_PARTITION"
echo "GPU: CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
nvidia-smi -L | head -1
echo "Started: $(date)"

eval "$(conda shell.bash hook)"
conda activate BindCraft

REPO=/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/repo
SETTINGS=/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/settings

python -u "$REPO/bindcraft.py" \
  --settings "$SETTINGS/ab42_CEG_p1.json" \
  --filters "$REPO/settings_filters/default_filters.json" \
  --advanced "$SETTINGS/advanced_ab42.json"

echo "Finished: $(date)"
