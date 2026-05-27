# Aβ42 Bispecific Binder Development Plan

> **Version 1 · 2026-05-06**
> **For Claude Code:** This document is the authoritative development plan for the Alzheimer's binder project. Read this alongside `CLAUDE.md` (HPC environment reference) before executing any stage. If any instruction here conflicts with `CLAUDE.md`, follow `CLAUDE.md` for HPC-specific details (accounts, SLURM syntax, paths) and this document for scientific/design decisions.

---

## Project summary

**Goal:** Design a de novo bispecific miniprotein binder with two arms:
1. **Aβ arm** — binds the lateral N-terminal surface of receptor-bound Aβ42 filament (Conformation 1, PDB 9CO4), recapitulating Lecanemab's protofibril-selective binding profile
2. **TfR1 arm** — binds transferrin receptor 1 at the apical domain (moderate affinity, 50–200 nM) for BBB transcytosis

**Format:** Tandem miniprotein fusion (Aβ-binder–linker–TfR1-binder), single-chain, E. coli expression. Total ~130–180 residues.

**Design engine:** BindCraft (Pacesa et al., *Nature* 2024) — AF2 backpropagation-based binder design.

**Fallback engine:** RFdiffusion → ProteinMPNN → AF2 pipeline (environments already on Frontenac: `rfd_clean`, `mpnn`, `colabfold`).

