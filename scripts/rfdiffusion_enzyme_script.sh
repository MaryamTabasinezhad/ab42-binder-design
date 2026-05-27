#!/usr/bin/env bash
#SBATCH -J rfd_test
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH -t 02:00:00
#SBATCH --output=logs/rfd_test_%j.out
#SBATCH --error=logs/rfd_test_%j.err

set -euo pipefail

module load StdEnv/2023 apptainer/1.4.5

WORK_DIR="/global/project/hpcg6049/protein/rfdiffusion_test"
SIF_PATH="/global/scratch/hpc6049/protein/container/rfdiffusion.sif"
SCHEDULES_DIR="${WORK_DIR}/schedules"

mkdir -p "${WORK_DIR}/input" "${WORK_DIR}/output" "${SCHEDULES_DIR}"

echo "Starting RFdiffusion job on $(hostname)"
echo "Working directory: ${WORK_DIR}"

export HYDRA_FULL_ERROR=1

apptainer run --nv \
  --bind ${WORK_DIR}/input:/input \
  --bind ${WORK_DIR}/output:/output \
  --bind ${SCHEDULES_DIR}:/app/RFdiffusion/schedules \
  ${SIF_PATH} \
  inference.output_prefix=/output/design_enzyme \
  inference.model_directory_path=/app/RFdiffusion/models \
  inference.input_pdb=/input/5an7.pdb \
  inference.num_designs=3 \
  'contigmap.contigs=[10-100/A1083-1083/10-100/A1051-1051/10-100/A1180-1180/10-100]' \
  potentials.guide_scale=1 \
  "potentials.guiding_potentials=['type:substrate_contacts,s:1,r_0:8,rep_r_0:5.0,rep_s:2,rep_r_min:1']" \
  potentials.substrate=LLK \
  inference.ckpt_override_path=/app/RFdiffusion/models/ActiveSite_ckpt.pt

echo "Job finished successfully."
