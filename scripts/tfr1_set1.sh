#!/usr/bin/env bash
#SBATCH -J rfd_test
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH -t 48:00:00
#SBATCH --output=logs/rfd_test_%j.out
#SBATCH --error=logs/rfd_test_%j.err

set -euo pipefail

module load StdEnv/2023 apptainer/1.4.5

WORK_DIR="/global/project/hpcg6049/protein/rfdiffusion_test"
SIF_PATH="/global/scratch/hpc6049/protein/container/rfdiffusion.sif"
SCHEDULES_DIR="${WORK_DIR}/schedules"

mkdir -p "${WORK_DIR}/input" "${WORK_DIR}/output" "${SCHEDULES_DIR}" logs

echo "Starting RFdiffusion job on $(hostname)"
echo "Working directory: ${WORK_DIR}"

apptainer run --nv \
  --bind ${WORK_DIR}/input:/input \
  --bind ${WORK_DIR}/output:/output \
  --bind ${SCHEDULES_DIR}:/app/RFdiffusion/schedules \
  ${SIF_PATH} \
  inference.output_prefix=/output/TfR1_set1_binder \
  inference.model_directory_path=/app/RFdiffusion/models \
  inference.input_pdb=/input/TfR1crop_renumber.pdb \
  'contigmap.contigs=[A1-71/0 70-120]' \
  'ppi.hotspot_res=[A19,A23,A26]' \
  inference.num_designs=50 \
  inference.ckpt_override_path=/app/RFdiffusion/models/Complex_base_ckpt.pt

echo "Job finished successfully."
