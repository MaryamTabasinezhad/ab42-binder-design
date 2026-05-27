# Campaign Dashboard

**Last updated:** 2026-05-27 by Agent Narval

## Active Campaign: Abeta-42 BindCraft Binder Design

### Development Plan Stage: **Stage 2 COMPLETE, Stage 3 PENDING**

Full development plan: `alzheimer/DEVELOPMENT_PLAN.md`

### Cluster Status

| Cluster | Agent | Current Stage | SLURM Jobs | Trajectories | Accepted Designs | Last Update |
|---------|-------|---------------|------------|--------------|------------------|-------------|
| Frontenac | F | Stage 2 complete | (none running) | 1,342 | 62 (38 scaffolds) | 2026-05-26 |
| Nibi | Nibi | Setup pending | — | 0 | 0 | — |
| Narval | Narval | Stage 3 running | 61679472_[0-7] | — | — | 2026-05-27 |

### Combined Metrics

| Metric | Value |
|--------|-------|
| Total trajectories | 1,342 (Frontenac only) |
| Total MPNN designs evaluated | 2,977 |
| Total accepted designs | 62 |
| Unique scaffolds | 38 |
| Acceptance rate (MPNN) | 2.1% |
| Acceptance rate (trajectory) | 5.3% |
| Campaign champion | s453481_mpnn1 (i_pTM=0.85, dG=-102.5) |

### Stage 3 Plan: Negative Counter-Screen

**Status:** Narval ready — ColabFold installed, inputs prepared, SLURM script ready, pending job submission

The counter-screen tests all accepted designs against 8 targets (1 positive re-confirmation + 7 negative):
- **Positive:** 9CO4 (pae_interaction < 10)
- **Negative (all 7 must have pae_interaction > 15):** 9CKI, 9CK6, 7Q4B, 7Q4M, 6SHS, 1IYT, Abeta40 monomer

**Estimated compute:** 62 designs x 8 targets = 496 ColabFold runs, ~5 min each = ~41 GPU-hours

**Work split (TBD):** Manifests will be created in `coordination/manifests/` to divide runs across clusters.

### Recent Actions

| Date | Agent | Action |
|------|-------|--------|
| 2026-05-27 | Narval | Submitted Stage 3 counter-screen: job 61679472 (array 0-7, 62 designs x 8 targets). ColabFold 1.6.1, JAX 0.9.1, single_sequence mode, multimer_v3. |
| 2026-05-26 | F | Confirmed Stage 2 complete: 62 designs, 38 scaffolds. Generated 62-design analysis report. |
| 2026-05-26 | F | Set up GitHub repo and multi-cluster coordination infrastructure. |
| 2026-05-20 | F | Prepared Nibi sync package (not yet deployed). |
| 2026-05-08 | F | Generated design report, accepted models info, binder considerations PDFs. |
| 2026-05-06 | F | Submitted BindCraft main job 8375335 (A100, 14-day). |

### Scratch Touch Schedule (Alliance clusters)

| Cluster | Last touched | Next due |
|---------|-------------|----------|
| Nibi | N/A (not set up) | After setup |
| Narval | 2026-05-27 | 2026-06-27 |
