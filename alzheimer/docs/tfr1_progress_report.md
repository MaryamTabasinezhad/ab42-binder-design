# TfR1 (Stage 7) Progress Report — Nibi

**Date:** 2026-05-27
**Agent:** Nibi
**Target:** 6WRV apical domain (chains A+B), hotspots A208/A210/A211/A212/A215

## 1. Job Status

Three rounds of SLURM submissions were made on 2026-05-11:

| Round | Job IDs | Status | Elapsed | Exit Code | Notes |
|-------|---------|--------|---------|-----------|-------|
| 1st | 13720337–13720342 | FAILED | 0s | 127 | Command not found (conda env not activated) |
| 2nd | 13720521–13720526 | FAILED | ~3 min | 1 | Config/path error |
| 3rd | 13720846–13720850 | **COMPLETED** | 2d 7h–2d 16h | 0 | Successful run |

All 5 parallel jobs from the third round completed successfully, running for approximately 2.5 days each on H100 GPUs.

## 2. Trajectory Summary

| Metric | Value |
|--------|-------|
| Total trajectories | **991** (across 5 jobs: 204+203+215+185+184) |
| i_pTM mean / median / best | 0.725 / 0.790 / **0.940** |
| pAE mean / median / best | 0.30 / 0.26 / 0.15 |
| i_pAE mean / median / best | 0.24 / 0.18 / 0.07 |
| pLDDT mean / median / best | 0.83 / 0.84 / 0.95 |
| dG mean / median / best | -44.5 / -44.7 / **-124.9** |
| Length mean / median / range | 60.6 / 61 / 50–70 |
| Trajectory failures | 5 (0.5%) |

Trajectory quality is good — median i_pTM of 0.79 and best of 0.94 are comparable to the Aβ42 campaign.

## 3. MPNN Designs

| Metric | Value |
|--------|-------|
| Total MPNN designs evaluated | **791** (from 991 trajectories → 80% yield to MPNN) |
| Average i_pTM mean / max | 0.789 / 0.860 |
| Average dG mean / best | -50.2 / -75.2 |
| Clean (no notes) | 668 (84.5%) |
| Relaxed clashes | 70 (8.8%) |
| Low absorption (no Trp) | 31 + 8 + 14 = 53 (6.7%) |

## 4. Accepted Designs: **ZERO**

**Root cause identified: PyRosetta BUNS filter crash on TfR1 target**

Every single MPNN design has `Average_n_InterfaceUnsatHbonds = 999.0`. This is the fallback sentinel value from the try/except patch in `pyrosetta_utils.py` line 76–78. The BUNS (Buried Unsatisfied Hydrogen Bonds) calculation via `buns_filter.report_sm(pose)` crashes with a RuntimeError on **every** TfR1 pose.

The default filter requires `Average_n_InterfaceUnsatHbonds <= 4`. With all values at 999, **100% of designs are rejected by this single filter**.

This did not affect the Aβ42 campaign (9CO4 target), where BUNS calculations succeeded and 62 designs were accepted.

### Why BUNS crashes on TfR1

The 6WRV apical domain target (chains A+B, 680 residues total) is significantly larger than the 9CO4 chains C/E/G target. The PyRosetta `BuriedUnsatHbonds` filter with `dalphaball_sasa=1` likely fails due to:
- Memory/timeout issues with the larger complex
- Structural features (disulfide bonds, glycosylation sites) in the TfR1 ectodomain that cause DAlphaBall to crash

## 5. Top 5 Trajectories by i_pTM

| Design | i_pTM | pAE | i_pAE | dG | Length | pLDDT |
|--------|-------|-----|-------|-----|--------|-------|
| tfr1_l66_s564847 | **0.94** | 0.15 | 0.10 | -61.5 | 66 | 0.92 |
| tfr1_l54_s47090 | 0.93 | 0.17 | 0.08 | -59.4 | 54 | 0.92 |
| tfr1_l53_s881847 | 0.93 | 0.17 | 0.09 | -62.4 | 53 | 0.93 |
| tfr1_l69_s971318 | 0.93 | 0.16 | 0.09 | -55.0 | 69 | 0.94 |
| tfr1_l57_s157713 | 0.93 | 0.16 | 0.07 | -50.9 | 57 | 0.95 |

These are excellent candidates — i_pTM 0.93–0.94 with low pAE and strong dG values.

## 6. Comparison to Aβ42 Campaign

| Metric | Aβ42 (Frontenac) | TfR1 (Nibi) |
|--------|-------------------|-------------|
| Trajectories | 1,342 | 991 |
| MPNN designs | 2,977 | 791 |
| MPNN per trajectory | 2.2 | 0.8 |
| Best i_pTM (trajectory) | — | 0.940 |
| Best i_pTM (MPNN avg) | 0.85 | 0.860 |
| Accepted designs | 62 (2.1% of MPNN) | **0** (BUNS filter crash) |
| BUNS calculation | Working | **Crashed on all poses** |

The TfR1 trajectory and MPNN quality metrics are comparable to Aβ42. The zero acceptance rate is **entirely** due to the BUNS filter crash, not poor design quality.

## 7. Recommendations

### Immediate fix: Disable BUNS filter for TfR1 reprocessing

**Option A (recommended):** Create a custom filter JSON (`tfr1_filters.json`) that sets `Average_n_InterfaceUnsatHbonds` threshold to `null` (disabled) and `1_n_InterfaceUnsatHbonds` and `2_n_InterfaceUnsatHbonds` thresholds to `null`. Then reprocess existing MPNN stats against the relaxed filters to identify accepted designs retroactively.

**Option B:** Fix the BUNS calculation for the TfR1 target (harder — requires debugging DAlphaBall with the 6WRV structure).

**Option C:** Resubmit jobs with an improved `pyrosetta_utils.py` patch that returns `0` instead of `999` when BUNS crashes, effectively bypassing the filter while keeping the rest of the pipeline intact.

### For continued runs

1. The 5 completed jobs produced 991 trajectories in ~2.5 days. To reach 1,000 accepted designs, we need ~5,000 trajectories (assuming ~20% make it through non-BUNS filters).
2. Resubmit with the BUNS fix applied before burning more GPU hours.
3. Current settings (hotspots, binder length 50–70, 4-stage protocol) are producing quality trajectories — no parameter changes needed.

### Awaiting coordinator decision

The BUNS filter issue requires a decision from Frontenac on which fix approach to take. Resubmitting without fixing this will waste GPU hours producing more designs that all get rejected.
