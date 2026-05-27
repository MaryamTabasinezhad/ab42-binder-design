"""Merge chain A from chainA_with_nterm.pdb (PDBFixer-extended) with chains B+C
from chainA_B_C.pdb (unmodified original cryo-EM coords).

Why: PDBFixer's addMissingResidues placed OD1 of ASP7 on top of the backbone N
when run on the multi-chain system, but produced reasonable geometry when run on
chain A alone. So we keep the chain-A-only output and stitch B and C back in.

Sanity: residues 9-42 of chain A in chainA_with_nterm.pdb must coincide with
chain A in chainA_B_C.pdb (PDBFixer should not have moved the existing residues
since it had no template for them). We verify and abort if they have drifted.
"""
from __future__ import annotations
import sys
import math
from pathlib import Path
from Bio.PDB import PDBParser, PDBIO, Select
from Bio.PDB.Structure import Structure
from Bio.PDB.Model import Model
from Bio.PDB.Chain import Chain

PREP = Path(__file__).parent
CHAIN_A_WITH = PREP / "chainA_with_nterm.pdb"
CHAIN_A_BC = PREP / "chainA_B_C.pdb"
OUT = PREP / "chainA_B_C_with_nterm.pdb"


def coord_dist(a1, a2):
    return math.sqrt(sum((a1.coord[i] - a2.coord[i]) ** 2 for i in range(3)))


def main():
    parser = PDBParser(QUIET=True)
    s_a = parser.get_structure("a", str(CHAIN_A_WITH))
    s_bc = parser.get_structure("bc", str(CHAIN_A_BC))

    chainA_new = s_a[0]["A"]
    chainA_orig = s_bc[0]["A"]

    # Drift check on residues 9-42 (the originally-modeled residues).
    max_drift = 0.0
    drift_residue = None
    for resid in range(9, 43):
        if resid not in [r.id[1] for r in chainA_new]: continue
        if resid not in [r.id[1] for r in chainA_orig]: continue
        r_new = chainA_new[(' ', resid, ' ')]
        r_orig = chainA_orig[(' ', resid, ' ')]
        if "CA" in r_new and "CA" in r_orig:
            d = coord_dist(r_new["CA"], r_orig["CA"])
            if d > max_drift:
                max_drift = d
                drift_residue = resid

    print(f"max chain-A CA drift (PDBFixer vs original) for residues 9-42: "
          f"{max_drift:.3f} Å at residue {drift_residue}")
    if max_drift > 0.5:
        sys.exit(
            f"FAILED: chain A residues 9-42 drifted by {max_drift:.2f} Å — "
            f"PDBFixer may have moved them; refusing to merge naively."
        )

    # Build new structure: chain A from PDBFixer file, chains B and C from BC file.
    new_struct = Structure("merged")
    new_model = Model(0)
    new_struct.add(new_model)

    for chain_id, source_chain in [("A", chainA_new),
                                   ("B", s_bc[0]["B"]),
                                   ("C", s_bc[0]["C"])]:
        new_chain = Chain(chain_id)
        for res in source_chain:
            if res.id[0] != " ": continue
            new_chain.add(res.copy())
        new_model.add(new_chain)

    io = PDBIO()
    io.set_structure(new_struct)
    io.save(str(OUT))
    print(f"wrote {OUT}")

    # Verify final.
    s = parser.get_structure("v", str(OUT))
    for chain in s[0]:
        resids = [r.id[1] for r in chain if r.id[0] == " "]
        print(f"  chain {chain.id}: {len(resids)} residues, range {min(resids)}-{max(resids)}")


if __name__ == "__main__":
    main()
