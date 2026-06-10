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

# Source the cluster env explicitly and export the container vars, rather than
# relying on the wrapper's hostname auto-detect — that failed on Narval compute
# nodes (job 62652492/62692747). Override with CLUSTER=<name> sbatch ... if needed.
if [ -z "${CLUSTER}" ]; then
    case "$(hostname -f)" in
        *frontenac*|frnt*) CLUSTER=frontenac ;;
        *nibi*)            CLUSTER=nibi ;;
        *narval*)          CLUSTER=narval ;;
        *) echo "ERROR: cannot detect cluster from $(hostname -f); resubmit with CLUSTER=<name> sbatch ..." >&2; exit 1 ;;
    esac
fi
source "${REPO}/clusters/${CLUSTER}.env"
export COLABFOLD_SIF COLABFOLD_CACHE APPTAINER_MODULE
echo "Cluster=${CLUSTER}  SIF=${COLABFOLD_SIF}"

# Default to split A; pass SPLIT=B for Narval's half
SPLIT=${SPLIT:-A}
INPUT=${REPO}/alzheimer/bindcraft/fusion/inputs/fusion_input_${SPLIT}.csv
OUTDIR=${REPO}/alzheimer/bindcraft/fusion/outputs/split_${SPLIT}

mkdir -p "${OUTDIR}"

echo "Running split ${SPLIT}: $(wc -l < "${INPUT}") sequences (including header)"

# Invoke via `bash` so a missing +x bit on the wrapper doesn't fail the job
# (this also bit Narval's first attempt, job 62652492).
bash "${REPO}/container/run_colabfold.sh" \
    "${INPUT}" \
    "${OUTDIR}" \
    --num-models 1 \
    --num-recycle 3 \
    --msa-mode single_sequence

echo "Stage 8 fusion ColabFold split ${SPLIT} complete."
