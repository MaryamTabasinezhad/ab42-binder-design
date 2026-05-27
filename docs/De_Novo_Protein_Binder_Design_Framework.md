# De Novo Protein Binder Design Framework

## A Comprehensive Guide to Philosophy, Strategy, and Execution

---

## Part I — Design Philosophies

These are the foundational beliefs that should govern every decision in a de novo binder design campaign. They are not optional refinements — they are the mental model that separates pipelines that produce papers from pipelines that produce binders.

### Philosophy 1: Geometry Precedes Everything

Binding is a three-dimensional shape-matching problem. A binder must present the correct atoms at the correct positions in space relative to the target surface. No amount of sequence optimization can rescue a backbone that places its interface residues in the wrong geometry.

This means backbone generation is the highest-leverage step in the entire pipeline. The quality of the binding pose — shape complementarity, approach angle, burial of polar groups — determines the ceiling of what downstream sequence design can achieve. If the backbone geometry is wrong, the best possible sequence will still fail.

Corollary: time spent improving backbone sampling and pose selection yields more return than equivalent time spent on sequence optimization.

### Philosophy 2: Explore Broadly, Then Optimize Ruthlessly

The design process has two fundamentally different modes, and conflating them is the most common source of pipeline failure.

**Exploration** is about coverage. The goal is to sample as many structurally distinct binding modes as possible — different approach angles, different scaffold topologies, different interface compositions. During exploration, the only filtering should remove physically implausible designs (severe clashes, disconnected chains). Everything else survives.

**Optimization** is about refinement. Once promising structural families are identified, the goal shifts to finding the best sequence for each backbone, improving core packing, maximizing interface complementarity, and satisfying developability constraints. Filtering here should be aggressive and multi-dimensional.

The failure mode is premature optimization: applying stringent filters during exploration, which collapses diversity before the landscape has been adequately sampled.

### Philosophy 3: Diversity Is the Primary Hedge Against Uncertainty

Computational metrics are imperfect predictors of experimental success. The correlation between predicted binding energy and measured Kd is weak. The correlation between AlphaFold confidence and actual binding is modest. Given this uncertainty, the most reliable strategy is structural diversity — maintaining multiple independent backbone families through the pipeline so that if any single family fails experimentally, others remain.

Diversity should be measured structurally (backbone RMSD clustering), not by sequence identity. Two sequences that are 40% identical but fold onto the same backbone are not diverse. Two backbones with different topologies that bind the same epitope from different angles are.

### Philosophy 4: Structure Prediction Is a Filter, Not a Validator

AlphaFold2 and related tools are powerful at identifying designs that are unlikely to work — those with poor predicted confidence, high interface PAE, or structural inconsistency between the designed model and the predicted fold. They are much less reliable at confirming that a design will work.

The practical implication: use AF2 to eliminate the bottom of the ranking, not to crown the top. A design that passes AF2 filtering has cleared a necessary but insufficient bar. A design that fails AF2 filtering should almost always be discarded.

### Philosophy 5: Specificity Must Be Designed, Not Assumed

A hydrophobic patch on a protein surface will bind many things nonspecifically. Without explicit negative design — evaluating whether a binder also binds homologs, decoys, or unrelated proteins — the pipeline will naturally converge on promiscuous hydrophobic interfaces that look great computationally but fail in any context where specificity matters.

Specificity is not a natural byproduct of affinity optimization. It must be engineered through explicit counter-selection.

### Philosophy 6: Developability Is a First-Class Constraint

A binder that expresses at 0.1 mg/L, aggregates at room temperature, or requires refolding from inclusion bodies is not a viable therapeutic or research tool regardless of its binding affinity. Developability constraints — expression yield, solubility, thermal stability, aggregation resistance — must be integrated into the design pipeline from the start, not applied as a post-hoc filter on the final candidate list.

For de novo miniproteins specifically, the dominant failure mode is misfolding into alternative conformational states rather than classical aggregation. This means core packing quality and fold specificity are more important developability metrics than surface hydrophobicity alone.

### Philosophy 7: Iteration Is the Mechanism, Not the Fallback

