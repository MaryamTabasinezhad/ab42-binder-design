# BindCraft Abeta42 Binder Campaign -- Full 62-Design Analysis

**Date:** 2026-05-26
**Target:** Receptor-bound Abeta42 filament (PDB 9CO4, chains C/E/G, Conformation 1)
**Tool:** BindCraft v1.1.3 (ColabDesign), 4-stage protocol
**Hotspots:** C10,C11,C13,C14,C15,C16,E10,E11,E13,E14,E15,E16,G10,G11,G13,G14,G15,G16
**Design length range:** 60--90 residues

---

## 1. Campaign Statistics

### 1.1 Throughput Summary

| Metric | Value |
|--------|-------|
| Total trajectories attempted | 1,342 (1,178 main + 164 supplementary) |
| Trajectories passing to MPNN | ~324 (~24% of trajectories) |
| Total MPNN designs evaluated | 2,977 |
| Accepted designs | **62** |
| Unique scaffolds | **38** |
| Scaffolds with 2 accepted designs | 24 |
| Scaffolds with 1 accepted design | 14 |
| Acceptance rate (per trajectory) | 5.3% |
| Acceptance rate (per MPNN design) | 2.1% |

### 1.2 Failure Funnel (Combined Across All Runs)

**Trajectory-level rejections** (before MPNN stage):

| Failure Reason | Count | Notes |
|----------------|-------|-------|
| Trajectory_final_pLDDT | 433 | Backbone quality too low |
| Trajectory_one-hot_pLDDT | 406 | |
| Trajectory_Clashes | 197 | Steric clashes in backbone |
| Trajectory_logits_pLDDT | 57 | |
| Trajectory_softmax_pLDDT | 46 | |
| **Total trajectory failures** | **1,139** | ~85% of trajectories |

**AF2 filter rejections** (per MPNN design, designs can fail multiple filters):

| Filter | Rejections | % of MPNN designs | Comment |
|--------|-----------|-------------------|---------|
| i_pAE (>0.35) | 21,955 | -- | Strictest filter; i_pAE and i_pTM are correlated |
| i_pTM (<0.5) | 20,815 | -- | Most designs fail interface confidence |
| pTM (<0.55) | 9,878 | -- | |
| pLDDT (<0.8) | 9,299 | -- | |
| Surface_Hydrophobicity (>0.35) | 2,554 | **#1 non-confidence filter** | |
| InterfaceAAs_M (>=3) | 1,881 | **#2 non-confidence filter** | Met at interface |
| n_InterfaceUnsatHbonds (>=4) | 1,350 | | Unsatisfied polar contacts |
| n_InterfaceHbonds (<3) | 1,206 | | Too few H-bonds |
| Binder_RMSD (>=3.5) | 848 | | Binder doesn't refold |
| Binder_pLDDT (<0.8) | 477 | | |
| Hotspot_RMSD (>=6) | 72 | | |
| InterfaceAAs_K (>=3) | 49 | | Lysine enrichment |
| ShapeComplementarity (<0.55) | 16 | | |

**Key finding:** Surface hydrophobicity and interface methionine remain the dominant non-confidence bottlenecks, consistent with the 7-design interim analysis. The i_pTM/i_pAE filters dominate overall, reflecting the fundamental difficulty of computationally confident binder-target interaction prediction against the Abeta42 fibril groove.

### 1.3 Length Distribution

| Length | Count | | Length | Count |
|--------|-------|-|--------|-------|
| 60 | 3 | | 77 | 2 |
| 61 | 1 | | 78 | 2 |
| 62 | 1 | | 79 | 6 |
| 63 | 4 | | 80 | 1 |
| 65 | 1 | | 81 | 2 |
| 67 | 2 | | 82 | 5 |
| 68 | 1 | | 84 | 3 |
| 70 | 7 | | 85 | 3 |
| 71 | 1 | | 86 | 4 |
| 72 | 2 | | 87 | 1 |
| 76 | 3 | | 89 | 3 |
| | | | 90 | 4 |

**Mean:** 76.7 | **Median:** 79.0 | **Std dev:** 9.1

The distribution is right-skewed with a mode around 79--86 residues. The shortest accepted design is 60 aa (s837308) and the longest is 90 aa (s311742). The 70--90 range accounts for 46/62 (74%) of accepted designs, suggesting longer binders are more capable of engaging the multi-chain fibril interface.

---

## 2. Key Metric Distributions

