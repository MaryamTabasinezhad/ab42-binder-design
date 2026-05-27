#!/bin/bash
#SBATCH --job-name=rtx8k_check
#SBATCH --output=/global/project/hpcg6049/protein/alzheimer/env/rtx8000_check_%j.out
#SBATCH --error=/global/project/hpcg6049/protein/alzheimer/env/rtx8000_check_%j.err
#SBATCH --account=def-hpcg6049_gpu
#SBATCH --time=00:02:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:rtx8000:1

nvidia-smi --query-gpu=name,memory.total,driver_version,compute_cap --format=csv,noheader
echo "---"
hostname