No first-pass design campaign will produce an optimal binder. The pipeline should be architected for rapid iteration: backbone generation constraints should be easy to modify, sequence design parameters should be adjustable, and filtering thresholds should be tunable. Each experimental round generates data that feeds back into the next computational round.

This is not debugging. This is how the process works.

### Philosophy 8: Experiments Are the Only Ground Truth

Computational metrics are proxies. Binding is measured in the lab. A framework that cannot incorporate experimental feedback — adjusting hotspot definitions based on epitope mapping, modifying backbone constraints based on structural data, re-weighting filters based on expression outcomes — is incomplete.

The pipeline should be designed so that the gap between "we got experimental data" and "we launched a new design round incorporating that data" is as short as possible.

---

## Part II — Strategic Framework

These are the concrete strategies that implement the philosophies above. Each strategy maps to specific tools, metrics, and decision points.

### Strategy 1: Target Analysis and Hotspot Selection

Hotspot selection is arguably the single most consequential decision in the entire workflow. A poorly chosen hotspot will waste every downstream computation.

**What a hotspot is:** A set of residues on the target surface that the binder is designed to engage. These residues define the epitope and constrain the geometry of the binding interface.

**How to select hotspots:**

1. **Functional relevance.** If the goal is to block a protein-protein interaction, the hotspot should overlap with the known interaction interface. Use experimental data (alanine scanning mutagenesis, hydrogen-deuterium exchange, cross-linking mass spectrometry) when available.

2. **Structural accessibility.** The hotspot must be on a solvent-exposed surface accessible to a binding scaffold. Concave pockets are generally easier to target than flat or convex surfaces. Evaluate accessibility using solvent-accessible surface area (SASA) calculations.

3. **Chemical character.** Hotspots rich in polar residues (Arg, Asp, Glu, Asn, Gln) and aromatic residues (Trp, Tyr) tend to produce more specific interfaces than purely hydrophobic patches. Charged residues enable salt bridges and hydrogen bonds that contribute to both affinity and specificity.

4. **Conservation analysis.** If the binder must cross-react with orthologs, select conserved residues. If specificity to one species is required, select divergent positions.

5. **Glycosylation and post-translational modifications.** Check for N-linked glycosylation sites (Asn-X-Ser/Thr sequons) near the hotspot. Glycans can sterically block binding and are often absent from crystal structures but present on the native target.

**Hotspot definition in RFdiffusion:** Specify hotspot residues using the `hotspot_res` flag (e.g., `hotspot_res=[A30,A33,A37]`). Start with 3–6 residues. Fewer residues give more geometric freedom; more residues constrain the pose more tightly. Run initial campaigns with different hotspot subsets to explore binding mode diversity.

**Common pitfall:** Selecting too many hotspot residues over-constrains the backbone generation, producing geometrically similar designs that lack diversity.

### Strategy 2: Backbone Generation with RFdiffusion

**Objective:** Generate a diverse library of backbone scaffolds that present plausible binding geometries against the selected hotspot.

**Key parameters:**

- **Scaffold size.** Start with 60–100 residues for single-domain binders. Smaller scaffolds (50–70) are easier to express but have less surface area for interface contacts. Larger scaffolds (80–120) provide more interface but increase the risk of misfolding.

- **Contig definition.** Define the binder chain length and any structural constraints. For an unconstrained binder: `contigmap.contigs=[B1-100/0 A30-80]` where B is the target chain and A is the binder. Adjust ranges based on target geometry.

- **Number of designs.** Generate 1,000–10,000 backbones per hotspot definition in the exploration phase. This sounds expensive but backbone generation is fast relative to downstream steps.

- **Noise schedule.** Default diffusion parameters work well for most targets. For difficult targets (flat surfaces, small epitopes), consider partial diffusion from known binder scaffolds as a starting point.

**Diversity assessment:** Cluster generated backbones by interface Cα RMSD (typically 2–3 Å cutoff). Aim for at least 10–20 distinct structural clusters. If clustering produces fewer than 5 families, broaden the hotspot definition or reduce constraints.

**Output:** A library of backbone PDB files with diverse binding geometries, organized by structural cluster.

### Strategy 3: Sequence Design with ProteinMPNN

**Objective:** Design amino acid sequences that will fold into the generated backbones and form favorable interactions at the interface.

