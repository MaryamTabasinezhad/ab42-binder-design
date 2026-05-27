# BindCraft Aβ42 Binder Design Report

**Campaign:** ab42_CEG (9CO4 Conformation 1, chains C/E/G)
**Date:** 2026-05-07 (~31 hours elapsed)
**Target:** Lateral N-terminal surface of receptor-bound Aβ42 filament
**Hotspots:** Y10, E11, H13, H14, Q15, K16 × 3 chains (18 total)

---

## 1. Campaign Summary

| Metric | Value |
|--------|-------|
| Total trajectories | 297 (133 main + 164 parallel) |
| MPNN sequences tested | ~7,640 |
| Passed initial 2-model AF2 screen | 434 |
| Passed full 5-model evaluation | 73 (16.8%) |
| **Accepted (all filters)** | **6 (0.08% of MPNN seqs)** |
| Acceptance rate (per trajectory) | ~4.5% (main job only) |
| Active job | 8375335 on frnt190 (A100, 14-day) |

---

## 2. Pipeline Funnel

```
Trajectories generated:         297
  └─ Pre-MPNN trajectory failures:  105
     (logits_pLDDT=6, softmax_pLDDT=5, one-hot_pLDDT=45, final_pLDDT=49)

MPNN sequences tested:        ~7,640
  └─ Failed initial AF2 screen:
       i_pAE:                   2,126  (largest bottleneck)
       i_pTM:                   2,022
       pTM:                       963
       pLDDT:                     838
       Binder_pLDDT:               46
       Trajectory clashes:         26

  └─ Passed to 5-model eval:     434
       └─ Failed structural filters:
            Surface_Hydrophobicity:  312  (top structural bottleneck)
            InterfaceAAs_M (Met):    315
            n_InterfaceHbonds:       190
            n_InterfaceUnsatHbonds:  144
            Binder_RMSD:              89
            InterfaceAAs_K (Lys):     25
            ShapeComplementarity:      5

  └─ Passed all filters:           6  ACCEPTED
```

### Key Bottlenecks

1. **i_pAE filter** (initial screen): 2,126 failures — interface predicted aligned error too high. Most MPNN sequences fail to produce confident interface contacts.
2. **Surface Hydrophobicity** (structural filter): 66.1% of 5-model evaluated designs exceed the 0.35 threshold. This is the #1 reason structurally good designs get rejected.
3. **Interface H-bonds**: 38.0% of 5-model designs have <3 interface H-bonds.
4. **Methionine enrichment**: 315 designs rejected for >3 Met at the interface — BindCraft's gradient-based design over-produces Met.

---

## 3. Filter Thresholds & Pass Rates (5-Model Stage)

Applied to the 434 designs that passed the initial 2-model AF2 screen:

| Filter | Threshold | Pass Rate | Failures |
|--------|-----------|-----------|----------|
| pTM | >0.55 | 100% | 0 |
| pLDDT | >0.80 | 100% | 0 |
| i_pTM | >0.50 | 100% | 0 |
| i_pAE | <0.35 | 100% | 0 |
| n_InterfaceResidues | >7 | 100% | 0 |
| Hotspot_RMSD | <6.0 | 100% | 0 |
| Binder_Loop% | <90% | 100% | 0 |
| ShapeComplementarity | >0.60 | 98.8% | 5 |
| Binder_pLDDT | >0.80 | 93.1% | 30 |
| Binder_RMSD | <3.5 | 83.2% | 73 |
| n_InterfaceUnsatHbonds | <4 | 77.4% | 98 |
| n_InterfaceHbonds | >3 | 62.0% | 165 |
| **Surface_Hydrophobicity** | **<0.35** | **33.9%** | **287** |

**Designs passing ALL numeric filters: 73/434 (16.8%)**

Of these 73, only 6 survived additional checks (relaxed clashes, absorption, InterfaceAAs limits).

---

## 4. Metric Distributions (434 Designs at 5-Model Stage)

| Metric | Min | Median | Mean | Max |
|--------|-----|--------|------|-----|
| i_pTM | 0.55 | 0.77 | 0.75 | 0.85 |
| pTM | 0.72 | 0.81 | 0.81 | 0.88 |
| pLDDT | 0.81 | 0.89 | 0.88 | 0.94 |
| Surface Hydrophobicity | 0.24 | 0.39 | 0.39 | 0.63 |
| Shape Complementarity | 0.57 | 0.69 | 0.70 | 0.81 |
| Binder RMSD (Å) | 0.76 | 1.98 | 2.80 | 12.07 |
| dG (REU) | -144.6 | -74.6 | -81.3 | -47.3 |
| Interface H-bonds | 0.0 | 3.5 | 5.3 | 19.0 |
| Binder pLDDT | 0.68 | 0.90 | 0.89 | 0.96 |

