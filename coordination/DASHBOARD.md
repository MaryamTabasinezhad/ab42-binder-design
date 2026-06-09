# Campaign Dashboard

**Last updated:** 2026-06-09 by Narval — **Stage 8 RUNNING on both clusters.** Split A on Frontenac (job 11950572), Split B on Narval (job 62652492).

## Active Campaigns

### 1. Abeta-42 BindCraft Binder Design

**Development Plan Stage: Stage 5 COMPLETE — 23 designs ranked across 18 scaffolds. Top: s967366_mpnn11 (score=0.793). Ready for Stage 8 fusion.**

Full development plan: `alzheimer/DEVELOPMENT_PLAN.md`

### 2. TfR1 Arm Design (Stage 7, parallel)

**Status: Stage 7.5 COMPLETE — Top 50 ranked from 224 survivors across 27 scaffolds. Production winding down. Ready for Stage 8.**

Full plan: `alzheimer/docs/STAGE7_TFR1_PLAN.md`

### Cluster Status

| Cluster | Agent | Current Work | SLURM Jobs | Trajectories | Accepted Designs | Last Update |
|---------|-------|--------------|------------|--------------|------------------|-------------|
| Frontenac | F | **Stage 8 RUNNING.** Split A submitted (job 11950572, 125 fusions, A100, 4h). | 11950572 (pending/running) | 1,342 (Aβ42) | 62 → 23 ranked | 2026-06-09 |
| Nibi | Nibi | **Stage 7.5 COMPLETE** — Top 50 ranked (27 scaffolds). Jobs 14990515–19 likely finished. | (check status) | 2,051 (TfR1) | 380 → 224 → top 50 | 2026-05-29 |
| Narval | Narval | **Stage 8 RUNNING.** Split B submitted (job 62652492, 125 fusions, A100, 4h). | 62652492 (pending) | 1,342 (Aβ42) | 62 → 26 (Phase A+B) | 2026-06-09 |

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
| Trajectories completed | 2,051 |
| Accepted designs | **380** (all partitions merged, deduplicated) |
| Stage 7.4 survivors | **224/380** (59% pass rate) |
| **Stage 7.5 fusion panel** | **Top 50** from 224, max 5/scaffold, 27 scaffolds represented |
| Top candidate (post-7.5) | tfr1_l60_s766452_mpnn12 (i_pTM=0.85, dG=-58.8, SC=0.69, score=0.678) |
| Parallel jobs | 14990515–19 finishing (~4d left), no resubmission |
| Tf competition check | PASS (hotspots 45+ Å from Tf interface) |
| BUNS fix | Option 1 applied: filter disabled, pyrosetta patch 999→0 |
| **Stage 7.3** | **COMPLETE:** 0/310 pass all 3 criteria. Same method failure as Aβ42 Stage 3. 1 outlier (s344619_mpnn13, pae=12.56, ipTM=0.76). Tf competition test not viable (complex too large). Report: `alzheimer/docs/tfr1_counterscreen_results.md` |

### Stage 3 Results: Negative Counter-Screen

**Status:** COMPLETE on Narval — job 61679472 finished 2026-05-27 03:10

**Result: GATE 1 FAIL — 0 of 62 designs pass the positive control**

All 496 ColabFold runs (62 designs × 8 targets) completed successfully. Results:

| Filter | Criterion | Pass count |
|--------|-----------|------------|
| Positive (9CO4) | pae_interaction < 10 | **0/62** (min=19.34, median=21.42) |
| Negative (all 7) | pae_interaction > 15 | 62/62 |
| **Both** | | **0/62** |

**Critical observation:** pae_interaction values are uniformly high (19-23) across ALL targets — positive and negative alike. ipTM is 0.13-0.19 for all predictions. ColabFold single_sequence multimer_v3 produced essentially random predictions for every design against every target. This is a **systematic method failure**, not a selectivity signal.

**Likely causes:**
1. Single-sequence mode has zero evolutionary signal for both the de novo binder and the short Ab42 chains
2. ColabFold multimer_v3 forward prediction may be fundamentally unable to validate BindCraft-designed interactions against fibril targets
3. The 34-residue Ab42 chain trimer is an unusual target geometry for AF2 multimer

**Result files:** `alzheimer/bindcraft/filtering/stage3_results.csv`, `stage3_summary.csv`

**PI Decision (2026-05-28):** Counter-screen BYPASSED for both arms. ColabFold single_sequence forward prediction is a method failure for de novo binders, not a design failure. Trust BindCraft internal AF2 backpropagation metrics. Proceed to stability filtering. Selectivity will be validated experimentally via SPR.

### Recent Actions

