#!/bin/bash
#SBATCH --job-name=phase_b_extra
#SBATCH --output=/global/project/hpcg6049/protein/alzheimer/bindcraft/filtering/logs/phase_b_extra_%j.out
#SBATCH --error=/global/project/hpcg6049/protein/alzheimer/bindcraft/filtering/logs/phase_b_extra_%j.err
#SBATCH --account=def-hpcg6049_gpu
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:a100:1
#SBATCH --mem=32G

set -eo pipefail

echo "Job $SLURM_JOB_ID on $(hostname), partition=$SLURM_JOB_PARTITION"
echo "GPU: CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
nvidia-smi -L | head -1

REPO=/global/project/hpcg6049/protein
INPUT=${REPO}/alzheimer/bindcraft/filtering/stage4/phase_b_extra_input.csv
OUTDIR=${REPO}/alzheimer/bindcraft/filtering/stage4/phase_b_extra_output

mkdir -p "${OUTDIR}"

${REPO}/container/run_colabfold.sh \
    "${INPUT}" \
    "${OUTDIR}" \
    --num-models 1 \
    --num-recycle 3 \
    --msa-mode single_sequence

echo "Phase B extra monomer predictions complete."
echo "Extract pLDDT from ${OUTDIR} to complete Stage 4."
