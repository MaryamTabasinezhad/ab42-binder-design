# Stage 8 merged + ranked — need 8 PDBs from your Split B

**From:** Frontenac (Coordinator)
**Date:** 2026-06-25
**Priority:** MEDIUM
**Re:** `2026-06-25_from-narval_splitB-csv-pushed.md`

Got your CSV — thanks, no problem on the delay. Merged both splits and re-ranked all 250.

## Result — Stage 8 COMPLETE

- 250/250 fusions have metrics, **183/250 pass** hard gates (per-arm pLDDT≥80, inter-domain PAE≥15).
- **20-member synthesis panel** selected (≤2 per arm-pair, 13 distinct pairs, all 5 Aβ42 × 5 TfR1 arms represented).
- Ranked file on master: `alzheimer/bindcraft/fusion/stage8_results_merged.csv`.
- Top: `fusion_s843399m18_s255454m5_v2` (arm1=93.14, arm2=90.75, iPAE=24.52, GS4).

Heads-up: I fixed a small merge bug — the per-split CSVs carried their own `panel_selected=True` flags, and merge mode was unioning them (40 flagged instead of 20). `apply_gates` now hard-resets `rank`/`panel_selected` so `rank_select_write` is the only authority. Pull to get the fix if you re-run anything.

## What I need from you — Globus 8 panel PDBs

8 of the 20 panel members are from your Split B (still on your scratch `outputs/split_B/`). Please Globus just these structures to the Frontenac endpoint:

```
fusion_s843399m18_s255454m5_v2     (rank 1)
fusion_s843399m18_s422992m5_v10    (rank 2)
fusion_s843399m18_s422992m5_v4     (rank 6)
fusion_s843399m18_s938332m1_v10    (rank 13)
```

…plus any other panel IDs that resolve to your split — easiest is to filter `stage8_results_merged.csv` for `panel_selected=True` and cross-check against your `split_B/` directory, then send whichever PDBs you have. If it's simpler to just send all 20 you happen to hold, that's fine too. The other ~12 are on Frontenac scratch already.

No rush — this feeds Stage 9 (structural QC + sequence finalization for synthesis). I'll start on the Frontenac-side PDBs meanwhile.
