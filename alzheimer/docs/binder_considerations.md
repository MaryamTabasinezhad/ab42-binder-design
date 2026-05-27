---
title: "Considerations for A$\\beta$42 Binder Candidates"
subtitle: "Biological Function, Formatting Strategy, and Pre-Experimental Concerns"
date: "2026-05-08"
geometry: "margin=2cm"
fontsize: 10pt
header-includes:
  - \usepackage{booktabs}
  - \usepackage{longtable}
  - \usepackage{colortbl}
  - \usepackage{xcolor}
  - \definecolor{greenhl}{RGB}{220,245,220}
  - \definecolor{redhl}{RGB}{255,220,220}
  - \definecolor{bluehl}{RGB}{210,230,255}
  - \definecolor{yellowhl}{RGB}{255,250,210}
  - \usepackage{array}
  - \usepackage{enumitem}
  - \usepackage{newunicodechar}
  - \newunicodechar{β}{$\beta$}
  - \newunicodechar{∼}{$\sim$}
---

\tableofcontents
\newpage

# 1. Expected Biological Functions of the 7 Accepted Binders

## 1.1 What These Binders Target

All 7 accepted binders were designed against the **HHQK epitope** (Y10, E11, H13, H14, Q15, K16) on an A$\beta$42 trimer extracted from PDB 9CO4 (receptor-bound conformation 1). This epitope region is functionally significant:

- **H13/H14** coordinate Cu$^{2+}$ and Zn$^{2+}$ ions --- metal binding at these residues drives A$\beta$ aggregation and reactive oxygen species (ROS) generation.
- **K16** sits at the boundary of the hydrophobic core (KLVFF$_{17-21}$) that drives $\beta$-sheet stacking in amyloid fibrils.
- **The HHQK motif** mediates heparan sulfate proteoglycan (HSPG) binding on neuronal surfaces, a key pathway for A$\beta$ cytotoxicity.

The binders are therefore not binding an inert surface --- they mask a **functionally active region** of A$\beta$42.

## 1.2 Realistic Biological Activities

### What the binders CAN likely do

\begin{enumerate}[leftmargin=*]
\item \textbf{Block metal-induced aggregation.} By shielding H13/H14, binders prevent Cu$^{2+}$/Zn$^{2+}$ coordination that nucleates toxic oligomers. This is a mechanism no approved antibody specifically exploits.

\item \textbf{Cap oligomers and prevent elongation.} The binders were designed against a trimer, so they recognize the oligomeric conformation. Binding sterically blocks further monomer addition, acting as aggregation terminators.

\item \textbf{Block A$\beta$--cell surface interactions.} Masking the HHQK heparan sulfate binding motif reduces neuronal uptake and membrane disruption by oligomers.

\item \textbf{Superior tissue penetration.} At 68--87 amino acids (7--10 kDa), these binders are $\sim$15$\times$ smaller than an IgG ($\sim$150 kDa). This is a genuine advantage for CNS delivery, especially when fused to a TfR1-binding module for BBB transcytosis.
\end{enumerate}

### What the binders CANNOT do

\begin{enumerate}[leftmargin=*]
\item \textbf{Disaggregate preformed fibrils.} Fibril disassembly requires breaking hundreds of backbone H-bonds along the cross-$\beta$ spine. No small binder has the thermodynamic leverage for this. Even lecanemab does not truly disaggregate mature fibrils --- it preferentially binds soluble protofibrils.

\item \textbf{Recruit immune clearance.} Without an Fc domain, there is no antibody-dependent cellular phagocytosis (ADCP), no complement activation, and no microglial recruitment for plaque clearance.

\item \textbf{Long serum half-life (unmodified).} Small proteins are cleared renally in minutes to hours versus weeks for IgG. This is addressable via engineering (see Section 2).
\end{enumerate}

## 1.3 Comparison with Lecanemab

\small

