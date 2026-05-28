# HANDOFF — Aβ42 Bispecific Binder Project

> **Read this first.** This is the single-source onboarding document for any new Claude Code session on this project. It tells you what we're building, where we are, what's been decided, and what to watch out for.

---

## 1. Project in one paragraph

We are designing a de novo bispecific miniprotein that binds two targets: (1) the lateral N-terminal surface of receptor-bound Aβ42 filament (Conformation 1, PDB 9CO4) and (2) the TfR1 apical domain for blood-brain barrier transcytosis. The Aβ arm recapitulates Lecanemab's protofibril-selective binding by targeting the N-terminal epitope (Y10/E11/H13/H14/Q15/K16) where Q15's rotamer conformation differs between Conformation 1 and plaque-like fibrils — this is the primary selectivity handle. The design engine is BindCraft (AF2 backpropagation), with designs counter-screened against negative target panels to enforce selectivity. The bispecific format is a tandem miniprotein fusion (Aβ-binder–linker–TfR1-binder, ~130–180 residues, E. coli expression). The project runs across three HPC clusters: Frontenac (coordinator), Narval (Aβ42 counter-screen), and Nibi (TfR1 arm). Both arms are in active counter-screening (Stages 3 and 7.3).

---

## 2. Current status

### Completed
- [x] Structural analysis of 9CO4 (SASA, protofilament partition, chain A vs J equivalence)
- [x] Companion structure discovery (9CKI = plaque-like negative target, 9CK6 = plaque)
- [x] Source paper full review (Kostylev et al. 2025 — PrP^C binds at tips, Conf 2 ≈ plaque)
- [x] Strategy finalised: Lecanemab-logic lateral binding, Mode 1, hotspots Y10/E11/H13/H14/Q15/K16
- [x] HPC environment audit (GPU hardware, SLURM syntax, software inventory)
- [x] CLAUDE.md written (HPC environment reference)
- [x] DEVELOPMENT_PLAN.md written (11-stage plan with decision gates)
- [x] 9CO4, 9CKI, 9CK6 PDBs downloaded
- [x] Project memory system created (HANDOFF.md, PROJECT_STATUS.md, session_log.md)
- [x] Stage 0.2: BindCraft installed — conda env `BindCraft` (Python 3.10, JAX 0.6.0, ColabDesign 1.1.3, PyRosetta 2026.3). GPU-tested on A30 (2026-05-06). AF2 params downloaded.
- [x] Stage 0.3: Counter-target PDBs downloaded (7Q4B, 7Q4M, 6SHS, 1IYT, 9CKI, 9CK6 → structures/negative_targets/)
- [x] Stage 0.4: BindCraft target input prepared (9CO4_CEG.pdb — chains C/E/G, all 18 hotspots verified)
- [x] Stage 0.3: Aβ40 monomer AF2 prediction completed (job 8375013, best model pLDDT=57.1 → Ab40_monomer_af2.pdb)
- [x] **Stage 0 COMPLETE** (2026-05-06)
- [x] Stage 1: BindCraft configuration — settings validated on A100 (job 8375221), all 18 hotspots mapped correctly
- [x] **Stage 1 COMPLETE** (2026-05-06)

- [x] **Stage 2 COMPLETE** (2026-05-20) — 1,342 trajectories, 2,977 MPNN designs, 62 accepted, 38 unique scaffolds. Champion: s453481_mpnn1 (i_pTM=0.85, dG=-102.5). Full analysis: `docs/bindcraft_62design_analysis.md`
- [x] Multi-cluster coordination set up (2026-05-26) — GitHub repo, cluster env files, inbox system, DASHBOARD.md

### In progress
- [x] Stage 3 (Aβ42): Negative-design counter-screen — COMPLETED on Narval (job 61679472). **GATE 1 FAIL: 0/62 pass positive control.** ColabFold single_sequence multimer_v3 produced no signal (pae_interaction 19-23, ipTM 0.13-0.19) on ALL 496 predictions. Systematic method failure suspected — all targets (positive + negative) show identical random-level scores. Method validity needs review before concluding designs don't bind.
- [ ] Stage 7.2 (TfR1): Production run continuing on Nibi — 991 trajectories, 791 MPNN, **310 accepted** (39.2%) after BUNS fix. 5 new jobs (14990515–19) running toward 1,000 target. Top: tfr1_l59_s917497_mpnn2 (i_pTM=0.85).
- [ ] Stage 7.3 (TfR1): Counter-screen tasked to Nibi — 310 designs × 3 targets (TfR1 positive, TfR2 selectivity, Tf compatibility). Runs in parallel with production.

### Not started
- [ ] Stage 4: Stability filtering (Aβ42, after Stage 3 Gate 1)
- [ ] Stage 7.4: Stability + affinity-window filtering (TfR1, 50–200 nM sweet spot)
- [ ] Stages 5–6, 7.5, 8–10: (see DEVELOPMENT_PLAN.md)

