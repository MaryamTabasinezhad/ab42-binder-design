# TfR1 Counter-Screen Structure Choices

**Date:** 2026-05-27
**Agent:** Nibi

## Target 1 — Positive re-confirmation: 6WRV (TfR1 apical domain)

- **Source:** PDB 6WRV, chains A+B
- **File:** `alzheimer/structures/tfr1/6WRV_target.pdb` (chains A+B, residues 121-759 each)
- **Rationale:** Same target used for BindCraft design. Re-confirms binding with ColabFold multimer prediction.
- **Pass criterion:** pae_interaction < 10

## Target 2 — Negative selectivity: TfR2 apical domain

- **Source:** AlphaFold predicted structure, UniProt Q9UP52 (v6, model date 2025-08-01)
- **File:** `alzheimer/structures/tfr1/TfR2_apical.pdb` (chain A, residues 163-424)
- **Why AlphaFold:** No experimental TfR2 crystal structure exists in RCSB PDB. PDB 3KAS was initially considered but it contains Machupo virus GP1 bound to TfR1, not TfR2. The AlphaFold model has global pLDDT 83.9 with 70% of residues in the "very high" confidence category.
- **Domain mapping:** Pairwise sequence alignment of TfR1 (6WRV chain A) vs TfR2 ectodomain identified residues 163-424 as the apical domain equivalent to TfR1 residues 150-400. Overall ectodomain sequence identity: 47%.
- **Pass criterion:** pae_interaction > 15 (must NOT bind)

## Target 3 — Tf competition: 1SUV (TfR1 + transferrin complex)

- **Source:** PDB 1SUV — cryo-EM structure of human TfR1 bound to transferrin (2.4 Å)
- **File:** `alzheimer/structures/tfr1/1SUV_TfR1_Tf_complex.pdb`
- **Chains used:** A (TfR1, res 122-760), C (Tf N-lobe, res 3-331), E (Tf C-lobe, res 332-676)
- **Rationale:** Tests that binder can still engage TfR1 apical domain when transferrin is bound, confirming no steric clash. Uses one copy of the TfR1-Tf pair (chains A+C+E) rather than the full homodimer to keep the complex tractable for ColabFold.
- **Note:** 1SUV is older (3.2 Å resolution originally) but is the canonical TfR1-Tf co-crystal structure. The Tf binding site is in the helical/protease-like domain, distant from the apical domain hotspots (208/210/211/212/215), so binders targeting the apical domain are expected to pass this test.
- **Pass criterion:** pae_interaction < 12 (binder↔TfR1 binding preserved)

## Deleted structures

- `3KAS.pdb` — Initially downloaded thinking it was TfR2. Actually contains Machupo virus GP1 + TfR1. Not used.