\begin{longtable}{|p{3.8cm}|p{5.5cm}|p{5.5cm}|}
\hline
\textbf{Feature} & \textbf{Lecanemab} & \textbf{These Binders} \\
\hline
Target epitope & Conformational protofibril epitope & Linear HHQK epitope on oligomer \\
\hline
Size & $\sim$150 kDa (IgG) & $\sim$7--10 kDa \\
\hline
Primary mechanism & Fc $\rightarrow$ microglial phagocytosis & Epitope masking (aggregation prevention) \\
\hline
Fibril disaggregation & Minimal (targets protofibrils) & No \\
\hline
Aggregation prevention & Yes (sequesters protofibrils) & Yes (caps oligomers, blocks metal sites) \\
\hline
BBB penetration & Poor ($\sim$0.1\% of plasma) & Much better intrinsically \\
\hline
Half-life & $\sim$5--7 days & Minutes--hours (unmodified) \\
\hline
ARIA risk & \cellcolor{redhl}Yes (Fc-mediated inflammation) & \cellcolor{greenhl}No (major safety advantage) \\
\hline
Production cost & Very high (mammalian cell culture) & Low (bacterial expression) \\
\hline
\end{longtable}

\normalsize

## 1.4 Summary of Therapeutic Positioning

These binders are \textbf{not lecanemab-like in mechanism}. Lecanemab is fundamentally an immune recruiter that flags A$\beta$ for destruction by microglia. These binders are \textbf{passive blockers} that bind and mask a functional epitope.

The most compelling use case is as the \textbf{A$\beta$-binding arm of a bispecific} with TfR1 for BBB transcytosis --- a small, brain-penetrant aggregation inhibitor with no ARIA risk. This is a genuinely differentiated therapeutic hypothesis from the antibody approach.

\newpage

# 2. Molecular Format Decision: Fc Fusion vs. Albumin-Binding Domain (ABD)

## 2.1 The Three Options

\small

\begin{longtable}{|p{2.5cm}|p{2cm}|p{2.2cm}|p{2cm}|p{1.5cm}|p{1.5cm}|p{1.8cm}|}
\hline
\textbf{Format} & \textbf{Half-life} & \textbf{Immune clearance} & \textbf{Expression} & \textbf{Size} & \textbf{ARIA} & \textbf{Purification} \\
\hline
Naked binder & Minutes & No & E. coli & $\sim$8 kDa & None & His-tag IMAC \\
\hline
\cellcolor{greenhl}\textbf{ABD fusion} & \cellcolor{greenhl}\textbf{14--19 days} & \cellcolor{greenhl}\textbf{No} & \cellcolor{greenhl}\textbf{E. coli} & \cellcolor{greenhl}\textbf{$\sim$13 kDa} & \cellcolor{greenhl}\textbf{None} & \cellcolor{greenhl}\textbf{Albumin-Seph} \\
\hline
Fc fusion & 7--21 days & Yes & Mammalian (CHO) & $\sim$80 kDa+ & Yes & Protein A \\
\hline
\end{longtable}

\normalsize

## 2.2 The Recommended Path: ABD Fusion

An \textbf{albumin-binding domain (ABD)} is a small ($\sim$5 kDa, $\sim$46 aa) three-helix protein --- originally from streptococcal Protein G --- that binds serum albumin with nanomolar affinity. Once bound, the binder hitchhikes on albumin's FcRn recycling pathway and inherits its $\sim$19-day half-life.

\textbf{Key advantages:}

\begin{enumerate}[leftmargin=*]
\item \textbf{Stays in E. coli} --- ABDs are small, disulfide-free, and fold robustly in the cytoplasm. Production cost remains low.

\item \textbf{Half-life problem solved} --- the ABD--albumin complex is $\sim$75 kDa, well above the renal clearance threshold ($\sim$60 kDa). Clinically validated half-lives of 14--19 days.

\item \textbf{No ARIA} --- no Fc effector functions means no microglial over-activation, no vasogenic edema, no microhemorrhages. ARIA affects 20--35\% of patients on lecanemab/aducanumab.

\item \textbf{Clinically validated} --- ozoralizumab (Nanozora), an ABD-fused anti-TNF$\alpha$ nanobody, is approved in Japan since 2022.

\item \textbf{Dual-function purification handle} --- the ABD serves as both an in vivo half-life extender and an in vitro purification tag (albumin-Sepharose affinity chromatography).
\end{enumerate}

## 2.3 Proposed Bispecific Construct Architecture

\begin{verbatim}
[TfR1 binder]---linker---[Ab42 binder]---linker---[ABD]
      |                        |                     |
 BBB crossing           Ab engagement        half-life extension
   (~8 kDa)               (~8 kDa)              (~5 kDa)
                                           
              Total: ~25-30 kDa
              Expression: E. coli
              Half-life: ~2-3 weeks
              Purification: Albumin-Sepharose or His-tag IMAC + SEC
