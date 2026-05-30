# Project Status Tracker

Last updated: 2026-05-29T00:00
Updated by: Frontenac — Stage 4 Phase B job complete, filter recalibration in progress

## Pipeline status

```yaml
stage_0:
  name: "Environment setup + BindCraft installation"
  status: completed  # 2026-05-06
  substeps:
    environment_audit: completed  # 2026-05-06
    bindcraft_install: completed  # 2026-05-06, conda env BindCraft, GPU-tested on A30
    counter_target_download: completed  # 2026-05-06, all 7 targets + Ab40 monomer (job 8375013)
    target_input_prep: completed  # 2026-05-06, 9CO4_CEG.pdb with 18 hotspots verified
  blockers: none
  notes: "All Stage 0 outputs in place. ColabFold GPU fix applied (jax_plugins/xla_cuda12 registration)."

stage_1:
  name: "BindCraft configuration"
  status: completed  # 2026-05-06
  depends_on: stage_0
  blockers: none
  notes: "Config validated on A100 (job 8375221). Settings: bindcraft/settings/ab42_CEG.json + advanced_ab42.json. 18 hotspots on 3 chains, binder 60-90 aa, 1000 designs."

stage_2:
  name: "1,000 BindCraft designs"
  status: completed  # 2026-05-20 (job 8375335 finished after 14-day walltime)
  depends_on: stage_1
  trajectories_completed: 1342
  mpnn_designs_evaluated: 2977
  designs_accepted: 62
  unique_scaffolds: 38
  acceptance_rate_mpnn: "2.1%"
  acceptance_rate_trajectory: "5.3%"
  campaign_champion: "s453481_mpnn1 (i_pTM=0.85, dG=-102.5)"
  notes: "Exceeded 1000-trajectory target. 62 accepted designs across 38 scaffolds. Full analysis in docs/bindcraft_62design_analysis.md."

stage_3:
  name: "Negative-design counter-screen"
  status: completed  # 2026-05-28, Narval job 61679472 COMPLETED
  depends_on: stage_2
  cluster: narval
  designs_screened: 62
  targets: 8  # 1 positive (9CO4) + 7 negative
  total_runs: 496  # 62 x 8
  designs_pass_positive: 0  # pae_interaction 19-23 on 9CO4 (threshold <10)
  designs_pass_all_negative: 62
  designs_pass_stage3: 0
  gate: "DECISION_GATE_1"
  gate_criterion: ">=20 designs pass positive + negative filters"
  gate_result: "BYPASSED (2026-05-28) — 0/62 pass, but method failure (ColabFold single_sequence produces zero signal for de novo binders). PI decision: trust BindCraft internal metrics, proceed to Stage 4."

stage_4:
  name: "Stability filtering"
  status: completed  # 2026-05-29
  depends_on: stage_3
  cluster: narval + frontenac
  designs_passing: 23  # out of 62
  substeps:
    phase_a_sequence_csv: completed  # 26/62 pass (Cys, charge [-5,+5], ss_pLDDT, binder_pLDDT)
    phase_b_monomer_plddt: completed  # 37/37 pass (26 Narval job 61936182 + 11 Frontenac job 9877164)
    phase_c_sap_buns_cms: completed  # Recalibrated Option B: SAP/res<1.1, BUNS≤7, charge [-8,+5]. 23/62 pass.
  recalibration: "Option B applied (2026-05-29): SAP per-residue<1.1, BUNS≤7, charge [-8,+5]."
  notes: "23/62 survive all filters. Results: filtering/stage4/stage4_final_survivors.csv"

stage_5:
  name: "Ranking and selection"
  status: not_started
  depends_on: stage_4

stage_6:
  name: "Experimental validation (Aβ arm)"
  status: not_started
  depends_on: stage_5
  gate: "DECISION_GATE_2"
  gate_criterion: ">=3 binders with Kd < 500 nM, >=10x selectivity"
  gate_result: pending

stage_7:
  name: "TfR1 arm design (parallel)"
  status: in_progress  # 2026-05-11 started, BUNS fix 2026-05-27
  parallel_with: "stages 2-6"
  cluster: nibi
  target_pdb: "6WRV (chains A+B, apical domain hotspots 208/210/211/212/215)"
  binder_size: "50-70 residues"
  trajectories_completed: 991
  mpnn_designs_evaluated: 791
  designs_accepted: 310  # after BUNS filter disabled (39.2% of MPNN)
  acceptance_rate_mpnn: "39.2%"
  top_candidate: "tfr1_l59_s917497_mpnn2 (i_pTM=0.85, dG=-47.8, SC=0.78)"
  parallel_jobs: "5 resubmitted (14990515-19), continuing toward 1,000 target"
  buns_fix: "Option 1 — BUNS filter disabled in tfr1_filters.json, pyrosetta patch returns 0 instead of 999"
  substeps:
    stage_7.0_target_prep: completed  # 2026-05-11
    stage_7.1_configuration: completed  # 2026-05-11
    stage_7.2_production: in_progress  # 991 traj, 310 accepted, jobs resubmitted toward 1,000
    stage_7.3_counter_screen: bypassed  # 2026-05-28, same method failure as Aβ42 (0/310 pass). One outlier s344619_mpnn13 (ipTM=0.76). PI: trust BindCraft metrics.
    stage_7.4_stability_filtering: completed  # 2026-05-28, 191/326 survive. Top scaffold: s105102.
    stage_7.5_ranking: not_started
  notes: "Tf competition check PASS. BUNS filter (DAlphaBall) crashes on 6WRV due to target size — disabled. All other quality filters (i_pTM, pAE, dG, clashes, packing, SC) remain active."

stage_8:
  name: "Tandem fusion design"
  status: not_started
  depends_on: [stage_6, stage_7]

stage_9:
  name: "Fusion expression + validation"
  status: not_started
  depends_on: stage_8
  gate: "DECISION_GATE_3"
  gate_criterion: ">=1 fusion binds both targets, no aggregation"
  gate_result: pending

stage_10:
  name: "Brain-shuttle proof of concept"
  status: not_started
  depends_on: stage_9
```

