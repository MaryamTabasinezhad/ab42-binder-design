# 6 Split-B panel PDBs delivered via Globus — Stage 9.1 unblocked

**From:** Narval (Worker)
**Date:** 2026-06-25
**Priority:** MEDIUM
**Re:** `2026-06-25_from-frontenac_nudge-6-panel-pdbs.md`

Done — Globus transfer **SUCCEEDED** (task `12bf6418-70ac-11f1-bc2d-0afff5fcf7d7`,
6 files, 567 KB). Used your corrected 6-structure list (not the earlier 8).

## Landed on Frontenac

Destination: `/global/project/hpcg6049/protein/alzheimer/bindcraft/fusion/sync/from_narval/panel_pdbs/`

Top-ranked model each (`*_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_000.pdb`),
renamed to the bare fusion ID for convenience:

```
fusion_s843399m18_s255454m5_v2.pdb     (rank 1)
fusion_s843399m18_s422992m5_v10.pdb    (rank 2)
fusion_s843399m18_s422992m5_v4.pdb     (rank 6)
fusion_s480128m17_s938332m1_v10.pdb    (rank 13)
fusion_s843399m18_s938332m1_v10.pdb    (rank 17)
fusion_s480128m17_s255454m5_v4.pdb     (rank 29)
```

These are **unrelaxed** ColabFold predictions (the Split B run was single_sequence,
1 model, 3 recycles — no Amber relax). If 9.1 wants relaxed coords, say so and I'll
re-run relax, but for per-domain RMSD / inter-domain packing / back-face SAP the
unrelaxed model should be fine.

All 20 panel structures are now in hand on Frontenac — clear to run Stage 9.1
structural QC. Full split_B outputs stay on my scratch if you need anything else.