\end{verbatim}

## 2.4 Purification Strategy Without Fc

The concern that Fc enables simple Protein A purification is valid but solvable:

\small

\begin{longtable}{|p{3cm}|p{4cm}|p{3cm}|p{3cm}|}
\hline
\textbf{Step} & \textbf{Method} & \textbf{Purity} & \textbf{Effort} \\
\hline
Capture & Albumin-Sepharose (via ABD) or Ni-NTA IMAC (His-tag) & $\sim$90--95\% & One step \\
\hline
Polish & Size-exclusion chromatography (SEC) & $>$98\% & One step \\
\hline
Endotoxin & Polymyxin B column or Triton X-114 & Endotoxin-free & One step \\
\hline
\end{longtable}

\normalsize

This is comparable effort to Protein A + SEC, which is what industry does with Fc-fused proteins (Protein A alone is never the final step).

## 2.5 When Would Fc Be Needed?

Fc fusion should only be considered if:

\begin{itemize}[leftmargin=*]
\item Experimental data shows that \textbf{active immune clearance} of A$\beta$ deposits is required for efficacy (i.e., passive blocking alone is insufficient).
\item You need to move toward clinical development under an \textbf{established regulatory framework} (Fc-fusion biologics have a well-trodden FDA path).
\end{itemize}

However, the field is increasingly shifting toward the view that \textbf{soluble oligomers are the toxic species}, not mature plaques --- which favors the sequestration/capping approach over immune-mediated plaque clearance.

## 2.6 Cost Comparison at Research Scale

\small

\begin{longtable}{|p{4cm}|p{4.5cm}|p{4.5cm}|}
\hline
& \textbf{Fc fusion (CHO cells)} & \textbf{E. coli + ABD/His-tag} \\
\hline
Cell line development & 3--6 months, \$50--100K & None \\
\hline
Media cost per liter & \$200--500 (serum-free) & \$5--10 (LB/TB) \\
\hline
Yield & 0.5--2 g/L (optimized) & 10--100 mg/L (sufficient) \\
\hline
Time to first milligram & 4--6 months & 2--3 weeks \\
\hline
Endotoxin removal & Not needed & Needed (standard protocol) \\
\hline
\end{longtable}

\normalsize

At the current stage (binding validation, aggregation assays, cell culture, possibly mouse models), milligrams are needed, not grams. E. coli delivers this in weeks, not months.

\newpage

# 3. Pre-Experimental Concerns and Mitigation Strategies

## 3.1 Concern Priority Matrix

\small

\begin{longtable}{|c|p{4.5cm}|c|c|p{4cm}|}
\hline
\textbf{Priority} & \textbf{Concern} & \textbf{Severity} & \textbf{Fix before lab?} & \textbf{Key mitigation} \\
\hline
\cellcolor{redhl}1 & Target conformation uncertainty & High & Partially & MD simulation \\
\hline
\cellcolor{redhl}2 & Low MPNN recovery (5/7 designs) & High & Yes & Prioritize s480128 \\
\hline
\cellcolor{yellowhl}3 & Interface Met oxidation (3/7) & Medium & Yes & MPNN M$\rightarrow$L/I redesign \\
\hline
\cellcolor{yellowhl}4 & Hydrophobic-dominated interfaces & Medium & Partially & $\Delta\Delta$G alanine scan \\
\hline
\cellcolor{yellowhl}5 & Limited scaffold diversity (4 unique) & Medium & Partially & More BindCraft runs \\
\hline
\cellcolor{yellowhl}6 & AF2 false-positive rate & Medium & No & Test multiple designs \\
\hline
\cellcolor{bluehl}7 & Cross-polymorph reactivity unknown & Low--Med & Yes & ColabFold re-prediction \\
\hline
\end{longtable}

\normalsize

## 3.2 Concern 1: Target Conformational Heterogeneity (HIGHEST RISK)

A$\beta$42 is an intrinsically disordered peptide that adopts dozens of polymorphs. The binders were designed against one specific trimer conformation from PDB 9CO4. The hotspot residues (9--16) sit at the boundary between the disordered N-terminus (residues 1--8) and the ordered core --- this region is \textbf{partially flexible even in 9CO4}.\newline

