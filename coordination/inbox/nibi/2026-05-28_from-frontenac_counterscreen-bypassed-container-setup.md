**From:** Frontenac (Agent F)
**Date:** 2026-05-28
**Subject:** Counter-screen BYPASSED — container shipped — next steps

## 1. PI Decision: Skip counter-screen for both arms

ColabFold single_sequence multimer_v3 forward prediction is a **method failure** for validating de novo binders — zero discriminatory signal on both Abeta-42 (0/62) and TfR1 (0/310). This is NOT a design failure.

**Decision:** Trust BindCraft's internal AF2 backpropagation metrics (i_pTM, dG, pAE, SC) as primary quality filters. Skip computational counter-screen. Selectivity will be validated experimentally via SPR.

**Your outlier s344619_mpnn13 (ipTM=0.76)** is flagged as a lead candidate regardless.

## 2. ColabFold Container — set up on Nibi

We've containerized ColabFold for cross-cluster reproducibility. The container image and AF2 params cache are being transferred to you via Globus.

**After Globus transfer completes**, verify the files landed at:
```
${PROJECT_ROOT}/container/colabfold_1.6.1-cuda12.sif  (3.7 GB)
${PROJECT_ROOT}/container/colabfold_cache/params/      (4.9 GB, 16 .npz + 2 .txt markers)
```

Then test:
```bash
# Option A: Use the setup script (will detect existing files)
bash container/setup_colabfold_container.sh

# Option B: Quick manual test on a GPU node
source clusters/nibi.env
module load ${APPTAINER_MODULE}
srun --account=${SLURM_ACCOUNT} --gres=${GPU_GRES} --time=00:15:00 --mem=32G \
  bash container/run_colabfold.sh /path/to/test_input.csv /path/to/output/ \
  --num-models 1 --num-recycle 1 --msa-mode single_sequence
```

**Key Apptainer flags already handled by the wrapper:**
- `--nv --no-home` (GPU + isolate from ~/.local Python packages)
- `-B <workdir>:/work` (don't use deep host paths inside container)
- `-B <cache>:/cache/colabfold` (AF2 params)

**Cluster env file updated** — pull latest `clusters/nibi.env` for `COLABFOLD_SIF`, `COLABFOLD_CACHE`, `APPTAINER_MODULE` vars.

## 3. Next steps for Nibi

1. **Continue TfR1 production** (jobs 14990515-19) toward 1,000 trajectories
2. **When ready:** Start Stage 7.4 stability filtering on the 310 accepted designs using BindCraft metrics. Filters per `DEVELOPMENT_PLAN.md` Stage 4 + affinity-window filter (pae_interaction sweet-spot 8-12).
3. **Use containerized ColabFold** for any future ColabFold runs (monomer fold checks in Stage 7.4, etc.)

## 4. Documentation

Update your `clusters/nibi/CLAUDE.md` to note:
- ColabFold now runs via container, not conda env
- Wrapper script: `container/run_colabfold.sh`
- The conda `colabfold` env is deprecated for production use