---

## 5. Accepted Designs — Detailed Profiles

### Design 1: ab42_l79_s120913_mpnn1 — BEST OVERALL

| Property | Value |
|----------|-------|
| Length | 79 aa (8.7 kDa) |
| Sequence | MDTREQLWWFATAQLLVRHIIEHMRAVGDTSQLARWEADLEILEERARRKEFTIPEDTEIYRLMKTLKENTKGHKIVEE |
| Binder Rg | 13.4 Å |
| Helicity | 67.1% helix, 2.5% sheet, 30.4% loop |
| MPNN score | 1.05 |
| Avg pLDDT | 0.88 |
| Avg pTM | 0.84 |
| **Avg i_pTM** | **0.81** |
| Avg i_pAE | 0.19 |
| Avg dG | -93.7 REU |
| Avg dSASA | 2929 Å² |
| Avg dG/dSASA | -3.20 |
| Shape Complementarity | 0.68 |
| Surface Hydrophobicity | 0.26 |
| Interface Residues | 32.5 |
| Interface H-bonds | 7.5 |
| Unsat H-bonds | 1.5 |
| Binder RMSD | 2.61 Å |
| Hotspot RMSD | 1.02 Å |
| Relaxed Clashes | 0 |
| **Hotspot contacts** | **14/18** (C: 6/6, E: 5/6, G: 3/6) |
| Notes | Clean — no clashes, no warnings |

**Strengths:** Highest i_pTM (0.81), contacts all 6 hotspots on chain C plus 5/6 on chain E. Large buried surface area (2929 Å²). Low surface hydrophobicity (0.26). Zero relaxed clashes.

---

### Design 2: ab42_l79_s120913_mpnn2 — STRONGEST BINDING

| Property | Value |
|----------|-------|
| Length | 79 aa (8.7 kDa) |
| Sequence | MPTREKLWWFATAQLLVRHIIEHMRARGDTSQLAQWEADLEILEENARKKIFEIPEDTPIYRLMKTLKENTKGHEIVEE |
| Binder Rg | 13.4 Å |
| Helicity | 65.8% helix, 2.5% sheet, 31.7% loop |
| MPNN score | 1.08 |
| Avg pLDDT | 0.88 |
| Avg pTM | 0.84 |
| **Avg i_pTM** | **0.81** |
| Avg dG | **-98.9 REU** |
| Avg dSASA | **3146 Å²** |
| Shape Complementarity | 0.69 |
| Surface Hydrophobicity | 0.28 |
| Interface Residues | **39.5** |
| Interface H-bonds | **11.5** |
| Binder RMSD | 2.18 Å |
| Relaxed Clashes | 0.5 (1 in model 1, 0 in model 2) |
| **Hotspot contacts** | **14/18** (C: 6/6, E: 5/6, G: 3/6) |
| Notes | Relaxed structure contains clashes (minor, 1 clash in 1/2 models) |

**Strengths:** Largest buried surface area (3146 Å²), strongest binding energy (-98.9 REU), most interface H-bonds (11.5), most interface residues (39.5). Same scaffold as mpnn1 (seed s120913) with different MPNN sequence variant.

---

### Design 3: ab42_l82_s967366_mpnn11 — BEST CONFIDENCE

| Property | Value |
|----------|-------|
| Length | 82 aa (9.0 kDa) |
| Sequence | MPKEVEIWEFLQMFFMDYFYAEIYRGKLSEEEKEIVEKIDKTWQKVIDNMKKNNGVMSEEDQKEMQEVLLDIINLKKKLEEK |
| Binder Rg | 13.3 Å |
| Helicity | 82.9% helix, 0% sheet, 17.1% loop |
| MPNN score | 1.08 |
| **Avg pLDDT** | **0.94** |
| **Avg Binder pLDDT** | **0.95** |
| Avg pTM | 0.84 |
| Avg i_pTM | 0.79 |
| Avg dG | -71.8 REU |
| Shape Complementarity | **0.76** |
| Surface Hydrophobicity | 0.32 |
| Interface Residues | 21.5 |
| Interface H-bonds | 3.5 |
| Binder RMSD | 1.11 Å |
| Relaxed Clashes | 0 |
| Hotspot contacts | 10/18 (C: 2/6, E: 3/6, G: 5/6) |
| Notes | Clean — no clashes, no warnings |

