# Alzheimer's Aβ42 Binder Design Project — HPC Environment Reference

## Project
De novo bispecific miniprotein binder targeting receptor-bound Aβ42
filament (Conformation 1, PDB 9CO4) × TfR1 for BBB-crossing
Alzheimer's therapeutic. Lecanemab-logic lateral-binding strategy.

## HPC: Frontenac (CAC, Queen's University)
- User: hpc6049
- Project root: /global/project/hpcg6049/protein/alzheimer
- Scratch: /global/scratch/hpc6049/
- Conda envs: ~/.conda/envs/

## GPU Hardware

### Confirmed GPU models (tested 2026-05-06)

| GPU Model | VRAM | Compute Cap. | Driver | CUDA | Example Node(s) | GPUs/Node |
|-----------|------|-------------|--------|------|------------------|-----------|
| NVIDIA A100-PCIE-40GB | 40 GB | 8.0 | 595.58.03 | 12.9+ | frnt107 (1), frnt154/190/191 (8) | 1 or 8 |
| Quadro RTX 8000 | 45 GB | 7.5 | 595.58.03 | 12.9+ | frnt156 | 8 |
| Tesla V100-PCIE-32GB | 32 GB | 7.0 | 575.57.08 | 12.9 | frnt110 | 1 |
| Quadro RTX 6000 | 22.5 GB | 7.5 | 595.58.03 | 13.2 | frnt108/109, frnt149-155 | 2 or 8 |
| NVIDIA A30 | 24 GB (spec) | 8.0 (spec) | not tested | — | frnt140-148 | 2 |
| NVIDIA L4 | 24 GB (spec) | 8.9 (spec) | not tested | — | frnt201 | 2 |

The 8-GPU A100 nodes (frnt154, frnt190, frnt191) are DGX systems with 1 TB RAM.

## SLURM GPU Syntax

### CRITICAL: Two things you MUST do

1. **Use `--account=def-hpcg6049_gpu`** — the default account is `def-hpcg6049_cpu` and ALL GPU requests fail silently with it.
2. **Do NOT specify `--partition` / `-p`** — specifying any GPU partition (even the correct one) causes the error "partition does not exist or submitted job cannot fit." Let the scheduler auto-route.

### Syntax that WORKS

```bash
# srun (interactive)
srun --account=def-hpcg6049_gpu --gres=gpu:1 --time=00:05:00 <command>

# srun with specific GPU type
srun --account=def-hpcg6049_gpu --gres=gpu:a100:1 --time=00:05:00 <command>
srun --account=def-hpcg6049_gpu --gres=gpu:rtx6000:1 --time=00:05:00 <command>
srun --account=def-hpcg6049_gpu --gres=gpu:rtx8000:1 --time=00:05:00 <command>

# Alternative flags (also work)
srun --account=def-hpcg6049_gpu --gpus=1 --time=00:05:00 <command>
srun --account=def-hpcg6049_gpu --gpus-per-node=1 --time=00:05:00 <command>

# sbatch
#SBATCH --account=def-hpcg6049_gpu
#SBATCH --gres=gpu:1                   # any GPU
#SBATCH --gres=gpu:a100:1              # specific type
# Do NOT add #SBATCH --partition=...
```

### Syntax that FAILS

```bash
# FAILS: specifying partition (even with correct account)
srun -p gpubase_6hrs --account=def-hpcg6049_gpu --gres=gpu:1 ...
# ERROR: "partition does not exist or submitted job cannot fit"

# FAILS: without GPU account
srun --gres=gpu:1 --time=00:05:00 ...
srun -p gpubase_6hrs --gres=gpu:1 ...
# ERROR: same partition error (routes to CPU account)

# FAILS: requesting node directly with -w
srun --account=def-hpcg6049_gpu --gres=gpu:a100:1 -w frnt154 ...
# ERROR: "Requested nodes not in this partition"
```

### Available GPU GRES types for --gres=gpu:TYPE:N
`a100`, `a30`, `rtx6000`, `rtx8000`, `v100`, `l4` (lowercase for sacctmgr; node config uses `L4` but SLURM GRES uses lowercase in accounting)

### Partition reference (auto-selected by scheduler)

