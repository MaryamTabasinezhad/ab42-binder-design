#!/bin/bash
#SBATCH --job-name=s4_monomer
#SBATCH --output=alzheimer/bindcraft/filtering/logs/monomer_plddt_%j.out
#SBATCH --error=alzheimer/bindcraft/filtering/logs/monomer_plddt_%j.err
#SBATCH --account=def-ghaedi
#SBATCH --time=03:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:a100:1
#SBATCH --mem=48G

set -eo pipefail

echo "Job $SLURM_JOB_ID on $(hostname), partition=$SLURM_JOB_PARTITION"
echo "GPU: CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
nvidia-smi -L | head -1

REPO_ROOT="/scratch/ghaedi/ab42-binder-design"
INPUT_CSV="${REPO_ROOT}/alzheimer/bindcraft/filtering/inputs/monomer_input.csv"
OUTPUT_DIR="${REPO_ROOT}/alzheimer/bindcraft/filtering/outputs/monomer_plddt"

source "${REPO_ROOT}/clusters/narval.env"

module load apptainer 2>/dev/null || true

if [ ! -f "${COLABFOLD_SIF}" ]; then
    echo "ERROR: Container not found: ${COLABFOLD_SIF}" >&2
    exit 1
fi

mkdir -p "${OUTPUT_DIR}"

echo "Running ColabFold monomer prediction (62 designs, alphafold2_ptm, single_sequence)"
echo "Input: ${INPUT_CSV}"
echo "Output: ${OUTPUT_DIR}"
echo "Container: ${COLABFOLD_SIF}"

WORK_PARENT="/scratch/ghaedi"
CONTAINER_INPUT="/work${INPUT_CSV#${WORK_PARENT}}"
CONTAINER_OUTPUT="/work${OUTPUT_DIR#${WORK_PARENT}}"

apptainer exec --nv --no-home \
    -B "${WORK_PARENT}:/work" \
    -B "${COLABFOLD_CACHE}:/cache/colabfold" \
    "${COLABFOLD_SIF}" \
    colabfold_batch \
        "${CONTAINER_INPUT}" \
        "${CONTAINER_OUTPUT}" \
        --model-type alphafold2_ptm \
        --msa-mode single_sequence \
        --num-models 5 \
        --num-recycle 3

echo "ColabFold monomer prediction complete."
echo "Output files: $(ls "${OUTPUT_DIR}" | wc -l)"