---

## 3. Key decisions and their rationale

These are settled — do not revisit unless the PI explicitly asks.

1. **Design engine: BindCraft** (not RFdiffusion) — higher hit rates, implicit conformational discrimination, simpler pipeline. RFdiffusion is the fallback if Gate 1 fails.
2. **Target: 9CO4 Conformation 1** — the only Aβ42 conformation structurally distinct from plaque (1.5 Å rmsd vs 7Q4B).
3. **NOT 9CKI:** Conformation 2 is plaque-equivalent (0.22 Å rmsd vs 7Q4B) — it is a NEGATIVE counter-target.
4. **Binding mode: Mode 1 lateral** (not Mode 3 tip) — follows Lecanemab's validated mechanism and epitope.
5. **Hotspots: Y10/E11/H13/H14/Q15/K16** — the Lecanemab N-terminal epitope region, all exposed on interior chains.
6. **NOT F19/F20:** buried on interior chains (SASA < 2.4 Å²), only exposed at tips — irrelevant for Mode 1.
7. **Q15 rotamer:** the structural switch between Conf 1 and Conf 2 (paper Fig. 5) — the primary selectivity handle.
8. **Bispecific format: Option A tandem miniprotein fusion** — simplest, fastest to express, sufficient for proof of concept.
9. **TfR1 affinity: moderate 50–200 nM** (not high) — high affinity causes lysosomal degradation, not transcytosis.
10. **Number of designs: 1,000** — deep enough pool to survive 7-target negative filtering.
11. **Terminology: "receptor-bound Aβ42 filament"** not "oligomer" — per source paper's explicit argument.
12. **Chain A ≡ Chain J:** structurally equivalent (backbone RMSD 0.001 Å, identical Q15 rotamer) — one BindCraft campaign on interior chains (C/E/G) suffices.
13. **N-terminus MD deferred:** residues 1–8 are disordered in 9CO4; design against the crystal structure as-is. MD ensemble is a stretch goal.
14. **TfR1 BUNS fix: disable filter (Option 1)** — PyRosetta DAlphaBall crashes on 6WRV due to target size (~680 residues). Disabled BUNS in `tfr1_filters.json`, patched pyrosetta_utils.py to return 0. All other quality filters remain active.
15. **TfR1 counter-screen: 2 negatives sufficient** — TfR2 (selectivity) + Tf competition (compatibility). Globular target doesn't need the 7-target panel used for fibril selectivity.
16. **Start TfR1 counter-screen with 310, don't wait for 1,000** — production jobs continue in parallel; counter-screen the existing pool now.

---

## 4. Critical warnings

Things that have gone wrong before or are easy to get wrong:

1. **9CKI IS A NEGATIVE TARGET** — it was initially (incorrectly) proposed as the primary design target in v1 of the status report. This was corrected in v2. Never design against 9CKI.
2. **SLURM requires `--account=def-hpcg6049_gpu`** for ALL GPU jobs. The default account (`def-hpcg6049_cpu`) is CPU-only and GPU requests fail silently with a misleading partition error.
3. **NEVER specify `--partition` in SLURM GPU jobs** — always fails regardless of account. Let the scheduler auto-route.
4. **The source paper** (Kostylev et al. 2025) is a bioRxiv preprint, not yet peer-reviewed.
5. **BindCraft env is `BindCraft` (capital B)** — activate with `conda activate BindCraft`. The installer script fails on Frontenac because it hardcodes `${CONDA_BASE}/envs/BindCraft` but Frontenac puts user envs in `~/.conda/envs/`. Manual step-by-step install works fine.
6. **XLA autotuner warnings on A30 are benign** — JAX 0.6.0 logs "Results do not match the reference" during GEMM fusion autotuning. These are precision comparison warnings during kernel selection, not computation errors. The matmul results are correct.
7. **ColabFold GPU fix (2026-05-06):** The `colabfold` conda env's `jax-cuda12-pjrt` Compute Canada build was missing the `jax_plugins/xla_cuda12/` registration directory. Fixed by `pip install --force-reinstall jax-cuda12-pjrt==0.6.0` inside the env. Without this, ColabFold silently falls back to CPU.
8. **BindCraft is NOT an array job:** The dev plan (Stage 2.1) proposed a 1000-task SLURM array, but BindCraft runs a single while-loop process that generates designs until `number_of_final_designs` is reached. Use one long-running job (14-day wall time), not an array.
9. **PDBFixer multichain bug:** when building multichain PDB inputs, build each chain separately then merge with BioPython — PDBFixer misplaces chains when run on multi-chain inputs directly. Also do not use `-pbc mol` after energy minimisation.
10. **PyRosetta BUNS (DAlphaBall) crashes on large targets:** The `BuriedUnsatHbonds` filter with `dalphaball_sasa=1` crashes on 6WRV (TfR1, ~680 residues). The try/except patch catches the crash but sentinel value (999 or 0) must be handled by filters. This did NOT affect 9CO4 (~130 residues). If designing against other large targets, expect BUNS to fail.

