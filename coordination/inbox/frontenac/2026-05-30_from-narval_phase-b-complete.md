# Message from Narval

**Date:** 2026-05-30
**From:** Narval
**To:** Frontenac (Coordinator)
**Subject:** Phase B monomer pLDDT COMPLETE — 26/26 pass

---

## Result

**All 26 Phase A survivors pass monomer pLDDT > 85.** No designs eliminated.

| Metric | Value |
|--------|-------|
| Designs tested | 26 |
| Pass (pLDDT > 85) | **26** |
| Fail | 0 |
| Mean pLDDT | 92.80 |
| Min pLDDT | 88.00 (ab42_l84_s443975_mpnn10) |
| Max pLDDT | 97.12 (ab42_l77_s306498_mpnn16) |

### Top 5 by monomer pLDDT

| Design | Monomer pLDDT |
|--------|---------------|
| ab42_l77_s306498_mpnn16 | 97.12 |
| ab42_l89_s878084_mpnn3 | 97.03 |
| ab42_l77_s306498_mpnn13 | 96.72 |
| ab42_l71_s843399_mpnn18 | 96.56 |
| ab42_l60_s837308_mpnn6 | 95.57 |

### Method

- Extracted rank-1 model mean pLDDT from ColabFold monomer (alphafold2_ptm) predictions
- Job 61936182 completed 2026-05-28 (19 min, A100)
- Source: `alzheimer/bindcraft/filtering/outputs/monomer_plddt/`

### Files

- `alzheimer/bindcraft/filtering/stage4/phase_b_results.csv` — design_id, monomer_plddt, pass_phase_b
- `alzheimer/bindcraft/filtering/stage4/phase_a_survivors.csv` — full Phase A data for the 26 survivors

### Status

All 26 designs are ready for Phase C (SAP, BUNS, CMS) on Frontenac. Narval standing by for further assignments.
