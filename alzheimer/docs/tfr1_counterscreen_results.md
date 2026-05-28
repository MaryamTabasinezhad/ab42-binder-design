# Stage 7.3 TfR1 Counter-Screen Results

**Date:** 2026-05-28
**Agent:** Nibi
**Job:** 15068061 (array 0-2), all COMPLETED

## Summary

**0/310 designs pass all 3 criteria.** This is the same systematic method failure seen in Narval's Aβ42 Stage 3 counter-screen.

## Results by filter

| Filter | Target | Criterion | Pass |
|--------|--------|-----------|------|
| Positive (re-confirmation) | 6WRV (TfR1) | pae_interaction < 10 | **0/310** |
| TfR2 selectivity | TfR2 apical | pae_interaction > 15 | 310/310 |
| Tf competition | 1SUV (TfR1+Tf) | pae_interaction < 12 | **0/310** |
| **All 3** | | | **0/310** |

## PAE interaction distributions

| Target | Min | Median | Mean | Max |
|--------|-----|--------|------|-----|
| 6WRV_positive | 12.56 | 30.38 | 30.23 | 31.06 |
| TfR2_negative | 24.82 | 27.26 | 27.24 | 29.18 |
| 1SUV_Tf_competition | 29.65 | 30.84 | 30.84 | 31.18 |

## ipTM distributions

| Target | Min | Median | Mean | Max |
|--------|-----|--------|------|-----|
| 6WRV_positive | 0.14 | 0.16 | 0.16 | **0.76** |
| TfR2_negative | 0.07 | 0.11 | 0.15 | **0.73** |
| 1SUV_Tf_competition | 0.14 | 0.15 | 0.15 | 0.18 |

## Notable outlier

**tfr1_l59_s344619_mpnn13** stands out:
- 6WRV positive: pae=12.56, ipTM=0.76 (best by far — next best pae is 23.01)
- TfR2 negative: pae=26.52 (safely above 15)
- 1SUV Tf competition: pae=30.57 (fails — same as all others)

This design nearly passes the positive control (12.56 vs threshold 10) and has the highest ipTM (0.76 vs median 0.16). The Tf competition failure is shared with all 310 designs.

## Interpretation

1. **Positive control (6WRV):** 309/310 designs have pae > 29, ipTM ~0.16–0.18. One outlier (s344619_mpnn13) shows real signal (pae=12.56, ipTM=0.76). ColabFold single_sequence *can* detect binding for this target, but nearly all designs fail.

2. **TfR2 selectivity:** All 310 pass (pae > 24). However, since the positive control also mostly fails with high pae values, this "selectivity" is likely artifactual — the method produces high pae for everything.

3. **Tf competition (1SUV):** Uniformly high pae (29.6–31.2) with no outliers. This is a much larger complex (binder + TfR1 + Tf N-lobe + Tf C-lobe ≈ 1,400+ residues). ColabFold single_sequence clearly cannot handle this complex size.

## Comparison to Narval Aβ42 Stage 3

| Metric | Aβ42 (Narval) | TfR1 (Nibi) |
|--------|---------------|-------------|
| Designs screened | 62 | 310 |
| Pass positive | 0/62 | 0/310 (but 1 outlier near threshold) |
| Pass negative(s) | 62/62 | 310/310 |
| pae_positive range | 19–23 | 12.6–31.1 |
| ipTM_positive range | 0.13–0.19 | 0.14–0.76 |
| Signal detected? | No | **Partial** — 1 design shows real signal |

Key difference: TfR1 is a globular target, not a fibril. ColabFold single_sequence does show *some* ability to distinguish binding (the s344619_mpnn13 outlier), whereas on the Aβ42 fibril target it produced zero signal. However, the method is still insufficient as a reliable screen.

## Recommendations for coordinator

1. **Tf competition test is not viable with single_sequence mode.** The 4-chain complex is too large. Consider: (a) drop this test entirely (structural analysis already confirms no Tf overlap), or (b) use MSA mode, or (c) use a different validation method.

2. **Positive control shows partial signal for TfR1** (unlike Aβ42). Consider whether to:
   - Lower the pae threshold (e.g., < 15 instead of < 10) to capture borderline binders
   - Use MSA mode for better predictions
   - Accept BindCraft's internal metrics (i_pTM, pAE, dG) as the primary filter and skip the ColabFold counter-screen for TfR1

3. **s344619_mpnn13 is worth noting** as a potential lead even if it doesn't formally pass.

## Result files

- Detail: `alzheimer/bindcraft/tfr1/filtering/stage7_3_results.csv`
- Summary: `alzheimer/bindcraft/tfr1/filtering/stage7_3_summary.csv`