| Partition | Time limit | Nodes | Notes |
|-----------|-----------|-------|-------|
| gpubase_interac | 6 hrs | 6 | Max 1 node, higher priority |
| gpubase_6hrs | 6 hrs | 24 | All GPU node types |
| gpubase_24hrs | 1 day | 14 | Subset of nodes |
| gpubase_14days | 14 days | 10 | Long-running jobs (BindCraft) |
| gpu-L4 | 6 hrs | 1 | frnt201 only |

### SLURM environment on GPU nodes
- `CUDA_VISIBLE_DEVICES` is set correctly by the scheduler (e.g., `=0` for 1 GPU)
- `nvidia-smi` shows ALL node GPUs, but CUDA apps only see the allocated one(s)
- `SLURM_JOB_GPUS` and `SLURM_GPUS_ON_NODE` are set
- Partition is auto-assigned; check `$SLURM_JOB_PARTITION` in scripts

### Standard sbatch template for GPU jobs

```bash
#!/bin/bash
#SBATCH --job-name=<name>
#SBATCH --output=logs/<name>_%j.out
#SBATCH --error=logs/<name>_%j.err
#SBATCH --account=def-hpcg6049_gpu
#SBATCH --time=HH:MM:SS
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
# Optional: request specific GPU type
# #SBATCH --gres=gpu:a100:1
# Optional: memory (default is 256 MB/CPU)
# #SBATCH --mem=32G

set -eo pipefail

echo "Job $SLURM_JOB_ID on $(hostname), partition=$SLURM_JOB_PARTITION"
echo "GPU: CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
nvidia-smi -L | head -1

# Your commands here
```

## Software

| Tool | How to activate | Version | Notes |
|------|----------------|---------|-------|
| GROMACS | `module load gromacs/2024.6` | 2024.6 | Mixed precision, MPI-enabled |
| ColabFold | `conda activate colabfold` | 1.6.1 | Has JAX 0.6.0, OpenMM 8.5.1, PDBFixer, AlphaFold-ColabFold 2.3.13 |
| ProteinMPNN | `conda activate mpnn` | — | CPU-only PyTorch 2.7.1 |
| RFdiffusion | Apptainer + `conda activate rfdiffusion` | — | PyTorch 2.0.1+CUDA 11.7 |
| RFdiffusion (clean) | `conda activate rfd_clean` | — | PyTorch 2.5.1+CUDA 11.8 |
| JAX (GPU) | In `colabfold` env | 0.6.0 | CUDA 12 plugin; GPU visible only on compute nodes |
| AlphaFold | HMMER module only (`hmmer-alphafold3/3.4`) | 3.4 (HMMER) | No standalone AF2/AF3 install |
| Python (base) | default | 3.12.4 | Anaconda 2024.06 |
| Python (colabfold) | `conda activate colabfold` | 3.11.15 | |
| BindCraft | `conda activate BindCraft` | 1.1.3 (ColabDesign) | JAX 0.6.0, PyRosetta 2026.3, Python 3.10. Repo: `bindcraft/repo/`. AF2 params: `bindcraft/repo/params/`. GPU-tested on A30 (2026-05-06). |
| OpenMM | In `colabfold` env | 8.5.1 | CPU platforms only (Reference, CPU); no CUDA platform on login node |

## BindCraft Compatibility Assessment

### VRAM requirements
BindCraft uses AF2 with backpropagation through the structure module for gradient-based binder design. Memory requirements depend on protein complex size:
- Standard AF2 backprop: ~40 GB VRAM minimum for moderate complexes (~300 residues)
- With model sharding / reduced features: ~24 GB possible for small complexes

### GPU suitability

| GPU | VRAM | BindCraft viable? |
|-----|------|-------------------|
| A100-PCIE-40GB | 40 GB | **Yes** — best option, marginal for large complexes |
| RTX 8000 | 45 GB | **Yes** — most VRAM, good fallback |
| V100-PCIE-32GB | 32 GB | **Marginal** — may work with sharding for small designs |
| A30 | 24 GB | **Tight** — only with aggressive sharding and short sequences |
| RTX 6000 | 22.5 GB | **Tight** — same constraints as A30 |
| L4 | 24 GB | **Tight** — same constraints as A30 |

