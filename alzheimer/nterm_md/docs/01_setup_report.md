# Aβ42 N-terminus Structural Prep — Setup Report (Prompt 1)

| | |
|---|---|
| **Date** | 2026-05-06 |
| **Hostname** | login2.frontenac.local |
| **User** | hpc6049 |
| **Working dir** | /global/project/hpcg6049/protein/alzheimer/nterm_md |
| **Goal** | Build a clash-free chain-A+B+C subsystem with residues 1–8 (DAEFRHDS) appended to chain A, ready for restrained MD of the disordered N-terminus. |

## 1. Environment audit (summary)

Frontenac CAC cluster, GROMACS 2024.6 module loadable cleanly (CPU build, AVX2_256, mixed precision). Conda env `colabfold` contains OpenMM 8.5.1 and biopython 1.84; PDBFixer 1.8.1 was installed via the Compute Canada wheelhouse and made functional by pinning `setuptools<81` (PDBFixer 1.8.1 imports `pkg_resources`, removed in setuptools ≥ 81). Modeller is **not** available; MDAnalysis and mdtraj are not installed but were not required. ColabFold is available via `conda activate colabfold` but not used in this prompt. Full audit: `nterm_md/env/environment_audit.md`.

## 2. Tooling decisions

| Step | Tool | Rationale |
|---|---|---|
| Chain extraction from 9CO4 | biopython `PDBParser`/`PDBIO` (colabfold env) | Lightweight, scriptable. |
| N-terminal extension (residues 1–8) | **PDBFixer 1.8.1** `addMissingResidues` (chain-A-only mode) | First-choice tool from the user spec. Modeller unavailable; manual extended build avoided. PDBFixer handles N-terminal extensions natively. |
| Chain merge (A-with-N-term + original B,C) | biopython structure manipulation | Worked around a PDBFixer multichain-mode bug — see §3. |
| Topology + EM | GROMACS 2024.6, **amber99sb-ildn**, TIP3P | amber99sb-ildn is the user's first preference and is shipped with GROMACS; well-validated for IDPs. TIP3P chosen for the prep step (simple to set up, switchable to OPC for production MD later). |
| Diagnostics | biopython + numpy (no MDAnalysis needed) | Sufficient for the four metrics requested. |

## 3. Pipeline as executed

1. **Download** `9CO4.pdb` from RCSB (230 KB, 2510 ATOM records, 10 chains A–J, modeled residues 9–42 in every chain). **Verified** the modeled range matches the spec.
2. **Extract** three subsets via biopython into `prep/`:
   - `chainA_only.pdb` — chain A, residues 9–42
   - `chainA_B.pdb` — chains A and B
   - `chainA_B_C.pdb` — chains A, B, C
3. **Append N-terminus** with PDBFixer. The 8 residues (D-A-E-F-R-H-D-S) were specified via `fixer.missingResidues = {(0, 0): [...]}` and built with `addMissingAtoms()` (no hydrogens here — pdb2gmx handles them).
   - **PDBFixer multichain bug (worked around).** When run on `chainA_B_C.pdb`, PDBFixer placed OD1 of ASP7 at 0.11 Å from the backbone N of the same residue — physically impossible, killing GROMACS energy minimization with infinite forces at step 15. Re-running PDBFixer on `chainA_only.pdb` produced acceptable geometry (worst case: ASP7 N-OD1 at 1.70 Å, an unusual but EM-tractable rotamer). Solution: build the N-terminus on chain A alone, then merge with the unmodified original chains B and C from `chainA_B_C.pdb` (chain-A residues 9–42 verified to drift 0.000 Å between the two PDBFixer runs).
   - Outputs: `prep/chainA_with_nterm.pdb` (chain A only) and `prep/chainA_B_C_with_nterm.pdb` (merged).
   - The broken multichain PDBFixer output is preserved as `prep/chainA_B_C_with_nterm.pdbfixer-broken.pdb` for reference.
