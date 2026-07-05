#!/bin/bash
#SBATCH --job-name=render_top5
#SBATCH --output=/global/project/hpcg6049/protein/alzheimer/album/logs/render_top5_%j.out
#SBATCH --error=/global/project/hpcg6049/protein/alzheimer/album/logs/render_top5_%j.err
#SBATCH --account=def-hpcg6049_cpu
#SBATCH --time=00:40:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G

set -eo pipefail
echo "Job $SLURM_JOB_ID on $(hostname), partition=$SLURM_JOB_PARTITION"
source /global/software/python/anaconda3-2024.06-1/etc/profile.d/conda.sh
conda activate pymol
cd /global/project/hpcg6049/protein/alzheimer/album
pymol -cq render_top5.py
echo "=== render outputs ==="
ls -la renders/
echo "RENDER_JOB_DONE"
