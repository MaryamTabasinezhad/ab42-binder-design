#!/bin/bash
#SBATCH --job-name=tfr1_cs
#SBATCH --output=/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/tfr1/filtering/logs/tfr1_cs_%A_%a.out
#SBATCH --error=/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/tfr1/filtering/logs/tfr1_cs_%A_%a.err
#SBATCH --account=def-ghaedi
#SBATCH --gres=gpu:h100:1
#SBATCH --time=11:59:00
#SBATCH --mem=48G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --array=0-2

set -eo pipefail

TARGETS=(6WRV_positive TfR2_negative 1SUV_Tf_competition)
TARGET=${TARGETS[$SLURM_ARRAY_TASK_ID]}

FILTER_DIR="/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/tfr1/filtering"
INPUT_CSV="${FILTER_DIR}/inputs/colabfold_${TARGET}.csv"
OUTPUT_DIR="${FILTER_DIR}/outputs/${TARGET}"

echo "Job $SLURM_JOB_ID task $SLURM_ARRAY_TASK_ID on $(hostname)"
echo "Target: ${TARGET}"
echo "Input: ${INPUT_CSV}"
echo "Output: ${OUTPUT_DIR}"
echo "GPU: CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
nvidia-smi -L | head -1

mkdir -p "${OUTPUT_DIR}"

module load python/3.11 cuda/12.6
source /home/ghaedi/envs/colabfold/bin/activate

colabfold_batch \
    "${INPUT_CSV}" \
    "${OUTPUT_DIR}" \
    --num-models 1 \
    --num-recycle 3 \
    --msa-mode single_sequence \
    --model-type alphafold2_multimer_v3

echo "Done: target=${TARGET}, exit=$?"