\textbf{Impact:} If the 9CO4 N-terminal conformation is rare under physiological conditions, the binders may fail to recognize real A$\beta$42 species.

\textbf{Mitigation:}
\begin{itemize}[leftmargin=*]
\item Run \textbf{MD simulations} (200--500 ns) on binder--trimer complexes to check interface stability
\item Complete the deferred \textbf{N-terminus MD project} to characterize epitope dynamics in the free trimer
\item Test binding experimentally against both \textbf{monomeric and oligomeric} A$\beta$42 --- if binding is oligomer-selective, this is a feature (toxic species targeting), not a bug
\end{itemize}

## 3.3 Concern 2: Low MPNN Sequence Recovery

\small

\begin{longtable}{|l|c|l|}
\hline
\textbf{Design} & \textbf{MPNN Recovery} & \textbf{Interpretation} \\
\hline
\cellcolor{greenhl}s480128\_mp13 & \cellcolor{greenhl}0.63 & Good sequence--structure compatibility \\
\cellcolor{greenhl}s480128\_mp17 & \cellcolor{greenhl}0.61 & Good sequence--structure compatibility \\
s120913\_mp1 & 0.41 & Moderate --- may still fold \\
s120913\_mp2 & 0.37 & Moderate --- monitor folding \\
\cellcolor{redhl}s716952\_mp20 & \cellcolor{redhl}0.33 & Weak --- higher misfolding risk \\
\cellcolor{redhl}s967366\_mp11 & \cellcolor{redhl}0.32 & Weak --- higher misfolding risk \\
\cellcolor{redhl}s311665\_mp6 & \cellcolor{redhl}0.31 & Weak --- highest misfolding risk \\
\hline
\end{longtable}

\normalsize

Recovery $<$0.4 means ProteinMPNN finds that the designed backbone does not strongly encode the designed sequence. These designs are more likely to misfold or adopt alternative conformations.

\textbf{Mitigation:}
\begin{itemize}[leftmargin=*]
\item Prioritize \textbf{s480128 designs} (recovery $>$0.6) for first experimental tests
\item Validate folding with \textbf{CD spectroscopy + thermal melt} before binding assays
\item For low-recovery designs: re-run ProteinMPNN at lower temperature (0.05--0.1) to find higher-compatibility sequences
\end{itemize}

## 3.4 Concern 3: Methionine Oxidation at Interface

\small

\begin{longtable}{|l|c|l|}
\hline
\textbf{Design} & \textbf{Interface Met count} & \textbf{Risk} \\
\hline
\cellcolor{greenhl}s480128\_mp13 & \cellcolor{greenhl}0 & None \\
\cellcolor{greenhl}s480128\_mp17 & \cellcolor{greenhl}0 & None \\
s120913\_mp1 & 1 & Low \\
s120913\_mp2 & 2 & Moderate \\
\cellcolor{redhl}s716952\_mp20 & \cellcolor{redhl}3 & High \\
\cellcolor{redhl}s967366\_mp11 & \cellcolor{redhl}3 & High \\
\cellcolor{redhl}s311665\_mp6 & \cellcolor{redhl}3 & High \\
\hline
\end{longtable}

\normalsize

AD brains have elevated oxidative stress. Surface-exposed methionine oxidizes to methionine sulfoxide, which changes side-chain geometry, disrupts binding contacts, creates heterogeneous protein populations, and may increase immunogenicity.

\textbf{Mitigation:}
\begin{itemize}[leftmargin=*]
\item For designs with Met $\geq$ 2 at interface: run \textbf{targeted MPNN redesign} fixing all non-Met positions and allowing only M$\rightarrow$L or M$\rightarrow$I substitutions (isosteric, oxidation-resistant)
\item Test oxidation susceptibility: incubate with 0.1\% H$_2$O$_2$ for 2 hours, then check binding by SPR
\item The \textbf{s480128 designs have zero interface Met} --- another reason to prioritize them
\end{itemize}

## 3.5 Concern 4: Hydrophobic-Dominated Interfaces and Specificity

5 of 7 designs have \textbf{zero salt bridges} and only 3--5 H-bonds. Interfaces are dominated by hydrophobic contacts (142--203 pairs). Hydrophobic interfaces tend to be less specific, more prone to non-specific aggregation, and less tolerant of conformational changes.