**Handoff from RFdiffusion:** Each backbone PDB from RFdiffusion is passed directly to ProteinMPNN. The target chain is fixed; only the binder chain is designed. Interface residues and core residues are both designed simultaneously.

**Key parameters:**

- **Sampling temperature.** Use T=0.1 for conservative, low-diversity sampling; T=0.2–0.3 for moderate diversity. Higher temperatures (>0.3) increase sequence diversity but reduce average quality.

- **Number of sequences per backbone.** Design 8–32 sequences per backbone during exploration. For top-ranked backbones entering optimization, increase to 48–96.

- **Tied positions.** If designing a symmetric binder or a binder with internal repeats, use tied positions to enforce sequence symmetry.

- **Fixed residues.** Fix any residues that are structurally critical (e.g., disulfide cysteines, catalytic residues if designing a functional binder).

**Interface-specific considerations:** ProteinMPNN designs the entire binder sequence simultaneously, but the interface and core have different requirements. The interface must complement the target surface chemistry; the core must pack well to ensure folding. If initial designs show poor core packing (low pLDDT in AF2 for core residues), consider a two-stage approach: design the interface first with fixed-backbone design, then redesign the core with the interface residues fixed.

**Output:** Multiple FASTA files of designed sequences, each associated with its parent backbone.

### Strategy 4: Structure Prediction Filtering with AlphaFold2

**Objective:** Eliminate designs that are unlikely to fold correctly or bind as intended.

**Handoff from ProteinMPNN:** Each designed sequence is run through AF2 (or ColabFold for speed) as a complex prediction — binder plus target. The predicted structure is compared against the designed structure.

**Key metrics and thresholds:**

- **pLDDT (binder).** Measures confidence in the predicted binder fold. Threshold: >80 for the binder chain overall, >70 for interface residues. Designs below 70 overall are almost always misfolded.

- **PAE (interface).** Predicted Aligned Error between binder and target chains. Threshold: <10 Å for interface residue pairs. High interface PAE (>15 Å) indicates AF2 is not confident the binder is positioned correctly relative to the target.

- **Cα RMSD (binder).** RMSD between the designed backbone and the AF2-predicted backbone for the binder chain. Threshold: <2 Å indicates the designed fold is recapitulated. RMSD >3 Å suggests the sequence folds into a different structure.

- **Interface RMSD.** RMSD of interface residues only between designed and predicted structures. Threshold: <1.5 Å. This is more sensitive than full-chain RMSD for detecting interface drift.

- **pTM and ipTM.** Predicted TM-score for the complex. ipTM >0.7 is a reasonable threshold; >0.8 is strong.

**Filtering strategy:** Apply filters sequentially — pLDDT first (cheapest to compute), then RMSD, then PAE/ipTM. This saves compute by eliminating obvious failures early.

**Common pitfall:** Treating high AF2 confidence as confirmation of binding. AF2 metrics are necessary but not sufficient. A design with ipTM=0.9 is more likely to work than one with ipTM=0.6, but the absolute probability of success is still modest.

**Output:** A filtered set of designs with AF2 metrics, ranked by composite score.

### Strategy 5: Negative Design and Specificity Evaluation

**Objective:** Ensure the binder is specific to the intended target and does not engage off-target proteins.

**Approaches:**

1. **Homolog cross-docking.** If the target has close homologs (e.g., IL-6 family cytokines, EGFR family receptors), run AF2 complex predictions of the binder against each homolog. Designs that show high ipTM against off-targets should be penalized or redesigned.

2. **Surface composition analysis.** Calculate the fraction of the binder interface that is hydrophobic vs. polar. Interfaces >70% hydrophobic are at high risk of nonspecific binding. Aim for a balanced interface with significant polar contact area.

3. **Electrostatic complementarity.** Compute the electrostatic surface of both binder and target at the interface. Good complementarity (positive patches facing negative patches) correlates with specificity.

4. **Rosetta interface analysis.** Use Rosetta's InterfaceAnalyzerMover to decompose interface energy into van der Waals, electrostatic, and solvation contributions. Designs dominated by van der Waals contacts with minimal electrostatic contribution are more likely to be nonspecific.