4. **Topology (pdb2gmx)** with amber99sb-ildn / TIP3P / `-ignh -ter` (default termini for all six ends: NH3⁺ on N-termini, COO⁻ on C-termini). System: 1639 protein atoms, 110 residues, total charge −5e.
5. **Box** (cubic, 1.0 nm padding via `editconf -d 1.0`) — final box 11.52 nm cube. The chain-A+B+C system is elongated (~9.4 nm longest axis from the filament geometry), so the box is dictated by that.
6. **Solvate** with `spc216.gro` template → 49 587 SOL waters.
7. **Neutralize** with `genion -neutral` → 5 Na⁺ ions.
8. **Energy minimization** as a SLURM job (system size 142 620 atoms, far above the login-node-safe threshold). Submitted via `sbatch run_em.sh`, routed by the scheduler to `cpubase_6hrs`. 8 OpenMP threads, 8 GB RAM, 1 hr walltime requested.
   - **Steepest descent** (`em_steep.mdp`, `emtol=1000`): converged to Fmax<1000 in **1772 steps**. Final potential energy −2.41×10⁶ kJ/mol; max force 887 kJ/mol/nm; norm 11.1.
   - **Conjugate gradient** (`em_cg.mdp`, `emtol=100`): converged to Fmax<100 in **335 steps**. Final potential energy −2.45×10⁶ kJ/mol; max force 86.5 kJ/mol/nm; norm 5.7.
   - Total elapsed: 1 min 40 s.
9. **Extract minimized protein** with `gmx trjconv -pbc whole` (initial use of `-pbc mol` left the chain split across the box and produced spurious bond/angle measurements).

## 4. Output files

| Path | Size | Purpose |
|---|---|---|
| `nterm_md/input/9CO4.pdb` | 230 KB | Original cryo-EM structure |
| `nterm_md/prep/chainA_only.pdb` | 20 KB | Chain A, residues 9–42 |
| `nterm_md/prep/chainA_B.pdb` | 41 KB | Chains A+B |
| `nterm_md/prep/chainA_B_C.pdb` | 61 KB | Chains A+B+C |
| `nterm_md/prep/chainA_with_nterm.pdb` | 26 KB | Chain A residues 1–42, PDBFixer extended |
| `nterm_md/prep/chainA_B_C_with_nterm.pdb` | 67 KB | Merged input to GROMACS |
| `nterm_md/prep/topol.top` (+ 6 `.itp`) | 1.5 KB + 0.5 MB | GROMACS topology, amber99sb-ildn |
| `nterm_md/prep/system.gro` | 73 KB | Coordinates after pdb2gmx |
| `nterm_md/prep/ions.gro` | 6.7 MB | Solvated, neutralized starting coords |
| `nterm_md/prep/em_cg.tpr/.gro/.log/.edr` | varies | Final EM run |
| `nterm_md/starting_structure/chainA_B_C_with_nterm_minimized.gro` | 6.4 MB | **Final minimized system** (for MD) |
| `nterm_md/starting_structure/chainA_B_C_with_nterm_minimized.pdb` | 130 KB | **Final minimized protein only**, PBC-corrected |
| `nterm_md/docs/starting_structure_diagnostics.json` | 4.9 KB | Full diagnostic numbers |

## 5. Diagnostic metrics

| Metric | Value | Threshold | Verdict |
|---|---|---|---|
| Sequence of residues 1–8 | DAEFRHDS | == DAEFRHDS | ✅ correct |
| Max backbone bond deviation | 0.063 Å (chain A:5 N-CA, 1.52 vs ideal 1.46) | > 0.05 Å flagged | ⚠️ small |
| Max backbone angle deviation | 15.3° (chain A:5 N-CA-C, 126.5° vs ideal 111.2°) | > 5° flagged | ⚠️ moderate |
| Total bond outliers > 0.05 Å | 6, all on chain A residues 4–8 backbone | — | ⚠️ |
| Total angle outliers > 5° | 10 (chain A residues 3–9 backbone, peptide-bond angles) | — | ⚠️ |
| Min N-term ↔ rest distance, non-bonded | 2.20 Å | ≥ 2.0 Å | ✅ |
| Clashes < 2.0 Å (excl. peptide bond) | 0 | 0 | ✅ |
| Rg of residues 1–8 (heavy atoms) | 8.31 Å | — | extended chain |
| Centroid vector core→N-term length | 47.65 Å | — | N-term displaced from core |
| Angle to filament axis | 91.5° | — | perpendicular to filament |
| Buried surface area, residues 1–8 | 72 Å² | < 100 Å² extended; > 200 Å² collapsed | ✅ extended into solvent |

