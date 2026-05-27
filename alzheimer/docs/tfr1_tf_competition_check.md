# TfR1 — Transferrin Competition Check

**Date:** 2026-05-11
**Status:** PASS — No competition risk

## Summary

Hotspot residues A:208, A:210, A:211, A:212, A:215 are located on the **apical domain** of TfR1 and do NOT overlap with the transferrin (Tf) binding interface. The binding site is safe for binder design without Tf competition.

## Analysis

### Hotspot residue identities (from 6WRV chain A)

| Residue | Amino acid | CA B-factor |
|---------|-----------|-------------|
| 208 | ARG | 104.35 |
| 210 | VAL | 78.97 |
| 211 | TYR | 60.81 |
| 212 | LEU | 69.64 |
| 215 | ASN | 62.24 |

### Transferrin binding interface (from PDB 1SUV)

Tf contacts TfR1 at residues in the helical/protease-like domain:
- Residues 123–126, 527–529, 604, 619–670, 759

These are entirely in the C-terminal half of the ectodomain (helical domain and protease-like domain).

### Spatial separation

- Minimum CA-CA distance from hotspots to nearest Tf contact: **~45 Å**
- Hotspots are on the **apical domain** (residues 190–340)
- Tf contacts are on the **helical/protease-like domain** (residues 527–670)
- The two sites are on opposite faces of the TfR1 ectodomain

### Validation against 3DS18 (existing binder in 6WRV)

The 3DS18 binder (Sahtoe et al., PNAS 2020) contacts TfR1 at residues:
- 199, 201, 202, 203, 207, 208, 209, 210, 211, 212, 215, 340, 344, 371, 374

**Our hotspot residues (208, 210, 211, 212, 215) are exactly at the validated 3DS18 binding site.** This binder was experimentally confirmed to NOT compete with Tf binding and to cross an in vitro BBB model.

### Chain F anomaly

In 6WRV, chain F (one of the 3DS18 copies) contacts chain A at residues 619–759 — these are Tf-interface residues. This is a crystal packing contact, not a biological interaction. The biological binding mode is represented by chains C→B and D→A (apical domain).

## Conclusion

- **PASS:** Hotspot residues are on the apical domain, 45+ Å from the Tf binding interface.
- The binding site is validated by 3DS18 (same site, no Tf competition confirmed experimentally).
- No need to modify hotspots or plan Tf-competition SPR as a risk mitigation.
