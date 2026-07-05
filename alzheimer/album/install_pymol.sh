#!/bin/bash
#SBATCH --job-name=install_pymol
#SBATCH --output=/global/project/hpcg6049/protein/alzheimer/album/logs/install_pymol_%j.out
#SBATCH --error=/global/project/hpcg6049/protein/alzheimer/album/logs/install_pymol_%j.err
#SBATCH --account=def-hpcg6049_cpu
#SBATCH --time=00:40:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G

set -eo pipefail

echo "Job $SLURM_JOB_ID on $(hostname), partition=$SLURM_JOB_PARTITION"

# Site anaconda (per PyMOL handoff doc, 2026-07-05)
source /global/software/python/anaconda3-2024.06-1/etc/profile.d/conda.sh

if conda env list | grep -qE '/\.conda/envs/pymol\b'; then
  echo "env 'pymol' already exists — skipping create"
else
  echo "creating conda env 'pymol' with pymol-open-source ..."
  conda create -y -n pymol -c conda-forge python=3.11 pymol-open-source
fi

conda activate pymol
echo "=== smoke test ==="
pymol -cq -d "print('PyMOL', cmd.get_version()[0])"
pymol -cq -d "fragment ala; show sticks; ray 300,300; png /global/project/hpcg6049/protein/alzheimer/album/logs/smoke.png; print('RENDER_OK')"
echo "=== done ==="
