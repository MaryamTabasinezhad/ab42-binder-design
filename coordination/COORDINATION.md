# Multi-Cluster Coordination Protocol

**Last updated:** 2026-05-26
**Coordinator:** Frontenac (Agent F)

## Campaign

De novo bispecific miniprotein binder targeting **Abeta-42** (PDB 9CO4, chains C/E/G) and **TfR1** (Stage 7, parallel). Each cluster runs independent BindCraft trajectories or ColabFold counter-screens; results converge on Frontenac for combined analysis.

## Agent Registry

| Agent | Cluster | Working Dir | GPU | Status |
|-------|---------|-------------|-----|--------|
| **F** (Frontenac) | CAC Queen's | `/global/project/hpcg6049/protein/` | A100 40GB | Stage 2 COMPLETE — 62 accepted designs from 1,342 trajectories |
| **Nibi** | Alliance (Waterloo) | `/home/ghaedi/projects/def-ghaedi/ghaedi/protein/` | H100 80GB | Setup pending |
| **Narval** | Alliance (ETS Montreal) | `/home/ghaedi/projects/def-ghaedi/ghaedi/protein/` | A100 40GB | Not started |

## Design Parameters (IDENTICAL across all agents — do NOT modify)

- **Target PDB:** `alzheimer/bindcraft/input/9CO4_CEG.pdb` (chains C, E, G)
- **Hotspots:** C10,C11,C13,C14,C15,C16,E10,E11,E13,E14,E15,E16,G10,G11,G13,G14,G15,G16
- **Binder lengths:** 60-90 residues (sampled uniformly)
- **Binder name prefix:** `ab42`
- **Design algorithm:** 4stage
- **MPNN:** soluble weights, 20 seqs, fix interface, temp 0.1
- **Filters:** `default_filters.json` (from BindCraft repo)
- **Advanced settings:** `advanced_ab42.json` (identical copy on each cluster)
- **Omit AAs:** C (cysteine)

## Communication Protocol (git-pull workflow)

This repo is the single source of truth. Agents communicate via git, NOT Globus sync.

### How it works

1. **Coordinator (Frontenac)** pushes instructions, manifests, and status updates to `master`
2. **Workers** pull `master` at session start to get latest instructions
3. **Workers** commit their results (summary stats, status updates) and push to `master`
4. **Large data** (accepted PDBs, full trajectory archives) transfers via Globus
5. **Small data** (stats CSVs, status markdown, manifests) goes through git

### Commit message convention

Prefix all commits with the cluster name in brackets:
```
[frontenac] Update dashboard: Stage 2 complete with 62 designs
[nibi] Add Nibi accepted designs stats (14 designs, 200 trajectories)
[narval] Complete counter-screen batch 1 (designs 1-20 x 8 targets)
```

### Conflict avoidance

Each cluster modifies only its own section in `coordination/DASHBOARD.md` and its own manifest files. The coordinator modifies the overall status and makes campaign decisions.

## Work Assignment

Work is assigned via manifest files in `coordination/manifests/`. Each manifest is a TSV listing exactly which tasks belong to which cluster.

### Rules
1. Each task appears in exactly ONE manifest — no overlap
2. Workers process only their assigned manifest
3. Workers update their manifest status as tasks complete
4. Coordinator creates and distributes manifests

## Globus Data Transfer (large files only)

See `coordination/globus/endpoints.md` for endpoint IDs and `coordination/globus/transfer_recipes.sh` for reusable commands.

### What goes via Globus (NOT git)
- Accepted design PDBs (each ~100KB, but hundreds of them)
- Full trajectory archives
- AF2 model parameters (5.3GB, initial setup only)
- Reference databases (ColabFold, if needed)

### What goes via git
- Stats CSVs (final_design_stats.csv, trajectory_stats.csv)
- Status updates (DASHBOARD.md)
- Manifests
- Scripts, configs, docs

## SLURM Conventions

| | Frontenac | Nibi | Narval |
|---|---|---|---|
| Account | `def-hpcg6049_gpu` | `def-ghaedi` | `def-ghaedi` |
| GPU | A100 40GB | H100 80GB | A100 40GB |
| GPU request | `--gres=gpu:a100:1` | `--gres=gpu:h100:1` | `--gres=gpu:a100:1` |
| Max walltime | 14 days | 7 days | 7 days (28 available) |
| Main job time | `13-23:00:00` | `6-23:00:00` | `6-23:00:00` |
| Memory (main) | `64G` | `64G` | `64G` |
| Memory (parallel) | `48G` | `48G` | `48G` |
| Partition | (never specify) | (never specify) | (never specify) |

## Scratch Purge Warning (Alliance clusters)

Nibi and Narval purge scratch after **60 days** untouched. Workers must periodically touch their working directories:
```bash
find ${SCRATCH_ROOT} -exec touch {} +
```
Run this monthly or after any long idle period.

## Rules for All Agents

1. Use ONLY the provided settings, filters, and advanced config — no modifications
2. Use repo-provided scripts; adapt only cluster-specific paths via env files
3. Do NOT delete accepted designs
4. Log all SLURM job IDs in DASHBOARD.md
5. Pull before starting work; push after completing work
6. Ask coordinator (via git commit message or DASHBOARD.md note) before changing anything
7. All scripts use `set -eo pipefail`
8. All SLURM scripts use absolute paths

## Design Naming

All designs use the `ab42` prefix. BindCraft appends length, seed, MPNN sequence number, and model number automatically (e.g., `ab42_l79_s120913_mpnn1_model2`). Since seeds are random, name collisions between clusters are astronomically unlikely.

## Convergence

When campaigns complete, all accepted PDBs and `final_design_stats.csv` from each cluster are collected on Frontenac. The coordinator:
1. Transfers PDBs via Globus to a per-cluster directory (e.g., `combined_analysis/nibi_accepted/`)
2. Concatenates stats CSVs (skip duplicate headers)
3. Verifies no name collisions: `cut -d, -f2 combined_stats.csv | sort | uniq -d`
4. Runs combined ranking and analysis