Only s120913 has salt bridges (2--4 per design), providing electrostatic specificity.

\textbf{Mitigation:}
\begin{itemize}[leftmargin=*]
\item Run \textbf{Rosetta alanine scanning ($\Delta\Delta$G)} on each design to identify critical interface residues --- if binding energy is distributed over many weak hydrophobic contacts rather than concentrated on key residues, specificity is a concern
\item Test \textbf{off-target binding} against serum proteins (BSA, transferrin, IgG) by SPR --- a specific binder should show $<$1\% cross-reactivity
\item Consider computational re-design to introduce 1--2 additional polar contacts at the interface
\end{itemize}

## 3.6 Concern 5: Limited Scaffold Diversity

7 designs come from only \textbf{5 seeds / 4 unique scaffolds}:

\begin{itemize}
\item s120913: 2 designs (mpnn1, mpnn2) --- same backbone
\item s480128: 2 designs (mpnn13, mpnn17) --- same backbone
\item s967366: 1 design
\item s311665: 1 design
\item s716952: 1 design
\end{itemize}

If a scaffold has a fundamental problem (misfolding, aggregation, off-target binding), both designs from that scaffold fail together. Effective diversity is 5, not 7.

\textbf{Mitigation:}
\begin{itemize}[leftmargin=*]
\item Test \textbf{at least one design from each scaffold} --- do not test both s120913 variants while skipping another scaffold
\item Continue running BindCraft to generate more scaffold diversity
\item Consider the RFdiffusion $\rightarrow$ ProteinMPNN $\rightarrow$ ColabFold pipeline for orthogonal scaffold generation
\end{itemize}

## 3.7 Concern 6: AF2 Validation $\neq$ Experimental Binding

All 7 designs passed BindCraft's AF2-based filters (i\_pTM $>$ 0.5, pLDDT $>$ 0.8, etc.). However, AF2 is trained on natural proteins and can give false-positive confidence for designed sequences. Literature success rates for computationally designed binders range 15--50\% depending on method and target.

\textbf{Realistic expectation:} 2--4 of the 7 designs will actually bind in the lab.

\textbf{Mitigation:}
\begin{itemize}[leftmargin=*]
\item This is inherent uncertainty --- not fixable computationally
\item \textbf{Test all designs} (or at least 4--5) to maximize hit rate
\item Gene synthesis for all 7 costs $\sim$\$700 total --- cheap insurance
\item Use \textbf{yeast surface display} if available for parallel screening
\end{itemize}

## 3.8 Concern 7: Unknown Cross-Polymorph Reactivity

Binders were designed against 9CO4 (conformation 1), but the brain contains multiple A$\beta$42 polymorphs simultaneously. Whether these binders cross-react with other polymorphs (Type II fibrils, Osaka mutant, Iowa mutant) is unknown.

\textbf{Mitigation:}
\begin{itemize}[leftmargin=*]
\item Run \textbf{ColabFold re-prediction} of binders complexed with A$\beta$42 from other fibril structures (7Q4B, 6SHS, etc.) --- check if i\_pTM remains high
\item This is purely computational and costs only GPU time
\end{itemize}

\newpage

# 4. Recommended Pre-Experimental Action Plan

## Stage A: Computational Validation (1--2 weeks on HPC)

\begin{enumerate}[leftmargin=*]
\item \textbf{MD simulations} on top 3 binder--target complexes (s120913\_mp1, s480128\_mp13, s311665\_mp6)
\begin{itemize}
\item 200--500 ns each in explicit solvent using GROMACS
\item Monitor: interface RMSD, contact persistence, binding free energy (MM-GBSA)
\item \textbf{Kill criterion:} if binder dissociates or RMSD $>$5 \AA\ within 100 ns $\rightarrow$ discard design
\end{itemize}

\item \textbf{Rosetta $\Delta\Delta$G alanine scan} on all 7 designs
\begin{itemize}
\item Identifies critical residues and interface robustness
\item 1--2 hours per design on CPU
\end{itemize}

\item \textbf{Cross-polymorph ColabFold prediction}
\begin{itemize}
\item Predict binding to 2--3 other A$\beta$42 fibril structures
\item 30 min per design on GPU
\end{itemize}