**Strengths:** Highest overall confidence (pLDDT=0.94, binder pLDDT=0.95). Best shape complementarity (0.76). Lowest binder RMSD (1.11 Å) — very structurally consistent across AF2 models. Most helical (82.9%). Preferentially contacts chain G (5/6 hotspots).

---

### Design 4: ab42_l82_s480128_mpnn17

| Property | Value |
|----------|-------|
| Length | 82 aa (9.0 kDa) |
| Sequence | SFHQKYPKAWAWIQFLRFIVEQILGDTPEAQDIYDTVASEAKEKLEADKSGELGTTEEGANELFIEMLTRAFSLVADVLLNP |
| Binder Rg | 12.8 Å |
| Helicity | 85.4% helix, 0% sheet, 14.6% loop |
| Avg pLDDT | 0.92 |
| Avg pTM | 0.82 |
| Avg i_pTM | 0.76 |
| Avg dG | -71.0 REU |
| Shape Complementarity | 0.68 |
| Surface Hydrophobicity | 0.34 |
| Interface Residues | 25.5 |
| Interface H-bonds | 3.5 |
| Binder RMSD | 0.90 Å |
| Relaxed Clashes | 0.5 |
| Hotspot contacts | 11/18 (C: 3/6, E: 4/6, G: 4/6) |
| Notes | Relaxed structure contains clashes |

**Strengths:** Lowest binder RMSD overall (0.90 Å). High helicity (85.4%). Evenly distributed contacts across chains E and G.

---

### Design 5: ab42_l82_s480128_mpnn13

| Property | Value |
|----------|-------|
| Length | 82 aa (9.0 kDa) |
| Sequence | SFHQKYPKAWAWQQFLEFIVRQILGDTPEAKKIVEEVTSEAEKLLEADKSGELGTTEEGANKLFIEMLTRAFSKVADVLLNP |
| Binder Rg | 12.8 Å |
| Helicity | 85.4% helix, 0% sheet, 14.6% loop |
| Avg pLDDT | 0.89 |
| Avg pTM | 0.80 |
| Avg i_pTM | 0.72 |
| Avg dG | -73.7 REU |
| Shape Complementarity | 0.71 |
| Surface Hydrophobicity | 0.34 |
| Interface Residues | 24.0 |
| Interface H-bonds | 3.5 |
| Binder RMSD | 2.15 Å |
| Relaxed Clashes | 0.5 |
| Hotspot contacts | 11/18 (C: 3/6, E: 4/6, G: 4/6) |
| Notes | Relaxed structure contains clashes |

**Strengths:** Same scaffold as mpnn17 (seed s480128). Good shape complementarity (0.71). Identical hotspot contact pattern to mpnn17.

---

### Design 6: ab42_l68_s311665_mpnn6 — SMALLEST

| Property | Value |
|----------|-------|
| Length | 68 aa (7.5 kDa) |
| Sequence | MTREMLTDPWFMITDMIYHLFMKDNEEISKKYNEIIENADKMTPEEFREKLMELLVEAVRTWHKRNFE |
| Binder Rg | 11.9 Å |
| Helicity | 82.4% helix, 0% sheet, 17.7% loop |
| Avg pLDDT | 0.89 |
| Avg pTM | 0.80 |
| Avg i_pTM | 0.73 |
| Avg dG | -62.7 REU |
| Shape Complementarity | 0.67 |
| Surface Hydrophobicity | 0.30 |
| Interface Residues | 25.0 |
| Interface H-bonds | 3.5 |
| Binder RMSD | 1.22 Å |
| Relaxed Clashes | 0 |
| Hotspot contacts | 9/18 (C: 3/6, E: 3/6, G: 3/6) |
| Notes | Clean — no clashes, no warnings |

**Strengths:** Smallest binder (68 aa, 7.5 kDa) — advantageous for bispecific fusion. Lowest surface hydrophobicity (0.30). Symmetrically contacts Y10, Q15, K16 on all 3 chains. Zero relaxed clashes.

---

## 6. Comparative Ranking