**Decision point:** Designs that pass affinity filters but fail specificity checks should be returned to sequence design with modified constraints (e.g., polar residue enrichment at the interface, removal of large hydrophobic patches).

### Strategy 6: Developability Assessment

**Objective:** Ensure designs are compatible with experimental production and characterization.

**Key metrics:**

- **Aggregation propensity.** Calculate Spatial Aggregation Propensity (SAP) or CamSol solubility scores. Flag designs with SAP scores >0.15 for the full binder surface.

- **Net charge.** Designs with net charge between −5 and +5 at physiological pH are generally safer. Highly charged designs may have solubility advantages but can show nonspecific electrostatic interactions.

- **Core packing.** Use Rosetta's PackStat or void volume calculations. Designs with PackStat <0.6 are poorly packed and prone to misfolding or conformational heterogeneity. For de novo miniproteins, this is the most important developability metric.

- **Fold specificity.** Run AF2 on the binder sequence alone (without the target). If the predicted monomer structure matches the designed structure (RMSD <2 Å), the binder is likely to fold independently. If it predicts a different fold, the designed conformation may only be stable in the context of the complex — a significant risk.

- **Sequence complexity.** Flag designs with unusual amino acid composition (e.g., >15% Cys, >25% Gly, or >20% Pro). These often indicate backbone strain that ProteinMPNN is compensating for with unusual chemistry.

**Decision point:** Designs that fail developability checks but have strong binding metrics should be iterated — return to backbone generation with tighter constraints rather than trying to fix a fundamentally problematic scaffold.

### Strategy 7: Ranking and Selection for Experimental Testing

**Objective:** Select a diverse, high-confidence panel of designs for experimental characterization.

**Multi-objective ranking:** No single metric should dominate. A composite ranking should weight:

| Metric | Weight | Rationale |
|--------|--------|-----------|
| AF2 ipTM | 0.25 | Binding confidence |
| Binder pLDDT | 0.15 | Fold confidence |
| Interface RMSD | 0.20 | Design recapitulation |
| Rosetta ddG | 0.15 | Interface energy |
| Specificity score | 0.10 | Off-target discrimination |
| Developability score | 0.15 | Production feasibility |

**Diversity enforcement:** After ranking, do not simply take the top N designs. Instead, cluster the top 20% by backbone RMSD and select the top 1–3 designs from each cluster. A typical experimental panel of 50–100 designs should represent at least 10 distinct structural families.

**Experimental panel composition:**

- 70% top-ranked diverse designs (primary candidates)
- 15% designs from underrepresented structural families (diversity insurance)
- 15% designs with strong single-metric performance but moderate composite scores (hypothesis testing)

### Strategy 8: Iteration from Experimental Feedback

**Objective:** Incorporate experimental results into the next design round.

**Common experimental outcomes and pipeline adjustments:**

| Experimental Result | Pipeline Adjustment |
|---|---|
| No designs express | Relax backbone constraints; increase scaffold size; improve core packing filters |
| Designs express but do not bind | Re-evaluate hotspot selection; increase interface polar contacts; check for glycan occlusion |
| Binding detected but weak (µM) | Affinity maturation via partial diffusion from best hits; saturate interface positions with ProteinMPNN |
| Binding detected but nonspecific | Strengthen negative design; enrich polar interface; add electrostatic complementarity constraints |
| Good binding but poor stability | Improve core packing selection; add disulfide bonds; optimize charge-charge interactions on surface |
| Structure differs from design | Re-examine AF2 monomer predictions; filter more stringently on fold specificity |

**Partial diffusion for affinity maturation:** Take the best experimentally validated backbone and use RFdiffusion in partial diffusion mode to generate variants with small geometric perturbations. This explores the local structural neighborhood of a proven solution.

**Sequence saturation mutagenesis:** For the best binder, design all possible single-point mutations at interface positions using ProteinMPNN and filter with AF2. This identifies positions where mutations improve affinity.

---

## Part III — Pipeline Architecture

### Tool Chain and Handoffs

