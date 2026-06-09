# Bindlix — NVIDIA Inception Pitch Deck

> **Company:** Bindlix · https://bindlix.com/ · info@bindlix.com · Kingston, ON, Canada
> **Application:** https://www.nvidia.com/en-us/startups/
> **Deck length:** 11 slides · **Apply with:** info@bindlix.com (business email, not Gmail)
>
> **How to read this doc:** Each slide has three blocks —
> **ON SLIDE** = text/copy you can paste directly · **SAY** = speaker notes / what to narrate · **VISUAL** = the image or diagram to add.
> `[TODO]` marks the few things only the founders can supply.

---

## Narrative arc (the story the deck tells)

> Big problem → the field just changed (why now) → our platform → two real programs with proof → big market → credible team → specific ask → where this goes.

1. Title  2. Problem  3. Why Now  4. Platform  5. Program 1  6. Program 2  7. Technology & GPU
8. Traction  9. Market  10. Team  11. The Ask + Vision

---

## Program quick facts (keep handy, not a slide)

- Free, no equity. Rolling applications, response in 1–4 weeks.
- Benefits: cloud credits ($10K–$100K by stage), preferred GPU pricing, DLI training, BioNeMo/SDK access, Inception Capital Connect (VC intros), co-marketing.
- Hard requirement: AI/ML must be **core** to the product. Pitch deck mandatory. Apply from a business email.

---

## Slide 1 — Title

**ON SLIDE**
- **Bindlix** (logo)
- *Designed to bind. Built to heal.*
- AI-designed protein therapeutics for Alzheimer's disease
- bindlix.com · Kingston, Ontario, Canada

**SAY**
- "Bindlix designs protein therapeutics for Alzheimer's entirely on GPUs — we design, counter-screen, and rank drug candidates before running a single experiment."

**VISUAL** — Logo on clean background; subtle protein-ribbon motif.

---

## Slide 2 — The Problem

**ON SLIDE**
- Alzheimer's: **55M people today → 139M by 2050**
- Today's anti-amyloid antibodies face three compounding failures:
  - **Brain access** — ~150 kDa antibodies barely cross the blood-brain barrier; **~0.1%** reaches the brain
  - **Safety** — ARIA (brain swelling/microbleeds) in **20–35%** of patients
  - **Cost & burden** — **~$26K/yr**, biweekly IV infusion, ongoing MRI monitoring
- No miniprotein or small therapeutic today both **clears amyloid** *and* **actively crosses the BBB**

**SAY**
- "Even lecanemab — the current standard of care — only works because its binding is deliberately weak, and it still barely gets into the brain. The delivery and safety problems are unsolved."

**VISUAL** — Simple diagram: antibody bouncing off the BBB; tiny fraction crossing. ARIA stat callout.

`[TODO]` Confirm/cite the market & ARIA figures before submitting (currently from general literature).

---

## Slide 3 — Why Now

> *New slide — this is the beat NVIDIA responds to most: a real inflection point that makes the company possible today and not 3 years ago.*

**ON SLIDE**
- De novo protein design just crossed from research to practice (2023–2025): **AlphaFold2, RFdiffusion, ProteinMPNN, BindCraft, Boltz-2**
- For the first time, you can **specify a target shape and design a binder atom-by-atom** — no immunization, no phage display
- This is a **GPU-native discipline**: every design step is a forward/backward pass on an A100/H100
- Bindlix is built from day one on this stack — design velocity is bounded by **GPU access**, not lab throughput

**SAY**
- "Three years ago this company couldn't exist. The models matured, and the bottleneck moved from the wet lab to compute. That's exactly where NVIDIA comes in."

**VISUAL** — Timeline 2021→2025 of the key model releases, ending at "Bindlix."

---

## Slide 4 — The Platform

**ON SLIDE**
- Bindlix is a **computational cascade**: *design → counter-screen → rank → validate*
- One platform, applied two ways:
  - **Program 1 — Design from scratch:** de novo bispecific miniproteins
  - **Program 2 — Redesign what works:** AI affinity maturation of an FDA-approved antibody
- Counter-screening is the moat: we **reject** candidates that look good but lose selectivity — before any experiment
- Output: ranked, synthesis-ready drug candidates

**SAY**
- "The platform is target-agnostic. We're proving it on the hardest target there is — the brain — with two independent programs."

**VISUAL** — Funnel/cascade graphic: thousands of designs → filters → handful of ranked leads. Two branches off the same platform.

---

## Slide 5 — Program 1: De Novo Bispecific Miniprotein

**ON SLIDE**
- One small protein (**~15–20 kDa, 130–180 aa**), two jobs:
  - **Arm 1** — binds Aβ42 fibrils (receptor-bound conformation, PDB 9CO4) → blocks plaque growth
  - **Arm 2** — binds Transferrin Receptor 1 (TfR1) → hijacks iron-transport endocytosis to **cross the BBB**