| Design | i_pTM | dG (REU) | Hotspots | B_RMSD | Surf.Hydro | Clashes | Overall |
|--------|-------|----------|----------|--------|------------|---------|---------|
| s120913_mpnn1 | **0.81** | -93.7 | **14/18** | 2.61 | 0.26 | 0 | **#1** |
| s120913_mpnn2 | **0.81** | **-98.9** | **14/18** | 2.18 | 0.28 | 0.5 | **#2** |
| s967366_mpnn11 | 0.79 | -71.8 | 10/18 | **1.11** | 0.32 | 0 | **#3** |
| s480128_mpnn17 | 0.76 | -71.0 | 11/18 | **0.90** | 0.34 | 0.5 | #4 |
| s480128_mpnn13 | 0.72 | -73.7 | 11/18 | 2.15 | 0.34 | 0.5 | #5 |
| s311665_mpnn6 | 0.73 | -62.7 | 9/18 | 1.22 | **0.30** | 0 | #6 |

### Top picks for Stage 3 (negative-design counter-screen):
1. **s120913_mpnn1** — best i_pTM, broadest hotspot coverage, clean
2. **s120913_mpnn2** — strongest binding energy, most H-bonds, minor clashes
3. **s967366_mpnn11** — highest confidence, best structural consistency
4. **s311665_mpnn6** — smallest (bispecific advantage), cleanest surface

---

## 7. Design Patterns & Observations

### Scaffold diversity
Only **3 unique backbone scaffolds** from 6 accepted designs:
- **Seed 120913** (79 aa): 2 designs (mpnn1, mpnn2) — best performing scaffold
- **Seed 480128** (82 aa): 2 designs (mpnn13, mpnn17) — helical, some clashes
- **Seed 967366** (82 aa): 1 design (mpnn11) — highest confidence
- **Seed 311665** (68 aa): 1 design (mpnn6) — smallest, symmetric contacts

### Structural features
- All designs are **predominantly helical** (65-85% helix content)
- No beta-sheet content in any design (0-2.5%)
- Binder sizes range 68-82 aa (7.5-9.0 kDa) — all within the miniprotein range suitable for bispecific fusion
- All binders contact **Y10, Q15, K16** on at least some chains — these appear to be the anchor residues
- **H13/H14** are the hardest hotspots to reach — only contacted by the s120913 scaffold

### Hotspot coverage
- Q15 and K16: contacted by all 6 designs on all 3 chains (most accessible)
- Y10: contacted by all designs on at least 1 chain
- E11: contacted by 4/6 designs, usually on chains E/G
- H13, H14: contacted only by the s120913 designs (14/18 coverage)

### Surface hydrophobicity
The 0.35 threshold eliminates 66.1% of otherwise good designs. All 6 accepted designs have surface hydrophobicity ≤0.34, with the best at 0.26 (mpnn1). This is the single largest controllable bottleneck.

---

## 8. Recommendations

1. **Continue the main A100 job** — it's the only source producing accepted designs. At current pace (~6 designs per 133 main-job trajectories), reaching 20-30 total accepted designs would take ~3-5 more days.

2. **Consider relaxing Surface_Hydrophobicity to 0.40** — this would roughly triple the acceptance rate (from 33.9% to ~60% pass rate at the 5-model stage), yielding designs that are still experimentally viable. Hydrophobicity can be addressed with point mutations post-design.

3. **Parallel jobs produced 0 accepted designs** across 164 trajectories on non-A100 GPUs. This may reflect lower numerical precision or memory-limited design quality. Future parallelization should target A100 nodes specifically.

4. **Prioritize s120913 scaffold** for Stage 3 negative-design counter-screening — it has the best binding metrics and broadest hotspot coverage.

5. **s311665_mpnn6 (68 aa) is the best candidate for bispecific fusion** with the TfR1 arm — its small size minimizes steric clashes in the final construct.

---

## 9. File Locations

| File | Path |
|------|------|
| Accepted PDBs | `bindcraft/designs/Accepted/*.pdb` |
| Full metrics (accepted) | `bindcraft/designs/final_design_stats.csv` |
| 5-model evaluated designs | `bindcraft/designs/mpnn_design_stats.csv` (434 designs) |
| Trajectory stats | `bindcraft/designs/trajectory_stats.csv` |
| Cumulative filter failures | `bindcraft/designs/failure_csv.csv` |
| Target PDB | `bindcraft/input/9CO4_CEG.pdb` |
| Target settings | `bindcraft/settings/ab42_CEG.json` |
| Filter thresholds | `bindcraft/repo/settings_filters/default_filters.json` |
| This report | `bindcraft/designs/design_report.md` |
