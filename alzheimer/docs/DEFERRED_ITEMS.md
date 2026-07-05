# Deferred Items — Aβ42 × TfR1 Bispecific Campaign

Backlog of work that is scoped and ready but intentionally **not** being executed yet.
Each entry is self-contained enough to pick up cold. Newest first.

---

## D-1. Complete the 8 missing bispecific-fusion ternary models (12/20 → 20/20)

- **Status:** DEFERRED (noted 2026-07-05). Not started.
- **Origin:** Handed to Frontenac via commit `7e0d74c` — `alzheimer/docs/Prompt — Complete the 8 Missing Bispecific-Fusion Ternary Models`. Companion: `alzheimer/ternary_fusions/` (the 12 already built) + `alzheimer/ternary_fusions/README.md`.
- **Goal:** Build the 8 remaining ternary models so all 20 panel fusions have a "fusion bound to Aβ42 + TfR1" structure + PNG. Chains: **F** = fusion (drug), **A** = Aβ42 (9CO4), **T** = TfR1 apical (6WRV). Aβ side rigorous (co-folded); TfR1 side schematic.

### The 8 missing fusions
```
s843399m18_s255454m5_v2,  s843399m18_s422992m5_v10, s843399m18_s422992m5_v4,
s843399m18_s938332m1_v10, s480128m17_s938332m1_v10, s480128m17_s255454m5_v4,
s311742m16_s422992m5_v4,  s311742m16_s938332m1_v4
```
Why missing: 6 have no committed split-B fusion structure; 2 (s311742) lack the Aβ-arm docked complex.

### Inputs available on Frontenac (no local package needed)
- `alzheimer/bindcraft/fusion/stage9/synthesis_panel.csv` — source of the 8 fusion sequences (construct/fusion-protein column). Append 3× Aβ42(9–42) target `GYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVVIA` to each to form the ColabFold complex input.
- `alzheimer/bindcraft/tfr1/input/6WRV_apical.pdb` — TfR1 apical domain for chain T.
- `alzheimer/ternary_fusions/*.pdb` (the existing 12) — match their annotation/format/render style.
- NOTE: the prompt's "ready-to-run package" (`~/Documents/Bindlix/final_fusions_July4/t/to_run_on_hpc/` with pre-made `inputs/` + `run_missing_colabfold.sh`) is on a **local machine, not on Frontenac**. Either copy it over, or regenerate inputs from the panel CSV (fallback documented in the prompt).

### Pipeline to run when un-deferred
1. Build `ternary_missing/inputs/<id>_plus_Abeta.fasta` for each of the 8 (fusion : Aβ42 : Aβ42 : Aβ42).
2. ColabFold 8-task A100 array — match original fusion run: `--num-models 1 --num-recycle 3 --msa-mode single_sequence --model-type alphafold2_multimer_v3`. SLURM: `--account=def-hpcg6049_gpu --gres=gpu:a100:1`, NO `--partition`, `conda activate colabfold`, absolute paths. Outputs → `outputs/<id>_plus_Abeta/*rank_001*.pdb`.
3. Assemble ternary per fusion: keep co-folded fusion+Aβ as chains F/A; add 6WRV apical schematically as chain T (hotspots A208/210/211/212/215 facing the TfR1 arm, min interdomain dist > 3 Å); write annotated PDB (HEADER/TITLE/COMPND/SEQRES/REMARK — Aβ rigorous, TfR1 schematic, binding sequential in vivo).
4. Render per-chain PNG (F=blue, A=orange, T=green; cartoon + light VDW, dark bg).
5. Drop 8 `ternary_<id>.pdb` + `.png` into `alzheimer/ternary_fusions/`, update its README to 20/20, commit + push.

### Honesty caveats (carry into any output)
- Aβ42 side = rigorous (co-folded); TfR1 side = schematic (illustrative, not a computed dock).
- "Bound to both at once" is illustrative — in vivo binding is sequential (TfR1 at BBB, then Aβ in brain).
- `alphafold2_multimer_v3` approximates, not necessarily reproduces, the BindCraft-designed dock.

---

## D-2. Aβ42 N-terminus production MD

- **Status:** DEFERRED. Prep done; production MD not started. See project memory `project_alzheimer_nterm_md.md` for the prepared inputs and the PDBFixer multichain-build gotcha.
