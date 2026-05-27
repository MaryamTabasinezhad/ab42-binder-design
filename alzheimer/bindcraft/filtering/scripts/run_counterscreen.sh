#!/bin/bash
#SBATCH --job-name=stage3_cs
#SBATCH --output=/lustre07/scratch/ghaedi/ab42-binder-design/alzheimer/bindcraft/filtering/logs/stage3_%A_%a.out
#SBATCH --error=/lustre07/scratch/ghaedi/ab42-binder-design/alzheimer/bindcraft/filtering/logs/stage3_%A_%a.err
#SBATCH --account=def-ghaedi
#SBATCH --gres=gpu:a100:1
#SBATCH --time=05:59:00
#SBATCH --mem=48G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --array=0-7

set -eo pipefail

TARGETS=(9CO4 9CKI 9CK6 7Q4B 7Q4M 6SHS 1IYT Ab40_monomer)
TARGET=${TARGETS[$SLURM_ARRAY_TASK_ID]}

FILTER_DIR="/lustre07/scratch/ghaedi/ab42-binder-design/alzheimer/bindcraft/filtering"
INPUT_CSV="${FILTER_DIR}/inputs/colabfold_${TARGET}.csv"
OUTPUT_DIR="${FILTER_DIR}/outputs/${TARGET}"

echo "Job $SLURM_JOB_ID task $SLURM_ARRAY_TASK_ID on $(hostname)"
echo "Target: ${TARGET}"
echo "Input: ${INPUT_CSV}"
echo "Output: ${OUTPUT_DIR}"
echo "GPU: CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
nvidia-smi -L | head -1

mkdir -p "${OUTPUT_DIR}"

module load python/3.11
source /home/ghaedi/envs/colabfold/bin/activate

colabfold_batch \
    "${INPUT_CSV}" \
    "${OUTPUT_DIR}" \
    --data /home/ghaedi/.cache/colabfold \
    --num-models 1 \
    --num-recycle 3 \
    --msa-mode single_sequence \
    --model-type alphafold2_multimer_v3

echo "Done: target=${TARGET}, exit=$?"
