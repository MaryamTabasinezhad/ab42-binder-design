# HANDOFF — Aβ42 Bispecific Binder Project

> **Read this first.** This is the single-source onboarding document for any new Claude Code session on this project. It tells you what we're building, where we are, what's been decided, and what to watch out for.

---

## 1. Project in one paragraph

We are designing a de novo bispecific miniprotein that binds two targets: (1) the lateral N-terminal surface of receptor-bound Aβ42 filament (Conformation 1, PDB 9CO4) and (2) the TfR1 apical domain for blood-brain barrier transcytosis. The Aβ arm recapitulates Lecanemab's protofibril-selective binding by targeting the N-terminal epitope (Y10/E11/H13/H14/Q15/K16) where Q15's rotamer conformation differs between Conformation 1 and plaque-like fibrils — this is the primary selectivity handle. The design engine is BindCraft (AF2 backpropagation), with 1,000 designs counter-screened against 7 negative targets (plaque fibrils, monomers, Aβ40) to enforce conformational selectivity. The bispecific format is a tandem miniprotein fusion (Aβ-binder–linker–TfR1-binder, ~130–180 residues, E. coli expression). The project is currently at the very beginning of Stage 0: the HPC environment has been audited and documented, the development plan is written, but BindCraft is not yet installed.

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
- [ ] Stage 3: Negative-design counter-screen — running on Narval (job 61679472, array 0-7). 62 designs × 8 targets = 496 ColabFold runs. Gate 1: ≥20 designs must pass.

### Not started
- [ ] Stage 4: Stability filtering
- [ ] Stages 5–10: (see DEVELOPMENT_PLAN.md)

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

---

## 5. File locations

### This project (Frontenac HPC)

```
/global/project/hpcg6049/protein/alzheimer/
├── CLAUDE.md                    — HPC environment reference
├── DEVELOPMENT_PLAN.md          — 11-stage development plan (authoritative)
├── HANDOFF.md                   — This file (start here for onboarding)
├── PROJECT_STATUS.md            — Machine-readable status tracker
├── structures/                  — PDB files (to be populated)
│   └── negative_targets/        — Counter-target PDBs (to be populated)
├── bindcraft/                   — BindCraft campaign
│   ├── settings/ab42_CEG.json   — target settings (hotspots, chains, lengths)
│   ├── settings/advanced_ab42.json — advanced settings (iterations, weights, MPNN)
│   ├── scripts/run_bindcraft.sh — production SLURM script (14-day A100)
│   ├── input/9CO4_CEG.pdb       — target PDB (chains C/E/G)
│   └── designs/                 — output (populated by Stage 2)
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
│   └── session_log.md           — Running log of all Claude Code sessions
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
