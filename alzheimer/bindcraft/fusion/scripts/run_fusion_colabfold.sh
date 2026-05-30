#!/bin/bash
#SBATCH --job-name=stage8_fusion
#SBATCH --output=/global/project/hpcg6049/protein/alzheimer/bindcraft/fusion/logs/fusion_%j.out
#SBATCH --error=/global/project/hpcg6049/protein/alzheimer/bindcraft/fusion/logs/fusion_%j.err
#SBATCH --account=def-hpcg6049_gpu
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:a100:1
#SBATCH --mem=48G

set -eo pipefail

echo "Job $SLURM_JOB_ID on $(hostname), partition=$SLURM_JOB_PARTITION"
echo "GPU: CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
nvidia-smi -L | head -1

REPO=/global/project/hpcg6049/protein

# Default to split A; pass SPLIT=B for Narval's half
SPLIT=${SPLIT:-A}
INPUT=${REPO}/alzheimer/bindcraft/fusion/inputs/fusion_input_${SPLIT}.csv
OUTDIR=${REPO}/alzheimer/bindcraft/fusion/outputs/split_${SPLIT}

mkdir -p "${OUTDIR}"

echo "Running split ${SPLIT}: $(wc -l < "${INPUT}") sequences (including header)"

${REPO}/container/run_colabfold.sh \
    "${INPUT}" \
    "${OUTDIR}" \
    --num-models 1 \
    --num-recycle 3 \
    --msa-mode single_sequence

echo "Stage 8 fusion ColabFold split ${SPLIT} complete."
