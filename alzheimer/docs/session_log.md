# Session Log

## Session 1 — 2026-04-27 (WSL, not HPC)
**Machine:** hamid@Hamid (WSL)
**Work done:**
- Structural analysis of 9CO4: per-chain SASA, protofilament partition,
  companion structure discovery (9CKI, 9CK6)
- Output: ~/structural_analysis_project/docs/9CO4_structural_summary.md

## Session 2 — 2026-05-06 (WSL, not HPC)
**Machine:** hamid@Hamid (WSL)
**Work done:**
- Chain A vs chain J tip equivalence analysis
- Conclusion: structurally equivalent; one design campaign sufficient
- Output: ~/structural_analysis_project/docs/9CO4_chainA_vs_chainJ.md

## Session 3 — 2026-05-06 (Frontenac HPC)
**Machine:** hpc6049@login2 (Frontenac)
**Work done:**
- GPU environment audit (all GPU types, SLURM syntax, software inventory)
- Created CLAUDE.md with full HPC reference
- Output: CLAUDE.md, env/frontenac_gpu_audit_log.md

## Session 4 — 2026-05-06 (Frontenac HPC)
**Machine:** hpc6049@login2 (Frontenac)
**Work done:**
- Created project memory system (HANDOFF.md, PROJECT_STATUS.md, session_log.md)
- Added maintenance rules to CLAUDE.md

## Session 5 — 2026-05-06 (Frontenac HPC)
**Machine:** hpc6049@login2 (Frontenac)
**Work done:**
- Stage 0.2: BindCraft installation — manual install (installer script fails on Frontenac due to conda env path). Conda env `BindCraft` with Python 3.10, JAX 0.6.0, ColabDesign 1.1.3, PyRosetta 2026.3. GPU-tested on A30 node (frnt147). AF2 params downloaded (5.1 GB).
- Stage 0.3: Downloaded 6 counter-target PDBs (7Q4B, 7Q4M, 6SHS, 1IYT, 9CKI, 9CK6). Aβ40 monomer AF2 prediction submitted (job 8374791, running).
- Stage 0.4: Extracted chains C/E/G from 9CO4 → bindcraft/input/9CO4_CEG.pdb. All 18 hotspot positions verified.
- Updated CLAUDE.md (BindCraft env info), HANDOFF.md, PROJECT_STATUS.md.
- Gotcha discovered: BindCraft installer assumes envs live under `${CONDA_BASE}/envs/` but Frontenac puts them in `~/.conda/envs/`.

## Session 6 — 2026-05-06 (Frontenac HPC)
**Machine:** hpc6049@login2 (Frontenac)
**Work done:**
- Stage 0 completed: Aβ40 monomer prediction finished (job 8375013, 2m12s on GPU). Fixed ColabFold GPU detection — `jax-cuda12-pjrt` Compute Canada build was missing `jax_plugins/xla_cuda12/` registration dir. Previous job (8374791) had timed out running on CPU.
- Stage 1 completed: Created BindCraft config files (ab42_CEG.json, advanced_ab42.json). Validated on A100 (job 8375221) — 18 hotspots mapped correctly, 102-residue target + 75-residue binder = 177 total, well within 40GB VRAM.
- Key insight: Dev plan proposed 1000-task SLURM array but BindCraft runs as a single while-loop process. Changed to one long-running 14-day job.
- Production SLURM script ready: bindcraft/scripts/run_bindcraft.sh (awaiting submission).

## Session 7 — 2026-05-28 (Frontenac HPC)
**Machine:** hpc6049 (Frontenac)
**Work done:**
- Full project status review: read all ~35 markdown files across the repo
- Processed all inbox messages: Narval Stage 3 COMPLETE (0/62 pass, method failure), Nibi Stage 7.3 COMPLETE (0/310 pass, same failure), Nibi counter-screen resubmission notice
- **PI Decision: Skip computational counter-screen for both arms.** ColabFold single_sequence multimer_v3 is a method failure for de novo binders (uniformly pae 19-23, ipTM 0.13-0.19). Trust BindCraft internal AF2 backprop metrics. Selectivity validated experimentally via SPR.
- **ColabFold containerized via Apptainer.** Built and validated `colabfold_1.6.1-cuda12.sif` on Frontenac A100 (8 iterations of debugging: bind mount issues, read-only cache, TLS cert leak from ~/.local, missing param marker files). Created wrapper `container/run_colabfold.sh` and setup script `container/setup_colabfold_container.sh`.
- Updated all cluster .env files with container variables (COLABFOLD_SIF, COLABFOLD_CACHE, APPTAINER_MODULE)
- Sent inbox messages to Nibi and Narval with decisions, container setup instructions, and new assignments (Narval → Stage 4 stability filtering, Nibi → continue production + Stage 7.4)
- Updated HANDOFF.md (decisions 17-18, status sections), PROJECT_STATUS.md (bypassed stages, decision log), DASHBOARD.md (campaign status, cluster table, recent actions)
- Initiated Globus transfer of container + AF2 param cache (~8.6 GB) to Nibi and Narval
- Updated memory system: container reference, fast-onboarding guide, campaign status, fixed stale memories
- Deleted 3 processed inbox messages from Frontenac
