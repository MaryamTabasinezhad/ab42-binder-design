**From:** Nibi (Agent Nibi)
**Date:** 2026-05-28
**Subject:** Stage 7.3 TfR1 counter-screen COMPLETE — 0/310 pass, same method failure as Aβ42

## Results

Job 15068061 (array 0-2) all COMPLETED. Extracted results with `extract_results.py`.

**0/310 designs pass all 3 criteria.**

| Filter | Criterion | Pass | pae range |
|--------|-----------|------|-----------|
| Positive (6WRV) | pae < 10 | 0/310 | 12.6–31.1 |
| TfR2 selectivity | pae > 15 | 310/310 | 24.8–29.2 |
| Tf competition (1SUV) | pae < 12 | 0/310 | 29.7–31.2 |

## Key findings

1. **Same method failure as Narval Stage 3.** ColabFold single_sequence multimer_v3 produces uniformly high pae and low ipTM (~0.16) for nearly all designs on all targets.

2. **One outlier with real signal:** `tfr1_l59_s344619_mpnn13` — pae=12.56 (just above threshold 10), ipTM=0.76 on 6WRV positive. The next-best design has pae=23. This design shows ColabFold *can* detect TfR1 binding, unlike the Aβ42 fibril target where there was zero signal.

3. **Tf competition test is not viable.** The 4-chain complex (binder + TfR1 + Tf N-lobe + Tf C-lobe ≈ 1,400+ residues) is too large for single_sequence mode. Uniformly pae ~30 with no variation. The structural analysis already confirmed no Tf overlap (hotspots 45+ Å from Tf interface) — this test can likely be dropped.

## Recommendations (for coordinator decision)

1. **Drop the Tf competition test** — structural analysis is sufficient; ColabFold can't handle the complex size.
2. **Consider relaxing positive threshold** (e.g., pae < 15) to capture borderline binders, or use MSA mode for better predictions.
3. **Alternatively, trust BindCraft's internal metrics** (i_pTM, pAE, dG) as primary filters and skip ColabFold counter-screen for TfR1 — the globular target is simpler than the fibril and BindCraft's AF2 backprop already validates binding.
4. **s344619_mpnn13 is a lead candidate** worth flagging regardless of threshold decisions.

## Files

- Full report: `alzheimer/docs/tfr1_counterscreen_results.md`
- Detail CSV: `alzheimer/bindcraft/tfr1/filtering/stage7_3_results.csv`
- Summary CSV: `alzheimer/bindcraft/tfr1/filtering/stage7_3_summary.csv`

## Production status

Jobs 14990515–19 still running (~24h elapsed), continuing toward 1,000 trajectories.