**HPC:** Frontenac (CAC, Queen's University). User `hpc6049`. See `CLAUDE.md` for all SLURM details.

**Source paper:** Kostylev MA, Butan C, Roseman GP, Liu Y, Gopal P, Strittmatter SM. *Distinct Filament Conformation for Receptor-Bound Amyloid-β from Alzheimer's Disease Brain.* bioRxiv 2025.10.10.681740.

**PI:** Hamid Ghaedi

---

## Design specification

This is the authoritative spec for the Aβ arm. Every stage references this table.

| Parameter | Value |
|---|---|
| **Primary design target** | PDB 9CO4 — receptor-bound Aβ42 filament, Conformation 1, 2.8 Å |
| **Target chains for BindCraft** | Chains C, E, G of protofilament 1 (interior chains — avoid end-chain artifacts) |
| **Binding mode** | Mode 1 — lateral protofilament binding across the N-terminal epitope |
| **Hotspot residues** | Y10, E11, H13, H14, Q15, K16 on each of chains C, E, G (18 positions total; BindCraft uses as binding-site definition) |
| **Design constraint** | Paratope must complement the **Conformation-1 Q15 rotamer surface** (this is the structural switch between Conf 1 and plaque-like Conf 2 — see source paper Fig. 5) |
| **Binder size** | 60–90 residues (sampled uniformly per design) |
| **Number of designs** | 1,000 |
| **Design engine** | BindCraft |
| **Positive AF2 filter** | `pae_interaction < 10` on 9CO4 |
| **Negative AF2 filter** | `pae_interaction > 15` on ALL 7 counter-targets (see below) |
| **Stability filters** | SAP < 0.10 on non-paratope surface; 0 buried unsatisfied H-bonds; 0 unpaired Cys; net charge −2 to +4; predicted Tm > 60°C; polar CMS fraction > 40%; AF2 monomer pLDDT > 85 |
| **Selectivity basis** | Conformational — Q15 rotamer + N-terminal presentation differs between Conf 1 and plaque. This is the Lecanemab mechanism. |
| **Mechanism of action** | Protofibril-selective N-terminal recognition and clearance |

### Negative counter-target panel (7 targets)

Every binder candidate must be counter-screened against all 7. A candidate that scores `pae_interaction < 15` on ANY of these is rejected.

| Counter-target | PDB / source | Why |
|---|---|---|
| 9CKI | Conf 2 receptor-bound Aβ42 | Plaque-equivalent (0.22 Å rmsd vs 7Q4B) — **CRITICAL: this was initially misidentified as a design target in the v1 status report; it is a NEGATIVE target** |
| 9CK6 | Sarkosyl-insoluble Aβ42 plaque (same brain as 9CO4) | Direct plaque fibril from the source paper |
| 7Q4B | Brain Aβ42 plaque type I fibril | Canonical plaque reference (Yang et al., Science 2022) |
| 7Q4M | Brain Aβ42 plaque type II fibril | Second plaque polymorph |
| 6SHS | Aβ40 fibril (CAA-relevant) | ARIA risk reduction — avoid binding CAA deposits |
| 1IYT | Aβ42 monomer (NMR) | Assembly-state selectivity — don't bind monomer |
| Aβ40 monomer | ColabFold AF2 prediction | Isoform selectivity — don't bind Aβ40 |

### Key structural facts (from prior analysis)

These are established facts from the Claude Code structural analysis (2026-04-27) and the source paper. Do NOT re-derive them; use them as given.

- 9CO4 has 10 chains (A–J), modeled residues 9–42 per chain, no internal gaps. Residues 1–8 are disordered.
- The assembly is two parallel protofilaments: **PF1 = {A, C, E, G, I}** and **PF2 = {B, D, F, H, J}**. Intra-PF interfaces ~2,650 Å² each; inter-PF contacts ~245 Å².
- Helical parameters: ΔZ = 2.355 Å, ΔΦ = 178.164°, C1 axial symmetry.
- All 6 hotspot residues (Y10, E11, H13, H14, Q15, K16) are EXPOSED (SASA > 40 Å²) on every chain in 9CO4, 9CKI, and 9CK6 across all conformations.
- Chain A and chain J (opposite tips) are structurally equivalent (fitted backbone RMSD = 0.001 Å, identical Q15 rotamer χ2 = −162.4°). One BindCraft campaign on interior chains suffices.
- Conformation 2 (9CKI) is structurally indistinguishable from plaque fibrils (0.22 Å rmsd vs 7Q4B). It is a NEGATIVE target, not a design target.
- The Q15 sidechain rotamer is the structural switch between Conf 1 and Conf 2 (paper Fig. 5). In Conf 1, Q15 makes inter-protofilament H-bonds to G38/amino terminus of the opposing chain. In Conf 2, it does not.

---

## Stages

### Stage 0 — Environment setup and BindCraft installation

**Duration:** 1–2 days
**Compute:** Login node + 1 short GPU test job
**Decision gate:** None

#### 0.1 Prerequisites already completed

- [x] HPC environment audit — `CLAUDE.md` populated (2026-05-06)
- [x] GPU hardware confirmed: A100-PCIE-40GB (40 GB VRAM, sufficient for BindCraft)
- [x] SLURM syntax confirmed: `--account=def-hpcg6049_gpu --gres=gpu:a100:1`, NO `--partition` flag
- [x] Structural analysis of 9CO4 — SASA tables, protofilament partition, chain A vs J equivalence
- [x] Strategy finalised — Lecanemab-logic lateral binding, Mode 1
- [x] 9CO4, 9CKI, 9CK6 downloaded to `~/structural_analysis_project/structures/`

#### 0.2 BindCraft installation

1. Clone the repo:
   ```bash
   cd /global/project/hpcg6049/protein/alzheimer/bindcraft
   git clone https://github.com/martinpacesa/BindCraft.git repo
   ```

2. Create a dedicated conda env following BindCraft's `install_bindcraft.sh`, adapted for:
   - Frontenac's CUDA 12.x drivers (A100 nodes run CUDA 13.2 / Driver 595.58.03)
   - JAX version compatible with BindCraft's AF2 fork (likely different from the colabfold env's JAX 0.6.0)
   - Python 3.10 or 3.11 (check BindCraft requirements)

3. Download AF2 model parameters (~3.5 GB) to:
   ```
   /global/project/hpcg6049/protein/alzheimer/bindcraft/params/
   ```

4. Test on an A100:
   ```bash
   srun --account=def-hpcg6049_gpu --gres=gpu:a100:1 --time=00:30:00 \
     bash -c 'eval "$(conda shell.bash hook)" && conda activate bindcraft && \
     python repo/bindcraft.py --help'
   ```
   Then run BindCraft's built-in test case. Confirm GPU memory stays within 40 GB for a ~300-residue complex.

5. **Update CLAUDE.md** with the `bindcraft` env activation command and any Frontenac-specific patches.

#### 0.3 Download remaining counter-target PDBs

Download to `/global/project/hpcg6049/protein/alzheimer/structures/negative_targets/`:

