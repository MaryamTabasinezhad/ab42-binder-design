#!/bin/bash
#SBATCH --job-name=gpu_check
#SBATCH --output=/global/project/hpcg6049/protein/alzheimer/env/gpu_check_%j.out
#SBATCH --error=/global/project/hpcg6049/protein/alzheimer/env/gpu_check_%j.err
#SBATCH --account=def-hpcg6049_gpu
#SBATCH --time=00:05:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1

set -eo pipefail

echo "=== GPU Check Job ==="
echo "Date: $(date)"
echo "Hostname: $(hostname)"
echo "Job ID: $SLURM_JOB_ID"
echo "Partition: $SLURM_JOB_PARTITION"
echo ""

echo "=== nvidia-smi ==="
nvidia-smi
echo ""

echo "=== GPU Details ==="
nvidia-smi -L
echo ""

echo "=== GPU Specs ==="
nvidia-smi --query-gpu=name,memory.total,driver_version,compute_cap --format=csv,noheader
echo ""

echo "=== Environment ==="
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
echo "GPU_DEVICE_ORDINAL=$GPU_DEVICE_ORDINAL"
echo "SLURM_GPUS=$SLURM_GPUS"
echo "SLURM_JOB_GPUS=$SLURM_JOB_GPUS"
echo "SLURM_GPUS_ON_NODE=$SLURM_GPUS_ON_NODE"
echo ""

echo "=== Done ==="