\item \textbf{MPNN Met-substitution} for designs with $\geq$2 interface Met
\begin{itemize}
\item Re-design with M$\rightarrow$L/I constraint, re-validate with ColabFold
\end{itemize}
\end{enumerate}

## Stage B: Gene Synthesis + Pilot Expression (2--3 weeks)

\begin{enumerate}[leftmargin=*,start=5]
\item \textbf{Order synthetic genes} for 4--5 designs (one per scaffold)
\begin{itemize}
\item Codon-optimized for E. coli
\item With N-terminal His$_6$-SUMO tag for expression and purification
\item Estimated cost: \$500--700 total
\end{itemize}

\item \textbf{Express and assess folding}
\begin{itemize}
\item SDS-PAGE for expression level
\item SEC for monodispersity (no aggregation)
\item CD spectroscopy for secondary structure ($>$60\% helical expected)
\item Thermal melt (T$_m$ $>$50$^\circ$C is reassuring for a designed protein)
\end{itemize}
\end{enumerate}

## Stage C: Binding Validation (1--2 weeks after protein in hand)

\begin{enumerate}[leftmargin=*,start=7]
\item \textbf{SPR or BLI binding assay} against:
\begin{itemize}
\item Monomeric A$\beta$42 (HFIP-treated, freshly dissolved)
\item Oligomeric A$\beta$42 (4$^\circ$C incubation, 24 h)
\item Off-target controls (BSA, transferrin, IgG)
\end{itemize}

\item \textbf{ThT aggregation inhibition assay}
\begin{itemize}
\item Measure Thioflavin T fluorescence with and without binder
\item Determines if the binder slows A$\beta$42 fibril formation
\end{itemize}
\end{enumerate}

## Stage D: Functional Characterization (if binding confirmed)

\begin{enumerate}[leftmargin=*,start=9]
\item \textbf{Oligomer capping assay} --- DLS/SEC to check if binder arrests oligomer growth

\item \textbf{Metal competition assay} --- test if binder blocks Cu$^{2+}$/Zn$^{2+}$ binding to A$\beta$42 H13/H14

\item \textbf{Cell-based neurotoxicity protection} --- SH-SY5Y or primary neurons, measure viability with/without binder in the presence of A$\beta$42 oligomers

\item \textbf{Bispecific construct assembly} --- fuse best A$\beta$42 binder with TfR1 binder + ABD, express as single chain, validate dual binding
\end{enumerate}

\newpage

# 5. Recommended Minimum Test Panel

Based on balancing scaffold diversity, MPNN recovery, interface quality, and functional features:

\small

\begin{longtable}{|c|l|p{2.5cm}|p{7cm}|}
\hline
\textbf{Priority} & \textbf{Design} & \textbf{Scaffold} & \textbf{Rationale} \\
\hline
\cellcolor{greenhl}1 & s480128\_mp13 & s480128 & Highest MPNN recovery (0.63), zero interface Met, clean metrics. \textbf{Safest first bet.} \\
\hline
\cellcolor{greenhl}2 & s120913\_mp1 & s120913 & Highest i\_pTM (0.81), 14/18 hotspots, 4 salt bridges. \textbf{Best binding potential.} \\
\hline
\cellcolor{bluehl}3 & s716952\_mp20 & s716952 & Unique chain G coverage (6/6 including H13/H14). \textbf{Distinct epitope engagement.} \\
\hline
\cellcolor{bluehl}4 & s311665\_mp6 & s311665 & Smallest (68 aa, 7.5 kDa), best for bispecific fusion. \textbf{Format candidate.} \\
\hline
5 & s967366\_mp11 & s967366 & Highest pLDDT (0.94), best shape complementarity. Only if budget allows 5th design. \\
\hline
\end{longtable}

\normalsize

\vspace{0.5cm}

\textbf{Key principle:} Test at least one design from each unique scaffold. Do not test both s120913 variants (mpnn1 + mpnn2) while omitting a different scaffold entirely. Scaffold-level diversity matters more than sequence-level diversity for maximizing the probability of at least one experimental hit.

\vspace{1cm}

\begin{center}
\rule{0.7\textwidth}{0.5pt}

\small
\textit{Report generated for the A$\beta$42 $\times$ TfR1 bispecific binder design project.}

\textit{BindCraft campaign on Frontenac HPC (Queen's University).}

\textit{2026-05-08}
\end{center}