---

## 5. File locations

### This project (Frontenac HPC)

```
/global/project/hpcg6049/protein/alzheimer/
├── CLAUDE.md                    — HPC environment reference
├── DEVELOPMENT_PLAN.md          — 11-stage development plan (authoritative)
├── HANDOFF.md                   — This file (start here for onboarding)
├── PROJECT_STATUS.md            — Machine-readable status tracker
├── structures/                  — PDB files
│   ├── negative_targets/        — Aβ42 counter-targets (9CKI, 9CK6, 7Q4B, 7Q4M, 6SHS, 1IYT, Ab40)
│   └── tfr1/                    — TfR1 structures (6WRV, 1SUV, extracted chains)
├── bindcraft/                   — BindCraft campaigns
│   ├── settings/ab42_CEG.json   — Aβ42 target settings (hotspots, chains, lengths)
│   ├── settings/advanced_ab42.json — Aβ42 advanced settings
│   ├── scripts/run_bindcraft.sh — Aβ42 production SLURM script (14-day A100)
│   ├── input/9CO4_CEG.pdb       — Aβ42 target PDB (chains C/E/G)
│   ├── designs/                 — Aβ42 output (62 accepted, Stage 2 complete)
│   ├── filtering/               — Stage 3 counter-screen (Narval)
│   │   ├── scripts/             — run_counterscreen.sh, prepare_inputs.py, extract_results.py
│   │   ├── inputs/              — ColabFold input CSVs per target
│   │   └── outputs/             — ColabFold results per target
│   └── tfr1/                    — TfR1 arm (Stage 7, Nibi)
│       ├── settings/            — tfr1_AB.json, advanced_tfr1.json, tfr1_filters.json (BUNS disabled)
│       ├── scripts/             — run_tfr1.sh + p1-p4 parallel scripts
│       ├── input/6WRV_apical.pdb — TfR1 target PDB (chains A+B)
│       └── designs/             — TfR1 output (310 accepted from 991 traj)
├── nterm_md/                    — N-terminus MD work (deferred)
│   ├── input/9CO4.pdb
│   ├── prep/                    — Structure preparation files
│   ├── starting_structure/      — Minimised starting structure
│   ├── env/environment_audit.md
│   └── docs/01_setup_report.md
├── env/                         — Environment audit artifacts
│   ├── frontenac_gpu_audit_log.md
│   └── gpu_check_*.out
├── docs/
│   ├── session_log.md           — Running log of all Claude Code sessions
│   ├── bindcraft_62design_analysis.md — Full Aβ42 Stage 2 analysis
│   ├── STAGE7_TFR1_PLAN.md      — TfR1 arm development plan
│   ├── tfr1_tf_competition_check.md — Tf competition structural analysis (PASS)
│   └── tfr1_progress_report.md  — TfR1 progress: 991 traj, 310 accepted, BUNS fix
└── README.md
```

### Prior structural analysis (PI's WSL machine, NOT on HPC)

```
~/structural_analysis_project/
├── structures/9CO4.pdb, 9CKI.pdb, 9CK6.pdb
├── analysis/
│   ├── 9CO4_sasa.csv, 9CKI_sasa.csv, 9CK6_sasa.csv
│   ├── 9CO4_targets.csv (hotspot SASA per chain)
│   ├── 9CO4_pairwise_interfaces.csv
│   ├── 9CO4_faces.json (protofilament partition)
│   ├── chainA_vs_chainJ_hotspot_sasa.csv
│   ├── chainA_vs_chainJ_full_sasa.csv
│   └── chainJ_C2_rotated.pdb
└── docs/
    ├── 9CO4_structural_summary.md
    └── 9CO4_chainA_vs_chainJ.md
```

---

## 6. Maintenance rules for HANDOFF.md

1. After completing any stage or sub-task, update Section 2 (status checklist) immediately. Move items from "Not started" to "In progress" to "Completed" as appropriate.
2. After any major decision change, add a new entry to Section 3 with date and rationale. Do NOT delete old entries — strike them through instead so the decision history is preserved.
3. After any new failure mode or gotcha is discovered, add it to Section 4 (critical warnings).
4. After creating or moving significant files, update Section 5 (file locations).
5. Always update HANDOFF.md BEFORE ending a session, even if the update is just "Stage X step Y completed, no issues."
6. HANDOFF.md is the FIRST file a new session should read. If HANDOFF.md and DEVELOPMENT_PLAN.md disagree on current status, HANDOFF.md is authoritative (it's updated more frequently).
