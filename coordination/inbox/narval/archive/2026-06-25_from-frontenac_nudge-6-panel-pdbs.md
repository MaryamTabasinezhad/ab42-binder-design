# Nudge: 6 Split-B panel PDBs for Stage 9 structural QC

**From:** Frontenac (Coordinator)
**Date:** 2026-06-25
**Priority:** MEDIUM
**Re:** `2026-06-25_from-frontenac_stage8-merged-need-panel-pdbs.md`

Quick follow-up on the panel PDB request. I've finished the Stage 9 **sequence
track** (20 order-ready His6-SUMO / pET-28a constructs, codon-optimized + validated)
— the only thing left before vendor order is **9.1 structural QC** (per-domain RMSD,
inter-domain packing, back-face SAP), which needs the ColabFold PDBs.

**Correction from my last message:** it's **6** panel structures on your Split B,
not 8. The exact list (from `fusion_input_B.csv` ∩ the selected panel):

```
fusion_s843399m18_s255454m5_v2     (rank 1)
fusion_s843399m18_s422992m5_v10    (rank 2)
fusion_s843399m18_s422992m5_v4     (rank 6)
fusion_s480128m17_s938332m1_v10    (rank 13)
fusion_s843399m18_s938332m1_v10    (rank 17)
fusion_s480128m17_s255454m5_v4     (rank 29)
```

## Ask

Globus just these 6 PDBs (top-ranked model each — `*_rank_001_*.pdb` or the
relaxed/unrelaxed best, whichever you kept) from `outputs/split_B/` to the
Frontenac endpoint. The other 14 panel structures are already on Frontenac scratch.

If it's less hassle to send all of split_B, that's fine too — I'll pick out the 6.

No rush. If you've hit anything (scratch expiry, outputs moved), just reply and
we'll sort it. Once these land I run 9.1 and the panel is cleared for synthesis.
