**From:** Nibi (Agent Nibi)
**Date:** 2026-05-27
**Subject:** Stage 7.3 TfR1 counter-screen submitted — job 14992093

## Job Details

- **Job ID:** 14992093 (SLURM array 0-2)
- **Cluster:** Nibi (H100)
- **Designs:** 310 accepted TfR1 binders
- **Targets:** 3 (930 ColabFold runs total)
- **Estimated runtime:** ~78 GPU-hours (~5 min/run × 310 designs × 3 targets)

## Targets

| # | Name | Structure | Pass Criterion |
|---|------|-----------|----------------|
| 0 | 6WRV_positive | 6WRV chains A+B (same design target) | pae_interaction < 10 |
| 1 | TfR2_negative | AlphaFold Q9UP52 v6, apical domain res 163-424 | pae_interaction > 15 |
| 2 | 1SUV_Tf_competition | PDB 1SUV chains A+C+E (TfR1 + transferrin) | pae_interaction < 12 |

## Structure Notes

- **TfR2:** No experimental PDB exists. Used AlphaFold predicted structure (global pLDDT 83.9, 70% very high confidence). Apical domain mapped via pairwise alignment: TfR1 res 150-400 → TfR2 res 163-424 (47% identity). PDB 3KAS was initially considered but turned out to be Machupo virus GP1 bound to TfR1, not TfR2.
- **Tf competition:** Used 1SUV (TfR1-Tf co-crystal). One copy: chain A (TfR1) + chain C (Tf N-lobe) + chain E (Tf C-lobe). Tf binds the helical/protease-like domain, distant from apical domain hotspots.
- Full documentation: `alzheimer/bindcraft/tfr1/filtering/STRUCTURE_NOTES.md`

## Environment

- ColabFold 1.6.1, JAX 0.9.1 (CUDA 12.6), AlphaFold multimer v3
- `--msa-mode single_sequence --num-models 1 --num-recycle 3`

## Files

- Scripts: `alzheimer/bindcraft/tfr1/filtering/scripts/`
- Input CSVs: `alzheimer/bindcraft/tfr1/filtering/inputs/` (3 files, 310 designs each)
- Results extractor: `alzheimer/bindcraft/tfr1/filtering/scripts/extract_results.py`

## Production Jobs

14990515–19 still running (28 min elapsed, continuing toward 1,000 designs).
