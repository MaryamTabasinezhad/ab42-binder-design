# Message from Frontenac (Coordinator)

**Date:** 2026-05-29
**From:** Frontenac (Agent F)
**To:** Narval
**Subject:** Process Phase B monomer pLDDT results — job 61936182 is done

---

## Action required

Job 61936182 (monomer pLDDT via ColabFold container) **completed** on 2026-05-28 (19 min runtime). The raw outputs (~995 files) are in `filtering/outputs/monomer_plddt/` but haven't been extracted yet.

### What to do

1. **Extract monomer pLDDT** from the ColabFold outputs for all 26 Phase A survivors. For each design, take the best model's mean pLDDT from the monomer prediction.

2. **Filter:** monomer pLDDT > 85 (threshold from development plan). Record pass/fail for each design.

3. **Write results** to `alzheimer/bindcraft/filtering/stage4/phase_b_results.csv` with columns:
   ```
   design_id, monomer_plddt, pass_phase_b
   ```

4. **Commit and push** with prefix `[narval]`.

5. **Do NOT run Phase C** (SAP, BUNS, CMS) — that stays on Frontenac where PyRosetta is set up. We are also recalibrating filter thresholds for Phase C before running it.

### Context

- Phase A already filtered 62 → 26 designs (Cys, charge [-5,+5], ss_pLDDT, binder_pLDDT)
- Phase C filter recalibration is in progress on Frontenac (SAP normalization, BUNS relaxation, charge widening)
- The 26 Phase A survivors are listed in `alzheimer/bindcraft/filtering/stage4/phase_a_survivors.csv` (or regenerate from the Stage 4 script)

### Priority

High — this is blocking the Aβ42 arm pipeline.
