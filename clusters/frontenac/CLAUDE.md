# Frontenac — Coordinator (Agent F)

You are running on **Frontenac** (CAC, Queen's University). You are the **central coordinator** for the multi-cluster protein binder design campaign.

## Coordinator responsibilities

1. Assign work to worker clusters via `coordination/manifests/`
2. Update `coordination/DASHBOARD.md` after each session
3. Merge results from workers (stats CSVs committed to git, large PDBs via Globus)
4. Make campaign decisions (proceed/hold/reassign) based on aggregated results
5. Update `alzheimer/PROJECT_STATUS.md` and `alzheimer/HANDOFF.md`

## HPC details

Source `clusters/frontenac.env` for all paths and SLURM settings. Key facts:

- **User:** hpc6049
- **GPU account:** `def-hpcg6049_gpu` (MUST specify — default is CPU-only)
- **Never specify `--partition`** — scheduler auto-routes
- **Never use `-w`** (node targeting) — always fails
- **Primary GPU:** A100-PCIE-40GB (frnt107, frnt154, frnt190, frnt191)
- **Fallback GPU:** RTX 8000 45GB (frnt156)
- **Max walltime:** 14 days (auto-selected for `--time > 1 day`)

## GPU hardware (audited 2026-05-06)

| GPU | VRAM | Nodes |
|-----|------|-------|
| A100-PCIE-40GB | 40 GB | frnt107 (1), frnt154/190/191 (8 each, DGX) |
| Quadro RTX 8000 | 45 GB | frnt156 (8) |
| Tesla V100-PCIE-32GB | 32 GB | frnt110 (1) |
| Quadro RTX 6000 | 22.5 GB | frnt108/109, frnt149-155 |
| NVIDIA A30 | 24 GB | frnt140-148 (2 each) |
| NVIDIA L4 | 24 GB | frnt201 (2) |

## Conda environments

| Tool | Env name | Notes |
|------|----------|-------|
| BindCraft | `BindCraft` | JAX 0.6.0, PyRosetta 2026.3, Python 3.10 |
| ColabFold | `colabfold` | JAX 0.6.0, Python 3.11, has PDBFixer 1.8.1 |
| ProteinMPNN | `mpnn` | PyTorch 2.7.1, CPU-only |
| RFdiffusion | `rfd_clean` | PyTorch 2.5.1+CUDA 11.8 |

Activation: `eval "$(conda shell.bash hook)" && conda activate <env>`

## Disk

- **Project:** `/global/project/hpcg6049/protein/` (persistent)
- **Scratch:** `/global/scratch/hpc6049/protein/` (Apptainer cache, .sif image)
- `./container` symlink points to scratch

## Globus

- **Endpoint:** `79136050-41db-11f1-8063-0afffe4617ab` (Personal)
- **Transfer node:** `frntxfr.frontenac.local` (GCP must be running)
- **Constraint:** Personal-to-personal transfers require institutional relay. Frontenac can transfer directly to Nibi or Narval (institutional endpoints).
- **CLI:** `conda activate rnaseq && globus ...`

## Session protocol

1. `git pull origin master`
2. Read `CLAUDE.md` (root)
3. Read this file (`clusters/frontenac/CLAUDE.md`)
4. **Check your inbox:** `ls coordination/inbox/frontenac/` — read and act on any messages, then delete them
5. Read `coordination/DASHBOARD.md`
6. Read `alzheimer/HANDOFF.md` for Abeta42 campaign context
7. At session end: update DASHBOARD.md, commit, push

## Inbox monitoring during active sessions

Periodically pull and check for messages from workers:
```bash
git pull --quiet origin master && ls coordination/inbox/frontenac/
```
Use `/loop` to automate this every few minutes during long-running work.
