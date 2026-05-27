# Project Status Tracker

Last updated: 2026-05-26T23:00
Updated by: Claude Code — Stage 2 completion + multi-cluster setup

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
  status: not_started
  depends_on: stage_2
  gate: "DECISION_GATE_1"
  gate_criterion: ">=20 designs pass positive + negative filters"
  gate_result: pending

stage_4:
  name: "Stability filtering"
  status: not_started
  depends_on: stage_3

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
  status: not_started
  parallel_with: "stages 2-6"

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
designs_passing_negative_screen: 0  # Stage 3 not started
designs_passing_stability: 0
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