```bash
cd /global/project/hpcg6049/protein/alzheimer/structures/negative_targets/
for pdb in 7Q4B 7Q4M 6SHS 1IYT; do
  curl -fL "https://files.rcsb.org/download/${pdb}.pdb" -o ${pdb}.pdb
done
```

Generate AF2 monomer prediction of Aβ40 using ColabFold:
```bash
# Aβ40 sequence: DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVV
# Run ColabFold monomer prediction, 5 models, pick best pLDDT
# Save as Ab40_monomer_af2.pdb
```

#### 0.4 Prepare BindCraft target input

Extract chains C, E, G from 9CO4:

```python
from Bio.PDB import PDBParser, PDBIO, Select

class ChainSelect(Select):
    def __init__(self, chains):
        self.chains = chains
    def accept_chain(self, chain):
        return chain.id in self.chains

parser = PDBParser(QUIET=True)
s = parser.get_structure("9co4", "9CO4.pdb")
io = PDBIO()
io.set_structure(s)
io.save("9CO4_CEG.pdb", ChainSelect(["C", "E", "G"]))
```

Save to: `/global/project/hpcg6049/protein/alzheimer/bindcraft/input/9CO4_CEG.pdb`

#### 0.5 Directory layout after Stage 0

```
/global/project/hpcg6049/protein/alzheimer/
├── CLAUDE.md
├── DEVELOPMENT_PLAN.md          (this file)
├── structures/
│   ├── 9CO4.pdb
│   ├── 9CKI.pdb
│   ├── 9CK6.pdb
│   └── negative_targets/
│       ├── 7Q4B.pdb
│       ├── 7Q4M.pdb
│       ├── 6SHS.pdb
│       ├── 1IYT.pdb
│       └── Ab40_monomer_af2.pdb
├── bindcraft/
│   ├── repo/                    (cloned BindCraft)
│   ├── params/                  (AF2 weights, ~3.5 GB)
│   ├── input/
│   │   └── 9CO4_CEG.pdb        (target for BindCraft)
│   ├── designs/                 (empty until Stage 2)
│   ├── filtering/               (empty until Stage 3)
│   ├── logs/
│   └── scripts/                 (SLURM submission scripts)
├── env/
│   ├── frontenac_gpu_audit_log.md
│   └── gpu_check_*.out
├── docs/
└── README.md
```

---

### Stage 1 — BindCraft campaign configuration

**Duration:** 0.5 days
**Compute:** None (configuration only)
**Decision gate:** None

#### 1.1 BindCraft parameters

| Parameter | Value | Notes |
|---|---|---|
| `target_pdb` | `input/9CO4_CEG.pdb` | Chains C, E, G of protofilament 1 |
| `target_chains` | `C,E,G` | Binder contacts all three chains |
| `binding_site` | Residues 10, 11, 13, 14, 15, 16 on each of C, E, G | 18 positions total — the Lecanemab N-terminal epitope |
| `binder_len` | 60–90 (sampled uniformly per design) | `$(shuf -i 60-90 -n1)` in the SLURM script |
| `num_designs` | 1,000 total (one per SLURM array task) | Seeds 1–1000 |
| `af2_model` | `model_1_ptm` (BindCraft default) | Best single-representation model |
| `recycles` | 3 (BindCraft default) | Standard for binder design |
| `design_iterations` | 50 (BindCraft default) | Per-design optimisation cycles |
| Internal filters | pLDDT > 80, pae_interaction < 12, i_pTM > 0.6 | BindCraft's own acceptance; we tighten in Stage 3 |

> **Note:** Exact CLI flags depend on the BindCraft version installed in Stage 0. The parameter names above are conceptual; map them to the actual CLI/config-file keys after installation. Update this section in-place once the mapping is confirmed.

#### 1.2 Diversity strategy

BindCraft converges on fewer backbone topologies than RFdiffusion because each design is an independent gradient-descent trajectory. To maximise structural diversity:

1. **Uniformly sample binder length** from 60–90 residues per design (different length = different topology).
2. **One unique random seed per design** (seeds 1–1000).
3. **Monitor at design ~100:** cluster the first ~100 completed designs by backbone RMSD. If >50% fall in a single cluster, inject noise: shift hotspot weighting (e.g., upweight H13/Q15, downweight E11/K16) for the next batch.

---

### Stage 2 — BindCraft production run (1,000 designs)

