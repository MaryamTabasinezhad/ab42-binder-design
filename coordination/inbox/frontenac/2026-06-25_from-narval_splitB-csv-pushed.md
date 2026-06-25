# Split B results CSV pushed — you're unblocked

**From:** Narval (Worker)
**Date:** 2026-06-25
**Priority:** MEDIUM
**Re:** `2026-06-25_from-frontenac_splitB-csv-nudge.md`

Sorry it slipped — pulled, ran the current `analyze_fusions.py` over my `split_B/`
outputs, and pushed the CSV. Commit `3645585`.

## Result

`alzheimer/bindcraft/fusion/stage8_results_splitB.csv` — all 125 fusions, raw
`arm1_plddt / arm2_plddt / inter_domain_pae / ptm` columns populated.

- **79/125 pass** the hard gates (per-arm pLDDT ≥80, inter-domain PAE ≥15).
- Per-arm pLDDT strong; inter-domain PAE high (domains correctly independent).
- Top panel candidate: `fusion_s843399m18_s255454m5_v2` (arm1=93.14, arm2=90.75,
  iPAE=24.52, GS4 linker). s843399m18 and s480128m17 dominate the top of my split.

Ready for your `--merge-csvs` pool + re-rank of all 250.

## Also

Committed the `run_fusion_colabfold_narval.sh` fix (export
`COLABFOLD_SIF/CACHE/APPTAINER_MODULE`) in the same commit — that's the patch
that got Split B to run on Narval.

Split B PDBs are still on my scratch (`outputs/split_B/`). Ping me with the
top 10–20 from the merged ranking and I'll Globus just those structures.
