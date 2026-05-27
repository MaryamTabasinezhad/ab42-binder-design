"""Step 1: Parse 9CO4 — per-chain modeled residues + chain A sequence verification."""
import sys
import traceback
from pathlib import Path
from Bio.PDB import PDBParser
from Bio.PDB.Polypeptide import is_aa
from Bio.PDB.Polypeptide import protein_letters_3to1 as _AA3TO1


def three_to_one(resname):
    return _AA3TO1[resname.upper()]

PROJECT = Path.home() / "structural_analysis_project"
PDB_PATH = PROJECT / "structures" / "9CO4.pdb"
EXPECTED_SEQ = "DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVVIA"  # residues 1-42


def chain_residue_summary(chain):
    """Return (first, last, count, gaps, seq_dict) for standard amino acids."""
    residues = [r for r in chain.get_residues() if is_aa(r, standard=True)]
    if not residues:
        return None
    nums = [r.id[1] for r in residues]
    first, last = min(nums), max(nums)
    count = len(residues)
    seen = set(nums)
    gaps = []
    run_start = None
    for n in range(first, last + 1):
        if n not in seen:
            if run_start is None:
                run_start = n
            run_end = n
        else:
            if run_start is not None:
                gaps.append((run_start, run_end))
                run_start = None
    if run_start is not None:
        gaps.append((run_start, run_end))
    seq_dict = {}
    for r in residues:
        try:
            seq_dict[r.id[1]] = three_to_one(r.get_resname())
        except Exception:
            seq_dict[r.id[1]] = "X"
    return first, last, count, gaps, seq_dict


def main():
    print(f"[step1] parsing {PDB_PATH}")
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("9CO4", str(PDB_PATH))
    model = next(structure.get_models())

    chain_data = {}
    print("\n[step1] per-chain modeled residue summary")
    print(f"{'chain':<6}{'first':>6}{'last':>6}{'count':>7}  gaps")
    for chain in sorted(model, key=lambda c: c.id):
        cid = chain.id
        info = chain_residue_summary(chain)
        if info is None:
            continue
        first, last, count, gaps, seq_dict = info
        chain_data[cid] = info
        gap_str = ", ".join(f"{a}-{b}" if a != b else str(a) for a, b in gaps) or "none"
        print(f"{cid:<6}{first:>6}{last:>6}{count:>7}  {gap_str}")

    # Chain A sequence verification
    if "A" not in chain_data:
        raise RuntimeError("Chain A not found")
    first, last, count, gaps, seq_dict = chain_data["A"]
    # Build observed sequence over expected positions 1..42
    print("\n[step1] chain A sequence comparison (positions 1-42)")
    print("pos  expected  observed")
    mismatches = []
    for pos in range(1, 43):
        exp = EXPECTED_SEQ[pos - 1]
        obs = seq_dict.get(pos, "-")
        flag = "" if obs == exp or obs == "-" else "  <-- MISMATCH"
        if obs != "-" and obs != exp:
            mismatches.append((pos, exp, obs))
        print(f"{pos:>3}  {exp:^8}  {obs:^8}{flag}")
    if mismatches:
        raise RuntimeError(f"Sequence mismatches: {mismatches}")
    observed_first = min(seq_dict)
    print(f"\n[step1] chain A first modeled residue = {observed_first} "
          f"(residues 1-{observed_first - 1} missing as expected)")
    print("[step1] sequence matches expected at all observed positions.")

    return chain_data


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