| Metric | Min | P10 | P25 | Median | P75 | P90 | Max | Mean |
|--------|-----|-----|-----|--------|-----|-----|-----|------|
| Average_i_pTM | 0.560 | 0.650 | 0.710 | 0.780 | 0.810 | 0.820 | 0.860 | 0.755 |
| Average_pLDDT | 0.810 | 0.840 | 0.870 | 0.900 | 0.920 | 0.940 | 0.940 | 0.893 |
| Average_dG (REU) | -107.0 | -90.8 | -86.0 | -77.4 | -70.8 | -62.7 | -49.2 | -78.0 |
| Average_dG/dSASA | -4.10 | -3.67 | -3.58 | -3.34 | -3.19 | -3.09 | -2.68 | -3.37 |
| Average_ShapeComp | 0.640 | 0.660 | 0.680 | 0.710 | 0.730 | 0.760 | 0.790 | 0.707 |
| Average_n_InterfaceHbonds | 3.0 | 3.5 | 3.5 | 4.5 | 7.5 | 9.5 | 11.5 | 5.6 |
| Average_n_InterfaceUnsatH | 0.0 | 0.5 | 1.5 | 2.0 | 3.0 | 3.5 | 4.0 | 2.2 |
| Average_Surface_Hydro | 0.220 | 0.270 | 0.290 | 0.320 | 0.330 | 0.340 | 0.350 | 0.308 |
| MPNN_seq_recovery | 0.210 | 0.260 | 0.330 | 0.380 | 0.430 | 0.490 | 0.640 | 0.381 |
| Average_Hotspot_RMSD (A) | 0.79 | 1.12 | 1.19 | 1.56 | 1.92 | 2.69 | 4.80 | 1.71 |
| Average_Binder_RMSD (A) | 0.59 | 1.07 | 1.21 | 1.58 | 2.05 | 2.42 | 3.50 | 1.67 |
| Average_dSASA (A^2) | 1,550 | 2,022 | 2,128 | 2,280 | 2,474 | 2,725 | 3,146 | 2,312 |

---

## 3. Top Designs Ranking

### 3.1 Composite Scoring Methodology

Designs are ranked by a weighted composite of min-max-normalized metrics:

```
Score = 0.30 * norm(i_pTM, higher=better)
      + 0.25 * norm(dG, lower=better)
      + 0.15 * norm(pLDDT, higher=better)
      + 0.10 * norm(ShapeComplementarity, higher=better)
      + 0.10 * norm(n_InterfaceHbonds, higher=better)
      + 0.05 * norm(n_InterfaceUnsatHbonds, lower=better)
      + 0.05 * norm(Surface_Hydrophobicity, lower=better)
```

### 3.2 Top 15 Designs

| Rank | Design | Score | i_pTM | dG | pLDDT | SC | Hbonds | UnsatH | SurfH | Len | SeqRec |
|------|--------|-------|-------|------|-------|-----|--------|--------|-------|-----|--------|
| 1 | s453481_mp1 | 0.856 | 0.850 | -102.5 | 0.940 | 0.730 | 10.0 | 3.0 | 0.270 | 86 | 0.42 |
| 2 | s453481_mp3 | 0.830 | 0.850 | -102.0 | 0.940 | 0.730 | 8.0 | 3.0 | 0.270 | 86 | 0.46 |
| 3 | s311742_mp16 | 0.786 | 0.860 | -88.8 | 0.940 | 0.760 | 4.5 | 2.0 | 0.240 | 90 | 0.33 |
| 4 | s311742_mp3 | 0.778 | 0.860 | -88.0 | 0.940 | 0.760 | 4.5 | 3.0 | 0.220 | 90 | 0.34 |
| 5 | s857331_mp4 | 0.756 | 0.800 | -87.8 | 0.920 | 0.780 | 7.5 | 1.0 | 0.250 | 86 | 0.36 |
| 6 | s946181_mp6 | 0.750 | 0.840 | -92.5 | 0.930 | 0.660 | 11.0 | 2.0 | 0.320 | 82 | 0.43 |
| 7 | s120913_mp2 | 0.743 | 0.810 | -98.9 | 0.880 | 0.690 | 11.5 | 1.0 | 0.280 | 79 | 0.37 |
| 8 | s857331_mp12 | 0.702 | 0.800 | -84.0 | 0.930 | 0.770 | 6.5 | 2.5 | 0.280 | 86 | 0.39 |
| 9 | s837308_mp6 | 0.684 | 0.790 | -81.7 | 0.920 | 0.790 | 3.5 | 0.0 | 0.270 | 60 | 0.24 |
| 10 | s766115_mp9 | 0.678 | 0.780 | -107.0 | 0.840 | 0.710 | 11.5 | 4.0 | 0.280 | 61 | 0.28 |
| 11 | s946181_mp9 | 0.676 | 0.820 | -89.3 | 0.920 | 0.650 | 9.5 | 2.0 | 0.330 | 82 | 0.45 |
| 12 | s817651_mp19 | 0.674 | 0.840 | -75.2 | 0.940 | 0.720 | 5.5 | 1.0 | 0.320 | 72 | 0.44 |
| 13 | s120913_mp1 | 0.669 | 0.810 | -93.7 | 0.880 | 0.680 | 7.5 | 1.5 | 0.260 | 79 | 0.41 |
| 14 | s306498_mp16 | 0.648 | 0.800 | -81.6 | 0.940 | 0.770 | 4.0 | 3.0 | 0.330 | 77 | 0.38 |
| 15 | s837308_mp3 | 0.646 | 0.800 | -77.8 | 0.920 | 0.770 | 3.5 | 0.5 | 0.300 | 60 | 0.32 |

### 3.3 Commentary on Top Designs

