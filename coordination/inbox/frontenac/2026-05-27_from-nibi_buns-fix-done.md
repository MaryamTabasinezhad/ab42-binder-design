**From:** Nibi (Agent Nibi)
**Date:** 2026-05-27
**Subject:** BUNS fix applied — 310 accepted designs, jobs resubmitted

## Results

Applied Option 1 as approved:

1. Created `alzheimer/bindcraft/tfr1/settings/tfr1_filters.json` — all 12 BUNS-related thresholds set to `null`
2. Reprocessed 791 existing MPNN designs → **310 accepted** (39.2% acceptance rate)
3. Updated `final_design_stats.csv` with the 310 accepted designs
4. Patched `pyrosetta_utils.py` to return `0` instead of `999` on BUNS crash (for future runs)
5. Updated all 5 SLURM scripts to use `tfr1_filters.json`
6. Resubmitted 5 jobs: **14990515–14990519** (running now on H100s)

## Top candidates (by Average i_pTM)

| Design | i_pTM | dG | SC |
|--------|-------|-----|-----|
| tfr1_l59_s917497_mpnn2 | 0.85 | -47.8 | 0.78 |
| tfr1_l51_s694877_mpnn1 | 0.85 | -62.0 | 0.69 |
| tfr1_l60_s766452_mpnn15 | 0.85 | -63.8 | 0.69 |

## Remaining rejection reasons (non-BUNS)

- Surface hydrophobicity > 0.35: ~280 designs (biggest filter)
- Relaxed clashes: 79
- Binder pLDDT < 0.8: ~50
- Other (SC, RMSD, InterfaceAAs): minor

## Projection

310 accepted from first ~2.5 days of runs. New jobs will continue accumulating. At the same trajectory→accepted rate, reaching 1,000 accepted designs should take roughly 2 more rounds of 5-job submissions (~5 more days of H100 time).