```
Target Structure (PDB)
       │
       ▼
┌──────────────────┐
│  Hotspot Analysis │  ← SASA, conservation, glycan check, PPI data
│  (PyMOL / FreeSASA│
│   / ConSurf)      │
└────────┬─────────┘
         │  hotspot residue list
         ▼
┌──────────────────┐
│   RFdiffusion    │  ← contig, hotspot_res, num_designs
│  (Backbone Gen)  │
└────────┬─────────┘
         │  backbone PDBs (1,000–10,000)
         ▼
┌──────────────────┐
│  Backbone         │  ← cluster by interface Cα RMSD
│  Clustering       │  ← select representatives
│  (scikit-learn)   │
└────────┬─────────┘
         │  clustered backbone representatives
         ▼
┌──────────────────┐
│  ProteinMPNN     │  ← temperature, num_seqs, fixed residues
│  (Sequence Design)│
└────────┬─────────┘
         │  designed sequences (FASTA + parent PDB)
         ▼
┌──────────────────┐
│  AlphaFold2 /    │  ← complex prediction
│  ColabFold       │  ← pLDDT, PAE, ipTM, RMSD
│  (Filtering)     │
└────────┬─────────┘
         │  filtered designs with metrics
         ▼
┌──────────────────┐
│  Negative Design │  ← homolog cross-prediction
│  + Specificity   │  ← surface composition analysis
└────────┬─────────┘
         │  specificity-annotated designs
         ▼
┌──────────────────┐
│  Developability  │  ← SAP, PackStat, monomer AF2, charge
│  Assessment      │
└────────┬─────────┘
         │  fully annotated design set
         ▼
┌──────────────────┐
│  Multi-Objective │  ← composite ranking + diversity enforcement
│  Selection       │
└────────┬─────────┘
         │  experimental panel (50–100 designs)
         ▼
┌──────────────────┐
│  Experimental    │  ← expression, binding, biophysical assays
│  Validation      │
└────────┬─────────┘
         │  experimental data
         ▼
┌──────────────────┐
│  Feedback &      │  ← adjust hotspots, constraints, filters
│  Iteration       │──────────────────────────────────────────┐
└──────────────────┘                                          │
         ▲                                                    │
         └────────────────────────────────────────────────────┘
```

### Scalability Considerations

- **Backbone generation (RFdiffusion):** Embarrassingly parallel. Run on GPU cluster; 10,000 designs in hours.
- **Sequence design (ProteinMPNN):** Lightweight; CPU-sufficient for most campaigns. Parallelize across backbones.
- **Structure prediction (AF2):** Most expensive step. Use ColabFold with MMseqs2 for MSA generation to reduce cost. Parallelize across GPU nodes. Budget 2–5 minutes per complex prediction.
- **Analysis and filtering:** CPU-only. Script all metrics into a single per-design scoring pipeline. Store results in a structured database (SQLite or Parquet) for downstream querying.

### Tracking and Reproducibility

Every design should carry a full lineage record:

- Parent backbone ID and RFdiffusion parameters
- ProteinMPNN sampling temperature and sequence rank
- AF2 model version and all metrics
- Filter pass/fail at each stage
- Cluster membership
- Experimental results (when available)

Use a design database — not filenames — to track this. A minimal schema: one table for backbones, one for sequences, one for predictions, one for experimental results, linked by foreign keys.

---

## Appendix: Quick-Reference Decision Checklist

Before launching a design campaign:

- [ ] Is the target structure high-resolution (<2.5 Å) and complete at the binding site?
- [ ] Have glycosylation sites near the hotspot been identified?
- [ ] Are hotspot residues accessible (SASA > 40 Å² per residue)?
- [ ] Is the hotspot definition constrained to 3–6 residues?
- [ ] Are at least 2 distinct hotspot definitions being explored?

Before filtering backbones:

- [ ] Have at least 1,000 backbones been generated per hotspot?
- [ ] Do clusters represent at least 10 distinct structural families?
- [ ] Has filtering been limited to physical plausibility (no premature metric-based cuts)?

Before selecting for experiments:

- [ ] Does the panel include designs from at least 10 structural families?
- [ ] Have monomer AF2 predictions confirmed independent folding?
- [ ] Have off-target predictions been run against at least 3 homologs?
- [ ] Do all designs pass developability thresholds (SAP, PackStat, net charge)?
- [ ] Are 15% of slots reserved for diversity insurance and hypothesis testing?
