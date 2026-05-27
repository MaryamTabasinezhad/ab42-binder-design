"""Append residues 1-8 (DAEFRHDS) to chain A of an Aβ42 PDB using PDBFixer.

PDBFixer.addMissingResidues handles N-terminal extensions natively. The function
takes a dict {(chain_index, residue_index): sequence}: chain_index is the 0-based
chain ordinal, residue_index is the position before which the sequence is inserted
(0 for an N-terminal extension), sequence is a list of three-letter codes.
"""
from pathlib import Path
import sys
from pdbfixer import PDBFixer
from openmm.app import PDBFile

PREP = Path(__file__).parent

# Aβ N-terminal residues 1-8: D-A-E-F-R-H-D-S
NTERM_3LETTER = ["ASP", "ALA", "GLU", "PHE", "ARG", "HIS", "ASP", "SER"]


def fix_one(input_pdb: Path, output_pdb: Path, chain_letter: str = "A"):
    """Append the 8-residue N-terminus to `chain_letter` of input_pdb."""
    print(f"\n=== {input_pdb.name} -> {output_pdb.name} (chain {chain_letter}) ===")

    fixer = PDBFixer(filename=str(input_pdb))

    # Determine the 0-based chain ordinal that matches `chain_letter`.
    chain_ids = [c.id for c in fixer.topology.chains()]
    if chain_letter not in chain_ids:
        raise RuntimeError(f"chain {chain_letter} not in {chain_ids}")
    chain_index = chain_ids.index(chain_letter)
    print(f"chains in input: {chain_ids}; targeting index {chain_index}")

    # PDBFixer's findMissingResidues fills in missingResidues from SEQRES/REMARKs;
    # for our case the input PDBs have no SEQRES with full-length sequence, so we
    # populate missingResidues manually for an N-terminal extension.
    fixer.missingResidues = {(chain_index, 0): NTERM_3LETTER}
    fixer.missingTerminals = {}
    fixer.missingAtoms = {}

    # Trigger the standard pipeline.
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    # Don't add hydrogens here — pdb2gmx will protonate later, and adding here can
    # collide with GROMACS's HIE/HID/HIP nomenclature.

    with open(output_pdb, "w") as fh:
        PDBFile.writeFile(fixer.topology, fixer.positions, fh, keepIds=True)

    # Verify the result.
    n_res_chainA = sum(
        1 for c in fixer.topology.chains() if c.id == chain_letter for _ in c.residues()
    )
    first_resnum = None
    last_resnum = None
    for c in fixer.topology.chains():
        if c.id == chain_letter:
            ids = [int(r.id) for r in c.residues()]
            first_resnum = ids[0]
            last_resnum = ids[-1]
            break
    print(
        f"chain {chain_letter} now has {n_res_chainA} residues "
        f"(numbered {first_resnum}-{last_resnum})"
    )
    return n_res_chainA, first_resnum, last_resnum


def main():
    inputs = [
        (PREP / "chainA_only.pdb", PREP / "chainA_with_nterm.pdb"),
        (PREP / "chainA_B_C.pdb", PREP / "chainA_B_C_with_nterm.pdb"),
    ]
    for inp, out in inputs:
        if not inp.exists():
            sys.exit(f"missing input: {inp}")
        n, lo, hi = fix_one(inp, out)
        if n != 42 or lo != 1 or hi != 42:
            sys.exit(
                f"FAILED: chain A in {out.name} has {n} residues, range {lo}-{hi}; "
                f"expected 42 residues, range 1-42"
            )
    print("\nAll N-terminal extensions complete.")


if __name__ == "__main__":
    main()
