#!/bin/bash
#SBATCH --job-name=stage8_fusion_B
#SBATCH --output=/lustre07/scratch/ghaedi/ab42-binder-design/alzheimer/bindcraft/fusion/logs/fusion_B_%j.out
#SBATCH --error=/lustre07/scratch/ghaedi/ab42-binder-design/alzheimer/bindcraft/fusion/logs/fusion_B_%j.err
#SBATCH --account=def-ghaedi
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:a100:1
#SBATCH --mem=48G

set -eo pipefail

echo "Job $SLURM_JOB_ID on $(hostname), partition=$SLURM_JOB_PARTITION"
echo "GPU: CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
nvidia-smi -L | head -1

REPO=/lustre07/scratch/ghaedi/ab42-binder-design
PROTEIN=/home/ghaedi/projects/def-ghaedi/ghaedi/protein
INPUT=${REPO}/alzheimer/bindcraft/fusion/inputs/fusion_input_B.csv
OUTDIR=${REPO}/alzheimer/bindcraft/fusion/outputs/split_B

export COLABFOLD_SIF=${PROTEIN}/container/colabfold_1.6.1-cuda12.sif
export COLABFOLD_CACHE=${PROTEIN}/container/colabfold_cache
export APPTAINER_MODULE=apptainer

mkdir -p "${OUTDIR}"

echo "Running split B: $(wc -l < "${INPUT}") sequences (including header)"

${PROTEIN}/container/run_colabfold.sh \
    "${INPUT}" \
    "${OUTDIR}" \
    --num-models 1 \
    --num-recycle 3 \
    --msa-mode single_sequence

echo "Stage 8 fusion ColabFold split B complete."
