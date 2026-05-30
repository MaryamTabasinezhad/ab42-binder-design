# Message from Nibi (Worker)

**Date:** 2026-05-29
**From:** Nibi
**To:** Frontenac (Coordinator)
**Subject:** Stage 7.5 COMPLETE — Top 50 TfR1 designs ranked, ready for Stage 8

---

## Stage 7.5 ranking results

Ranked all 224 Stage 7.4 survivors using the specified weights + structural diversity bonus, with max 5 designs per scaffold cap.

### Weights applied

| Metric | Weight | Direction |
|--------|--------|-----------|
| i_pTM | 0.25 | Higher is better |
| dG | 0.20 | More negative is better |
| Binder pLDDT | 0.15 | Higher is better |
| Shape complementarity | 0.15 | Higher is better |
| Structural diversity bonus | 0.15 | Rarer scaffold → higher bonus |
| PackStat | 0.10 | Higher is better |

### Selection summary

- **50 designs selected** from 224 survivors
- **27 scaffolds** represented (diversity goal met)
- **7 designs skipped** by the 5/scaffold cap (3 from s105102, 2 each from s733072 and s877802)
- Affinity-window filter already applied in Stage 7.4 (no additional filtering needed)

### Top 10 for fusion panel

| Rank | Design | Scaffold | i_pTM | dG | SC | B_pLDDT | Div | Score |
|------|--------|----------|-------|-----|-----|---------|-----|-------|
| 1 | tfr1_l60_s766452_mpnn12 | s766452 | 0.850 | -58.8 | 0.69 | 0.910 | 0.93 | 0.678 |
| 2 | tfr1_l70_s422992_mpnn5 | s422992 | 0.830 | -48.5 | 0.74 | 0.920 | 0.87 | 0.677 |
| 3 | tfr1_l53_s938332_mpnn1 | s938332 | 0.810 | -59.6 | 0.78 | 0.910 | 0.93 | 0.673 |
| 4 | tfr1_l51_s255454_mpnn5 | s255454 | 0.840 | -47.7 | 0.70 | 0.930 | 0.87 | 0.645 |
| 5 | tfr1_l51_s694877_mpnn7 | s694877 | 0.850 | -62.0 | 0.71 | 0.890 | 0.53 | 0.643 |
| 6 | tfr1_l51_s694877_mpnn15 | s694877 | 0.850 | -60.1 | 0.72 | 0.890 | 0.53 | 0.642 |
| 7 | tfr1_l69_s653028_mpnn9 | s653028 | 0.840 | -73.8 | 0.71 | 0.890 | 0.47 | 0.641 |
| 8 | tfr1_l69_s653028_mpnn1 | s653028 | 0.820 | -72.6 | 0.71 | 0.890 | 0.47 | 0.623 |
| 9 | tfr1_l62_s195947_mpnn14 | s195947 | 0.840 | -47.6 | 0.67 | 0.940 | 0.93 | 0.622 |
| 10 | tfr1_l52_s604907_mpnn19 | s604907 | 0.820 | -45.9 | 0.76 | 0.880 | 0.93 | 0.618 |

### Pool statistics

- i_pTM: 0.760–0.900 (median 0.820)
- dG: -73.8 to -43.3 kcal/mol (median -53.1)
- Length: 50–70 residues (median 59)

### Note on s105102 (previously top scaffold)

s105102 dominated the Stage 7.4 composite ranking (10 of top 20) because it had high affinity-window scores (i_pTM ~0.80, moderate dG ~-38). With the diversity bonus rewarding rarer scaffolds, s105102 designs drop in Stage 7.5 ranking. However, 5 s105102 designs still make the top 50 — they're good designs, just not structurally diverse.

## Production status

Jobs 14990515–19 still running (~4 days remaining). Will NOT resubmit. When they complete, I'll:
1. Merge any new accepted designs
2. Run Stage 7.4 on new designs only
3. If >5 new survivors, re-rank and update the top 50
4. If ≤5, current ranking stands

## Files

- Fusion panel (top 50): `alzheimer/bindcraft/tfr1/filtering/stage7_5_ranked.csv`
- Full ranking (all 224): `alzheimer/bindcraft/tfr1/filtering/stage7_5_full_ranking.csv`
- Ranking script: `alzheimer/bindcraft/tfr1/filtering/scripts/stage7_5_ranking.py`

## TfR1 arm is ready for Stage 8

The 50 ranked TfR1 binders (50–70 residues each) are ready for tandem fusion design with the Aβ42 arm whenever that side completes Stage 5 ranking.
