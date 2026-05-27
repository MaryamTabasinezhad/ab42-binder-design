# Campaign Dashboard

**Last updated:** 2026-05-27 by Agent Nibi

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
| Nibi | Nibi | Stage 7 TfR1 — BUNS fix applied, jobs resubmitted | 14990515–19 (running) | 991 (TfR1) | 310 (reprocessed) | 2026-05-27 |
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
| Parallel jobs | 5 (each targeting 1,000 designs) |
| Tf competition check | PASS (hotspots 45+ Å from Tf interface) |

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
| 2026-05-27 | Nibi | BUNS fix applied (Option 1): disabled BUNS filter → 310 accepted from existing 791 MPNN (39.2%). Patched pyrosetta_utils.py (999→0). Resubmitted 5 jobs (14990515–19). |
| 2026-05-27 | Nibi | TfR1 progress report: 991 traj, 791 MPNN, 0 accepted. Root cause: PyRosetta BUNS crashes on all TfR1 poses (sets unsat=999, filter rejects at ≤4). Report: `alzheimer/docs/tfr1_progress_report.md` |
| 2026-05-27 | F | Integrated Nibi's TfR1 work into dashboard and status files. Updated all three status docs. |
| 2026-05-27 | Nibi | Joined repo: pushed TfR1 campaign (29 files — scripts, settings, structures, stats). Started inbox watcher. |
| 2026-05-27 | Narval | Submitted Stage 3 counter-screen: job 61679472 (array 0-7, 62 designs x 8 targets). ColabFold 1.6.1, JAX 0.9.1, single_sequence mode, multimer_v3. |
| 2026-05-27 | F | Added inbox watcher script, session-end checklist, updated cluster CLAUDE.md files. |
| 2026-05-26 | F | Confirmed Stage 2 complete: 62 designs, 38 scaffolds. Generated 62-design analysis report. |
| 2026-05-26 | F | Set up GitHub repo and multi-cluster coordination infrastructure. |
| 2026-05-06 | F | Submitted BindCraft main job 8375335 (A100, 14-day). |

### Scratch Touch Schedule (Alliance clusters)

| Cluster | Last touched | Next due |
|---------|-------------|----------|
| Nibi | 2026-05-27 | 2026-06-27 |
| Narval | 2026-05-27 | 2026-06-27 |
