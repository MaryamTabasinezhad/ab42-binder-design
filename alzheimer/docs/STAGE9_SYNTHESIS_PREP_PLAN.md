# Stage 9 — Computational Synthesis-Prep / Construct Finalization

**Status:** Sequence track COMPLETE (9.2–9.5, 2026-06-25, Frontenac); structural QC (9.1) pending Narval PDBs. Results: `STAGE9_SYNTHESIS_PREP.md`.
**Prerequisite:** Stage 8 COMPLETE — 20-design fusion panel in
`alzheimer/bindcraft/fusion/stage8_results_merged.csv` (`panel_selected=True`).

## Goal

Turn the 20-design Stage 8 panel into an **order-ready synthesis sheet**: full
*E. coli* expression constructs (His6-SUMO cassette), DNAChisel codon-optimized
DNA, and a final in-silico QC + developability-liability pass. Output goes
straight to a synthesis vendor (Twist/IDT) and a pET-28a(+) NdeI/XhoI vector.

This is the computational bridge between Stage 8 (fusion design) and the
development plan's wet-lab Stage 9 (expression + SPR characterisation). The
wet-lab arm-validation gate (Stage 6) was bypassed — campaign is computational.

## Construct architecture (DECIDED 2026-06-25)

```
NdeI–ATG–[His6]–[SUMO/Smt3]…GG ↓(Ulp1) [FUSION (Aβ–linker–TfR1 or TfR1–linker–Aβ)]–STOP–XhoI
```

- **Tag:** N-terminal His6-SUMO (Smt3). Ulp1/SUMO-protease cleaves after the
  SUMO C-terminal di-Gly, leaving the **native N-terminus** of the fusion (no
  scar). His6 enables IMAC capture; SUMO boosts solubility for the ~15–20 kDa
  miniprotein fusions.
- **Vector:** pET-28a(+), cloned NdeI/XhoI. Full ORF synthesised (tag is part of
  the insert — no separate pET-SUMO vector required).
- **Host:** *E. coli* (BL21(DE3) class).
- The fusion sequences already start with Met; that becomes the native
  post-cleavage N-terminus.

## Panel facts (from Stage 8)

- 20 designs, full AA sequences in `fusion/inputs/fusion_manifest.csv`.
- Length 129–177 aa; both domain orders present (`ab-tfr1`, `tfr1-ab`).
- **All Cys-free** — no free-thiol / disulfide-scrambling liability.
- Gates already passed: per-arm pLDDT ≥80, inter-domain PAE ≥15.

## Sub-steps

| Step | Needs PDBs? | Tool/env | Output |
|------|-------------|----------|--------|
| 9.1 Structural QC (per-domain RMSD <2 Å, no inter-domain packing, back-face SAP) | **Yes** | colabfold env + Stage 4 SAP routine | `stage9_structural_qc.csv` |
| 9.2 Sequence-liability scan (deamidation NG/NS, isomerization DG/DP, Met-ox, glyc sequons, protease sites, low-complexity) + ProtParam (pI, GRAVY, MW, ext. coeff) | No | biopython (colabfold env) | `stage9_liabilities.csv` |
| 9.3 Construct assembly (His6-SUMO + fusion + stop) | No | python | per-design protein seq |
| 9.4 Codon optimization (E. coli K-12; strip NdeI/XhoI/internal RBS/hairpins/repeats; add cloning overhangs) | No | **DNAChisel** (`stage9/.venv-dnachisel`) | per-design DNA |
| 9.5 Final cut + synthesis sheet (merge Stage 8 rank + Stage 9 flags; drop severe liabilities, backfill from rank 21+) | merges all | python | `synthesis_panel.csv` + report |

## Dependency / sequencing

- **9.2–9.5 (sequence-based) need no PDBs → started immediately.**
- **9.1 (structural) is gated on 8 Narval Split-B PDBs** (requested via inbox
  `2026-06-25_from-frontenac_stage8-merged-need-panel-pdbs.md`). 12 Frontenac
  PDBs can be QC'd now; the 8 inbound complete the set.
- RMSD step needs standalone arm monomer models: Aβ arms have them (Stage 4
  Phase B); TfR1 arm monomers may need fresh ColabFold runs — **best-effort**.

## Deliverables

- `alzheimer/bindcraft/fusion/stage9/synthesis_panel.csv` — final order sheet:
  `id, final_protein_seq, codon_opt_dna, tag_architecture, vector, MW, pI,
  ext_coeff, liabilities, arm1/arm2_plddt, inter_pae, final_rank`.
- Per-design 1-pagers.
- `STAGE9_SYNTHESIS_PREP.md` report (this plan's results section, filled on completion).

## Decisions log

- 2026-06-25 — Tag architecture: **His6-SUMO** (cleavable, native N-term). Codon
  optimization: **DNAChisel**, produced in-house for reproducibility. (PI: Hamid)