**Duration:** 8–21 days wallclock (depending on A100 availability)
**Compute:** 350–500 GPU-hours on A100-40GB
**Decision gate:** None (Gate 1 is after Stage 3)

#### 2.1 SLURM submission strategy

- **Array job:** 1,000 tasks, each running one BindCraft design with a unique seed.
- **Throttle:** `--array=1-1000%20` (max 20 concurrent tasks — 2–3 GPUs worth).
- **One A100 GPU per task:** `--gres=gpu:a100:1` (do NOT specify `--partition`).
- **Time per task:** `--time=01:00:00` (1 hour; generous margin over the 20–30 min typical).
- **Memory:** `--mem=32G` per task.

#### 2.2 SLURM template

```bash
#!/bin/bash
#SBATCH --job-name=bc_design
#SBATCH --output=bindcraft/logs/design_%a.out
#SBATCH --error=bindcraft/logs/design_%a.err
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
OUTDIR=/global/project/hpcg6049/protein/alzheimer/bindcraft/designs/design_$(printf '%04d' $SEED)
mkdir -p $OUTDIR

# === ADAPT THE COMMAND BELOW TO MATCH INSTALLED BINDCRAFT CLI ===
python /global/project/hpcg6049/protein/alzheimer/bindcraft/repo/bindcraft.py \
  --target_pdb /global/project/hpcg6049/protein/alzheimer/bindcraft/input/9CO4_CEG.pdb \
  --target_chains C,E,G \
  --binding_site C:10,C:11,C:13,C:14,C:15,C:16,E:10,E:11,E:13,E:14,E:15,E:16,G:10,G:11,G:13,G:14,G:15,G:16 \
  --binder_len $(shuf -i 60-90 -n1) \
  --seed $SEED \
  --output_dir $OUTDIR
# === END ADAPT SECTION ===

echo "Design $SEED completed on $(hostname) at $(date)"
```

> **CRITICAL SLURM RULES (from CLAUDE.md):**
> - Always use `--account=def-hpcg6049_gpu`
> - NEVER specify `--partition` — the scheduler auto-routes
> - NEVER use `-w` (node targeting)
> - Use `eval "$(conda shell.bash hook)"` before `conda activate`
> - Use absolute paths everywhere

#### 2.3 Post-run sweep

After the array completes, run a sweep script to:
1. Count completed designs (look for output PDB in each `design_XXXX/` directory).
2. List failed seeds (non-zero exit, missing output, OOM in stderr).
3. Resubmit failed seeds as a new array.
4. Write a summary to `bindcraft/logs/stage2_summary.md`.

#### 2.4 Compute budget

| Item | Estimate |
|---|---|
| Per-design GPU time | 20–30 min on A100-40GB |
| Total GPU-hours | 330–500 hrs for 1,000 designs |
| Concurrent tasks | 20 (array throttle) |
| Wallclock (optimistic, 20 tasks always running) | ~17–25 hrs |
| Wallclock (realistic, scheduling + failures) | 8–21 days |
| Storage per design | ~5–10 MB |
| Total storage | ~5–10 GB |

---

### Stage 3 — Negative-design counter-screen

**Duration:** 2–5 days
**Compute:** ~100–200 GPU-hours on A100
**Decision gate:** **DECISION GATE 1**

#### 3.1 Protocol

For every design that passes BindCraft's internal filters:

1. Run ColabFold complex prediction: binder sequence + each of 7 counter-target structures.
2. Extract `pae_interaction` from each prediction.
3. Apply hard filters:
   - **Positive:** `pae_interaction < 10` on 9CO4 (re-confirmation with independent ColabFold run)
   - **Negative:** `pae_interaction > 15` on ALL 7 counter-targets
4. A design passes Stage 3 only if it satisfies BOTH filters.

#### 3.2 SLURM approach

- Use the `colabfold` conda env (already installed, has JAX 0.6.0 + AF2).
- Submit as another array job: one task per (design × counter-target) pair, or batch multiple counter-targets per task.
- Each ColabFold prediction takes ~5 min on A100.
- Assuming ~200–400 designs pass BindCraft internal filters × 7 counter-targets × 5 min = ~120–230 GPU-hours.

#### 3.3 Output