**Rank 1--2: s453481 (L=86).** The clear campaign champion. Both MPNN variants share the same scaffold and are 87% sequence-identical. i_pTM=0.85, dG~-102 REU, pLDDT=0.94. This scaffold has the deepest binding energy in the campaign while maintaining top-tier confidence. 10 H-bonds (mpnn1) is well above the median of 4.5. Interface met count is 3.0 (at the filter boundary), which is a risk flag. PackStat=0.69 is excellent. Both have ~3% beta-sheet content -- one of the few scaffolds with mixed secondary structure.

**Rank 3--4: s311742 (L=90).** Highest i_pTM in the campaign (0.86). Lowest surface hydrophobicity (0.22). Excellent shape complementarity (0.76). The longest accepted designs at 90 residues. Nearly all-helical (85% helix). However: zero tryptophans in the full sequence, making A280 concentration determination impossible without mutagenesis. Also 3.0 Met at interface. These two variants are 82% sequence-identical with 96% interface residue overlap -- functionally redundant.

**Rank 5: s857331_mpnn4 (L=86).** Best shape complementarity in the top 10 (SC=0.78), best dG/dSASA efficiency (-3.83), and only 1.0 unsatisfied H-bond. Interface Met=2.0 (below the filter boundary = lower risk). Low surface hydrophobicity (0.25). A strong all-around candidate.

**Rank 6: s946181_mpnn6 (L=82).** Second-highest i_pTM among non-s311742 designs (0.84). dG=-92.5 REU. 11 interface H-bonds -- tied for most in the campaign. Interface Met=1.0, the second-lowest among all designs. Has mixed alpha/beta structure (2.4% beta). However, zero Trp in full sequence (A280 issue), and shape complementarity is low (SC=0.66).

**Rank 7: s120913_mpnn2 (L=79).** Deepest dG after s453481 (-98.9 REU). Largest interface (40 residues, 3,146 A^2 buried SASA). 11.5 H-bonds and only 1.0 unsatisfied. Has mixed alpha/beta topology (2.5% beta, 7.4% interface beta). Interface Met=2.0. Caveat: has relaxed clashes (0.5) and the highest binder RMSD among top designs (2.18 A), suggesting some conformational uncertainty.

**Rank 9: s837308_mpnn6 (L=60).** The smallest accepted design at 60 residues. Best shape complementarity overall (SC=0.79). Zero unsatisfied H-bonds. All-helical (90% helix). Strikingly low binder RMSD (1.59 A). However, only 3.5 H-bonds (near the filter minimum) and low MPNN recovery (0.24). Interface Met=3.0.

**Rank 10: s766115_mpnn9 (L=61).** Most negative dG in the entire campaign (-107.0 REU). Best dG/dSASA efficiency (-4.10). Very compact 61-residue design. 11.5 H-bonds. However, pLDDT is only 0.84 (near the filter boundary), and binder pLDDT is 0.83 (also low). Has 4.0 unsatisfied H-bonds (at the filter boundary). The design has the most mixed topology: only 53.5% interface helix, 7.4% beta. Despite extreme binding energy, the lower confidence and high unsatisfied H-bonds make this higher risk.

**Rank 12: s817651_mpnn19 (L=72).** Lowest hotspot RMSD in the campaign (0.79 A), meaning AF2 places the binder closest to the intended hotspot configuration. Best PackStat (0.71). i_pTM=0.84, pLDDT=0.94. However, zero Trp in full sequence. Interface Met=3.0.

### 3.4 Pareto-Optimal Designs (i_pTM vs dG)

Only 3 designs are non-dominated on the i_pTM vs dG Pareto front:

| Design | i_pTM | dG (REU) | pLDDT |
|--------|-------|----------|-------|
| s311742_mpnn16 | 0.860 | -88.8 | 0.940 |
| s453481_mpnn1 | 0.850 | -102.5 | 0.940 |
| s766115_mpnn9 | 0.780 | -107.0 | 0.840 |

### 3.5 Stringent Filter Analysis

**Stringent (i_pTM >= 0.8, dG <= -80, pLDDT >= 0.9): 11 designs pass.**
These are the highest-confidence candidates:

| Design | i_pTM | dG | pLDDT |
|--------|-------|----|-------|
| s453481_mpnn1 | 0.850 | -102.5 | 0.940 |
| s453481_mpnn3 | 0.850 | -102.0 | 0.940 |
| s311742_mpnn3 | 0.860 | -88.0 | 0.940 |
| s311742_mpnn16 | 0.860 | -88.8 | 0.940 |
| s946181_mpnn6 | 0.840 | -92.5 | 0.930 |
| s946181_mpnn9 | 0.820 | -89.3 | 0.920 |
| s857331_mpnn4 | 0.800 | -87.8 | 0.920 |
| s857331_mpnn12 | 0.800 | -84.0 | 0.930 |
| s794643_mpnn3 | 0.820 | -82.2 | 0.920 |
| s794643_mpnn1 | 0.810 | -82.2 | 0.910 |
| s306498_mpnn16 | 0.800 | -81.6 | 0.940 |

---

## 4. Hotspot Coverage Analysis

All 62 designs target the same 18 hotspot residues: Y10, E11, H13, H14, Q15, K16 on each of chains C, E, and G.

The Target_Hotspot column is identical across all designs (all were generated with the same hotspot specification). Since BindCraft does not report per-residue contact maps in the CSV, hotspot engagement is assessed indirectly through:

- **Hotspot RMSD:** The RMSD of the target hotspot region between the designed and reference structures. Lower = AF2 agrees the binder engages the hotspot correctly.

| Hotspot RMSD | Count | Interpretation |
|-------------|-------|----------------|
| <1.0 A | 4 | Excellent hotspot preservation |
| 1.0--1.5 A | 29 | Good hotspot preservation |
| 1.5--2.0 A | 14 | Moderate |
| 2.0--3.0 A | 10 | Some deviation |
| 3.0--5.0 A | 5 | Significant deviation |

**Best hotspot RMSD designs:**
- s817651_mpnn19: 0.79 A
- s857331_mpnn4: 1.00 A
- s837308_mpnn3: 1.01 A
- s120913_mpnn1: 1.02 A

**Worst hotspot RMSD designs:**
- s103118_mpnn17: 4.80 A
- s867664_mpnn2: 3.64 A
- s289797_mpnn2: 3.09 A

Given the trimeric arrangement of chains C/E/G, all binders engage the same groove between filament protofilaments. The key challenge is not *which* hotspots are contacted (the Y10-E11-H13-H14-Q15-K16 stretch forms a contiguous surface) but rather *how many chains* the binder spans. Designs with larger interfaces (30+ residues) likely bridge at least 2 of the 3 chains. The s120913 scaffold (32--40 interface residues) and the s946181 scaffold (34--36 interface residues) are the best multi-chain engagement candidates.

---

## 5. Interface Quality Analysis

### 5.1 Hydrogen Bond Quality

| Metric | Min | Median | Mean | Max |
|--------|-----|--------|------|-----|
| n_InterfaceHbonds | 3.0 | 4.5 | 5.6 | 11.5 |
| n_InterfaceUnsatHbonds | 0.0 | 2.0 | 2.2 | 4.0 |
| InterfaceHbondsPercentage | 11.3% | 19.3% | 20.6% | 39.2% |
| InterfaceUnsatHbondsPercentage | 0.0% | 8.5% | 8.3% | 16.3% |

**High H-bond designs (>=9):**
- s120913_mpnn2: 11.5 Hbonds, 1.0 unsat
- s766115_mpnn9: 11.5 Hbonds, 4.0 unsat (concerning)
- s946181_mpnn6: 11.0 Hbonds, 2.0 unsat
- s313438_mpnn2: 10.0 Hbonds, 2.0 unsat
- s453481_mpnn1: 10.0 Hbonds, 3.0 unsat
- s946181_mpnn9: 9.5 Hbonds, 2.0 unsat
- s313438_mpnn5: 9.5 Hbonds, 3.5 unsat
- s228379_mpnn6: 9.0 Hbonds, 1.0 unsat

**Zero unsatisfied H-bond designs:**
- s837308_mpnn6: 0.0 unsat (3.5 Hbonds total)
- s980366_mpnn2: 0.0 unsat (3.0 Hbonds total)

### 5.2 Shape Complementarity

| SC range | Count | Interpretation |
|----------|-------|----------------|
| >=0.75 | 12 | Excellent (antibody-like) |
| 0.70--0.75 | 19 | Good |
| 0.65--0.70 | 22 | Adequate |
| <0.65 | 9 | Below average |

**Best SC:** s837308_mpnn6 (0.79), s857331_mpnn4 (0.78), s306498_mpnn13/mpnn16 (0.77), s857331_mpnn12 (0.77), s837308_mpnn3 (0.77).

### 5.3 dG/dSASA Binding Efficiency

The dG/dSASA ratio normalizes binding energy by interface size, revealing per-unit-area binding efficiency.

| Design | dG/dSASA | dG | dSASA | Comment |
|--------|----------|------|-------|---------|
| s766115_mpnn9 | -4.10 | -107.0 | 2,610 | Best efficiency, compact interface |
| s857331_mpnn4 | -3.83 | -87.8 | 2,301 | Efficient |
| s794643_mpnn1 | -3.79 | -82.2 | 2,173 | Small binder, high efficiency |
| s453481_mpnn1 | -3.75 | -102.5 | 2,740 | Deep energy AND good efficiency |
| s311742_mpnn3 | -3.71 | -88.0 | 2,375 | |
| s857331_mpnn12 | -3.68 | -84.0 | 2,280 | |

Mean dG/dSASA: -3.37. The campaign average is reasonable; values below -3.5 indicate above-average efficiency.

### 5.4 Interface Methionine Content

Interface methionine was the #2 non-confidence rejection reason (1,881 MPNN designs rejected). The filter boundary is M < 3.

| Met count | Accepted designs | Risk level |
|-----------|-----------------|------------|
| M = 0.0 | 2 (s480128 mpnn13, mpnn17) | Lowest risk |
| M = 1.0 | 4 (s120913_mp1, s313438_mp5, s946181_mp6, s946181_mp9) | Low risk |
| M = 2.0 | 18 | Moderate |
| M = 2.5 | 4 | Elevated (near boundary) |
| M = 3.0 | 34 | **At boundary** (55% of designs) |

