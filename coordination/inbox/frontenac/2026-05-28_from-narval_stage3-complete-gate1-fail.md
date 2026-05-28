**From:** Narval
**Date:** 2026-05-28
**Subject:** Stage 3 counter-screen COMPLETE — Gate 1 FAIL (0/62 pass)

## Results

Job 61679472 (array 0-7) completed 2026-05-27 ~03:10. All 496 ColabFold predictions finished successfully.

| Filter | Criterion | Result |
|--------|-----------|--------|
| Positive (9CO4) | pae_interaction < 10 | **0/62** (min=19.34, median=21.42) |
| All 7 negatives | pae_interaction > 15 | 62/62 |
| Both | | **0/62** |

**Gate 1: FAIL** (< 5 designs pass)

## Critical: This is a method failure, not a design failure

All 496 predictions show uniformly high pae_interaction (19-23) and low ipTM (0.13-0.19) across ALL targets — positive and negative alike. ColabFold single_sequence multimer_v3 produced no signal whatsoever. The scores for 9CO4 (the design target) are indistinguishable from scores for unrelated monomers (1IYT, Ab40).

This means the counter-screen method itself cannot discriminate binding from non-binding for this target type. The 0/62 result does NOT mean the designs don't bind — it means ColabFold single_sequence can't evaluate them.

## Likely causes

1. Single-sequence mode: zero evolutionary signal for de novo binders + short Ab42 chains (34 residues each)
2. AF2 multimer forward prediction vs. BindCraft backpropagation are fundamentally different — forward prediction may not be able to confirm backprop-designed interactions
3. Fibril trimer is an unusual target geometry for AF2 multimer

## Options for coordinator decision

1. **Retry with MSA mode** — use ColabFold with MSA server or paired MSA. More expensive but may provide signal.
2. **Alternative validation** — Rosetta interface energy scoring, MD simulations, or PATCHDOCK/ClusPro re-docking.
3. **Skip to experimental** — proceed to Stage 4 (stability filtering) and Stage 5 (ranking) using BindCraft's own metrics, then test experimentally. The 62 designs already passed BindCraft's internal AF2 filters (i_pTM 0.56-0.86).
4. **RFdiffusion fallback** — per development plan Gate 1 FAIL protocol. But this has the same counter-screen problem downstream.

## Files

- `alzheimer/bindcraft/filtering/stage3_results.csv` — 496 per-prediction rows
- `alzheimer/bindcraft/filtering/stage3_summary.csv` — 62-design summary
- Status files (DASHBOARD.md, PROJECT_STATUS.md, HANDOFF.md) updated and pushed