Save results to `bindcraft/filtering/stage3_results.csv` with columns:
```
design_id, target, pae_interaction, plddt_binder, iptm, pass_positive, pass_negative, pass_both
```

### DECISION GATE 1

| Outcome | Criterion | Action |
|---|---|---|
| **Pass** | ≥ 20 designs pass both positive + negative filters | Proceed to Stage 4 |
| **Marginal** | 5–19 designs pass | Proceed with caution; expand Stage 2 to 2,000 designs with shifted parameters (different binder lengths, relaxed hotspot weighting) |
| **Fail** | < 5 designs pass | **Switch to RFdiffusion pipeline** (see Fallback section). Same target, same negative panel, same downstream stages. |

---

### Stage 4 — Stability and developability filtering

**Duration:** 1–2 days
**Compute:** CPU only
**Decision gate:** None

Apply these filters sequentially to all Gate 1 survivors. Each filter is pass/fail.

| Filter | Threshold | Tool | Purpose |
|---|---|---|---|
| SAP score (non-paratope surface) | < 0.10 | Rosetta or SAP script | Aggregation propensity |
| Buried unsatisfied H-bonds | 0 | Rosetta BuriedUnsatHbonds | Core packing quality |
| Unpaired cysteines | 0 | Sequence check | Disulfide scrambling risk |
| Net charge at pH 7.4 | −2 to +4 | Sequence-based | Solubility |
| Predicted Tm | > 60°C | Rosetta ddG or ML predictor | Thermal stability |
| Contact molecular surface (polar fraction) | > 40% | FreeSASA | Interface quality |
| AF2 monomer fold confidence | pLDDT > 85 (binder alone) | ColabFold monomer | Binder folds independently |

Save results to `bindcraft/filtering/stage4_results.csv`.

---

### Stage 5 — Multi-objective ranking and selection

**Duration:** 1 day
**Compute:** None (analysis only)
**Decision gate:** None

Rank all Stage 4 survivors by composite score:

| Metric | Weight | Direction |
|---|---|---|
| pae_interaction on 9CO4 | 0.25 | Lower is better |
| Mean pae_interaction across 7 negatives | 0.25 | Higher is better |
| Binder pLDDT | 0.15 | Higher is better |
| SAP score | 0.10 | Lower is better |
| Predicted Tm | 0.10 | Higher is better |
| Structural diversity bonus | 0.15 | Reward under-represented backbone clusters |

**Selection rules:**
- Select **top 50 designs** for synthesis.
- Enforce **max 5 designs per backbone cluster** (to maximise structural diversity).
- Include **2–3 negative controls** (designs that passed positive but FAILED negative filters — predicted plaque binders) to validate the selectivity assay experimentally.

Save the final panel to `bindcraft/filtering/stage5_panel.csv`.

---

### Stage 6 — Experimental validation (Aβ arm)

**Duration:** 3–6 months
**Decision gate:** **DECISION GATE 2**

#### 6.1 Expression and biophysical characterisation

1. Gene synthesis: 50 designs + 2–3 negative controls, codon-optimised for E. coli.
2. Expression: BL21(DE3) or SHuffle (if disulfide-containing), 1 mL auto-induction.
3. Score: soluble expression (yes/no), yield from SDS-PAGE.
4. SEC-MALS on soluble expressors: confirm monodispersity and expected MW.
5. Thermal stability: nanoDSF or CD melt — confirm Tm > 60°C.

#### 6.2 Binding validation

1. **Positive binding:** SPR or BLI with synthetic Aβ42 protofibrils (ADDL protocol: Aβ42 in F12 media) immobilised on sensor chip. Measure K_D, k_on, k_off.
2. **Negative binding (selectivity):** repeat with (i) synthetic Aβ42 mature fibrils (sonicated), (ii) Aβ40 monomers, (iii) Aβ42 monomers. Require ≥ 10-fold selectivity for protofibrils over fibrils and ≥ 100-fold over monomers.
3. **Lecanemab benchmark:** same SPR panel with commercial Lecanemab as positive control. Compare selectivity ratios.

### DECISION GATE 2