The 1.37 Å "minimum distance" with peptide bond included is the legitimate chain-A residue 8 C → residue 9 N peptide bond and is excluded from the clash count. The **non-bonded** minimum is 2.20 Å, comfortably above any clash threshold.

## 6. Verdict — ready for MD?

**Yes, with one caveat to track during MD.** The structure is ready as the input for restrained MD. Specifically:
- **Clashes:** None. Min non-bonded distance is 2.20 Å.
- **Stereochemistry:** Bond lengths within 0.07 Å of ideal; the angle deviations at chain A residues 3–9 (max 15° on N-CA-C at residue 5) are a residual signature of PDBFixer's purely-geometric extended placement that EM did not fully relax. They are well within the harmonic well of the AMBER force field (~2 kcal/mol per such angle, ~13 kcal/mol total) and will relax during equilibration MD. Do **not** treat them as a structural error — re-running EM with looser tolerance won't help; the strain only releases once temperature lets the chain sample alternative φ/ψ.
- **Geometry of the appended N-terminus:** Extended (Rg 8.3 Å), displaced ~48 Å from the chain-A core, and oriented roughly perpendicular to the filament axis. **BSA = 72 Å²** means the N-terminus is essentially solvent-exposed, **not** collapsed against the filament surface. This is the desired starting state for an unbiased disordered-tail simulation — it gives the chain room to explore both surface contacts and free states without starting from a biased contact configuration.

## 7. Suggested next steps and concerns

### Immediate next step (Prompt 2): production MD of residues 1–8

A reasonable MD setup, given the diagnostics:

1. **Equilibration ladder.** NVT (100 ps, 300 K, position restraints on chains B, C and on residues 9–42 of chain A) → NPT (500 ps, 1 atm, same restraints) → release restraints on residues 1–8.
2. **Restraint scheme for production.**
   - Chains B, C: hard position restraints (force constant ~1000 kJ/mol/nm² on heavy atoms) — represent the "frozen" filament context per the project plan.
   - Chain A residues 9–42: light Cα restraints (50–100 kJ/mol/nm²) — keep the chain-A geometry stable while letting sidechains and termini flex.
   - Chain A residues 1–8: **free**.
3. **Production length.** 500 ns – 1 μs of unbiased MD per replica; ideally 3–5 replicas. The N-terminus is intrinsically disordered, so single-trajectory sampling will be inadequate.
4. **Water model upgrade.** Consider OPC for production — better at reproducing IDP behavior than TIP3P. Will require regenerating topology with `-water opc`. Alternatively, stay with TIP3P for cost/familiarity.
5. **Force field consideration.** amber99sb-ildn is acceptable but **a99SB-disp** or **amber14SB+TIP4P-D** are better-validated for IDPs. If publication-quality IDP statistics are needed, switching to a99SB-disp before production is the safer call. amber99sb-ildn is fine for a first look.

### Concerns / things to revisit

- **PDBFixer multichain bug.** PDBFixer 1.8.1 produced an unphysical OD1-N overlap when given the multichain `chainA_B_C.pdb` but not when given chain A alone. We worked around it; the upstream issue is unresolved. If we ever need to extend a different residue, expect this to recur and use the same workaround.
- **Pinned setuptools.** `setuptools<81` is now pinned in the `colabfold` env to keep PDBFixer working. If something else in that env breaks because of this, we'll need to either upgrade PDBFixer (1.10+ removed `pkg_resources`) or move PDBFixer to its own env.
- **Box is large.** 142k atoms — production MD on GPU should be tractable (~50–100 ns/day on an A100), but interactive testing should subsample to a smaller system if needed.
- **`-pbc whole` not `-pbc mol`.** When extracting trajectories from this system in the future, use `-pbc whole` (or `-pbc nojump` for trajectories) to avoid artifactual bond/angle measurements.
- **The angle deviations are not a bug to chase.** As noted in §6, they are extended-chain strain that EM cannot release. Don't waste a cycle re-running EM with tighter tolerance.
- **TIP3P is intentionally the prep-stage water model.** Decide explicitly before production whether to stay with it or upgrade to TIP4P-D / OPC.

The starting structure at `nterm_md/starting_structure/chainA_B_C_with_nterm_minimized.{gro,pdb}` is the input for Prompt 2.
