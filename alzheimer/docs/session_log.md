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
