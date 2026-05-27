# Agent Nibi Status
**Last updated:** 2026-05-11 01:15

## Current Work
- Stage 7 (TfR1 arm) — production design jobs running
- Stage 2 (Aβ arm) — jobs ready to submit (BindCraft installed, not yet launched)

## Completed
- BindCraft installation (conda env, PyRosetta, ColabDesign, AF2 weights)
- PyRosetta BUNS crash fix applied
- Stage 7.0: TfR1 target preparation
  - Downloaded 6WRV, extracted chains A+B (stripped 3DS18 binder C/D/F)
  - Verified hotspot residues A:208(ARG), A:210(VAL), A:211(TYR), A:212(LEU), A:215(ASN)
  - Transferrin competition check: PASS — hotspots on apical domain, 45+ Å from Tf interface
- Stage 7.1: BindCraft configuration
  - Created settings (tfr1_AB.json), advanced config, default filters
  - 5 parallel jobs configured (main + p1–p4), each targeting 1000 designs
  - Binder length: 50–70 residues, target chains A+B (B as steric context)

## Blocked/Failed
- None

## SLURM Jobs
- 13720337 (bc_tfr1) — submitted
- 13720338 (bc_tfr1_p1) — submitted
- 13720339 (bc_tfr1_p2) — running
- 13720341 (bc_tfr1_p3) — pending (Resources)
- 13720342 (bc_tfr1_p4) — pending (Priority)

## Accepted Designs
- TfR1: 0 (jobs just started)
- Aβ: 0 (jobs not yet submitted)