### What needs to be installed for BindCraft
1. Clone BindCraft repo (https://github.com/martinpacesa/BindCraft)
2. Install in a new conda env (BindCraft has strict JAX/AF2 version pins)
3. Download AF2 weights (params/ directory, ~3.5 GB)
4. Test on A100 node first (`--gres=gpu:a100:1`)
5. The `colabfold` env has JAX 0.6.0 and AlphaFold-ColabFold 2.3.13, which may conflict with BindCraft's requirements — use a separate env

### Recommended partition for BindCraft production
Use `gpubase_14days` (auto-selected for `--time` > 24h) with A100 GPUs:
```bash
#SBATCH --account=def-hpcg6049_gpu
#SBATCH --time=7-00:00:00
#SBATCH --gres=gpu:a100:1
```

## Key Constraints / Gotchas

1. **Account is everything**: Default account `def-hpcg6049_cpu` silently blocks all GPU requests. Always add `--account=def-hpcg6049_gpu` to every GPU job.
2. **Never specify `--partition`**: The scheduler auto-routes based on `--time` and GPU request. Specifying a partition always fails (as of 2026-05-06).
3. **Never use `-w` (node targeting)**: Fails with "Requested nodes not in this partition." The scheduler picks the node.
4. **Login nodes have no GPU**: JAX/CUDA code on login nodes sees only CPU. Test GPU code only via srun/sbatch.
5. **Different CUDA versions per node**: V100 nodes run CUDA 12.9 / Driver 575.57.08; most other GPU nodes run CUDA 13.2 / Driver 595.58.03. Compile CUDA code for the lowest common CC (7.0).
6. **nvidia-smi shows ALL node GPUs**: Even if you requested 1, nvidia-smi lists all. But `CUDA_VISIBLE_DEVICES` is set correctly — applications using CUDA will only see your allocated GPU(s).
7. **Conda activation in scripts**: Use `eval "$(conda shell.bash hook)"` followed by `conda activate <env>` (not `source activate`).
8. **Absolute paths in SLURM scripts**: Compute nodes don't inherit submit-side CWD. Always use full paths.
9. **RestrictedCoresPerGPU**: Some nodes (V100, A30) restrict 4 CPU cores per GPU. This is transparent but affects CPU-heavy workflows.

## Directory Layout

```
alzheimer/
├── CLAUDE.md              (this file)
├── DEVELOPMENT_PLAN.md    (11-stage development plan — authoritative)
├── HANDOFF.md             (project onboarding — read second)
├── PROJECT_STATUS.md      (machine-readable status tracker)
├── env/                   (environment audit artifacts, GPU check scripts/outputs)
├── docs/                  (reports and session log)
├── structures/            (PDB files — to be populated)
├── nterm_md/              (N-terminus MD — deferred)
├── bindcraft/             (BindCraft campaign — to be populated)
└── README.md
```

## Project Memory System

### Files to read at session start (in this order)
1. `CLAUDE.md` (this file) — HPC environment, SLURM syntax, software
2. `HANDOFF.md` — project context, current status, key decisions, warnings
3. `DEVELOPMENT_PLAN.md` — full stage-by-stage plan (reference as needed)
4. `PROJECT_STATUS.md` — machine-readable status tracker

### Maintenance responsibilities
At the END of every Claude Code session that modifies project state:
1. Update `HANDOFF.md` Section 2 (status checklist)
2. Update `PROJECT_STATUS.md` stage statuses and metrics
3. If a new decision was made, add it to both `HANDOFF.md` Section 3
   and `PROJECT_STATUS.md` Decision log
4. If a new gotcha was discovered, add it to `HANDOFF.md` Section 4
   and `CLAUDE.md` Key Constraints / Gotchas
5. If new files were created, update `HANDOFF.md` Section 5

### Session start protocol
When beginning a new session in this project:
1. Read CLAUDE.md (you're reading it now)
2. Read HANDOFF.md
3. Check PROJECT_STATUS.md for current stage
4. Ask the user what they'd like to work on, or continue from
   the next incomplete substep in the current stage
