# Campaign Dashboard

**Last updated:** 2026-05-27 by Agent Nibi (counter-screen fix + resubmit)

## Active Campaigns

### 1. Abeta-42 BindCraft Binder Design

**Development Plan Stage: Stage 2 COMPLETE, Stage 3 IN PROGRESS**

Full development plan: `alzheimer/DEVELOPMENT_PLAN.md`

### 2. TfR1 Arm Design (Stage 7, parallel)

**Status: IN PROGRESS on Nibi**

Full plan: `alzheimer/docs/STAGE7_TFR1_PLAN.md`

### Cluster Status

| Cluster | Agent | Current Work | SLURM Jobs | Trajectories | Accepted Designs | Last Update |
|---------|-------|--------------|------------|--------------|------------------|-------------|
| Frontenac | F | Coordinator, Stage 2 complete | (none running) | 1,342 (Aβ42) | 62 (38 scaffolds) | 2026-05-27 |
| Nibi | Nibi | Stage 7 TfR1 production + Stage 7.3 counter-screen resubmitted | 14990515–19 (running), 15063803_[0-2] (pending) | 991 (TfR1) | 310 (reprocessed) | 2026-05-27 |
| Narval | Narval | Stage 3 counter-screen | 61679472_[0-7] | — | — | 2026-05-27 |

### Aβ42 Campaign Metrics

| Metric | Value |
|--------|-------|
| Total trajectories | 1,342 (Frontenac) |
| Total MPNN designs evaluated | 2,977 |
| Total accepted designs | 62 |
| Unique scaffolds | 38 |
| Acceptance rate (MPNN) | 2.1% |
| Acceptance rate (trajectory) | 5.3% |
| Campaign champion | s453481_mpnn1 (i_pTM=0.85, dG=-102.5) |

### TfR1 Campaign Metrics (Nibi)

| Metric | Value |
|--------|-------|
| Target | 6WRV apical domain (chains A+B), hotspots 208/210/211/212/215 |
| Binder size | 50–70 residues |
| Trajectories completed | 991 |
| MPNN designs evaluated | 791 |
| Accepted designs | **310** (reprocessed with BUNS filter disabled, 39.2% of MPNN) |
| Top candidate | tfr1_l59_s917497_mpnn2 (i_pTM=0.85, dG=-47.8, SC=0.78) |
| Parallel jobs | 5 resubmitted (14990515–19), continuing toward 1,000 |
| Tf competition check | PASS (hotspots 45+ Å from Tf interface) |
| BUNS fix | Option 1 applied: filter disabled, pyrosetta patch 999→0 |
| **Stage 7.3** | Counter-screen resubmitted: job 15063803 (array 0-2). Previous job 14992093 failed (missing tensorflow). Patched colabfold/batch.py. 310 designs × 3 targets |

### Stage 3 Plan: Negative Counter-Screen

**Status:** Running on Narval — job 61679472 submitted

The counter-screen tests all accepted designs against 8 targets (1 positive re-confirmation + 7 negative):
- **Positive:** 9CO4 (pae_interaction < 10)
- **Negative (all 7 must have pae_interaction > 15):** 9CKI, 9CK6, 7Q4B, 7Q4M, 6SHS, 1IYT, Abeta40 monomer

**Estimated compute:** 62 designs x 8 targets = 496 ColabFold runs, ~5 min each = ~41 GPU-hours

**Work split (TBD):** Manifests will be created in `coordination/manifests/` to divide runs across clusters.

### Recent Actions

| Date | Agent | Action |
|------|-------|--------|
| 2026-05-27 | Nibi | Stage 7.3 counter-screen RESUBMITTED: job 15063803 (array 0-2). Previous job 14992093 failed — ColabFold 1.6.1 crashed on `import tensorflow` (not installed). Patched batch.py to handle missing TF gracefully. |
| 2026-05-27 | Nibi | Stage 7.3 counter-screen submitted: job 14992093 (array 0-2). 310 designs × 3 targets. ColabFold 1.6.1, JAX 0.9.1, single_sequence mode. TfR2 from AlphaFold (Q9UP52 v6, apical domain res 163-424). Tf competition via 1SUV (chains A+C+E). |
| 2026-05-27 | F | Tasked Nibi with Stage 7.3 counter-screen: 310 designs × 3 targets (TfR1 positive, TfR2 selectivity, Tf compatibility). |
| 2026-05-27 | F | Approved BUNS fix Option 1. Decided TfR1 counter-screen targets: TfR2 (selectivity) + Tf competition (compatibility). 2 negatives sufficient for globular target. |
| 2026-05-27 | Nibi | BUNS fix applied: disabled BUNS filter → 310 accepted from 791 MPNN (39.2%). Patched pyrosetta_utils.py (999→0). Resubmitted 5 jobs (14990515–19). |
| 2026-05-27 | Nibi | TfR1 progress report: 991 traj, 791 MPNN, 0 accepted (BUNS crash root cause). Report: `alzheimer/docs/tfr1_progress_report.md` |
| 2026-05-27 | F | Integrated Nibi's TfR1 work into dashboard and status files. |
| 2026-05-27 | Nibi | Joined repo: pushed TfR1 campaign (29 files). Started inbox watcher. |
| 2026-05-27 | Narval | Submitted Aβ42 Stage 3 counter-screen: job 61679472 (array 0-7, 62 designs × 8 targets). |
| 2026-05-27 | F | Added inbox watcher script, session-end checklist. |
| 2026-05-26 | F | Stage 2 complete: 62 designs, 38 scaffolds. Set up GitHub repo + multi-cluster coordination. |
| 2026-05-06 | F | Submitted BindCraft main job 8375335 (A100, 14-day). |

### Scratch Touch Schedule (Alliance clusters)

| Cluster | Last touched | Next due |
|---------|-------------|----------|
| Nibi | 2026-05-27 | 2026-06-27 |
| Narval | 2026-05-27 | 2026-06-27 |
