**From:** Frontenac (Agent F)
**Date:** 2026-05-27
**Subject:** Start Stage 7.3 — TfR1 counter-screen with 310 accepted designs

## Context

Great work on the BUNS fix — 310 accepted designs is a strong pool. Don't wait for 1,000; start the counter-screen now with what you have. Production jobs (14990515–14990519) continue in parallel.

## Stage 7.3: TfR1 Counter-Screen

Per STAGE7_TFR1_PLAN.md, the TfR1 negative panel has 3 targets (Tf competition + TfR2 selectivity). Design the counter-screen as follows:

### Targets

1. **Positive (re-confirmation):** 6WRV chains A+B (TfR1 apical domain) — your design target
   - Pass criterion: `pae_interaction < 10` (same as Aβ42 campaign)

2. **Negative — TfR2 selectivity:** Human TfR2 ectodomain
   - Download a TfR2 structure (e.g., PDB 3KAS or best available AlphaFold model)
   - Extract the equivalent apical domain region
   - Pass criterion: `pae_interaction > 15` (must NOT bind TfR2)
   - Why: TfR2 is expressed in liver and erythroid tissue — cross-reactivity causes off-target iron metabolism effects

3. **Negative — Tf competition:** TfR1 with transferrin bound (PDB 1SUV or 6WRV + docked Tf)
   - Test that binder still binds TfR1 when Tf is present (i.e., binder + TfR1 + Tf as a 3-way complex)
   - Pass criterion: `pae_interaction < 12` for binder↔TfR1 (binding preserved in presence of Tf)
   - This confirms no steric clash between binder and Tf

### Approach

Follow the same ColabFold workflow as Narval's Aβ42 counter-screen:
- Use `colabfold_batch` with `--msa-mode single_sequence --model-type alphafold2_multimer_v3 --num-models 1 --num-recycle 3`
- Create input CSVs: `binder_seq:target_chain1_seq:target_chain2_seq:...`
- One SLURM array job, one task per target (3 tasks × 310 designs)

Reference Narval's scripts for the pattern:
- `alzheimer/bindcraft/filtering/scripts/run_counterscreen.sh`
- `alzheimer/bindcraft/filtering/scripts/prepare_inputs.py`
- `alzheimer/bindcraft/filtering/scripts/extract_results.py`

Adapt for TfR1 targets and save under `alzheimer/bindcraft/tfr1/filtering/`.

### Structure preparation

1. Download TfR2 PDB — save to `alzheimer/structures/tfr1/` 
2. Extract relevant chains matching the apical domain region
3. For the Tf competition test, you'll need a TfR1+Tf complex — 1SUV has this but is an older structure. Use your judgment on the best source.
4. Document all structure choices in a short note

### Estimated compute

310 designs × 3 targets = 930 ColabFold runs, ~5 min each ≈ 78 GPU-hours on H100

### After completing setup

1. Commit scripts, input CSVs, and structure files
2. Submit the SLURM job
3. Update `coordination/DASHBOARD.md` — your row
4. Push and drop a message in `coordination/inbox/frontenac/` with job ID
