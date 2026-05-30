# Stage 8 — Tandem Fusion Design Plan

**Created:** 2026-05-29
**Status:** READY TO EXECUTE
**Prerequisite:** Stage 5 (Aβ42 ranking) + Stage 7.5 (TfR1 ranking) both COMPLETE

---

## 1. Objective

Design tandem miniprotein fusions combining the top Aβ42 binders with the top TfR1 binders. Each fusion is a single-chain protein: `[Arm1]–[linker]–[Arm2]`, expressed in E. coli. Target size: ~130–180 residues.

The goal is to find fusions where both arms retain their independent folds and binding capacity, with no inter-domain packing artifacts.

---

## 2. Input pools

### Aβ42 arm (Stage 5, top 5)

| Rank | Design | Length | i_pTM | dG | Composite |
|------|--------|--------|-------|-----|-----------|
| 1 | ab42_l82_s967366_mpnn11 | 82 | 0.790 | -71.8 | 0.793 |
| 2 | ab42_l89_s578974_mpnn11 | 89 | 0.800 | -70.8 | 0.733 |
| 3 | ab42_l90_s311742_mpnn16 | 90 | 0.860 | -88.8 | 0.713 |
| 4 | ab42_l71_s843399_mpnn18 | 71 | 0.800 | -76.6 | 0.708 |
| 5 | ab42_l90_s311742_mpnn3 | 90 | 0.860 | -88.0 | 0.696 |

Note: Ranks 3 and 5 share scaffold s311742. To maximize diversity, substitute rank 6 (ab42_l82_s480128_mpnn17, composite=0.691) for rank 5.

**Final Aβ42 panel (5 designs, 5 scaffolds):**
1. ab42_l82_s967366_mpnn11
2. ab42_l89_s578974_mpnn11
3. ab42_l90_s311742_mpnn16
4. ab42_l71_s843399_mpnn18
5. ab42_l82_s480128_mpnn17

### TfR1 arm (Stage 7.5, top 5 with diversity cap)

| Rank | Design | Length | i_pTM | dG | Score |
|------|--------|--------|-------|-----|-------|
| 1 | tfr1_l60_s766452_mpnn12 | 60 | 0.85 | -58.8 | 0.678 |
| 2 | tfr1_l70_s422992_mpnn5 | 70 | 0.83 | -48.5 | 0.677 |
| 3 | tfr1_l53_s938332_mpnn1 | 53 | 0.81 | -59.6 | 0.673 |
| 4 | tfr1_l51_s255454_mpnn5 | 51 | 0.84 | -47.7 | 0.645 |
| 5 | tfr1_l51_s694877_mpnn7 | 51 | 0.85 | -62.0 | 0.643 |

All 5 from different scaffolds.

---

## 3. Linker variants (10 per pair)

| Variant | Domain order | Linker | Linker length | Rationale |
|---------|-------------|--------|---------------|-----------|
| 1 | Aβ–TfR1 | (GGGGS)×3 | 15 aa | Flexible, standard |
| 2 | Aβ–TfR1 | (GGGGS)×4 | 20 aa | Flexible, more spacing |
| 3 | Aβ–TfR1 | (GGGGS)×5 | 25 aa | Flexible, maximal spacing |
| 4 | Aβ–TfR1 | A(EAAAK)×3A | 17 aa | Rigid α-helical |
| 5 | Aβ–TfR1 | PAPAP | 5 aa | Short rigid Pro-rich |
| 6 | TfR1–Aβ | (GGGGS)×3 | 15 aa | Reverse order, flexible |
| 7 | TfR1–Aβ | (GGGGS)×4 | 20 aa | Reverse order, flexible |
| 8 | TfR1–Aβ | (GGGGS)×5 | 25 aa | Reverse order, flexible |
| 9 | TfR1–Aβ | A(EAAAK)×3A | 17 aa | Reverse order, rigid |
| 10 | TfR1–Aβ | PAPAP | 5 aa | Reverse order, short rigid |

---

## 4. Scale

- **Pairs:** 5 Aβ42 × 5 TfR1 = 25 pairs
- **Variants per pair:** 10 (5 linkers × 2 domain orders)
- **Total fusion candidates:** 250
- **Estimated fusion sizes:** 117–205 residues (depending on arm lengths + linker)
- **ColabFold time per prediction:** ~3–8 min on A100 (monomer, single_sequence)
- **Total GPU time:** ~15–35 GPU-hours
- **Wallclock (with 2 clusters):** ~1–2 days

---

## 5. Execution plan

### 5.1. Generate fusion sequences (CPU, Frontenac)

Script: `alzheimer/bindcraft/fusion/scripts/generate_fusions.py`

