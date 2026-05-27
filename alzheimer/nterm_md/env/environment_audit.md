# Environment Audit — Frontenac (CAC, Queen's)

Date: 2026-05-06
User: hpc6049 (qaedi65@gmail.com)
Host: login2.frontenac.local
Working dir: /global/project/hpcg6049/protein/alzheimer

## 1. System / mounts

```
USER=hpc6049
HOME=/global/home/hpc6049
SCRATCH=/scratch/hpc6049
SHELL=/bin/bash
```

`/global` mounts present and relevant to this work:

| Mount | Purpose |
|---|---|
| `/global/home`     | User home, small quota |
| `/global/project`  | Persistent group project space (this work lives here) |
| `/global/scratch`  | Large/ephemeral storage (existing protein design pipeline uses `hpc6049/protein/`) |
| `/global/software` | System anaconda3-2024.06-1 (the default `python`) |
| `/cvmfs/soft.computecanada.ca` | Compute Canada module tree (gromacs, openmm, etc.) |

## 2. GROMACS

`module avail gromacs` returns the full chemistry tree (all MPI-dependent avx2):

```
gromacs/2016.6  gromacs/2023.3  gromacs/2023.5  gromacs/2024.1
gromacs/2024.4  gromacs/2024.6  gromacs/2025.4  gromacs/2026.1 (D)

gromacs-plumed/2020.7  gromacs-plumed/2023.5
gromacs-ramd/2024.1-RAMD-2.1
gromacs-swaxs/2021.7-0.5.1
```

`module load gromacs/2024.6` succeeded. `gmx --version` reports:

```
GROMACS version:    2024.6-EasyBuild_5.1.2
Precision:          mixed
MPI library:        thread_mpi
OpenMP support:     enabled (max 128 threads)
GPU support:        disabled
SIMD:               AVX2_256
CPU FFT:            fftw-3.3.10
Executable:         /cvmfs/.../gromacs/2024.6/bin/gmx
```

This is a CPU-only build, which is fine for energy minimization. The 2024.6 module is loadable, contains all the standard `gmx` tools, and ships with the default amber99sb-ildn force field via the GMXLIB pointer.

## 3. ColabFold

- No `colabfold_batch` on default PATH.
- No `module avail colabfold`.
- **However**, conda env `colabfold` exists at `~/.conda/envs/colabfold` and contains `colabfold_batch` at `/global/home/hpc6049/.conda/envs/colabfold/bin/colabfold_batch`.

Activation:

```bash
eval "$(conda shell.bash hook)"
conda activate colabfold
```

ColabFold is **not used in this prep prompt** — flagged here for the future MD/design phase.

## 4. SLURM partitions (sinfo -s)

```
PARTITION         AVAIL TIMELIMIT      NODES (A/I/O/T)
cpubase_interac   up    6:00:00        12/0/0/12
cpubase_6hrs      up    6:00:00        71/11/1/83
cpubase_24hrs     up    1-00:00:00     57/2/0/59
cpubase_14days    up    14-00:00:00    54/0/0/54
gpubase_interac   up    6:00:00        6/0/0/6
gpubase_6hrs      up    6:00:00        21/3/0/24
gpubase_24hrs     up    1-00:00:00     14/0/0/14
gpubase_14days    up    14-00:00:00    10/0/0/10
gpu-L4            up    6:00:00        1/0/0/1
cpularge_24hrs    up    1-00:00:00     2/5/0/7
cpularge_14days   up    14-00:00:00    2/5/0/7
teaching          up    1-00:00:00     4/4/0/8
```

Energy minimization in this prompt will run on the login node (small system, < 30 min). Future MD goes to `gpubase_*` (or `cpubase_*` for short setup steps).

## 5. Disk

`df -h /global/project/hpcg6049/`:

```
Filesystem      Size  Used Avail Use% Mounted on
global          3.4P  2.2P  1.2P  66% /global
```

`diskusage_report` is broken on this login node (TypeError in CC's wrapper). The shared `global` filesystem has ~1.2 PB free, so we are not space-constrained for setup files. Per-user quota is not retrievable here; if a future job hits a quota error, we will revisit.

## 6. Modelling tools

| Tool        | Available?            | Source                                             |
|-------------|-----------------------|----------------------------------------------------|
| **PDBFixer**| ✅ (after install)    | Compute Canada wheelhouse `pdbfixer-1.8.1+computecanada` in `colabfold` env |
| **OpenMM**  | ✅ 8.5.1 in conda env | `~/.conda/envs/colabfold` (also `module avail openmm` shows 8.0.0 / 8.1.1 / 8.2.0) |
| **biopython** | ✅ 1.84             | `colabfold` env. Also 1.81 in `mpnn` env. |
| **Modeller** | ❌                   | not on PATH, no module                             |
| **MDAnalysis** | ❌                  | not installed in any env                           |
| **mdtraj**  | ❌                    | not installed in any env                           |
| **ProDy**   | ❌                    | not installed                                      |
| **pdb2pqr** | ❌                    | not on PATH                                        |
| **GROMACS** | ✅ via module         | gromacs/2024.6 (will be used for EM)               |

### Install notes

PDBFixer 1.8.1 from the CC wheelhouse imports `pkg_resources`, which was dropped from `setuptools >= 81`. The colabfold env originally had setuptools 82.0.1, which broke PDBFixer with `ModuleNotFoundError: No module named 'pkg_resources'`. Resolved by:

```bash
pip install "setuptools<81"   # pinned at 80.10.2+computecanada
```

PDBFixer now imports cleanly (modulo a deprecation warning that does not affect functionality). This pin is required for the `colabfold` env going forward.

If a future need for MDAnalysis/mdtraj arises, both are pip-installable into the `colabfold` env.

## 7. Python

Default `python`: `/global/software/python/anaconda3-2024.06-1/bin/python` (Python 3.12.4). Has `numpy 1.26.4`, `pandas 2.2.2`, but no biopython/openmm.

Conda envs (relevant subset):

| Env         | Python | Notes                                                  |
|-------------|--------|--------------------------------------------------------|
| `colabfold` | 3.11.15 | **Primary env for this prep work** — has openmm, pdbfixer, biopython, colabfold_batch |
| `mpnn`      | (mixed) | ProteinMPNN — biopython 1.81, no openmm                |
| `rfdiffusion`, `rfd_clean`, `SE3nv` | — | for RFdiffusion; not needed here  |

## Tooling decisions for this run

1. **Structure work (chain extraction + N-terminus addition)**: Python in `colabfold` env (biopython 1.84 + pdbfixer 1.8.1 + openmm 8.5.1).
2. **Energy minimization**: `gromacs/2024.6` module on the login node, force field **amber99sb-ildn** (well-validated for IDPs and shipped with GROMACS), TIP3P water for the prep step.
3. **Diagnostics**: biopython + numpy in colabfold env (no MDAnalysis needed for the computations specified).
4. **No ColabFold, no GPU, no MD** in this prompt.

## Missing / deferred

- Modeller — not available; not needed because PDBFixer worked.
- MDAnalysis / mdtraj — not installed; not needed for this prompt's diagnostics.
- diskusage_report quota query is broken on the CC side — not blocking.