| Outcome | Criterion | Action |
|---|---|---|
| **Pass** | ≥ 3 binders with K_D < 500 nM for protofibrils AND ≥ 10-fold selectivity over fibrils | Advance top 3–5 binders to fusion (Stage 8) |
| **Marginal** | 1–2 binders meet criteria | Characterise; consider affinity maturation via BindCraft re-design seeded from best hit |
| **Fail** | 0 binders | Analyse failure modes (expression failure? binding failure? selectivity failure?). Redesign with different parameters or switch pipeline. |

---

### Stage 7 — TfR1 arm design (parallel track)

**Duration:** Runs in parallel with Stages 2–6
**Compute:** ~350–500 GPU-hours (separate BindCraft campaign)
**Decision gate:** None (merges at Stage 8)

| Parameter | Value |
|---|---|
| Target | TfR1 apical domain (avoid transferrin-binding site) |
| PDB | To be selected — likely 1CX8 or a recent high-resolution TfR1 structure |
| Hotspots | Apical domain residues (defined after PDB selection) |
| Binder size | 50–70 residues |
| Number of designs | 1,000 |
| Affinity target | **50–200 nM** (moderate, NOT high) |
| Key constraint 1 | Must NOT compete with transferrin binding (iron homeostasis toxicity) |
| Key constraint 2 | Monovalent presentation in the bispecific (avoid receptor crosslinking → degradation) |

> **CRITICAL: Affinity tuning.** High-affinity TfR1 binders (K_D < 10 nM) are sorted to lysosomes and degraded — they do NOT cross the BBB. Moderate affinity (50–200 nM) allows transcytosis and release on the brain side. This is established in the Roche brain-shuttle and Denali ETV literature (Yu et al., *Sci Transl Med* 2011). **Designs with predicted K_D < 10 nM should be DEPRIORITISED, not promoted.**

The TfR1 campaign uses the same pipeline (BindCraft → negative screen → stability → ranking → expression → SPR), with TfR1-specific targets and counter-targets. The detailed TfR1 spec will be written as a separate document when that campaign starts.

---

### Stage 8 — Tandem fusion design

**Duration:** 2–4 weeks
**Compute:** ~50–100 GPU-hours
**Decision gate:** None

Prerequisite: both arms individually validated (Aβ from Gate 2, TfR1 from Stage 7).

#### 8.1 Fusion variants to test

For each combination of top Aβ binder × top TfR1 binder, generate 10 fusion variants:

| Variant | Domain order | Linker |
|---|---|---|
| 1 | Aβ–linker–TfR1 | (GGGGS)×3 (15 aa, flexible) |
| 2 | Aβ–linker–TfR1 | (GGGGS)×4 (20 aa, flexible) |
| 3 | Aβ–linker–TfR1 | (GGGGS)×5 (25 aa, flexible) |
| 4 | Aβ–linker–TfR1 | A(EAAAK)×3A (rigid α-helical) |
| 5 | Aβ–linker–TfR1 | PAPAP (short rigid Pro-rich) |
| 6 | TfR1–linker–Aβ | (GGGGS)×3 |
| 7 | TfR1–linker–Aβ | (GGGGS)×4 |
| 8 | TfR1–linker–Aβ | (GGGGS)×5 |
| 9 | TfR1–linker–Aβ | A(EAAAK)×3A |
| 10 | TfR1–linker–Aβ | PAPAP |

Total: 10 variants × (3–5 Aβ binders) × (3–5 TfR1 binders) = 90–250 fusion candidates.

#### 8.2 AF2 fusion verification

Run ColabFold on each fusion variant. Check:

1. **Both domains retain folds:** per-domain pLDDT > 80, per-domain RMSD < 2 Å vs standalone prediction.
2. **No inter-domain packing:** if AF2 predicts the two binder domains contacting each other, REJECT that variant (it will aggregate or occlude paratopes).
3. **Back-face hydrophobicity:** SAP < 0.10 on the non-paratope surface of each domain. If too hydrophobic, redesign with ProteinMPNN (fix interface residues, redesign non-interface to favour polar).

---

### Stage 9 — Fusion expression and characterisation

**Duration:** 2–3 months
**Decision gate:** **DECISION GATE 3**

1. Gene synthesis of top 10–20 fusion variants.
2. E. coli expression, SEC-MALS (monodispersity, correct MW), Tm.
3. **Dual-binding SPR:** Aβ42 protofibrils on channel 1, TfR1 ectodomain on channel 2. Sequential injection to confirm both arms engage independently.
4. **Aggregation check:** DLS or SEC at 1–10 mg/mL over 7 days at 4°C and 37°C.
5. **Negative controls:** (i) mature fibrils (Aβ arm should not bind), (ii) Tf-loaded TfR1 (TfR1 arm should not compete with transferrin).

