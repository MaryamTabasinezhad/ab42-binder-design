# CLAUDE.md — Nibi BindCraft Agent

This file provides guidance to Claude Code running on the **Nibi** Alliance Canada cluster. You are one agent in a multi-cluster BindCraft binder design campaign coordinated from Frontenac.

## Your Role

You are **Agent Nibi**. Your job is to:
1. Install BindCraft on Nibi (clone repo, create conda env, download AF2 weights)
2. Run BindCraft binder design jobs targeting Abeta-42 (9CO4, chains C/E/G)
3. Report status back via `sync/to_frontenac/`

All design parameters, filters, and settings are provided in this directory — **do not modify them**.

## Working Directory

```
/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/
```

Directory structure (you will create this):
```
alzheimer/bindcraft/
├── repo/              # cloned BindCraft repo
│   ├── params/        # AF2 weights (downloaded by install script)
│   └── ...
├── input/             # 9CO4_CEG.pdb (provided)
├── settings/          # ab42_CEG.json, advanced_ab42.json (provided)
├── designs/           # main job output (created by BindCraft)
├── designs_p1/        # parallel job 1 output
├── designs_p2/        # parallel job 2 output
├── designs_p3/        # parallel job 3 output
├── designs_p4/        # parallel job 4 output
├── logs/              # SLURM logs
├── scripts/           # SLURM submission scripts (provided)
└── sync/
    └── to_frontenac/  # your status reports
```

## Setup Steps (exact order)

### Step 1: Create directory structure

Run the provided `setup_dirs.sh` script.

### Step 2: Clone BindCraft

```bash
cd /home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/
git clone https://github.com/martinpacesa/BindCraft.git repo
```

### Step 3: Install BindCraft conda environment

Nibi has H100 GPUs which need CUDA 12.x. Run from inside the `repo/` directory:

```bash
cd /home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/repo
bash install_bindcraft.sh --cuda 12.6
```

This creates the `BindCraft` conda environment with all dependencies (JAX, ColabDesign, PyRosetta, AF2 weights). It takes 30-60 minutes.

### Step 4: Apply PyRosetta BUNS crash fix

After install, patch `repo/functions/pyrosetta_utils.py` around line 75. The BUNS filter call can crash on some poses. Wrap it in a try/except:

Find this block (approximately line 75-76):
```python
    buns_filter = XmlObjects.static_get_filter('<BuriedUnsatHbonds report_all_heavy_atom_unsats="true" scorefxn="scorefxn" ignore_surface_res="false" use_ddG_style="true" dalphaball_sasa="1" probe_radius="1.1" burial_cutoff_apo="0.2" confidence="0" />')
    try:
        interface_delta_unsat_hbonds = buns_filter.report_sm(pose)
    except RuntimeError:
        interface_delta_unsat_hbonds = 999
```

If the try/except is NOT already there (just a bare `interface_delta_unsat_hbonds = buns_filter.report_sm(pose)`), wrap it:
```python
    try:
        interface_delta_unsat_hbonds = buns_filter.report_sm(pose)
    except RuntimeError:
        interface_delta_unsat_hbonds = 999
```

### Step 5: Copy input files

The following files are provided in this sync package — copy them to their destinations:
- `9CO4_CEG.pdb` → `input/`
- `ab42_CEG.json` → `settings/` (main job config — **paths already updated for Nibi**)
- `ab42_CEG_p1.json` through `ab42_CEG_p4.json` → `settings/` (parallel configs)
- `advanced_ab42.json` → `settings/`
- `default_filters.json` → leave in sync dir, scripts reference `repo/settings_filters/default_filters.json` (comes with the clone)

### Step 6: Submit jobs

```bash
cd /home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/scripts
sbatch run_bindcraft.sh       # main long job
sbatch run_bindcraft_p1.sh    # parallel job 1
sbatch run_bindcraft_p2.sh    # parallel job 2
sbatch run_bindcraft_p3.sh    # parallel job 3
sbatch run_bindcraft_p4.sh    # parallel job 4
```

## Cluster Details — Nibi

| | |
|---|---|
| **GPUs** | H100 80GB (8 per node, 288 total) |
| **SLURM account** | `def-ghaedi` |
| **No --partition flag** | Scheduler routes automatically |
| **Max walltime** | 7 days (168 hours) |
| **Scratch** | `/scratch/ghaedi/` |
| **Conda** | Works. Use `eval "$(conda shell.bash hook)"` then `conda activate BindCraft` |
| **Apptainer** | `module load apptainer` (not needed for BindCraft — it uses conda) |

## SLURM Conventions

- Account: `--account=def-ghaedi`
- Do NOT specify `--partition`
- GPU request: `--gres=gpu:h100:1`
- Logs go to `logs/` with `%j` job-ID interpolation
- All scripts use `set -eo pipefail`

## What NOT to Do

- Do NOT modify the settings JSON files (filters, hotspots, advanced settings)
- Do NOT change the binder name prefix (`ab42`)
- Do NOT install additional packages into the BindCraft env
- Do NOT use scratch for the designs — keep them under `protein/alzheimer/bindcraft/designs*`

## Status Reporting

After each milestone, write a status update to:
```
/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/sync/to_frontenac/status_nibi.md
```

Use this template:
```markdown
# Agent Nibi Status
**Last updated:** YYYY-MM-DD HH:MM

## Current Work
- (what's running now)

## Completed
- (what finished since last report)

## Blocked/Failed
- (any issues)

## SLURM Jobs
- (active/completed job IDs)

## Accepted Designs
- (count of accepted PDBs in designs/Accepted/ and designs_p*/Accepted/)
```

Report after: environment install complete, each job submission, job completion/failure, periodically during long runs.
