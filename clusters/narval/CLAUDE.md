# Narval — Worker (Agent Narval)

You are running on **Narval** (Alliance Canada, ETS Montreal). You are a **worker agent** in the multi-cluster protein binder design campaign coordinated from Frontenac.

## Worker responsibilities

1. Pull latest from `origin master` at session start
2. Execute assigned work (BindCraft runs, ColabFold counter-screens, etc.)
3. Commit summary results (stats CSVs, status updates) to git and push
4. Transfer large data (accepted PDBs) to Frontenac via Globus
5. Follow coordinator instructions in `coordination/COORDINATION.md`
6. Do NOT modify campaign parameters, filters, or settings

## HPC details

Source `clusters/narval.env` for all paths and SLURM settings. Key facts:

- **User:** ghaedi
- **Account:** `def-ghaedi`
- **Never specify `--partition`** — scheduler auto-routes
- **GPU:** A100 40GB (4 per node)
- **Max walltime:** 7 days standard, 28 days available for long jobs
- **Scratch purge:** 60 days untouched — run `find ${SCRATCH_ROOT} -exec touch {} +` monthly

## Paths

- **Project:** `/home/ghaedi/projects/def-ghaedi/ghaedi/protein/`
- **Scratch:** `/scratch/ghaedi/protein/`
- **BindCraft repo:** `${PROJECT_ROOT}/alzheimer/bindcraft/repo/` (clone locally)
- **AF2 params:** `${PROJECT_ROOT}/alzheimer/bindcraft/repo/params/` (download locally, 5.3GB)

## ColabFold container (preferred over conda)

ColabFold now runs via Apptainer container for cross-cluster reproducibility:
- **SIF:** `/home/ghaedi/projects/def-ghaedi/ghaedi/protein/container/colabfold_1.6.1-cuda12.sif` (3.7 GB)
- **Cache:** `/home/ghaedi/projects/def-ghaedi/ghaedi/protein/container/colabfold_cache/`
- **Wrapper:** `container/run_colabfold.sh` (in `protein/` repo root)
- **Setup:** `container/setup_colabfold_container.sh`
- Verified on Narval (2026-05-28): container present, 15 .npz param files, both markers
- Key flags: `--nv --no-home`, bind work to `/work`, bind cache to `/cache/colabfold`

## Conda environments

BindCraft: `BindCraft` (install via `repo/install_bindcraft.sh --cuda 12.4`)
ColabFold: `colabfold` (legacy — use container instead)
ProteinMPNN: `mpnn`

Activation: `eval "$(conda shell.bash hook)" && conda activate <env>`

## Narval-specific gotcha

**`module load scipy-stack` is required** for numpy/scipy/pandas on Narval. Base Python has no scientific packages, and `conda` is not on the default PATH. Always `module load scipy-stack` before running analysis scripts.

## BindCraft setup (first time only)

Same as Nibi setup (see `clusters/nibi/CLAUDE.md`) but use `--cuda 12.4` for A100s.

## SLURM template

```bash
#SBATCH --account=def-ghaedi
#SBATCH --gres=gpu:a100:1
#SBATCH --time=6-23:00:00
#SBATCH --mem=64G
#SBATCH --nodes=1
#SBATCH --ntasks=1
```

## Globus

- **Endpoint:** `a1713da6-098f-40e6-b3aa-034efe8b6e5b` (Institutional)
- Narval is institutional — direct transfers to/from all other endpoints work
- See `coordination/globus/transfer_recipes.sh` for commands

## Session protocol

1. `git pull origin master`
2. Read `CLAUDE.md` (root)
3. Read this file (`clusters/narval/CLAUDE.md`)
4. Read `coordination/DASHBOARD.md` for current status
5. **Check your inbox:** `ls coordination/inbox/narval/` — read and act on any messages, then delete them
6. **Start inbox watcher:** `nohup bash coordination/scripts/inbox_watcher.sh &`
7. Check `coordination/manifests/` for assigned work
8. At session end: update DASHBOARD.md with your progress, commit, push

## Inbox monitoring

Start the inbox watcher at the beginning of every session:
```bash
nohup bash coordination/scripts/inbox_watcher.sh &
```
This pulls git every 2 minutes and logs new messages to `coordination/inbox/narval/.watcher.log`.

Check the log for new messages:
```bash
tail -20 coordination/inbox/narval/.watcher.log
```

Stop when session ends: `kill $(cat /tmp/inbox_watcher_narval.pid)`
