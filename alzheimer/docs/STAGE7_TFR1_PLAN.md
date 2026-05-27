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

1. Download 6WRV.pdb.
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

### 7.2 — Production run (1,000 designs)

**Duration:** 5–15 days wallclock
**Compute:** ~170–350 GPU-hours on H100

### 7.3 — Negative-design counter-screen

**Duration:** 1–3 days
**Compute:** ~50–100 GPU-hours

### 7.4 — Stability and affinity-window filtering

**Duration:** 1–2 days
**Compute:** CPU only

### 7.5 — Ranking and selection

**Duration:** 1 day
**Compute:** None

### 7.6 — Experimental validation (TfR1 arm)

**Duration:** 2–4 months
**Gate:** Feeds into Stage 8 (fusion design)

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