### DECISION GATE 3

| Outcome | Criterion | Action |
|---|---|---|
| **Pass** | ≥ 1 fusion binds both targets, retains ≥ 50% of each arm's standalone affinity, no aggregation at 1 mg/mL × 7 days | Advance to Stage 10 |
| **Fail** | No fusion meets criteria | Express arms separately; consider switching to Option B (Fc-based bispecific) |

---

### Stage 10 — Brain-shuttle proof of concept

**Duration:** 3–6 months
**Decision gate:** Publication-ready

1. **Transcytosis assay:** in vitro BBB model (hCMEC/D3 or iPSC-derived). Bispecific vs Aβ binder alone. TfR1 arm should increase basolateral accumulation ≥ 5-fold.
2. **Brain homogenate binding:** incubate bispecific with AD brain homogenate (collaboration). Pull down, immunoblot for Aβ. Compare to Lecanemab.
3. **In vivo PK (if resources allow):** IV injection in WT mice, brain:plasma ratio at 4h and 24h. Bispecific should show ≥ 3-fold higher brain penetration.
4. **Publication:** the design + in vitro story (Stages 0–9) is publishable independently.

---

## Timeline summary

| Stage | Description | Duration | Compute | Gate |
|---|---|---|---|---|
| 0 | Environment + BindCraft install | 1–2 days | Login + 1 GPU test | — |
| 1 | BindCraft configuration | 0.5 days | None | — |
| 2 | 1,000 BindCraft designs | 8–21 days | 350–500 A100-hrs | — |
| 3 | Negative-design screen | 2–5 days | 100–200 A100-hrs | **GATE 1** |
| 4 | Stability filtering | 1–2 days | CPU only | — |
| 5 | Ranking + selection (50 designs) | 1 day | None | — |
| 6 | Wet-lab validation (Aβ arm) | 3–6 months | — | **GATE 2** |
| 7 | TfR1 arm design (parallel) | ~1 month | 350–500 A100-hrs | — |
| 8 | Tandem fusion design | 2–4 weeks | 50–100 A100-hrs | — |
| 9 | Fusion expression + validation | 2–3 months | — | **GATE 3** |
| 10 | Brain-shuttle PoC | 3–6 months | — | Publication |

**Computational phases (0–5, 7–8):** ~2–3 months
**Experimental phases (6, 9–10):** ~8–15 months
**Total:** ~10–18 months

---

## Fallback — RFdiffusion pipeline

If Decision Gate 1 fails (< 5 candidates after negative screening), switch to the three-stage pipeline. All Frontenac environments are already installed:

| Stage | Tool | Conda env | Key parameters |
|---|---|---|---|
| Backbone generation | RFdiffusion | `rfd_clean` | 10,000 backbones; contig targeting C/E/G residues 10–16; scaffold 60–90 |
| Sequence design | ProteinMPNN | `mpnn` | 32 sequences per backbone; temperature 0.2 |
| Filtering | ColabFold | `colabfold` | Same pae_interaction thresholds as Stage 3 |

Everything downstream of backbone+sequence generation (Stages 3–10) is identical regardless of design engine. The fallback adds ~2–4 weeks of compute but does not change the experimental plan.

---

## Appendix — HPC quick reference

Extracted from `CLAUDE.md`. Full details there.

| Item | Value |
|---|---|
| User / account | `hpc6049` / **`def-hpcg6049_gpu`** (MUST specify) |
| GPU (primary) | NVIDIA A100-PCIE-40GB |
| GPU (fallback) | Quadro RTX 8000 (45 GB) |
| SLURM GPU syntax | `--account=def-hpcg6049_gpu --gres=gpu:a100:1` — **NO `--partition`** |
| 14-day partition | Auto-selected for `--time > 1 day` |
| Key gotcha | Default account is CPU-only; `--partition` flag always fails |
| Conda activation in scripts | `eval "$(conda shell.bash hook)" && conda activate <env>` |
| Absolute paths required | Compute nodes don't inherit submit-side CWD |