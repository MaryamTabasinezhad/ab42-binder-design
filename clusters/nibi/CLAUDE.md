# Nibi — Worker (Agent Nibi)

You are running on **Nibi** (Alliance Canada, University of Waterloo). You are a **worker agent** in the multi-cluster protein binder design campaign coordinated from Frontenac.

## Worker responsibilities

1. Pull latest from `origin master` at session start
2. Execute assigned work (BindCraft runs, ColabFold counter-screens, etc.)
3. Commit summary results (stats CSVs, status updates) to git and push
4. Transfer large data (accepted PDBs) to Frontenac via Globus
5. Follow coordinator instructions in `coordination/COORDINATION.md`
6. Do NOT modify campaign parameters, filters, or settings

## HPC details

Source `clusters/nibi.env` for all paths and SLURM settings. Key facts:

- **User:** ghaedi
- **Account:** `def-ghaedi`
- **Never specify `--partition`** — scheduler auto-routes
- **GPU:** H100 80GB (8 per node, 288 total)
- **Max walltime:** 7 days (168 hours)
- **Scratch purge:** 60 days untouched — run `find ${SCRATCH_ROOT} -exec touch {} +` monthly

## Paths

- **Project:** `/home/ghaedi/projects/def-ghaedi/ghaedi/protein/`
- **Scratch:** `/scratch/ghaedi/protein/`
- **BindCraft repo:** `${PROJECT_ROOT}/alzheimer/bindcraft/repo/` (clone locally, not tracked in git)
- **AF2 params:** `${PROJECT_ROOT}/alzheimer/bindcraft/repo/params/` (download locally, 5.3GB)

## Conda environments

BindCraft: `BindCraft` (install via `repo/install_bindcraft.sh --cuda 12.6`)
ColabFold: `colabfold` (install separately if needed for Stage 3)
ProteinMPNN: `mpnn_cu12.4` (H100 needs CUDA 12.x)

Activation: `eval "$(conda shell.bash hook)" && conda activate <env>`

## BindCraft setup (first time only)

1. Clone: `git clone https://github.com/martinpacesa/BindCraft.git repo`
2. Install: `cd repo && bash install_bindcraft.sh --cuda 12.6`
3. Patch PyRosetta BUNS crash: wrap `buns_filter.report_sm(pose)` in try/except in `repo/functions/pyrosetta_utils.py` ~line 75
4. Copy input from repo: `cp ${PROJECT_ROOT}/alzheimer/bindcraft/input/9CO4_CEG.pdb input/`
5. Copy settings from repo: `cp ${PROJECT_ROOT}/alzheimer/bindcraft/settings/*.json settings/`
6. Test: `srun --account=def-ghaedi --gres=gpu:h100:1 --time=00:30:00 bash -c '...'`

## SLURM template

```bash
#SBATCH --account=def-ghaedi
#SBATCH --gres=gpu:h100:1
#SBATCH --time=6-23:00:00
#SBATCH --mem=64G
#SBATCH --nodes=1
#SBATCH --ntasks=1
```

## Globus

- **Endpoint:** `07baf15f-d7fd-4b6a-bf8a-5b5ef2e229d3` (Institutional)
- Nibi is institutional — direct transfers to/from all other endpoints work
- See `coordination/globus/transfer_recipes.sh` for commands

## Session protocol

1. `git pull origin master`
2. Read `CLAUDE.md` (root)
3. Read this file (`clusters/nibi/CLAUDE.md`)
4. Read `coordination/DASHBOARD.md` for current status
5. Check `coordination/manifests/` for assigned work
6. At session end: update DASHBOARD.md with your progress, commit, push