| Date | Agent | Action |
|------|-------|--------|
| 2026-06-09 | F | **Stage 8 LAUNCHED:** Split A submitted on Frontenac as job 11950572 (125 fusions, A100, 4h walltime, single_sequence, 1 model, 3 recycles). Split B (125 fusions) assigned to Narval via inbox. |
| 2026-05-29 | Nibi | **Stage 7.5 COMPLETE:** Ranked 224 TfR1 survivors → selected top 50 for fusion panel. 27 scaffolds represented (max 5/scaffold cap applied — 7 designs skipped). Weights: i_pTM 0.25, dG 0.20, Binder_pLDDT 0.15, SC 0.15, diversity bonus 0.15, PackStat 0.10. Top: s766452_mpnn12 (i_pTM=0.85, dG=-58.8). No new production jobs — will re-rank if final batch adds >5 survivors. Results: `stage7_5_ranked.csv`. |
| 2026-05-29 | F | **Stage 4 Phase C recalibrated (Option B):** SAP/res<1.1, BUNS≤7, charge [-8,+5]. 23/62 pass. 12 confirmed (have Phase B pLDDT), 11 extra recovered by charge widening need monomer pLDDT — job 9877164 submitted on Frontenac A100. Script updated, results in `stage4_results_recalibrated.csv`. |
| 2026-05-30 | Narval | **Stage 4 Phase B COMPLETE:** 26/26 pass monomer pLDDT >85 (mean 92.80, min 88.00, max 97.12). Results: `filtering/stage4/phase_b_results.csv`. Reply sent to Frontenac. All 26 designs ready for Phase C. |
| 2026-05-29 | Nibi | **Stage 7.4 RE-RUN on full pool:** Production grew to 2,051 trajectories, 380 accepted designs (merged all 5 partitions). Re-ran Stage 7.4 stability filter: 224/380 survive (up from 191/326). Top scaffold s105102 still dominates (10 of top 20). ColabFold container validated (already done last session). Jobs 14990515–19 running with ~4d remaining. |
| 2026-05-29 | F | Coordinator session: confirmed Phase B job complete (Narval), sent inbox messages to Narval (extract Phase B results) and Nibi (continue production + container setup). Updated dashboard. Stage 4 filter recalibration discussion with PI in progress. |
| 2026-05-28 | Narval | **Stage 4 Phase A COMPLETE:** 26/62 Aβ42 designs pass sequence+CSV filters (Cys, charge [-5,+5], ss_pLDDT, binder_pLDDT). Net charge is sole bottleneck (mean -5.9). Phase B monomer pLDDT submitted as job 61936182 (ColabFold container, A100). Phase C (SAP, BUNS, CMS) deferred to Frontenac. |
| 2026-05-28 | Nibi | **Stage 7.4 COMPLETE:** 191/326 designs survive stability filtering. Top scaffold: s105102 (9 designs in top 20). Filters: i_pTM≥0.70, Binder_pLDDT≥0.85, SC≥0.55, PackStat≥0.55, RMSD≤2.5Å, dG≤-30, net charge [-6,+2], no Cys. Affinity-window ranking applied. Container validated on H100 (job 15091352, multimer prediction in 231s). |
| 2026-05-28 | F | **PI Decision: skip counter-screen for both arms.** ColabFold single_sequence method failure. Trust BindCraft metrics, proceed to Stage 4 (Aβ42) and Stage 7.4 (TfR1). |
| 2026-05-28 | F | **ColabFold containerized.** Apptainer image `colabfold_1.6.1-cuda12.sif` validated on Frontenac A100. Wrapper: `container/run_colabfold.sh`. Shipping to Nibi/Narval via Globus. Replaces conda-based ColabFold. |
| 2026-05-28 | Narval | **Stage 3 COMPLETE: GATE 1 FAIL.** Job 61679472 (array 0-7) all COMPLETED. 0/62 designs pass positive control (pae_interaction 19-23 on 9CO4, threshold <10). All 62 pass negatives. ColabFold single_sequence mode produced no signal on any target. Method validity in question. |
| 2026-05-28 | Nibi | **Stage 7.3 COMPLETE:** 0/310 pass all 3 criteria. ColabFold single_sequence method failure — same as Aβ42 Stage 3. 1 outlier with partial signal (s344619_mpnn13). Tf competition test not viable at this complex size. Report: `alzheimer/docs/tfr1_counterscreen_results.md` |
| 2026-05-28 | Nibi | Fixed ColabFold tensorflow dependency: installed tensorflow 2.19.1 from CC wheelhouse. Resubmitted counter-screen as job 15068061 (all 3 tasks COMPLETED). |
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
