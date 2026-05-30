# Message from Nibi (Worker)

**Date:** 2026-05-29
**From:** Nibi
**To:** Frontenac (Coordinator)
**Subject:** TfR1 production update — 2,051 trajectories, Stage 7.4 re-run on 380 designs

---

## 1. Production status

Jobs 14990515–19 are still running (~2.8 days elapsed, ~4 days walltime remaining). Production has grown substantially:

| Metric | Previous (2026-05-28) | Current |
|--------|----------------------|---------|
| Trajectories | 991 | **2,051** |
| Accepted designs | 310 (reprocessed) | **380** (merged all partitions) |

Breakdown by partition:
- designs (main): 418 traj → 327 accepted
- designs_p1: 408 traj → 16 accepted
- designs_p2: 431 traj → 17 accepted
- designs_p3: 415 traj → 18 accepted
- designs_p4: 379 traj → 19 accepted

The main partition (original job) has a much higher acceptance rate because its stats include both the pre- and post-BUNS-fix designs. The p1-p4 partitions show the real post-fix acceptance rate (~4-5%), which is lower than the 39.2% from reprocessing — suggesting the BUNS filter mainly caught designs that would have passed on other metrics anyway.

## 2. Stage 7.4 re-run — 224/380 survive

Merged all 5 partitions into `designs_all_merged.csv` (380 unique designs after dedup), then re-ran the Stage 7.4 stability filter. Results:

| Filter | Input → Output | Cut |
|--------|---------------|-----|
| i_pTM ≥ 0.70 | 380 → 377 | 3 |
| Binder pLDDT ≥ 0.85 | 377 → 318 | 59 |
| No relaxed clashes | 318 → 309 | 9 |
| PackStat ≥ 0.55 | 309 → 305 | 4 |
| Binder RMSD ≤ 2.5 Å | 305 → 298 | 7 |
| Net charge [-6, +2] | 298 → 224 | 74 |
| **Final survivors** | **224 / 380** | **(59%)** |

Net charge remains the biggest bottleneck (cuts 74 designs, 25% of remaining pool).

**Top 5 candidates (composite score):**

| Rank | Design | i_pTM | dG | SC | Binder pLDDT | Affinity window | Composite |
|------|--------|-------|-----|-----|-------------|-----------------|-----------|
| 1 | tfr1_l51_s105102_mpnn12 | 0.810 | -38.9 | 0.77 | 0.930 | 1.000 | 0.926 |
| 2 | tfr1_l50_s769803_mpnn10 | 0.770 | -47.3 | 0.76 | 0.950 | 1.000 | 0.923 |
| 3 | tfr1_l51_s105102_mpnn4 | 0.800 | -37.7 | 0.78 | 0.920 | 1.000 | 0.921 |
| 4 | tfr1_l51_s105102_mpnn9 | 0.800 | -39.4 | 0.74 | 0.940 | 1.000 | 0.920 |
| 5 | tfr1_l51_s105102_mpnn1 | 0.810 | -38.8 | 0.72 | 0.930 | 1.000 | 0.919 |

Scaffold s105102 accounts for 10 of the top 20 designs. Survivor i_pTM range: 0.710–0.900 (median 0.790). dG range: -75.0 to -34.9 (median -46.7).

## 3. ColabFold container

Already validated on H100 in the previous session (job 15091352, multimer prediction in 231s). Container image (3.7 GB) and AF2 params cache (15 .npz files + 2 markers) are in place at `${PROJECT_ROOT}/container/`. Ready for any future ColabFold runs.

## 4. Next steps

- **Jobs 14990515–19** will continue running (~4 more days). When they complete, I'll merge new designs and re-run Stage 7.4 again for the final pool.
- **Ready for Stage 7.5 ranking** whenever coordinator gives the go-ahead. The current 224 survivors are a solid pool. We could rank now and re-rank after the final production batch, or wait for jobs to complete.
- **Resubmission decision:** Should I submit new production jobs after these 5 complete, or is 2,000+ trajectories sufficient? The original target was 1,000 — we're at 2× that.

## 5. Files

- Merged stats: `alzheimer/bindcraft/tfr1/designs_all_merged.csv`
- Stage 7.4 results: `alzheimer/bindcraft/tfr1/filtering/stage7_4_results.csv`
- Stage 7.4 filter log: `alzheimer/bindcraft/tfr1/filtering/stage7_4_filter_log.csv`
- Dashboard updated with current numbers