For each (Aβ42_design, TfR1_design, linker_variant):
1. Extract binder sequence from each arm's design
2. Concatenate: `arm1_seq + linker_seq + arm2_seq`
3. Write to ColabFold input CSV: `id,sequence`
4. Naming convention: `fusion_{ab42_short}_{tfr1_short}_v{1-10}`
   - e.g., `fusion_s967366m11_s766452m12_v1`

Output: `alzheimer/bindcraft/fusion/inputs/fusion_input.csv` (250 rows)

### 5.2. Run ColabFold monomer predictions (GPU, Frontenac + Narval)

Split the 250 predictions across two clusters:
- **Frontenac:** variants 1–125 (job A)
- **Narval:** variants 126–250 (job B)

ColabFold settings:
- Mode: `monomer` (alphafold2_ptm)
- `--msa-mode single_sequence` (de novo, no MSA)
- `--num-models 1` (rank_1 sufficient for screening)
- `--num-recycle 3`

Use the containerized ColabFold (`container/run_colabfold.sh`).

SLURM: 1 A100 per job, ~4 hours walltime, 48G memory.

### 5.3. Extract and filter results (CPU, Frontenac)

Script: `alzheimer/bindcraft/fusion/scripts/analyze_fusions.py`

For each fusion prediction, extract:

| Metric | Method | Pass criterion |
|--------|--------|----------------|
| **Arm1 pLDDT** | Mean pLDDT over arm1 residue range | > 80 |
| **Arm2 pLDDT** | Mean pLDDT over arm2 residue range | > 80 |
| **Linker pLDDT** | Mean pLDDT over linker residues | Informational (flexible linkers expected low) |
| **Overall pTM** | From ColabFold scores JSON | > 0.6 |
| **Inter-domain contact** | PAE between arm1 and arm2 residue ranges | Mean inter-domain PAE > 15 (= no contact) |
| **Total length** | Sequence length | 117–205 aa |

**Pass criteria (all must be met):**
1. Both arms retain fold: per-arm pLDDT > 80
2. No inter-domain packing: mean PAE between arm1 and arm2 > 15 (high PAE = domains are independent)
3. Overall pTM > 0.6

**Ranking (for survivors):**
- Primary: mean(arm1_pLDDT, arm2_pLDDT) — higher is better
- Secondary: inter-domain PAE — higher is better (more independent)
- Tertiary: shorter linker preferred (less proteolysis risk)

### 5.4. Select top 10–20 for synthesis

- Apply max 2 fusions per (Aβ42, TfR1) pair to enforce diversity
- Prefer Aβ–TfR1 order over TfR1–Aβ if scores are similar (conventional N→C for brain shuttle)
- Include at least one rigid linker variant if it passes

Output: `alzheimer/bindcraft/fusion/stage8_panel.csv`

---

## 6. Directory structure

```
alzheimer/bindcraft/fusion/
├── scripts/
│   ├── generate_fusions.py      — build 250 fusion sequences
│   ├── run_fusion_colabfold.sh  — SLURM submission script
│   └── analyze_fusions.py       — extract metrics, filter, rank
├── inputs/
│   ├── fusion_input.csv         — 250 fusion sequences for ColabFold
│   ├── fusion_input_A.csv       — Frontenac split (1–125)
│   └── fusion_input_B.csv       — Narval split (126–250)
├── outputs/                     — ColabFold prediction outputs
├── stage8_results.csv           — all 250 with extracted metrics
└── stage8_panel.csv             — final 10–20 for synthesis
```

---

## 7. Cluster assignments

| Task | Cluster | Estimated time |
|------|---------|---------------|
| Generate fusion sequences | Frontenac | 5 min (CPU) |
| ColabFold batch A (125 fusions) | Frontenac | ~2–4 hrs (A100) |
| ColabFold batch B (125 fusions) | Narval | ~2–4 hrs (A100) |
| Extract + filter + rank | Frontenac | 10 min (CPU) |

---

## 8. Risk mitigation

1. **All arms fail to fold in fusion context:** unlikely — both arms have monomer pLDDT > 85 standalone. If it happens, try longer flexible linkers (GGGGS)×6-8 to give more spatial separation.

2. **Inter-domain packing (arms stick together):** the main failure mode. Filter by inter-domain PAE. If too many fail, consider redesigning the back-face of one arm with ProteinMPNN (fix interface, redesign non-interface to polar).

3. **Linker is too short for both arms to reach their targets simultaneously:** the Aβ42 filament (~50 Å wide) and TfR1 (on cell surface, ~100 Å from membrane) will be far apart in vivo. Even (GGGGS)×3 spans ~50 Å fully extended. This is not a concern for the AF2 screen — the fusion just needs to fold correctly as a monomer.

4. **SAP threshold for fusions:** the dev plan mentions SAP < 0.10 on non-paratope surface, but this threshold was already recalibrated for standalone arms. For fusions, rely on per-arm pLDDT as the primary fold-quality metric. SAP can be computed post-hoc on the top 20 if needed.
