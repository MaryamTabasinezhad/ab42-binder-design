#!/bin/bash
#SBATCH --job-name=bc_ab42_p%a
#SBATCH --output=/global/project/hpcg6049/protein/alzheimer/bindcraft/logs/bc_ab42_p%a_%j.out
#SBATCH --error=/global/project/hpcg6049/protein/alzheimer/bindcraft/logs/bc_ab42_p%a_%j.err
#SBATCH --account=def-hpcg6049_gpu
#SBATCH --time=13-23:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --array=1-4

set -eo pipefail

echo "Job $SLURM_JOB_ID (array task $SLURM_ARRAY_TASK_ID) on $(hostname), partition=$SLURM_JOB_PARTITION"
echo "GPU: CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
nvidia-smi -L | head -1
echo "Started: $(date)"

eval "$(conda shell.bash hook)"
conda activate BindCraft

REPO=/global/project/hpcg6049/protein/alzheimer/bindcraft/repo
SETTINGS=/global/project/hpcg6049/protein/alzheimer/bindcraft/settings

python -u "$REPO/bindcraft.py" \
  --settings "$SETTINGS/ab42_CEG_p${SLURM_ARRAY_TASK_ID}.json" \
  --filters "$REPO/settings_filters/default_filters.json" \
  --advanced "$SETTINGS/advanced_ab42.json"

echo "Finished: $(date)"