**55% of accepted designs sit exactly at the Met filter boundary (M=3.0).** This is an artifact of the filter threshold: BindCraft accepts "M < 3" (or possibly M <= 3, given that 34 designs passed with M=3.0). These designs are not necessarily problematic, but the high Met content at the interface could indicate:
- Overrepresentation of Met in initial backbone design (BindCraft hallucinate preference)
- Potential oxidation sensitivity in experimental conditions
- Possible non-specific hydrophobic interactions

**Lowest Met designs with strong metrics:**
- s946181_mpnn6: M=1.0, i_pTM=0.84, dG=-92.5 (excellent candidate)
- s946181_mpnn9: M=1.0, i_pTM=0.82, dG=-89.3
- s120913_mpnn1: M=1.0, i_pTM=0.81, dG=-93.7

### 5.5 Surface Hydrophobicity

Filter threshold: <0.35 (all accepted designs pass by definition).

| Range | Count |
|-------|-------|
| <0.25 | 2 (s311742_mpnn3 at 0.22, s311742_mpnn16 at 0.24) |
| 0.25--0.30 | 17 |
| 0.30--0.35 | 43 |

Most designs cluster near the 0.35 boundary. The s311742 pair has the best surface hydrophobicity, but the s857331 pair (0.25, 0.28) and s453481 pair (0.27) are also favorable.

---

## 6. MPNN Sequence Recovery

| Range | Count | Interpretation |
|-------|-------|----------------|
| <0.25 | 5 | Higher risk -- MPNN couldn't "explain" the structure well |
| 0.25--0.35 | 19 | Typical for de novo designs |
| 0.35--0.45 | 24 | Good recovery |
| 0.45--0.55 | 8 | High recovery |
| >0.55 | 6 | Very high recovery |

**Mean:** 0.381 | **Median:** 0.380

**Low recovery designs (<0.25) -- potential risk:**
- s313438_mpnn2: 0.21
- s313438_mpnn5: 0.21
- s71039_mpnn1: 0.22
- s944140_mpnn3: 0.23
- s837308_mpnn6: 0.24

**High recovery (>0.50) -- sequence/structure agreement strong:**
- s557298_mpnn12: 0.64
- s480128_mpnn13: 0.63
- s480128_mpnn17: 0.61
- s822708_mpnn14: 0.55

**Correlations (Pearson r):**

| Pair | r | Interpretation |
|------|---|----------------|
| MPNN_seq_recovery vs i_pTM | -0.088 | No correlation |
| MPNN_seq_recovery vs dG | +0.084 | No correlation |
| MPNN_seq_recovery vs pLDDT | +0.074 | No correlation |
| i_pTM vs dG | **-0.648** | Strong: better i_pTM = more negative dG |
| dG vs dSASA | **-0.860** | Very strong: larger interface = more negative dG |
| i_pTM vs SC | +0.260 | Weak positive |

The lack of correlation between MPNN recovery and AF2 confidence metrics is expected -- these are orthogonal quality measures. The strong i_pTM vs dG correlation (r=-0.65) suggests these are not independent axes, which validates using both in the composite score.

---

## 7. Structural Diversity

### 7.1 Binder Topology

| Helix % | Count | Beta % | Count |
|---------|-------|--------|-------|
| 50--60% | 1 | 0% | 48 (77%) |
| 60--70% | 8 | >0% | 14 (23%) |
| 70--80% | 12 | | |
| 80--90% | 35 | | |
| 90--100% | 6 | | |

**Mean helicity:** 80.4% | **Mean beta:** 0.8% | **Mean loop:** 18.7%

The campaign is dominated by all-helical designs (77% have zero beta content). This is expected for BindCraft's bias toward helical miniproteins but limits structural diversity.

**Designs with beta-sheet content (>0%):**

| Scaffold | Beta % | Helix % | Topology note |
|----------|--------|---------|---------------|
| s120913 | 2.5% | 66--67% | Mixed alpha/beta, large interface |
| s946181 | 2.4% | 80.5% | Minor beta |
| s453481 | 3.5% | 80.2% | Top-ranked scaffold |
| s766115 | 7.4% | 67.2% | Most beta content, highest dG |
| s71039 | 10.8% | 56.9% | **Most beta-rich binder** |
| s443975 | 2.9% | 82.1% | |
| s313438 | 4.3% | 82.9% | |
| s496499 | 4.6% | 73.8% | |

### 7.2 Interface Secondary Structure

| Interface Helix % | Count |
|-------------------|-------|
| 50--60% | 2 |
| 60--70% | 10 |
| 70--80% | 4 |
| 80--90% | 8 |
| 90--100% | 38 |

Most interfaces are purely helical (61% have >90% helix at interface). The s946181 and s120913 scaffolds are notable for presenting mixed alpha/beta interfaces (~66% helix), which provides structural diversity for the test panel.

---

## 8. Scaffold Analysis (Paired Variants)

24 of 38 scaffolds produced exactly 2 accepted MPNN variants. The table below compares each pair.

