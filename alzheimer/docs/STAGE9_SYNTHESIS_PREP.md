# Stage 9 — Synthesis-Prep Results

**Date:** 2026-06-25 (Frontenac)
**Status:** Sequence track COMPLETE (9.2–9.5). Structural QC (9.1) PENDING Narval PDBs.
Plan: `STAGE9_SYNTHESIS_PREP_PLAN.md`.

## What ran

| Step | Status | Script | Output |
|------|--------|--------|--------|
| 9.2 Liability scan + ProtParam | ✅ | `stage9/stage9_sequence_prep.py` (colabfold env) | `stage9/stage9_sequence_prep.csv` |
| 9.3 His6-SUMO construct assembly | ✅ | (same) | `construct_protein` column |
| 9.4 Codon optimization (E. coli) | ✅ | `stage9/stage9_codon_optimize.py` (DNAChisel venv) | `stage9/synthesis_panel.csv` |
| 9.5 Final synthesis sheet | ✅ | (same) | `stage9/synthesis_panel.csv` |
| 9.1 Structural QC (RMSD, packing, back-face SAP) | ⏳ pending | — | needs 8 Narval PDBs |

## Deliverable — `stage9/synthesis_panel.csv` (20 order-ready constructs)

- **Construct:** His6-SUMO(Smt3), Ulp1-cleavable → native fusion N-terminus. 236–284 aa.
- **Vector:** pET-28a(+), NdeI/XhoI. Full ORF synthesised (tag in insert).
- **DNA:** DNAChisel codon-optimized for *E. coli*; GC 46.7–51.3%; inserts 723–867 bp.
  Validated 20/20: CDS translates exactly to construct protein; NdeI+XhoI unique
  and terminal; tandem stop (TAA TGA) present.
- Sheet columns: `final_rank, id, domain_order, linker_name, arm1/arm2_plddt,
  inter_domain_pae, construct_len_aa, construct_mw_kda, construct_pI, fusion_pI,
  fusion_gravy, fusion_ext_coeff, liabilities, severe_flags, tag_architecture,
  vector, cds_gc_pct, constraints_ok, construct_protein, order_dna_NdeI_XhoI`.

## Developability summary

- **0/20 severe flags.** Panel is entirely Cys-free (no disulfide scrambling),
  no non-GS low-complexity runs.
- All fusions acidic (pI 4.5–5.5) with negative GRAVY → favourable solubility.
- Mild, low-count liabilities only: scattered Asn-deamidation (NG/NS/NT) and
  Asp-isomerization (DG/DP) motifs; a few N-glyc sequons (N-X-S/T) that are
  **irrelevant in E. coli** — flagged for completeness, not a defect.
- Rank 19 (`fusion_s311742m16_s938332m1_v4`) is fully clean (no liabilities).

## Tooling notes (HPC gotchas)

- DNAChisel installed in a dedicated venv: `stage9/.venv-dnachisel`. The Compute
  Canada wheelhouse (`PIP_CONFIG_FILE`) serves `+computecanada` numpy that won't
  import under the Anaconda base python; **must install and run with
  `env -u PIP_CONFIG_FILE -u PYTHONPATH`** forcing `--index-url https://pypi.org`
  and `numpy==1.26.4` (PyPI manylinux2014 wheel, glibc-2.17 compatible). PyPI
  numpy 2.x needs GLIBC_2.29 — unavailable on the RHEL8 nodes.
- Sequence steps run under the `colabfold` conda env (biopython 1.84). The
  `anaconda-cloud-auth` GLIBC warnings on conda activate are harmless noise.

## Next

1. **9.1 structural QC** once Narval Globus-transfers the 8 Split-B panel PDBs.
   RMSD step needs standalone arm monomers (Aβ arms: Stage 4 Phase B; TfR1 arms
   may need fresh monomer ColabFold) — best-effort.
2. Hand `synthesis_panel.csv` (`order_dna_NdeI_XhoI` column) to vendor (Twist/IDT)
   once 9.1 confirms no inter-domain packing rejections.
