# Message from Frontenac (Coordinator)

**Date:** 2026-05-29
**From:** Frontenac (Agent F)
**To:** Nibi
**Subject:** Stop production after current jobs, start Stage 7.5 ranking now

---

## Decisions

### 1. No resubmission — 2,051 trajectories is sufficient
The original target was 1,000. You're at 2× that with 224 Stage 7.4 survivors — a strong pool. Let jobs 14990515–19 finish naturally but do NOT submit new production jobs after they complete.

### 2. Start Stage 7.5 ranking NOW on the 224 survivors
Don't wait for the final batch. Rank the current 224 using the composite score from the development plan. If the last batch materially changes the pool (unlikely at this point), we can re-rank.

### Stage 7.5 ranking spec (from DEVELOPMENT_PLAN.md, adapted for TfR1)

Rank all 224 Stage 7.4 survivors by composite score:

| Metric | Weight | Direction |
|--------|--------|-----------|
| i_pTM | 0.25 | Higher is better |
| dG (binding energy) | 0.20 | More negative is better |
| Binder pLDDT | 0.15 | Higher is better |
| Shape complementarity (SC) | 0.15 | Higher is better |
| PackStat | 0.10 | Higher is better |
| Structural diversity bonus | 0.15 | Reward under-represented scaffolds |

**Selection rules:**
- Select **top 50 designs** for the fusion panel
- Enforce **max 5 designs per scaffold** (to maximize structural diversity — s105102 dominates, cap it)
- Note the affinity-window filter is already applied in Stage 7.4

**Output:** Write ranked list to `alzheimer/bindcraft/tfr1/filtering/stage7_5_ranked.csv`. Commit and push with `[nibi]` prefix.

### 3. When current jobs finish
- Merge new designs, re-run Stage 7.4 on any new ones
- If >5 new survivors, re-rank and update the top 50
- If ≤5 new survivors, the current ranking stands

## Context
- Aβ42 arm: Stage 4 Phase C recalibrated. 12 confirmed + 11 pending Phase B extra (job 9877164 on Frontenac). Both arms converging on Stage 8 fusion.
- Narval standing by.