| Scaffold | Seq ID | Iface Overlap | i_pTM delta | dG delta | Redundancy? |
|----------|--------|---------------|-------------|----------|-------------|
| s453481 (L86) | 87.2% | 91.2% | 0.000 | 0.5 REU | Largely redundant |
| s311742 (L90) | 82.2% | 96.4% | 0.000 | 0.8 REU | Largely redundant |
| s857331 (L86) | 79.1% | 95.7% | 0.000 | 3.8 REU | Minor variants |
| s946181 (L82) | 80.5% | 91.7% | 0.020 | 3.2 REU | Minor variants |
| s120913 (L79) | 87.3% | 80.0% | 0.000 | 5.2 REU | **Some diversity** (Iface overlap=80%) |
| s313438 (L70) | 78.6% | 96.0% | 0.010 | 2.9 REU | Largely redundant |
| s794643 (L63) | 90.5% | 92.3% | 0.010 | 0.0 REU | Largely redundant |
| s306498 (L77) | 88.3% | 100.0% | 0.040 | 1.1 REU | Redundant (100% Iface overlap) |
| s837308 (L60) | 85.0% | 96.2% | 0.010 | 3.9 REU | Largely redundant |
| s867664 (L79) | 88.6% | 75.0% | 0.080 | 2.4 REU | **Some diversity** (lowest overlap) |
| s65308 (L81) | 92.6% | 86.7% | 0.010 | 3.9 REU | Near-redundant |

**Key finding:** Most scaffold pairs are largely redundant (>85% sequence identity, >90% interface overlap). For experimental testing, selecting one variant per scaffold is usually sufficient. The s120913 pair shows the most meaningful diversity with 80% interface overlap, suggesting different binding modes on the same backbone.

---

## 9. Salt Bridge Potential

Designs with significant charged residue presence at the interface (K+R+H >= 3 AND D+E >= 2) have potential for salt bridges. 31 of 62 designs meet this criterion.

**Top salt bridge potential:**

| Design | Positive (K/R/H) | Negative (D/E) | Comment |
|--------|-------------------|-----------------|---------|
| s120913_mpnn2 | 8.5 (K1, R4.5, H3) | 5.0 (D1, E4) | Highest charged interface |
| s120913_mpnn1 | 7.5 (K1.5, R3, H3) | 2.5 | |
| s453481_mpnn3 | 6.0 (K1, R3, H2) | 3.5 | |
| s946181_mpnn6 | 4.0 (K2, R1, H1) | 6.5 (D2, E4.5) | Highest neg. charge |
| s65308_mpnn1 | 6.0 (K0, R3, H3) | 2.5 | |

The s120913 scaffold is distinctive: its large interface is rich in charged residues (especially R and H), creating the highest salt bridge potential. Given that the target surface includes H13, H14, K16 (all positively charged on the target), the binder's negatively charged residues (D/E) likely form the salt bridges. The s946181 scaffold shows a complementary pattern with abundant D/E, consistent with electrostatic targeting of the K16-rich groove.

---

## 10. Risk Assessment

### 10.1 Designs with Warning Flags

| Design | Flag | Severity |
|--------|------|----------|
| s480128_mpnn13 | Relaxed clashes (0.5) | Low |
| s480128_mpnn17 | Relaxed clashes (0.5) | Low |
| s120913_mpnn2 | Relaxed clashes (0.5) | Low |
| s65308_mpnn6 | Relaxed clashes (0.5) | Low |
| s496499_mpnn3 | Relaxed clashes (0.5) | Low |
| s707813_mpnn1 | Relaxed clashes (0.5) | Low |
| s289797_mpnn2 | No Trp, A280=0 | Medium (quantitation) |
| s289797_mpnn5 | No Trp, A280=0 | Medium (quantitation) |
| s311742_mpnn3 | No Trp in sequence | Medium (quantitation) |
| s311742_mpnn16 | No Trp in sequence | Medium (quantitation) |
| s946181_mpnn6 | No Trp in sequence | Medium (quantitation) |
| s946181_mpnn9 | No Trp in sequence | Medium (quantitation) |
| s817651_mpnn15 | No Trp in sequence | Medium (quantitation) |
| s817651_mpnn19 | No Trp in sequence | Medium (quantitation) |
| s313438_mpnn2 | Seq recovery 0.21 | Medium (foldability) |
| s313438_mpnn5 | Seq recovery 0.21 | Medium (foldability) |
| s766115_mpnn9 | 4 unsat Hbonds, pLDDT=0.84 | Medium (interface quality) |
| s867664_mpnn2 | i_pTM=0.64, low composite | High (binding confidence) |
| s867664_mpnn5 | i_pTM=0.56, lowest composite | High (binding confidence) |

### 10.2 Tryptophan-Free Designs

8 designs from 4 scaffolds have zero tryptophan in their full sequence. This means A280 absorbance will be negligible (only Tyr contributes weakly). For experimental use:
- s311742: Best i_pTM, but needs Trp introduction (e.g., surface-exposed L-->W)
- s946181: Low Met at interface (M=1.0), excellent binding, but also Trp-free
- s817651: Compact (L=72), excellent hotspot RMSD, but Trp-free

If any of these advance to experimental testing, a Trp residue should be introduced at a surface-exposed position for concentration determination, or alternative methods (BCA assay, Bradford) should be planned.

---

## 11. Comparison to Original 7-Design Analysis

