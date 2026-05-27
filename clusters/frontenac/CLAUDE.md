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
5. **Start inbox watcher:** `nohup bash coordination/scripts/inbox_watcher.sh &`
6. Read `coordination/DASHBOARD.md`
7. Read `alzheimer/HANDOFF.md` for Abeta42 campaign context
8. At session end: run the **session-end checklist** below, commit, push

## Session-end checklist (MANDATORY)

Before ending ANY session that changes project state, update ALL THREE status files:

1. **`coordination/DASHBOARD.md`** — cluster table (stage, jobs, trajectories, accepted designs), combined metrics, recent actions log
2. **`alzheimer/PROJECT_STATUS.md`** — stage statuses (not_started → in_progress → completed), key metrics, decision log
3. **`alzheimer/HANDOFF.md`** — Section 2 status checklist (move items between completed/in-progress/not-started), add new decisions to Section 3, new warnings to Section 4, new files to Section 5

These three files are the coordination backbone. If a worker commits progress (new job, results, status change), Frontenac must propagate that change to all three files in the same session. Do NOT defer updates to the next session — stale status files cause workers to make wrong decisions.

## Inbox monitoring

Start the inbox watcher at the beginning of every session:
```bash
nohup bash coordination/scripts/inbox_watcher.sh &
```
This pulls git every 2 minutes and logs new messages to `coordination/inbox/frontenac/.watcher.log`.

Check the log for new messages:
```bash
tail -20 coordination/inbox/frontenac/.watcher.log
```

Stop when session ends: `kill $(cat /tmp/inbox_watcher_frontenac.pid)`
