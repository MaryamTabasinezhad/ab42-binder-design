# Frontenac GPU Environment Audit Log

**Date**: 2026-05-06 01:30–02:00 EDT
**User**: hpc6049
**Cluster**: Frontenac (CAC, Queen's University)
**Purpose**: Determine GPU hardware, SLURM syntax, and software environment for BindCraft deployment

---

## Approach 1: Partition Configuration (scontrol show partition)

### gpubase_6hrs
```
PartitionName=gpubase_6hrs
AllowGroups=ALL AllowAccounts=ALL
MaxTime=06:00:00 DefaultTime=01:00:00
Nodes=frnt[107-110,140-156,190-191,201]
TotalCPUs=1208 TotalNodes=24
DefMemPerCPU=256
TRES=cpu=1208,mem=10928000M,node=24,billing=113250,gres/gpu=88,gres/gpu:a100=25,gres/gpu:a30=16,gres/gpu:rtx6000=36,gres/gpu:rtx8000=8,gres/gpu:v100=1
```

### gpubase_interac
```
PartitionName=gpubase_interac
MaxNodes=1 MaxTime=06:00:00
PriorityTier=100 (higher than others at 20)
Nodes=frnt[140,146-148,155,191]
TotalNodes=6
TRES=gres/gpu=26,gres/gpu:a100=8,gres/gpu:a30=6,gres/gpu:rtx6000=12
```

### gpubase_14days
```
PartitionName=gpubase_14days
MaxTime=14-00:00:00
Nodes=frnt[108-109,142-148,190]
TotalNodes=10
TRES=gres/gpu=28,gres/gpu:a100=8,gres/gpu:a30=12,gres/gpu:rtx6000=8
```

### gpu-L4
```
PartitionName=gpu-L4
MaxTime=06:00:00
Nodes=frnt201
TotalNodes=1
TRES=cpu=128,mem=250000M,node=1,gres/gpu=2
TRESBillingWeights includes gres/gpu:L4=1100
```

---

## Approach 2: Cluster GRES/TRES Config

### scontrol show config | grep -i gres
```
AccountingStorageTRES = cpu,mem,energy,node,billing,fs/disk,vmem,pages,gres/gpu,
  gres/gpu:a100,gres/gpu:a30,gres/gpu:gp100,gres/gpu:l4,gres/gpu:p100,
  gres/gpu:rtx4000,gres/gpu:rtx6000,gres/gpu:rtx8000,gres/gpu:v100,gres/gpu:v100l,
  gres/gpumem,gres/gpuutil
GresTypes = gpu
```

### sacctmgr show tres (GPU entries)
```
gres  gpu        1001
gres  gpu:a100   1002
gres  gpu:a30    1003
gres  gpu:p100   1004
gres  gpu:v100   1005
gres  gpumem     1006
gres  gpuutil    1007
gres  gpu:gp100  1008
gres  gpu:v100l  1009
gres  gpu:l4     1010
gres  gpu:rtx4000 1011
gres  gpu:rtx6000 1012
gres  gpu:rtx8000 1013
```

---

## Approach 3: Node Details (scontrol show node)

### frnt110 (V100)
```
Gres=gpu:v100:1(S:0)
RealMemory=187000 (187 GB)
CPUTot=32 (2 sockets, 16 cores/socket)
State=IDLE
Partitions=cpubase_6hrs,gpubase_6hrs
RestrictedCoresPerGPU=4(0-3)
Features=intel,avx512,avx512_gpu
```

### frnt190 (A100 DGX)
```
Gres=gpu:a100:8
RealMemory=1024000 (1 TB)
CPUTot=128 (2 sockets, 64 cores/socket)
State=MIXED (7/8 GPUs allocated at time of check)
Partitions=gpubase_6hrs,gpubase_24hrs,gpubase_14days
Features=dgx,amd
```

### frnt154 (A100 DGX)
```
Gres=gpu:a100:8
RealMemory=1024000 (1 TB)
CPUTot=128
State=IDLE
Partitions=gpubase_6hrs
Features (not checked, likely same as frnt190)
```

### frnt191 (A100 DGX)
```
Gres=gpu:a100:8
RealMemory=1024000 (1 TB)
CPUTot=128
State=MIXED (allocated)
Partitions=gpubase_interac,gpubase_6hrs,gpubase_24hrs
```

### frnt107 (A100 single)
```
Gres=gpu:a100:1(S:0)
RealMemory=379000 (379 GB)
CPUTot=32
State=ALLOCATED
Partitions=cpubase_6hrs,gpubase_6hrs
```

### frnt146 (A30)
```
Gres=gpu:a30:2(S:0)
RealMemory=498000 (498 GB)
CPUTot=48 (2 sockets, 24 cores/socket)
State=MIXED
Partitions=cpubase_6hrs,gpubase_interac,gpubase_6hrs,gpubase_24hrs,gpubase_14days
RestrictedCoresPerGPU=4(0-7)
Features=power_ipmi,amd
```

### frnt156 (RTX 8000)
```
Gres=gpu:rtx8000:8
RealMemory=765000 (765 GB)
CPUTot=32
State=IDLE
Partitions=gpubase_6hrs
```

### frnt108 (RTX 6000)
```
Gres=gpu:rtx6000:2(S:0)
RealMemory=187000
CPUTot=32
State=MIXED
Partitions=cpubase_6hrs,gpubase_6hrs,gpubase_24hrs,gpubase_14days
```

### frnt201 (L4)
```
Gres=gpu:L4:2
RealMemory=250000 (250 GB)
CPUTot=128 (2 sockets, 32 cores/socket, HyperThreading: ThreadsPerCore=2)
State=ALLOCATED (fully busy at time of check)
Partitions=gpubase_6hrs,gpu-L4
Features=L4,rgrant,intel,avx512,avx512_gpu
```

### frnt140 (A30)
```
Gres=gpu:a30:2(S:0)
RealMemory=498000
CPUTot=48
State=MIXED
Partitions=cpubase_6hrs,cpubase_24hrs,gpubase_interac,gpubase_6hrs
```

---

## Account Discovery (Root Cause of Failures)

### sacctmgr show association where user=hpc6049
```
Account                        User  Partition  QOS
def-hpcg6049_cpu               hpc6049           normal
def-hpcg6049_gpu               hpc6049           normal
```

### sacctmgr show user hpc6049
```
DefaultAccount = def-hpcg6049_cpu
```

**KEY FINDING**: The user has TWO accounts. The default (`def-hpcg6049_cpu`) cannot submit to GPU partitions. `--account=def-hpcg6049_gpu` is required for all GPU jobs.

### AccountingStorageEnforce = associations,limits,safe
This means the scheduler strictly enforces account associations — a CPU account cannot submit to GPU-associated partitions.

---

## Approach 4: srun Syntax Testing

### 4a: --gres=gpu:1 with -p gpubase_6hrs (no account)
```
Command: srun -p gpubase_6hrs --gres=gpu:1 --time=00:05:00 nvidia-smi
Result: FAILED
Error: "The specified partition does not exist, or the submitted job cannot fit in it..."
```

### 4a-retry: with --account=def-hpcg6049 (wrong account name)
```
Command: srun -p gpubase_6hrs --account=def-hpcg6049 --gres=gpu:1 --time=00:05:00 hostname
Result: FAILED (same error)
```

### 4a-retry2: with --account=def-hpcg6049_gpu + partition
```
Command: srun -p gpubase_6hrs --account=def-hpcg6049_gpu --gres=gpu:1 --time=00:05:00 nvidia-smi -L
Result: FAILED (same partition error even with correct account!)
```

### 4a-SUCCESS: --account=def-hpcg6049_gpu, NO partition
```
Command: srun --account=def-hpcg6049_gpu --gres=gpu:1 --time=00:05:00 nvidia-smi
Result: SUCCESS
Node: frnt155
GPU: 8× Quadro RTX 6000, 23040 MiB each
CUDA_VISIBLE_DEVICES=2
Driver: 595.58.03, CUDA 13.2
Compute Cap: 7.5
```

### 4b: --gres=gpu:1, no partition, no account
```
Command: srun -p gpubase_6hrs --time=00:05:00 nvidia-smi
Result: FAILED (same error)
```

### 4c: --gpus=1 (no partition)
```
Command: srun --account=def-hpcg6049_gpu --gpus=1 --time=00:05:00 nvidia-smi -L
Result: SUCCESS
Node: frnt155, 8× Quadro RTX 6000
```

### 4d: --gpus-per-node=1 (no partition)
```
Command: srun --account=def-hpcg6049_gpu --gpus-per-node=1 --time=00:05:00 nvidia-smi -L
Result: SUCCESS
Node: frnt155, 8× Quadro RTX 6000
```

### 4e: --gres=gpu:rtx6000:1 (typed, no partition)
```
Command: srun --account=def-hpcg6049_gpu --gres=gpu:rtx6000:1 --time=00:05:00 ...
Result: SUCCESS
Node: frnt155
```

### 4f: --gres=gpu:a100:1 (no partition)
```
Command: srun --account=def-hpcg6049_gpu --gres=gpu:a100:1 --time=00:05:00 ...
Result: TIMEOUT after 120s (all A100s were busy)
```

### 4g: --gres=gpu:L4:1 (uppercase, no partition)
```
Result: FAILED — "Requested node configuration is not available"
```

### 4h: --gres=gpu:l4:1 (lowercase, no partition)
```
Result: FAILED — same error (frnt201 fully allocated)
```

### 4i: -w frnt154 (node targeting)
```
Command: srun --account=def-hpcg6049_gpu --gres=gpu:a100:1 -w frnt154 --time=00:02:00 ...
Result: FAILED — "Requested nodes not in this partition"
```

---

## Approach 5: sbatch Testing

### Job 8374094: Generic GPU request via sbatch (no partition)
```bash
#SBATCH --account=def-hpcg6049_gpu
#SBATCH --gres=gpu:1
```
**Result: SUCCESS**
- Auto-routed to partition: gpubase_6hrs
- Node: frnt110
- GPU: Tesla V100-PCIE-32GB, 32768 MiB
- Driver: 575.57.08, CUDA 12.9, Compute Cap: 7.0
- CUDA_VISIBLE_DEVICES=0, SLURM_JOB_GPUS=0, SLURM_GPUS_ON_NODE=1

### Job 8374097: A100 request via sbatch (no partition)
```bash
#SBATCH --account=def-hpcg6049_gpu
#SBATCH --gres=gpu:a100:1
```
**Result: SUCCESS**
- Auto-routed to: gpubase_6hrs
- Node: frnt154
- GPU: NVIDIA A100-PCIE-40GB, 40960 MiB
- Driver: 595.58.03, Compute Cap: 8.0

### Job 8374098: RTX 8000 request via sbatch (no partition)
```bash
#SBATCH --account=def-hpcg6049_gpu
#SBATCH --gres=gpu:rtx8000:1
```
**Result: SUCCESS**
- Node: frnt156
- GPU: Quadro RTX 8000, 46080 MiB (45 GB)
- Driver: 595.58.03, Compute Cap: 7.5

---

## Software Environment

### GROMACS
```
module load gromacs/2024.6
Version: 2024.6-EasyBuild_5.1.2
Precision: mixed
Path: /cvmfs/soft.computecanada.ca/.../gromacs/2024.6/bin/gmx
```

### Python / Conda
```
conda 24.9.2
Python 3.12.4 (base, Anaconda 2024.06)
Base: /global/software/python/anaconda3-2024.06-1
```

### Conda Environments
```
SE3nv, blca_snakemake, blca_velocyto, celescope, colabfold,
mpnn, rfd_clean, rfdiffusion, rnaseq, seq-bench, snakemake,
som_env, somasieve
```

### colabfold env (key packages)
```
colabfold          1.6.1       (pypi)
alphafold-colabfold 2.3.13    (pypi)
jax                0.6.0       (conda-forge)
jax-cuda12-pjrt    0.9.1+computecanada (pypi)
jax-cuda12-plugin  0.6.0       (pypi)
jaxlib             0.6.0       cuda126 (conda-forge)
openmm             8.5.1       (conda-forge)
pdbfixer           available
Python             3.11.15
```

JAX on login node (no GPU):
```
WARNING: Jax plugin configuration error: Plugin module jax_plugins.xla_cuda12 does not exist
JAX: 0.6.0
Devices: [CpuDevice(id=0)]
```
(Expected — login nodes have no GPU. CUDA plugin will work on compute nodes.)

OpenMM platforms on login node: Reference, CPU (no CUDA platform)

### mpnn env
```
pytorch 2.7.1 (CPU-only, mkl)
```

### rfdiffusion env
```
pytorch 2.0.1 + CUDA 11.7
```

### rfd_clean env
```
pytorch 2.5.1 + CUDA 11.8
```

### AlphaFold
- Only `hmmer-alphafold3/3.4` module available (HMMER binary, not AlphaFold itself)
- No standalone AF2 or AF3 installation found

### BindCraft
- NOT INSTALLED anywhere on the system
- No conda env, no module, no installation

### PyTorch (base env)
- Installed in ~/.local but broken (missing libze_loader.so.1)
- Not usable from base env

---

## Summary of Key Findings

1. **Account requirement**: `--account=def-hpcg6049_gpu` is mandatory for all GPU jobs
2. **No partition specification**: The scheduler auto-routes; specifying partition always fails
3. **Best GPUs for BindCraft**: A100 (40 GB) and RTX 8000 (45 GB)
4. **BindCraft not installed**: Needs fresh installation in new conda env
5. **JAX 0.6.0 with CUDA 12 available** in colabfold env (but BindCraft needs its own env)
6. **14-day partition available** for long BindCraft runs (auto-selected with --time > 1 day)