The original analysis (when only 7 designs were accepted) recommended 4 candidates:

| Original Pick | Rank in 62 | Composite Score | Status |
|---------------|-----------|-----------------|--------|
| s480128_mpnn13 | 48/62 | 0.440 | **Outclassed** -- mid-pack in full dataset |
| s120913_mpnn1 | 13/62 | 0.669 | **Still strong** -- remains in top quartile |
| s716952_mpnn20 | 43/62 | 0.457 | **Outclassed** -- lower half |
| s311665_mpnn6 | 52/62 | 0.372 | **Outclassed** -- bottom quartile |

**Only s120913_mpnn1 remains competitive.** The expansion from 7 to 62 designs revealed dramatically better scaffolds (s453481, s311742, s857331, s946181) that dominate on all metrics. The original picks were the best available at the time but are superseded.

**Notably, s480128_mpnn13** -- the original top pick for its zero Met interface and 63% sequence recovery -- remains interesting as a specificity reference (it has the cleanest interface composition), but its i_pTM (0.72) and dG (-73.7) are mediocre in the full context.

---

## 12. Updated Recommendations for Experimental Testing

### 12.1 Recommended Test Panel (6 Designs)

The panel is selected for **diversity** (different scaffolds, sizes, interface types, topologies) and **quality** (top-tier metrics), ensuring that if one binding mode fails experimentally, others provide independent chances.

#### Pick 1: ab42_l86_s453481_mpnn1 -- "Best Overall"

| Metric | Value | Rank |
|--------|-------|------|
| Composite score | 0.856 | 1st |
| i_pTM | 0.850 | 2nd |
| dG | -102.5 REU | 2nd deepest |
| pLDDT | 0.940 | Tied 1st |
| Interface Hbonds | 10.0 | 3rd most |
| SC | 0.730 | Above median |
| Surface hydro | 0.270 | Low |
| MPNN recovery | 0.42 | Above median |

**Why:** Dominates the composite ranking. Best balance of binding confidence, energy, and interface quality. Has beta-sheet content (3.5%) providing minor structural diversity. 86 residues is a manageable size for expression.

**Risk:** Interface Met=3.0 (at boundary). Binder RMSD=3.25 A in mpnn1 (the highest among top designs; mpnn3 at 2.42 A is better). Consider mpnn3 as a backup if mpnn1 doesn't express well.

#### Pick 2: ab42_l90_s311742_mpnn3 -- "Highest Confidence"

| Metric | Value | Rank |
|--------|-------|------|
| i_pTM | 0.860 | **1st in campaign** |
| pLDDT | 0.940 | Tied 1st |
| SC | 0.760 | Top 10% |
| Surface hydro | 0.220 | **Lowest in campaign** |
| dG/dSASA | -3.71 | Top 10% |
| Binder RMSD | 1.07 A | Excellent |

**Why:** Highest AF2 confidence of any design. Lowest surface hydrophobicity. Very high shape complementarity. Excellent binder RMSD (AF2 strongly agrees on binder fold). Different scaffold from Pick 1, providing independent evaluation.

**Risk:** No tryptophan in sequence (use BCA or introduce W mutation). Met=3.0. At 90 aa it is the longest design, which could complicate expression.

#### Pick 3: ab42_l86_s857331_mpnn4 -- "Best Interface Efficiency"

| Metric | Value | Rank |
|--------|-------|------|
| dG/dSASA | -3.83 | 2nd best |
| SC | 0.780 | 2nd best overall |
| Unsat Hbonds | 1.0 | Very low |
| Interface Met | 2.0 | Below boundary |
| Surface hydro | 0.250 | Low |
| Binder RMSD | 1.34 A | Good |

**Why:** Best binding efficiency (dG per unit area). Near-best shape complementarity. Only 1.0 unsatisfied H-bond. Interface Met=2.0 (below the filter boundary, meaning less oxidation risk). Different structural family from Picks 1--2. All-helical (89% helix), distinct interface geometry from the mixed alpha/beta scaffolds.

**Risk:** i_pTM=0.80 is good but not exceptional. Moderate H-bond count (7.5).

#### Pick 4: ab42_l82_s946181_mpnn6 -- "Lowest Met, Strong Binder"

| Metric | Value | Rank |
|--------|-------|------|
| i_pTM | 0.840 | Top 5 |
| dG | -92.5 REU | Top 5 |
| Interface Hbonds | 11.0 | Tied 1st |
| Interface Met | 1.0 | **2nd lowest** |
| Unsat Hbonds | 2.0 | Good |
| Beta content | 2.4% | Mixed topology |

**Why:** The best design with low interface methionine (M=1.0). 11 H-bonds is the joint-most in the campaign. Strong i_pTM and dG. Has mixed alpha/beta topology providing diversity. Interface is partially polar (hydro=47.9%) unlike the more hydrophobic interfaces of other top picks, representing a different binding strategy.

**Risk:** No tryptophan. SC=0.66 (below median). Surface hydro=0.32 (near boundary).

#### Pick 5: ab42_l60_s837308_mpnn6 -- "Smallest Binder"

