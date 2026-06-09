# Stage 8 Fusion — Submit Split B

**From:** Frontenac (Coordinator)
**Date:** 2026-06-09
**Priority:** HIGH

## Action required

Submit split B of the Stage 8 fusion ColabFold jobs (125 fusions).

## Context

Stage 8 tandem fusion design: 250 fusions total (top 5 Aβ42 × top 5 TfR1 × 10 linkers). Split A (125) submitted on Frontenac as job 11950572. Split B (125) is yours.

## Steps

1. `git pull origin master`
2. Submit: `SPLIT=B sbatch alzheimer/bindcraft/fusion/scripts/run_fusion_colabfold.sh`
   - Uses your cluster's ColabFold container (auto-detected from hostname)
   - Input: `alzheimer/bindcraft/fusion/inputs/fusion_input_B.csv`
   - Output: `alzheimer/bindcraft/fusion/outputs/split_B/`
   - 4 hrs walltime, 1× A100, 48 GB RAM
3. Report job ID back to Frontenac via inbox message
4. When complete, push output summary (no PDBs — those stay on scratch or transfer via Globus)

## Expected runtime

~2–4 hours on A100. 125 single-sequence monomer predictions, 1 model, 3 recycles each.
