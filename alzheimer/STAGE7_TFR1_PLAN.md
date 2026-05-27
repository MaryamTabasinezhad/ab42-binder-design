# Stage 7 — TfR1 Arm Development Plan

> **Version 1 · 2026-05-11**
> **For Claude Code:** This document details Stage 7 of the bispecific binder project. Read alongside `CLAUDE.md` (HPC reference), `HANDOFF.md` (project context), and `DEVELOPMENT_PLAN.md` (master plan). This document is authoritative for all TfR1-arm-specific decisions.

---

## Summary

Design a de novo miniprotein binder targeting human transferrin receptor 1 (TfR1) for BBB transcytosis. This is the second arm of the bispecific tandem fusion. The TfR1 arm runs in parallel with the Aβ arm (Stages 2–6) and merges at Stage 8 (fusion design).

---

## Design specification

| Parameter | Value |
|---|---|
| **Target PDB** | 6WRV — crystal structure of de novo binder 3DS18 in complex with human TfR1 ectodomain (Sahtoe et al., PNAS 2020) |
| **Target chain** | Chain A (hTfR1 ectodomain, residues 121–759 of UniProt P02786) |
| **Chains to REMOVE before design** | Chains C, D, F (the existing designed binder 3DS18 — must be stripped; we're designing a NEW binder) |
| **Context chains (keep for steric context)** | Chain B and/or E (TfR1 homodimer partners) — include as context so BindCraft avoids designing into the dimer interface |
| **Hotspot residues** | **208, 210, 211, 212, 215** on chain A |
| **Binder size** | 50–70 residues |
| **Number of designs** | 1,000 |
| **Design engine** | BindCraft |
| **Affinity target** | **50–200 nM (MODERATE)** — see critical note below |
| **Key constraint 1** | Must NOT compete with transferrin (Tf) binding — verify by checking overlap between hotspot residues and the known Tf-TfR1 interface |
| **Key constraint 2** | Monovalent presentation in the final bispecific — avoid bivalent TfR1 engagement (causes receptor crosslinking → lysosomal degradation) |

### CRITICAL: Affinity tuning

> **Do NOT optimise for maximum affinity.** High-affinity TfR1 binders (K_D < 10 nM) are sorted to lysosomes and degraded — they do NOT cross the BBB. Moderate affinity (50–200 nM) allows transcytosis and release on the brain side. This is established by Yu et al. (*Sci Transl Med* 2011) and the Roche brain-shuttle / Denali ETV literature.
>
> **In practice:** during filtering (Stage 7.4), designs with predicted pae_interaction scores suggesting very tight binding should be treated as MARGINAL, not top-ranked. The ranking function should have a sweet-spot penalty — designs predicted to bind too tightly are deprioritised.
>
> **Reference:** The existing 3DS18 binder in 6WRV binds at 20 nM. For a brain-shuttle therapeutic, this is borderline too tight. Our target is 2.5–10× weaker than 3DS18.

### Transferrin competition check (MANDATORY before production run)

The Tf-TfR1 binding interface involves contacts on the TfR1 helical domain and protease-like domain. Before running 1,000 designs, verify:

1. Map hotspot residues 208/210/211/212/215 onto the TfR1 structure.
2. Compare their positions to the known Tf binding interface (reference: PDB 1SUV, Tf-TfR complex; also Eckenroth et al., PNAS 2011).
3. If ANY hotspot residue is within 5 Å of a Tf contact residue, FLAG it — the binder may compete with Tf for TfR1 binding, which would cause iron-homeostasis toxicity.
4. The Baker lab 3DS18 binder was validated as NOT competing with Tf (it targets the apical domain). Confirm whether your hotspot residues are at the same site as 3DS18 or at a different site.

If the hotspots overlap with the Tf interface, we need to either (a) shift the hotspots away from Tf contacts, or (b) accept the competition risk and plan a Tf-competition SPR experiment early.

---

## Stage 7 substeps

### 7.0 — Target preparation

**Duration:** 0.5 days
**Compute:** None

1. Download 6WRV.pdb to `/global/project/hpcg6049/protein/alzheimer/structures/tfr1/6WRV.pdb`.
2. Extract chain A only (TfR1 ectodomain) → `6WRV_chainA.pdb`.
3. Extract chain A + chain B (homodimer context) → `6WRV_chainA_B.pdb`.
4. **Remove chains C, D, F** (the existing 3DS18 binder) from all target files. BindCraft must design a NEW binder, not rediscover the existing one.
5. Verify hotspot residues 208, 210, 211, 212, 215 are present and well-resolved in chain A. Print their residue names and B-factors.
6. Run the transferrin competition check (see above). Save the analysis to `docs/tfr1_tf_competition_check.md`.

**Output files:**
```
structures/tfr1/
├── 6WRV.pdb                    (full PDB, for reference only)
├── 6WRV_chainA.pdb             (TfR1 ectodomain only)
├── 6WRV_chainA_B.pdb           (TfR1 homodimer, for steric context)
└── 6WRV_target.pdb             (final BindCraft input — chain A, or A+B as context)
```

> **Decision needed:** Should BindCraft see chain A alone, or chains A+B as context? Including chain B prevents the designed binder from docking into the TfR1 homodimer interface (which is buried in vivo). **Recommendation: include chain B as context, with only chain A residues in the binding-site definition.**

### 7.1 — BindCraft configuration

**Duration:** 0.5 days
**Compute:** None

| Parameter | Value | Notes |
|---|---|---|
| `target_pdb` | `6WRV_target.pdb` | Chain A (+ B as context) |
| `target_chains` | `A` (binding site) + `B` (context, no binding site) | Binder contacts chain A only |
| `binding_site` | `A:208,A:210,A:211,A:212,A:215` | 5 hotspot positions |
| `binder_len` | 50–70 (sampled uniformly per design) | Smaller than Aβ arm — less surface needed |
| `num_designs` | 1,000 total (one per SLURM array task) | Seeds 1–1000 |
| `af2_model` | `model_1_ptm` | Same as Aβ campaign |
| `recycles` | 3 | Default |
| `design_iterations` | 50 | Default |
| Internal filters | pLDDT > 80, pae_interaction < 12, i_pTM > 0.6 | Same as Aβ campaign |

> **Note:** Exact CLI flags depend on the BindCraft version installed in Stage 0. Adapt parameter names to match the actual CLI/config after installation.

### 7.2 — Production run (1,000 designs)

**Duration:** 5–15 days wallclock
**Compute:** ~170–350 GPU-hours on A100

Shorter binders (50–70 aa) converge faster than the Aβ arm's 60–90 aa designs, so per-design time is ~10–20 min on A100 (vs 20–30 for Aβ).

#### SLURM template

```bash
#!/bin/bash
#SBATCH --job-name=bc_tfr1
#SBATCH --output=bindcraft/tfr1/logs/design_%a.out
#SBATCH --error=bindcraft/tfr1/logs/design_%a.err
#SBATCH --account=def-hpcg6049_gpu
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:a100:1
#SBATCH --mem=32G
#SBATCH --array=1-1000%20

set -eo pipefail
eval "$(conda shell.bash hook)"
conda activate bindcraft

SEED=$SLURM_ARRAY_TASK_ID
OUTDIR=/global/project/hpcg6049/protein/alzheimer/bindcraft/tfr1/designs/design_$(printf '%04d' $SEED)
mkdir -p $OUTDIR

# === ADAPT TO MATCH INSTALLED BINDCRAFT CLI ===
python /global/project/hpcg6049/protein/alzheimer/bindcraft/repo/bindcraft.py \
  --target_pdb /global/project/hpcg6049/protein/alzheimer/bindcraft/tfr1/input/6WRV_target.pdb \
  --target_chains A \
  --binding_site A:208,A:210,A:211,A:212,A:215 \
  --binder_len $(shuf -i 50-70 -n1) \
  --seed $SEED \
  --output_dir $OUTDIR
# === END ADAPT SECTION ===

echo "TfR1 design $SEED completed on $(hostname) at $(date)"
```

> **SLURM rules (from CLAUDE.md):**
> - Always `--account=def-hpcg6049_gpu`
> - NEVER `--partition`
> - NEVER `-w` (node targeting)
> - Absolute paths everywhere
> - `eval "$(conda shell.bash hook)"` before `conda activate`

#### Compute budget

| Item | Estimate |
|---|---|
| Per-design GPU time | 10–20 min on A100 (shorter binder = faster) |
| Total GPU-hours | 170–350 hrs for 1,000 designs |
| Concurrent tasks | 20 (array throttle) |
| Wallclock (realistic) | 5–15 days |
| Storage per design | ~5–10 MB |
| Total storage | ~5–10 GB |

#### Post-run sweep

Same protocol as the Aβ campaign:
1. Count completed designs (check for output PDB in each directory).
2. List failed seeds.
3. Resubmit failures.
4. Write `bindcraft/tfr1/logs/stage7_2_summary.md`.

### 7.3 — Negative-design counter-screen

**Duration:** 1–3 days
**Compute:** ~50–100 GPU-hours

The TfR1 arm has a different negative panel than the Aβ arm. The goal is to ensure the binder is specific to TfR1 and does not bind off-target proteins or compete with transferrin.

#### Counter-target panel

| Counter-target | Source | Why |
|---|---|---|
| Tf-loaded TfR1 complex | PDB 1SUV (or 3S9N) | Binder must NOT displace Tf — verify steric compatibility |
| TfR2 (transferrin receptor 2) | AF2 prediction or PDB 3KAS | TfR1 selectivity — TfR2 has different tissue distribution |
| Apo-TfR1 vs holo-TfR1 | Both from PDB or AF2 | Confirm binder works on both iron-loaded and unloaded states |

> **Note:** This is a smaller panel than the Aβ arm's 7 targets. The primary risk for TfR1 is Tf competition, not multi-conformer selectivity.

#### Protocol

1. For each candidate that passes BindCraft's internal filters, run ColabFold complex prediction with the binder + each counter-target.
2. **Tf competition test:** dock the binder onto TfR1 in the context of the Tf-TfR1 complex (1SUV). If the binder clashes with Tf (overlapping predicted contacts), reject it.
3. **TfR2 selectivity:** predict binder + TfR2 complex. Reject if `pae_interaction < 15` (binds TfR2).

### 7.4 — Stability and affinity-window filtering

**Duration:** 1–2 days
**Compute:** CPU only

Same stability filters as the Aβ arm (SAP, buried unsatisfied H-bonds, Cys check, charge, Tm, polar CMS, monomer fold confidence — see DEVELOPMENT_PLAN.md Stage 4 for thresholds).

**PLUS the affinity-window filter:**

| Metric | Target range | Action if out of range |
|---|---|---|
| Predicted binding strength (pae_interaction on TfR1) | 8–12 (sweet spot) | < 8: **DEPRIORITISE** (too tight, lysosomal trafficking risk) |
| | | > 12: reject (too weak) |

> **This is the opposite of the Aβ arm,** where lower pae_interaction is always better. For TfR1, there is a SWEET SPOT. Rank designs by distance from the centre of the 8–12 pae_interaction window, not by raw value.

### 7.5 — Ranking and selection

**Duration:** 1 day
**Compute:** None

Rank surviving designs by composite score:

| Metric | Weight | Direction |
|---|---|---|
| Distance from pae_interaction sweet spot (8–12) | 0.30 | Closer to centre is better |
| Tf competition margin (steric clash score) | 0.25 | Higher clearance from Tf is better |
| Binder pLDDT | 0.15 | Higher is better |
| SAP score | 0.10 | Lower is better |
| Predicted Tm | 0.10 | Higher is better |
| Structural diversity bonus | 0.10 | Reward under-represented clusters |

**Selection:**
- Select **top 30 designs** for synthesis.
- Max 5 per backbone cluster.
- Include 2 deliberate high-affinity designs (pae_interaction < 8) as controls — to test experimentally whether the affinity-window hypothesis holds for this specific binding site.

### 7.6 — Experimental validation (TfR1 arm)

**Duration:** 2–4 months
**Gate:** Feeds into Stage 8 (fusion design)

#### Expression and biophysics

1. Gene synthesis of 30 designs + 2 high-affinity controls, codon-optimised for E. coli.
2. Expression in BL21(DE3), 1 mL auto-induction.
3. SEC-MALS: monodispersity, expected MW.
4. Thermal stability: nanoDSF or CD — confirm Tm > 60°C.

#### Binding validation

1. **TfR1 binding:** SPR/BLI with TfR1 ectodomain. Measure K_D, k_on, k_off.
   - Target: K_D = 50–200 nM
   - Flag any binder with K_D < 10 nM (too tight for transcytosis)
2. **Tf competition:** SPR with Tf-loaded TfR1 and with Tf + TfR1 + binder. Confirm binder does NOT displace Tf.
3. **TfR1/TfR2 selectivity:** SPR with TfR2 ectodomain. Confirm ≥ 10-fold selectivity for TfR1.

#### Optional: transcytosis pilot

If an in vitro BBB model is available (hCMEC/D3 or iPSC-derived brain endothelial cells):
- Test top 3 TfR1 binders for basolateral accumulation.
- Compare to 3DS18 (the existing Baker lab binder from 6WRV, K_D = 20 nM) as positive control.
- This is not required for Stage 8 but gives early signal on brain-shuttle function.

#### Gate for fusion advancement

No formal gate number (the TfR1 arm feeds into Stage 8 via the master plan). Minimum requirement to advance:
- **≥ 2 binders** with K_D 50–200 nM, no Tf competition, soluble expression, Tm > 60°C.

---

## Directory layout

```
/global/project/hpcg6049/protein/alzheimer/
├── structures/
│   └── tfr1/
│       ├── 6WRV.pdb                     (full PDB reference)
│       ├── 6WRV_chainA.pdb              (TfR1 ectodomain only)
│       ├── 6WRV_chainA_B.pdb            (TfR1 homodimer)
│       └── 6WRV_target.pdb              (BindCraft input)
├── bindcraft/
│   ├── abeta/                           (Aβ campaign — Stage 2)
│   │   ├── input/
│   │   ├── designs/
│   │   ├── filtering/
│   │   ├── logs/
│   │   └── scripts/
│   └── tfr1/                            (TfR1 campaign — this plan)
│       ├── input/
│       │   └── 6WRV_target.pdb
│       ├── designs/
│       │   └── design_0001/ ... design_1000/
│       ├── filtering/
│       │   ├── stage7_3_negative_screen.csv
│       │   ├── stage7_4_stability.csv
│       │   └── stage7_5_panel.csv
│       ├── logs/
│       │   ├── design_1.out ... design_1000.out
│       │   └── stage7_2_summary.md
│       └── scripts/
│           └── run_tfr1_designs.sh
└── docs/
    └── tfr1_tf_competition_check.md
```

---

## How this connects to the master plan

| Master plan stage | TfR1 equivalent | Notes |
|---|---|---|
| Stage 2 (Aβ designs) | Stage 7.2 (TfR1 designs) | Run in parallel |
| Stage 3 (Aβ negative screen) | Stage 7.3 (TfR1 negative screen) | Different counter-panel |
| Stage 4 (Aβ stability) | Stage 7.4 (TfR1 stability + affinity window) | Extra affinity-window filter |
| Stage 5 (Aβ ranking) | Stage 7.5 (TfR1 ranking) | Different ranking weights (sweet-spot vs lower-is-better) |
| Stage 6 (Aβ wet lab) | Stage 7.6 (TfR1 wet lab) | Different assays (Tf competition, TfR2 selectivity) |
| Stage 8 (fusion) | Both arms merge | Top Aβ × top TfR1 → tandem fusion candidates |

---

## Key differences from the Aβ campaign

| Aspect | Aβ arm | TfR1 arm |
|---|---|---|
| Affinity goal | As tight as possible | Sweet spot: 50–200 nM |
| Binder size | 60–90 residues | 50–70 residues |
| Hotspots | 6 residues × 3 chains = 18 positions | 5 residues × 1 chain = 5 positions |
| Negative panel | 7 targets (plaque selectivity) | 3 targets (Tf competition + TfR2 selectivity) |
| Ranking | Lower pae_interaction = better | Distance from sweet spot = better |
| Key risk | Plaque binding (selectivity failure) | Tf competition OR too-tight binding (trafficking failure) |
| Existing precedent | Lecanemab (antibody, different format) | 3DS18 from 6WRV (de novo miniprotein, same format, same target site) |

---

## Maintenance

When this stage progresses, update:
1. `HANDOFF.md` Section 2 (status checklist) — add TfR1-specific line items
2. `PROJECT_STATUS.md` — update `stage_7` substeps and metrics
3. `docs/session_log.md` — log each session that works on TfR1
4. This file — update substep statuses inline as they complete

---

## Appendix: Reference structures for TfR1

| PDB | Description | Use in this plan |
|---|---|---|
| 6WRV | 3DS18 de novo binder + TfR1 ectodomain | **Primary target** (strip binder, keep TfR1) |
| 6WRW | 2DS25.5 binder + TfR1 (related design) | Reference for alternative binding modes |
| 6WRX | 2DS25.1 binder + TfR1 (related design) | Reference for alternative binding modes |
| 1SUV | Tf-TfR1 complex (cryo-EM) | **Tf competition check** |
| 3KAS | TfR2 ectodomain | **TfR2 selectivity counter-target** |
| 6OKD | Cystine-dense peptide + TfR1 | Reference for alternative TfR1 binding site |

The Sahtoe et al. paper (PNAS 2020) reports 3DS18 binds TfR1 at 20 nM, is hyperstable, and crosses an in vitro microfluidic BBB model. This validates the 6WRV binding site for brain-shuttle applications.
