# Ternary fusion models (fusion bound to both targets)

12 of the 20-design panel fusions, each modeled engaging both targets simultaneously.

Chains in every PDB:
- **F** = bispecific fusion binder (the drug)
- **A** = Amyloid-beta 42 target (disease target, PDB 9CO4) — bound by the Aβ arm
- **T** = TfR1 apical domain (blood-brain-barrier receptor, PDB 6WRV) — engaged by the TfR1 arm

Render colors: F = blue, A = orange, T = green.

## Method
- **Aβ42 (chain A): rigorous** — the fusion's Aβ arm was superposed onto the standalone Aβ binder-target
  complex, transferring the real designed pose (RMSD 0.13-0.79 Å).
- **TfR1 (chain T): schematic** — the docked TfR1 complex was unavailable; the 6WRV apical domain is placed
  with design hotspots (A208/210/211/212/215) facing the TfR1 arm, clash-checked. Illustrative, not a
  computed dock.
- **Biology note:** in vivo the two binding events are sequential (TfR1 at the BBB, then Aβ in brain), not
  simultaneous. This depicts that each arm is independently competent.

## Coverage
Built 12/20. The other 8 use Aβ arms s843399/s480128/s311742 and are missing a required input
(6 lack a committed fusion structure from split B; 2 lack the s311742 Aβ-arm complex). Regenerate those
structures on GPU and re-run the builder to complete all 20.