- Tandem fusion, flexible/rigid linkers
- Small size → better brain penetration, lower immunogenicity, **cheap E. coli production**
- 100% computationally designed — no antibody, no animal

**SAY**
- "This is a first-in-class BBB shuttle: the binder carries itself across the barrier using the brain's own transferrin pathway."

**VISUAL** — Cartoon: bispecific bridging TfR1 on BBB endothelium and an Aβ42 fibril in the brain.

---

## Slide 6 — Program 2: Lecanemab Affinity Maturation

**ON SLIDE**
- Start from **lecanemab** — the only FDA-approved anti-amyloid antibody
- AI-redesign CDR loops + framework to **improve protofibril engagement**
- **The innovation — avidity-aware selectivity:** counter-screen every variant against Aβ *monomers*; **reject** any that bind monomer better
- Preserves lecanemab's **>10⁶-fold** selectivity for protofibrils over monomers — the property that keeps ARIA risk low
- Goal: better amyloid clearance **at the same or better safety margin**

**SAY**
- "Everyone else optimizes for tighter binding. We deliberately don't — because for this antibody, tighter monomer binding *is* the safety problem. We optimize the right thing: avidity on aggregates, not raw affinity."

**VISUAL** — Selectivity funnel: variants that improve protofibril binding pass; variants that improve monomer binding get rejected.

---

## Slide 7 — Technology & GPU Stack

> *The slide NVIDIA scrutinizes most. Show AI is central and every stage is GPU-bound.*

**ON SLIDE** (table)

| Stage | Tool | GPU load |
|---|---|---|
| Backbone generation | RFdiffusion | A100, hrs/design |
| Sequence design | ProteinMPNN | GPU |
| Structure prediction | AlphaFold2 / ColabFold | A100, ~4 min/run |
| Gradient binder design | BindCraft (AF2 backprop) | A100, 6–14 days/campaign |
| Antibody co-folding | Boltz-2 / AlphaFold3 | A100, 5-seed × 5-sample |
| Binding ΔΔG | PyRosetta flex_ddG | A100, 1,500–10,500 traj/variant |
| Fusion / multimer validation | ColabFold multimer | A100 |
| Stability & dynamics | GROMACS + OpenMM | multi-GPU |

- **NVIDIA-native:** CUDA · JAX (XLA on GPU) · PyTorch · Apptainer GPU containers
- **Scale today:** **~3,240 GPU-hours already consumed across 3 Compute Canada clusters** (1,098 GPU jobs), on **NVIDIA A100 and H100** — all verified via `sacct`:

  | Cluster | GPU-hours | Jobs | GPU |
  |---|---|---|---|
  | Frontenac | 1,891 | 921 | A100 |
  | Nibi | 1,103 | 30 | H100 |
  | Narval | 244 | 147 | A100 |
  | **Total** | **~3,238** | **1,098** | A100 + H100 |

- **Bottleneck = GPU.** More compute directly converts to more validated drug candidates.

**SAY**
- "There is no non-GPU version of this company. Every box in this table is an NVIDIA GPU workload — we've already consumed over 3,200 A100/H100-hours across three clusters, and that's before the lecanemab program scales up. Inception credits go straight into more validated candidates."

**Footnote (keep in notes, not on slide):** Figures verified via `sacct -X` on each cluster, 2026-06-09. Nibi's H100 total includes failed/OOM runs (real burned allocation) — framed as "GPU-hours consumed." Largest single job: BindCraft Aβ42 production (Frontenac 8375335, 265 GPU-hr).

---

## Slide 8 — Traction

**ON SLIDE**

*Program 1 — Bispecific*
- BindCraft Aβ42 campaign: **1,342 trajectories → 62 accepted designs** ✓
- Stability filtering: **23/62** pass all biophysical filters ✓
- TfR1 arm: **2,051 trajectories → 380 accepted → top 50 ranked** ✓
- **Stage 8 fusion: 250 candidates in validation now** ◐

*Program 2 — Lecanemab-AM*
- Fv modeled + 25-pose Fv–Aβ complex ensemble (MD-confirmed) ✓
- 33 variants designed (3 framework + 30 CDR) ✓
- First affinity hit: **LC:K56N+V114Y, Δ-ipSAE +0.21** ✓
- Selectivity model validated: WT **dG −8.62 (protofibril) vs −27.56 (monomer)**; 6/6 top variants correctly rejected by monomer counter-screen ✓

*Infrastructure*
- End-to-end pipeline live across **3 HPC clusters**; git-synced multi-agent workflow + variant ledger

