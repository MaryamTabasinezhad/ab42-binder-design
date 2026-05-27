**From:** Nibi (Agent Nibi)
**Date:** 2026-05-27
**Subject:** TfR1 campaign BLOCKED — BUNS filter crashes on all poses, 0 accepted from 991 trajectories

## Summary

Completed Task 1 from your message. Full report at `alzheimer/docs/tfr1_progress_report.md`.

**Key findings:**
- All 5 successful jobs (13720846–13720850) COMPLETED, ~2.5 days each on H100
- **991 trajectories**, 791 MPNN designs evaluated — quality is strong (best i_pTM=0.94, median=0.79)
- **0 accepted designs** — every single design has `n_InterfaceUnsatHbonds = 999`

## Root cause

The PyRosetta `BuriedUnsatHbonds` filter (DAlphaBall SASA) crashes with RuntimeError on **every** TfR1 (6WRV) pose. Our try/except patch correctly catches it and sets the value to 999, but the default filter rejects anything > 4. This didn't happen on Aβ42 (9CO4).

The likely cause is the larger target size (6WRV chains A+B = ~680 residues vs 9CO4 chains C/E/G) or structural features (disulfides, glycosylation) that break DAlphaBall.

## Decision needed (Task 2 blocked on this)

I cannot continue toward 1,000 designs until this is resolved. Three options:

1. **Create custom `tfr1_filters.json`** with BUNS thresholds set to `null` — then retroactively reprocess existing 791 MPNN designs. Fastest fix, loses one quality filter.
2. **Change the try/except patch** to return `0` instead of `999` — effectively skips BUNS. Requires rerun.
3. **Debug DAlphaBall** for the 6WRV target — hardest, most correct fix.

**My recommendation:** Option 1. We already have 791 MPNN designs sitting there. Disabling the BUNS filter and reprocessing against relaxed filters could immediately yield accepted designs. The other quality filters (i_pTM, pAE, dG, clashes, packing) are still active and working.

Please advise which approach to take. I'll hold on resubmitting jobs until then.
