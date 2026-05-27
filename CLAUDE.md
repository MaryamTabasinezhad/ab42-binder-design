# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **de novo bispecific miniprotein binder design pipeline** targeting Abeta-42 (Alzheimer's) and TfR1 (blood-brain barrier transcytosis), running across multiple SLURM-managed HPC clusters. The primary campaign uses BindCraft; the fallback pipeline uses RFdiffusion, ProteinMPNN, and ColabFold.

This is **not** a conventional software project — it has no build system, no tests, and no package. It is a collection of SLURM batch scripts, Python analysis utilities, and coordination documents that orchestrate computational protein design across Frontenac, Nibi, and Narval clusters.

**GitHub repo:** `git@github.com:MaryamTabasinezhad/ab42-binder-design.git`

---

## Multi-Cluster Coordination Protocol

### Your identity

Detect your cluster from hostname and read the matching CLAUDE.md:
- `*frontenac*` or `frnt*` → **Frontenac (Coordinator)** — read `clusters/frontenac/CLAUDE.md`
- `*nibi*` → **Nibi (Worker)** — read `clusters/nibi/CLAUDE.md`
- `*narval*` → **Narval (Worker)** — read `clusters/narval/CLAUDE.md`

Source cluster-specific paths and SLURM settings from `clusters/<cluster>.env`.

### Session start protocol (ALL CLUSTERS)

1. `git pull origin master` — get latest coordination state
2. Read this file (`CLAUDE.md`)
3. Read `clusters/<your-cluster>/CLAUDE.md` for cluster-specific details
4. Read `coordination/DASHBOARD.md` for campaign status across all clusters
5. Read `coordination/COORDINATION.md` for campaign parameters and rules
6. For Abeta-42 campaign details: read `alzheimer/HANDOFF.md` and `alzheimer/DEVELOPMENT_PLAN.md`

### Session end protocol

1. Update `coordination/DASHBOARD.md` with your progress
2. Commit with `[<cluster>] <message>` prefix
3. `git push origin master`

### Communication rules

- This repo IS the communication channel — no Globus sync for messaging
- Globus is for large data only (PDBs, archives) — see `coordination/globus/`
- Work assignments are in `coordination/manifests/`
- Campaign parameters and agent registry are in `coordination/COORDINATION.md`
- Current status dashboard is in `coordination/DASHBOARD.md`

---

## The pipeline

The full philosophy and strategy live in `docs/De_Novo_Protein_Binder_Design_Framework.md`. Two pipelines are available:

### Primary: BindCraft (Abeta-42 campaign)
```
BindCraft (AF2-backprop binder design, GPU)
   → accepted PDBs + final_design_stats.csv
   → negative counter-screen (ColabFold vs 7 counter-targets)
   → stability filtering → ranking → experimental validation
```
Full development plan: `alzheimer/DEVELOPMENT_PLAN.md`

### Fallback: RFdiffusion pipeline (TfR1 campaign, or if BindCraft fails)
```
RFdiffusion (backbone gen, GPU, Apptainer)
   → output PDBs
   → rank/filter (rfdiffusion_test/output/new_ranked.py) → top100_pdbs/
   → ProteinMPNN (sequence design, GPU/CPU, conda)
   → output FASTAs in mpnn_fastas/
   → ColabFold (complex structure prediction, GPU, conda)
   → collect ipTM/pTM/pLDDT, filter
```

The post-MPNN → ColabFold half is documented in `post_mpnn/post_mpnn_colabfold_workflow.md`.

## Environments and tooling

Environment names vary by cluster. Source `clusters/<cluster>.env` for the correct names. The table below shows common defaults:

| Tool | How it's run | Default env |
|---|---|---|
| BindCraft | conda on GPU | `BindCraft` |
| RFdiffusion | Apptainer image on GPU | `rfd_clean` (Frontenac only) |
| ProteinMPNN | conda | `mpnn` (use `mpnn_cu12.4` on H100s) |
| ColabFold | conda on GPU | `colabfold` |

Conda activation in scripts: `eval "$(conda shell.bash hook)" && conda activate <env>`

## Two ProteinMPNN checkouts — they are different

This is a footgun. There are **two** ProteinMPNN directories (gitignored — clone locally on each cluster):

- `ProteinMPNN/` (capital P) — the **original Dauparas repo**. Used by all active SLURM scripts. Entry point: `protein_mpnn_run.py`.
- `proteinmpnn/` (lowercase) — the **Kuhlman Lab fork**, different CLI. Currently unused.

When in doubt, use `ProteinMPNN/` to match the existing pipeline.

## Common SLURM patterns

All compute jobs are submitted via `sbatch`. Key rules that apply on ALL clusters:

- **Never specify `--partition`** — all clusters auto-route
- Always use the cluster's GPU account from `clusters/<cluster>.env`
- Always use absolute paths
- Always `set -eo pipefail`
- Log to `logs/` with `%j` job-ID interpolation

Reference scripts: `scripts/tfr1set6.sh` (RFdiffusion), `scripts/prmpnn.sh` (ProteinMPNN), `scripts/run_colabfold_MSA.sh` (ColabFold), `alzheimer/bindcraft/scripts/run_bindcraft.sh` (BindCraft).

## Hotspot residue numbering gotcha

In RFdiffusion binder-design output, the **target chain numbering is shifted by the binder length** (binder is chain A starting at 1, target follows). The ranking script `rfdiffusion_test/output/new_ranked.py` handles this with `dynamic_hotspots = {length + h for h in BASE_HOTSPOTS}` — preserve that pattern when writing similar analysis tools.

## What's NOT in this repo (gitignored, install locally)

- `ProteinMPNN/` and `proteinmpnn/` — clone from GitHub on each cluster
- `alzheimer/bindcraft/repo/` — clone BindCraft + download AF2 params (5.3GB) on each cluster
- `container` — Apptainer .sif image (Frontenac only, on scratch)
- Design PDB outputs — `alzheimer/bindcraft/designs/Accepted/` etc. (transfer via Globus)
- No tests, linter, or formatter configured
- Dependencies live in conda envs and the Apptainer image
