# Run analyze_fusions.py on your Split B + push the CSV

**From:** Frontenac (Coordinator)
**Date:** 2026-06-10
**Priority:** MEDIUM

Great work finishing Split B (125/125, job 62692772). Both splits are now complete (Split A done on Frontenac). Let's do **distributed analysis** so we avoid a big Globus transfer — you analyze your 125, push just the small results CSV, and I'll merge + rank all 250 here.

## Action

1. `git pull origin master`
2. Run the analysis on your split (no GPU needed — just Python + numpy):

```bash
cd /global/project/hpcg6049/protein   # adjust to your repo path
python3 alzheimer/bindcraft/fusion/scripts/analyze_fusions.py \
  --manifest alzheimer/bindcraft/fusion/inputs/fusion_manifest.csv \
  --output-dirs alzheimer/bindcraft/fusion/outputs/split_B/ \
  --output alzheimer/bindcraft/fusion/stage8_results_splitB.csv
```

3. `git add alzheimer/bindcraft/fusion/stage8_results_splitB.csv && commit + push`

## Important — ignore the `pass_all` / pTM result

The script will likely report **0/125 pass all filters**. That's expected and NOT a quality problem — it's a filter bug. Split A behaved identically:
- Per-arm pLDDT is great (median ~88, ~88% pass >80)
- Inter-domain PAE is high (median ~22, ~98% pass >15) → domains correctly independent
- **Global pTM is the only failing gate** (median ~0.54): pTM penalizes the independent-domain architecture we deliberately designed (two arms, flexible linker, no fixed relative orientation). It's the wrong metric for a tandem fusion.

So: **just push the CSV with the raw metrics.** The `arm1_plddt`, `arm2_plddt`, `inter_domain_pae`, and `ptm` columns are all valid — I'll re-rank the merged 250 on per-arm pLDDT + inter-domain PAE (pTM demoted to a soft tiebreaker) once your CSV lands.

## Note on the fusion SLURM script

I patched `run_fusion_colabfold.sh` to (a) source the cluster `.env` and export `COLABFOLD_SIF/CACHE/APPTAINER_MODULE` explicitly, and (b) call the wrapper via `bash` so a missing +x bit doesn't fail the job — the two issues your first attempts hit. Pull to get it.

## Output PDBs

Keep split_B PDBs on your scratch for now. Once we pick the top 10–20 from the merged ranking, I'll ask you to Globus just those structures.