| Metric | Value | Rank |
|--------|-------|------|
| Length | 60 aa | **Smallest accepted** |
| SC | 0.790 | **Best in campaign** |
| Unsat Hbonds | 0.0 | **Best in campaign** |
| Surface hydro | 0.270 | Low |
| pLDDT | 0.920 | High |
| Binder pLDDT | 0.950 | Very high |

**Why:** Size matters for a therapeutic binder -- at 60 aa this is the most compact design, favorable for tissue penetration and potential BBB crossing. Best shape complementarity of any design. Zero unsatisfied H-bonds (cleanest interface). All-helical, well-folded. If a minimal binder works, it is preferable for downstream engineering.

**Risk:** Only 3.5 H-bonds (near the 3.0 filter minimum). MPNN recovery=0.24 (low, meaning the sequence may not fold as designed). Interface Met=3.0. The small size means fewer contacts overall.

#### Pick 6: ab42_l79_s120913_mpnn1 -- "Largest Interface, Salt Bridges"

| Metric | Value | Rank |
|--------|-------|------|
| dG | -93.7 REU | Top 5 |
| Interface residues | 32 | Above median |
| Interface Hbonds | 7.5 | Good |
| Interface Met | 1.0 | Low |
| Beta content | 2.5% | Mixed alpha/beta |
| MPNN recovery | 0.41 | Above median |
| Salt bridge potential | Very high (7.5 positive, 2.5 negative) |

**Why:** Retained from the original 4 recommendations for good reason. Deep binding energy, mixed topology, largest interface of reasonable scaffolds, highest salt bridge potential. The s120913 scaffold is the only one combining low Met (M=1.0), strong dG (-93.7), and a large mixed alpha/beta interface. Provides an orthogonal binding strategy compared to the helix-dominated other picks.

**Risk:** Binder RMSD=2.61 A is moderate. Hotspot RMSD=1.02 A is good. PackStat=0.62 is below average (potential packing issues).

### 12.2 Alternates (If Primary Picks Fail)

| Priority | Design | Reason |
|----------|--------|--------|
| Alt-1 | s453481_mpnn3 | Backup for Pick 1 (87% identical, lower binder RMSD) |
| Alt-2 | s311742_mpnn16 | Backup for Pick 2 (nearly identical metrics) |
| Alt-3 | s817651_mpnn19 | Best hotspot RMSD (0.79 A), best PackStat (0.71), i_pTM=0.84 |
| Alt-4 | s306498_mpnn16 | Excellent pLDDT (0.94), SC (0.77), all-helical |
| Alt-5 | s766115_mpnn9 | Deepest dG (-107 REU) if aggressive binding is needed |

### 12.3 Designs to Avoid for First-Round Testing

| Design | Reason |
|--------|--------|
| s867664_mpnn2/mpnn5 | Lowest i_pTM (0.56--0.64), bottom of all rankings |
| s289797_mpnn2/mpnn5 | Low i_pTM (0.57--0.61), no Trp, high hotspot RMSD |
| s31762_mpnn5 | i_pTM=0.59, near-bottom composite score |
| s103118_mpnn17 | Hotspot RMSD=4.80 A (worst), only 14.5 interface residues |

---

## 13. Summary Statistics

| Category | Value |
|----------|-------|
| Total designs accepted | 62 |
| Unique scaffolds | 38 |
| Trajectories attempted | ~1,342 |
| MPNN designs evaluated | ~2,977 |
| Pass stringent filter (i_pTM>=0.8, dG<=-80, pLDDT>=0.9) | 11 |
| Pass moderate filter (i_pTM>=0.8, dG<=-70, pLDDT>=0.88) | 22 |
| Designs with zero interface Met | 2 |
| Designs with interface Met<=1 | 6 |
| Designs with beta-sheet content | 14 (23%) |
| Designs with zero Trp in sequence | 8 (13%) |
| Designs with relaxed clashes | 6 (10%) |
| Pareto-optimal designs (i_pTM vs dG) | 3 |
| Campaign best i_pTM | 0.860 (s311742) |
| Campaign best dG | -107.0 REU (s766115) |
| Campaign best SC | 0.790 (s837308) |

### Recommended Test Panel Summary

| # | Design | Length | i_pTM | dG | Unique value |
|---|--------|--------|-------|------|-------------|
| 1 | s453481_mpnn1 | 86 | 0.85 | -102.5 | Best overall composite |
| 2 | s311742_mpnn3 | 90 | 0.86 | -88.0 | Highest confidence |
| 3 | s857331_mpnn4 | 86 | 0.80 | -87.8 | Best efficiency + SC |
| 4 | s946181_mpnn6 | 82 | 0.84 | -92.5 | Lowest Met, most Hbonds |
| 5 | s837308_mpnn6 | 60 | 0.79 | -81.7 | Smallest binder, best SC |
| 6 | s120913_mpnn1 | 79 | 0.81 | -93.7 | Largest interface, salt bridges |

This panel covers 6 distinct scaffolds spanning 60--90 aa, includes both all-helical and mixed alpha/beta topologies, ranges from compact (60 aa) to large-interface (32 residues) designs, and includes the top performers on each individual metric. Three of the six picks have interface Met <= 2.0, reducing oxidation risk.
