# 9CO4 — Structural Analysis Summary

Generated: 2026-04-27 · `varagent` (Python 3.11, biopython 1.87, pandas 2.2.1)

## 1. 9CO4 metadata

| Field | Value |
| --- | --- |
| PDB ID | **9CO4** |
| Title | Cryo-EM structure of the receptor-bound amyloid-β 42 oligomer from human brain tissue (Conformation 1) |
| Method | Cryo-EM, helical reconstruction |
| Resolution | 2.80 Å |
| Helical parameters | ΔZ = 2.355 Å, ΔΦ = 178.164°, axial symmetry C1 |
| Authors | Butan, C.; Strittmatter, S. |
| Deposition | 2024-07-16 (released 2026-01-21) |
| Biological assembly | Decameric (10 chains, A–J) |
| Sequence | Aβ42, `DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVVIA` (residues 1–42) |
| Modeled range (every chain) | residues 9–42 (residues 1–8 disordered/unmodeled) |
| Chain residue counts | 34 residues / chain, no internal gaps |

## 2. Companion entries (same authors, Aβ42 oligomer series)

Sourced via the RCSB search API (`audit_author.name` containing both "Butan"
and "Strittmatter"). The 9CO0–9COZ sequential header probe found no
co-authored entries, so the search API was the productive route.

| PDB ID | Title | Resolution | Chains | Deposited |
| --- | --- | --- | --- | --- |
| **9CK6** | Sarkosyl-insoluble Aβ42 filaments extracted from human brain tissue | 3.0 Å | 10 (A–I, R) | 2024-07-08 |
| **9CKI** | PSCMA-extractable Aβ42 oligomer from human brain tissue (Conformation 2) | 3.1 Å | 10 (A–J) | 2024-07-09 |
| 9CO4 | PSCMA-extractable Aβ42 oligomer (Conformation 1) — *this study* | 2.8 Å | 10 (A–J) | 2024-07-16 |

All three structures are 10-chain Aβ42 assemblies modeled over residues 9–42
with no internal gaps. 9CO4 and 9CKI form a Conformation 1/Conformation 2
pair; 9CK6 is the corresponding sarkosyl-insoluble filament.

## 3. Per-chain modeled residue table (9CO4)

| Chain | First | Last | Count | Internal gaps |
| --- | --- | --- | --- | --- |
| A | 9 | 42 | 34 | none |
| B | 9 | 42 | 34 | none |
| C | 9 | 42 | 34 | none |
| D | 9 | 42 | 34 | none |
| E | 9 | 42 | 34 | none |
| F | 9 | 42 | 34 | none |
| G | 9 | 42 | 34 | none |
| H | 9 | 42 | 34 | none |
| I | 9 | 42 | 34 | none |
| J | 9 | 42 | 34 | none |

Chain A sequence verified character-by-character against the expected Aβ42
peptide; positions 9–42 match exactly, positions 1–8 are absent in the model
as predicted.

## 4. Target-residue SASA across 9CO4 chains

Computed with `Bio.PDB.SASA.ShrakeRupley(probe_radius=1.40, n_points=960)`
at residue level. `sasa_alone` is the same residue's SASA when chain A is
extracted and analyzed as a free monomer (max-possible SASA reference).
Burial ratio = `sasa_assembly / sasa_alone_chainA`. Classification thresholds:
**BURIED** < 20 Å², **PARTIAL** 20–40 Å², **EXPOSED** > 40 Å².

