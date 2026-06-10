# Stage 8 Split B — COMPLETE

**From:** Narval
**Date:** 2026-06-10
**Priority:** HIGH

## Results

- **Job:** 62692772 (COMPLETED, 34 min on A100)
- **Predictions:** 125/125 complete
- **Output:** `alzheimer/bindcraft/fusion/outputs/split_B/` (1,003 files — PDBs, score JSONs, PAE plots)
- **Output size:** on Narval scratch, transfer via Globus if needed

## Notes

- First two attempts failed: job 62652492 (wrapper missing +x), job 62692747 (wrapper couldn't find `clusters/narval.env` via auto-detect). Fixed by exporting `COLABFOLD_SIF`/`COLABFOLD_CACHE`/`APPTAINER_MODULE` directly in the SLURM script.
- All 125 `.done.txt` markers present — no failed predictions.

## Next

Ready for `analyze_fusions.py` whenever Split A is also done. Outputs stay on Narval scratch — let me know if you want Globus transfer or if I should run analysis on my split locally.
