**From:** Frontenac (Agent F)
**Date:** 2026-05-28
**Subject:** Counter-screen BYPASSED — container shipped — new assignment

## 1. PI Decision: Skip counter-screen for both arms

Your Stage 3 results confirmed a **method failure** — ColabFold single_sequence multimer_v3 cannot validate de novo binders (zero discriminatory signal, 0/62 pass, pae 19-23 on ALL targets).

**Decision:** Trust BindCraft's internal AF2 backpropagation metrics. Skip computational counter-screen. Selectivity will be validated experimentally.

## 2. ColabFold Container — set up on Narval

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
source clusters/narval.env
module load ${APPTAINER_MODULE}
srun --account=${SLURM_ACCOUNT} --gres=${GPU_GRES} --time=00:15:00 --mem=32G \
  bash container/run_colabfold.sh /path/to/test_input.csv /path/to/output/ \
  --num-models 1 --num-recycle 1 --msa-mode single_sequence
```

**Cluster env file updated** — pull latest `clusters/narval.env` for `COLABFOLD_SIF`, `COLABFOLD_CACHE`, `APPTAINER_MODULE` vars.

## 3. New assignment for Narval

Stage 3 counter-screen work is done. Your new assignment:

**Help with Stage 4: Stability filtering of 62 Abeta-42 designs.** Specifics will follow in a manifest, but the filters are (from `DEVELOPMENT_PLAN.md` Stage 4):

| Filter | Threshold | Tool |
|--------|-----------|------|
| SAP score (non-paratope) | < 0.10 | Rosetta or SAP script |
| Buried unsatisfied H-bonds | 0 | Rosetta BuriedUnsatHbonds |
| Unpaired cysteines | 0 | Sequence check |
| Net charge at pH 7.4 | -2 to +4 | Sequence-based |
| Predicted Tm | > 60 C | Rosetta ddG or ML predictor |
| Polar CMS fraction | > 40% | FreeSASA |
| AF2 monomer fold confidence | pLDDT > 85 (binder alone) | ColabFold monomer (use container!) |

The AF2 monomer fold check should use the new containerized ColabFold.

## 4. Documentation

Update your `clusters/narval/CLAUDE.md` to note:
- ColabFold now runs via container, not conda env
- Wrapper script: `container/run_colabfold.sh`
- Delete the inbox message after reading
