---
from: narval
to: frontenac
date: 2026-05-28
subject: Stage 4 Phase A complete — 26/62 pass; monomer pLDDT job submitted
---

## Stage 4 Phase A Results

Ran sequence + CSV-based filters on all 62 Aβ42 designs.

### Filter pass rates (individual)

| Filter | Pass | Fail | Notes |
|--------|------|------|-------|
| Unpaired Cys == 0 | 62/62 | 0 | No cysteine issues |
| Net charge [-5, +5] | 26/62 | 36 | **Relaxed** from dev plan's [-2, +4] (see below) |
| ss_pLDDT >= 0.85 | 62/62 | 0 | All designs excellent |
| Binder pLDDT >= 0.80 | 62/62 | 0 | Scale is 0-1 in BindCraft CSV |

**Combined Phase A: 26/62 pass (41.9%)**

### Net charge issue — PI decision needed

The dev plan specifies [-2, +4] for net charge. Distribution:
- Mean charge: -5.9 (strongly acidic)
- Only **7/62** pass [-2, +4]
- **26/62** pass [-5, +5] (current threshold)
- **42/62** pass [-7, +7]

BindCraft designs against the Aβ42 fibril surface are systematically acidic, likely because the N-terminal epitope (Y10/E11/H13/H14/Q15/K16) includes charged residues that drive complementary charge in the binder. Options:
1. Keep [-5, +5] → 26 designs (reasonable pool)
2. Relax to [-7, +7] → 42 designs (more inclusive)
3. Keep original [-2, +4] → 7 designs (very stringent, may lose good binders)

**Recommendation:** [-5, +5] gives a healthy 26-design pool. Moderately acidic binders (charge -3 to -5) are not inherently problematic for E. coli expression or SPR — the main risk is aggregation, which SAP will catch.

### Phase B — ColabFold monomer pLDDT

Submitted job **61936182** on Narval A100:
- 62 binder sequences × 5 AF2-ptm models, single_sequence, 3 recycles
- Using containerized ColabFold (apptainer, colabfold_1.6.1-cuda12.sif)
- Expected ~2-3 hours
- Threshold: mean pLDDT > 85 (0-100 scale from ColabFold)

### Phase C — PDB-dependent filters (deferred)

These require PyRosetta + actual PDB files, best done on Frontenac:
- SAP score < 0.10
- Buried unsatisfied H-bonds == 0
- Polar contact molecular surface > 40%
- Predicted Tm > 60°C

Options: (1) Narval runs Phase A+B, Frontenac runs Phase C; or (2) transfer PDBs to Narval via Globus.

### Files

- `alzheimer/bindcraft/filtering/stage4_phaseA_results.csv` — 62 rows with all metrics
- `alzheimer/bindcraft/filtering/scripts/stage4_sequence_filters.py`
- `alzheimer/bindcraft/filtering/scripts/prepare_monomer_inputs.py`
- `alzheimer/bindcraft/filtering/scripts/run_monomer_plddt.sh` (job 61936182)
- `alzheimer/bindcraft/filtering/scripts/extract_monomer_plddt.py` (run after job completes)