| Chain | Y10 | E11 | H13 | H14 | Q15 | K16 | F19 | F20 | E22 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 145.7 / 0.64 / EXP | 105.3 / 0.75 / EXP | 90.8 / 0.78 / EXP | 126.7 / 0.71 / EXP | 96.3 / 0.61 / EXP | 126.8 / 0.77 / EXP | 77.4 / 0.63 / EXP | 60.8 / 0.55 / EXP | 115.7 / 0.81 / EXP |
| B | 146.6 / 0.65 / EXP | 105.8 / 0.76 / EXP | 90.1 / 0.77 / EXP | 125.4 / 0.71 / EXP | 91.0 / 0.57 / EXP | 127.8 / 0.78 / EXP | 67.2 / 0.54 / EXP | 59.4 / 0.53 / EXP | 114.4 / 0.81 / EXP |
| C | 103.1 / 0.45 / EXP | 55.2 / 0.39 / EXP | 25.3 / 0.22 / PAR | 76.5 / 0.43 / EXP | 50.7 / 0.32 / EXP | 59.4 / 0.36 / EXP | 0.3 / 0.00 / **BUR** | 2.4 / 0.02 / **BUR** | 54.8 / 0.39 / EXP |
| D | 102.6 / 0.45 / EXP | 55.6 / 0.40 / EXP | 25.1 / 0.22 / PAR | 76.6 / 0.43 / EXP | 15.8 / 0.10 / **BUR** | 58.8 / 0.36 / EXP | 0.0 / 0.00 / **BUR** | 2.4 / 0.02 / **BUR** | 54.4 / 0.38 / EXP |
| E | 102.7 / 0.45 / EXP | 55.1 / 0.39 / EXP | 25.7 / 0.22 / PAR | 76.9 / 0.43 / EXP | 16.3 / 0.10 / **BUR** | 58.8 / 0.36 / EXP | 0.0 / 0.00 / **BUR** | 2.1 / 0.02 / **BUR** | 53.9 / 0.38 / EXP |
| F | 64.3 / 0.28 / EXP | 55.9 / 0.40 / EXP | 25.5 / 0.22 / PAR | 75.2 / 0.42 / EXP | 11.8 / 0.07 / **BUR** | 57.5 / 0.35 / EXP | 0.0 / 0.00 / **BUR** | 2.1 / 0.02 / **BUR** | 54.5 / 0.38 / EXP |
| G | 62.9 / 0.28 / EXP | 56.4 / 0.40 / EXP | 26.0 / 0.22 / PAR | 76.7 / 0.43 / EXP | 11.8 / 0.07 / **BUR** | 59.4 / 0.36 / EXP | 0.0 / 0.00 / **BUR** | 2.2 / 0.02 / **BUR** | 55.5 / 0.39 / EXP |
| H | 55.9 / 0.25 / EXP | 55.6 / 0.40 / EXP | 25.3 / 0.22 / PAR | 75.8 / 0.43 / EXP | 10.8 / 0.07 / **BUR** | 59.2 / 0.36 / EXP | 0.0 / 0.00 / **BUR** | 2.4 / 0.02 / **BUR** | 54.7 / 0.38 / EXP |
| I | 124.6 / 0.55 / EXP | 90.2 / 0.64 / EXP | 51.5 / 0.44 / EXP | 126.4 / 0.71 / EXP | 59.4 / 0.37 / EXP | 98.8 / 0.60 / EXP | 44.5 / 0.36 / EXP | 53.0 / 0.48 / EXP | 82.7 / 0.58 / EXP |
| J | 126.3 / 0.56 / EXP | 89.6 / 0.64 / EXP | 51.6 / 0.44 / EXP | 126.6 / 0.71 / EXP | 60.0 / 0.38 / EXP | 96.3 / 0.59 / EXP | 44.1 / 0.36 / EXP | 52.8 / 0.47 / EXP | 81.2 / 0.57 / EXP |

Cell format: `SASA_assembly (Å²) / burial_ratio / classification`.
Full per-residue table for all 304 residues × 10 chains: `analysis/9CO4_sasa.csv`.

The four "edge" chains (A, B, I, J) have markedly higher SASA at every target
position than the six interior chains (C–H), consistent with the helical/oligomer
geometry of the model — A/B and I/J sit at the two axial termini of the protofilament
slab and have no neighbour above/below.

## 5. Target-residue mean SASA across conformations

Mean SASA (Å²) per target residue, averaged over all 10 chains in each entry:

| Residue | 9CK6 (filament, 3.0 Å) | 9CKI (Conf. 2, 3.1 Å) | 9CO4 (Conf. 1, 2.8 Å) |
| --- | --- | --- | --- |
| Y10 | 92.8 | 96.4 | 103.5 |
| E11 | 78.7 | 81.0 | 72.5 |
| H13 | 35.5 | 34.9 | 43.7 |
| H14 | 97.6 | 96.4 | 96.3 |
| Q15 | 43.9 | 43.4 | 42.4 |
| K16 | 99.9 | 100.5 | 80.3 |
| F19 | 23.1 | 23.6 | 23.3 |
| F20 | 23.5 | 24.3 | 24.0 |
| E22 | 76.3 | 72.0 | 72.2 |

Fraction of chains per conformation classified **EXPOSED** (SASA > 40 Å²):

| Residue | 9CK6 | 9CKI | 9CO4 |
| --- | --- | --- | --- |
| Y10 | 1.0 | 1.0 | 1.0 |
| E11 | 1.0 | 1.0 | 1.0 |
| H13 | 0.4 | 0.4 | 0.4 |
| H14 | 1.0 | 1.0 | 1.0 |
| Q15 | 0.4 | 0.4 | 0.5 |
| K16 | 1.0 | 1.0 | 1.0 |
| F19 | 0.4 | 0.4 | 0.4 |
| F20 | 0.4 | 0.4 | 0.4 |
| E22 | 1.0 | 1.0 | 1.0 |

Per-conformation full target tables: `analysis/9CO4_targets.csv`,
`analysis/9CK6_targets.csv`, `analysis/9CKI_targets.csv`. Combined long-form
table: `analysis/all_targets.csv`.

## 6. Symmetry and patch analysis (9CO4)

### 6.1 Pairwise inter-chain interfaces

Pairwise BSA = sum of (SASA_alone − SASA_in_pair) over both chains, in Å².
Top eight interfaces (full list in `analysis/9CO4_pairwise_interfaces.csv`):

| Pair | BSA (Å²) |
| --- | --- |
| D–F | 2670.4 |
| A–C | 2667.9 |
| E–G | 2666.4 |
| H–J | 2664.1 |
| F–H | 2663.3 |
| C–E | 2659.3 |
| B–D | 2654.6 |
| G–I | 2650.5 |

These eight pairs each bury ≥2.6 × 10³ Å² and clearly separate from the
ninth-largest pair (E–H, 248.8 Å² — an order of magnitude smaller). They
form two disjoint chains of strong contacts:

- **A–C–E–G–I** (four edges, all ≥ 2.65 × 10³ Å²)
- **B–D–F–H–J** (four edges, all ≥ 2.65 × 10³ Å²)

Inter-protofilament contacts (e.g. A–D, B–E, F–I) are all in the 240–250 Å²
range — non-zero but two orders of magnitude smaller than intra-protofilament.

### 6.2 Face partition

The interface-based connected-component partition recovers exactly the
hypothesized parity grouping:

- **Face A (protofilament 1):** A, C, E, G, I
- **Face B (protofilament 2):** B, D, F, H, J

The strict angular partition around the principal axis of all 10 Cα centroids
does **not** reproduce the parity grouping (it returns
{A,B,C,D,F} vs {E,G,H,I,J}). The reason is geometric: each protofilament
contains chains on both angular sides of the helical axis (e.g. chain A at
azimuth ≈ 0° and chains E,G,I at azimuth ≈ −178°). Within a protofilament
the per-step rise along the principal axis is ~0.9 Å; between protofilaments
the centroid-to-centroid offset is ~16 Å. So protofilament membership
(strong direct contacts) is the structurally meaningful "face" and matches
the user's expected parity, even though the chain-centroid azimuths do not
all cluster.

### 6.3 Candidate patch residues per face (target residues with SASA_assembly > 40 Å²)

**Face A — {A, C, E, G, I}, 34 patch entries:**

- All 9 target residues exposed on chain A
- Chain C: Y10, E11, H14, Q15, K16, E22 (6)
- Chain E: Y10, E11, H14, K16, E22 (5)
- Chain G: Y10, E11, H14, K16, E22 (5)
- Chain I: all 9 target residues (terminal chain)

**Face B — {B, D, F, H, J}, 33 patch entries:**