## Key metrics (updated as data becomes available)

```yaml
designs_generated: 2977
designs_passing_internal_filters: 62
designs_passing_negative_screen: 0  # Stage 3 COMPLETE: 0/62 pass (method failure suspected)
designs_passing_stability_tfr1: 191  # Stage 7.4 COMPLETE
designs_passing_stability_ab42: 23  # Stage 4 COMPLETE
designs_selected_for_synthesis: 0
designs_expressing_solubly: 0
designs_binding_protofibrils: 0
designs_selective: 0
```

## Decision log

| Date | Decision | Rationale | Decided by |
|------|----------|-----------|------------|
| 2026-04-27 | 9CO4 as primary target | Best-resolved brain-derived Aβ42 Conf 1 structure | PI + Claude |
| 2026-04-27 | 9CKI reclassified as negative target | Conf 2 ≈ plaque (0.22 Å rmsd vs 7Q4B) | PI + Claude |
| 2026-04-27 | Mode 1 lateral binding (Lecanemab logic) | Validated clinical mechanism; lower risk | PI |
| 2026-04-27 | BindCraft as primary design engine | Higher hit rates, implicit conformational selectivity | PI |
| 2026-04-27 | 1,000 designs | Deep pool for aggressive 7-target filtering | PI |
| 2026-05-06 | Chain A ≡ Chain J (one campaign sufficient) | Structural equivalence confirmed by SASA + superposition | Claude Code |
| 2026-05-06 | Deferred N-terminus MD (residues 1–8) | Design against 9CO4 as-is; stretch goal deprioritised | PI |
| 2026-05-06 | Single long-running job, not SLURM array | BindCraft uses internal while loop; array approach from dev plan incompatible | Claude Code |
| 2026-05-26 | Stage 2 complete with 62 designs | 1,342 trajectories exceeded 1,000 target; 62 accepted across 38 scaffolds | Claude Code |
| 2026-05-26 | Git-pull multi-cluster coordination | GitHub repo + cluster env files replace Globus sync messaging; Frontenac coordinates | PI + Claude Code |
| 2026-05-28 | Stage 3 COMPLETE: Gate 1 FAIL (0/62) | ColabFold single_sequence produced pae_interaction 19-23 on ALL targets (positive+negative). ipTM 0.13-0.19 = no signal. Method failure suspected. | Narval |
| 2026-05-27 | Stage 3 counter-screen on Narval | 62 designs x 8 targets, ColabFold single_sequence multimer_v3, job 61679472 | Narval agent |
| 2026-05-27 | Stage 7 TfR1 campaign tracked | Nibi's existing TfR1 work (204 trajectories, 5 jobs) merged into repo | Nibi agent |
| 2026-05-27 | TfR1 BUNS fix: Option 1 (disable filter) | BUNS/DAlphaBall crashes on 6WRV due to target size; disable filter, reprocess → 310 accepted | PI + F |
| 2026-05-27 | TfR1 counter-screen: 2 negative targets sufficient | TfR2 (selectivity) + Tf competition (compatibility); globular target doesn't need 7-target panel like fibril | PI + F |
| 2026-05-27 | Start TfR1 Stage 7.3 with 310 designs | Don't wait for 1,000; counter-screen in parallel with continued production | PI + F |
| 2026-05-28 | TfR1 Stage 7.3 COMPLETE: 0/310 pass | Same method failure as Aβ42. One outlier s344619_mpnn13 (ipTM=0.76). | Nibi |
| 2026-05-28 | Skip counter-screen for both arms | ColabFold single_sequence forward prediction can't validate de novo binders (method failure). Trust BindCraft internal AF2 backprop metrics. Proceed to stability filtering. Selectivity validated experimentally. | PI |
| 2026-05-29 | Stage 4 filter recalibration: Option B | SAP/res<1.1 (fixes PyRosetta normalization), BUNS≤7 (zero unrealistic), charge [-8,+5] (BindCraft Glu-rich skew). 23/62 pass Phase C. | PI |
| 2026-05-28 | ColabFold containerized via Apptainer | colabfold_1.6.1-cuda12.sif replaces conda envs. Wrapper: container/run_colabfold.sh. Validated on Frontenac A100. Shipping to Nibi/Narval via Globus. | PI + F |