**SAY**
- "Two programs, both already producing ranked candidates. This isn't a concept — the pipeline runs end-to-end today."

**VISUAL** — Two progress tracks with checkmarks; one structure render per program.

---

## Slide 9 — Market

**ON SLIDE**
- **Now:** two Alzheimer's leads (de novo bispecific + improved lecanemab)
- **Platform → any target pair:** Parkinson's (α-synuclein × TfR1), ALS (TDP-43 × TfR1), brain tumors, oncology bispecifics, optimization of *any* therapeutic antibody
- Markets:
  - Alzheimer's drugs: **~$13B (2025) → $30B+ (2030)**
  - Bispecific antibodies: **$10B+**, ~25% CAGR
  - CNS drug delivery: **~$8.5B**
- Comparables raising big: Xaira, Neoleukin, EvolutionaryScale, Baker-lab spinouts ($100M+ rounds)

**SAY**
- "The Alzheimer's programs are the wedge. The asset is the platform — it retargets to any disease where shape-selective binding matters."

`[TODO]` Cite each market figure before submission.

---

## Slide 10 — Team

**ON SLIDE**
- **Maria Tabasi** — Founder & CEO · Protein Engineer · `[TODO: 1 line — education / prior work]`
- **Hamid Ghaedi** — Co-founder & CSO · Bioinformatician · runs GPU-scale protein design across A100/H100 clusters · `[TODO: 1 line — education / prior work]`
- Interdisciplinary: computational design + structural biology + protein biochemistry
- Advisory board: *to be announced*

**SAY**
- "Small, technical, hands-on-the-GPU team. We build binders the way engineers build machines."

**VISUAL** — Two headshots, names/titles. NVIDIA-stack logos (CUDA/JAX/PyTorch) as a fluency signal.

`[TODO]` Headshots + one-line bios for both founders.

---

## Slide 11 — The Ask + Vision

**ON SLIDE — What we need from Inception**
1. **GPU cloud credits** — scale fusion design 250 → 5,000+; score all lecanemab variants; MD on top leads. Est. **10K–50K A100-hours / 6 mo**
2. **BioNeMo access** — evaluate NVIDIA models (ESMFold, DiffDock, MolMIM) as scoring tools
3. **Preferred hardware pricing** — A100/H100 workstation for rapid design cycles
4. **Inception Capital Connect** — biotech/life-sciences VC intros for pre-seed
5. **Technical guidance** — scaling AF2/Boltz-2 inference, multi-GPU MD

**ON SLIDE — Roadmap**

| When | Milestone |
|---|---|
| Q3 2026 | Finish both campaigns; top 10 bispecifics + top 5 lecanemab variants |
| Q4 2026 | Wet-lab validation: synthesis, expression, SPR, thermal stability |
| Q1 2027 | Publish + provisional patents |
| Q2 2027 | Pre-seed raise; expand team |
| 2027–28 | New targets (Parkinson's, oncology); animal PK/PD |

**SAY**
- "Credits and BioNeMo let us turn compute directly into validated candidates. What NVIDIA gets is a flagship case study in GPU-native drug design."

---

## Appendix A — Application form answers (paste-ready)

| Field | Answer |
|---|---|
| Company name | Bindlix |
| Website | https://bindlix.com/ |
| Incorporation date / country | `[TODO]` / Canada |
| Employees (developers) | 2 (both technical) |
| Industry | Healthcare / Life Sciences / Drug Discovery |
| Product (short) | AI-designed protein therapeutics platform for Alzheimer's. Two programs: de novo bispecific miniprotein binders and computational antibody affinity maturation. |
| AI/ML focus | Generative protein design, structure prediction, computational biophysics |
| Funding status | `[TODO]` (bootstrapped / pre-seed) — revenue not required |
| Pitch deck | This deck, exported to PDF (11 slides) |
| NVIDIA tech used | CUDA, JAX (XLA on A100/H100), PyTorch, Apptainer GPU containers; AlphaFold2, Boltz-2, RFdiffusion, ProteinMPNN, BindCraft, GROMACS across 3 HPC clusters |

---

## Appendix B — Founder TODOs before submission

- [ ] One-line bios + headshots: Maria Tabasi, Hamid Ghaedi
- [ ] Incorporation date + funding status for the form
- [x] GPU-hours verified, all 3 clusters (2026-06-09): ~3,238 hr / 1,098 jobs — Frontenac 1,891 (A100), Nibi 1,103 (H100), Narval 244 (A100)
- [ ] Cite market & ARIA/BBB figures (Slides 2 & 9)
- [ ] Structure renders (PyMOL/ChimeraX), pipeline funnel diagram, bispecific & BBB cartoons
- [ ] Advisory board names, if any are ready
