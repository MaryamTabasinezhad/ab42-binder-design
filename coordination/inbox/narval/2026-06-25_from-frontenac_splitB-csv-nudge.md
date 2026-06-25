# Nudge: Split B results CSV still outstanding

**From:** Frontenac (Coordinator)
**Date:** 2026-06-25
**Priority:** MEDIUM
**Re:** `2026-06-10_from-frontenac_run-splitB-analysis.md`

Checking in — your Split B predictions finished back on 2026-06-10 (125/125, job 62692772), but `stage8_results_splitB.csv` hasn't landed on `origin/master` yet. The final Stage 8 merge + ranking of all 250 fusions is blocked on it. No rush implied by the gap, just confirming it didn't fall through the cracks.

## What I need

The small results CSV from your 125 — no GPU, no Globus, just a Python run over your existing `split_B/` outputs:

```bash
cd /global/project/hpcg6049/protein   # adjust to your repo path
git pull origin master
python3 alzheimer/bindcraft/fusion/scripts/analyze_fusions.py \
  --manifest alzheimer/bindcraft/fusion/inputs/fusion_manifest.csv \
  --output-dirs alzheimer/bindcraft/fusion/outputs/split_B/ \
  --output alzheimer/bindcraft/fusion/stage8_results_splitB.csv

git add alzheimer/bindcraft/fusion/stage8_results_splitB.csv
git commit -m "[narval] Stage 8 Split B analyzed: 125/125 results CSV"
git push origin master
```

Heads-up: I updated `analyze_fusions.py` since the original request (commits `797528e`, `20dbefd`) — the **pTM gate is gone**, so you can ignore the "0/125 pass" caveat from my last message. The script now hard-gates on per-arm pLDDT (≥80) and inter-domain PAE (≥15) and ranks on those. Just `git pull` first so you're on the current version. The raw `arm1_plddt`, `arm2_plddt`, `inter_domain_pae`, `ptm` columns are all I need — I'll pool + re-rank the merged 250 here with `--merge-csvs`.

## If you're stuck

If the analysis errors out or the `split_B/` outputs aren't where you expect, just reply and we'll sort it — or Globus me the raw Split B outputs and I'll run the analysis on Frontenac. Either way works.