- All 9 target residues exposed on chain B (terminal)
- Chain D: Y10, E11, H14, K16, E22 (5)
- Chain F: Y10, E11, H14, K16, E22 (5)
- Chain H: Y10, E11, H14, K16, E22 (5)
- Chain J: all 9 target residues (terminal)

The two faces are sequence-symmetric: the same set of "always exposed"
residues (Y10, E11, H14, K16, E22) tile every chain on each protofilament.
Full per-chain patch listing: `analysis/9CO4_faces.json`.

## 7. Observations

- **Y10, E11, H14, K16, E22 are reliably exposed on every chain in every
  conformation** (100% of chains classified EXPOSED in 9CO4, 9CKI, and 9CK6).
  These five residues paint a continuous solvent-accessible stripe along
  each protofilament and are the strongest candidates for surface-targeting
  ligands or antibody epitopes that would generalise across the brain-derived
  Aβ42 conformer family.

- **F19 and F20 are buried at the protofilament core in interior chains**
  (≤ 2.4 Å² SASA in chains C–H of 9CO4) and exposed only on the four chain-end
  copies. This is consistent across all three conformations (40% exposed
  fraction = 4/10 chains in each), so the F19/F20 hydrophobic stack is a
  conformation-independent feature of the brain-derived oligomer architecture.

- **H13 is genuinely conformation-dependent:** in 9CO4 it averages 43.7 Å²
  vs 35.5/34.9 Å² in the filament/Conformation-2 entries — a ~25% increase.
  H13 sits at a partially solvent-exposed position whose accessibility shifts
  measurably between conformations and may distinguish receptor-bound
  Conformation 1 from the alternative conformer states.

- **Q15 toggles between BURIED and EXPOSED depending on chain position
  rather than conformation:** in 9CO4 chains A, B, I, J it is fully exposed
  (>50 Å²) while in chains D–H it is BURIED (<17 Å²). The same end-vs-interior
  pattern recurs in 9CK6 and 9CKI. So Q15 accessibility is dictated by
  axial position in the protofilament, not by global conformation.

- **K16 is the most conformation-sensitive of the always-exposed residues:**
  9CO4 K16 averages 80.3 Å² vs 99.9/100.5 Å² in 9CK6/9CKI — a ~20% drop.
  This likely reflects extra packing in the receptor-bound state (the K16
  side chain is implicated in heparin/PrPC binding for Aβ oligomers) and is
  a useful structural fingerprint for Conformation 1.

## 8. Files produced

```
~/structural_analysis_project/
├── structures/
│   ├── 9CO4.pdb          (16-JUL-24 deposit, 2848 lines)
│   ├── 9CK6.pdb          (companion: sarkosyl filament)
│   └── 9CKI.pdb          (companion: Conformation 2)
├── analysis/
│   ├── step1_parse.py
│   ├── step2_companions.py
│   ├── step2b_companion_chains.py
│   ├── step3_sasa.py
│   ├── step4_symmetry.py
│   ├── step5_compare.py
│   ├── companions.json
│   ├── 9CO4_sasa.csv                    (full per-residue SASA, 9CO4)
│   ├── 9CK6_sasa.csv                    (full per-residue SASA, 9CK6)
│   ├── 9CKI_sasa.csv                    (full per-residue SASA, 9CKI)
│   ├── 9CO4_targets.csv                 (target-residue table, 9CO4)
│   ├── 9CK6_targets.csv                 (target-residue table, 9CK6)
│   ├── 9CKI_targets.csv                 (target-residue table, 9CKI)
│   ├── all_targets.csv                  (combined long-form)
│   ├── cross_conformation_mean.csv      (mean SASA per residue × PDB)
│   ├── cross_conformation_exposed_frac.csv
│   ├── 9CO4_pairwise_interfaces.csv     (45 pair BSAs)
│   ├── 9CO4_sasa_assembly.json          (assembly SASA dict)
│   ├── 9CO4_sasa_alone_chainA.json      (chain-A-alone SASA dict)
│   └── 9CO4_faces.json                  (face partition + patch lists)
└── docs/
    └── 9CO4_structural_summary.md       (this file)
```
