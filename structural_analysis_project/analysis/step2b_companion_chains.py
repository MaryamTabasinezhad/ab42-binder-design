"""Step 2b: Per-chain modeled residue summary for companion entries."""
import sys
import traceback
from pathlib import Path
from Bio.PDB import PDBParser
from Bio.PDB.Polypeptide import is_aa

PROJECT = Path.home() / "structural_analysis_project"
COMPANIONS = ["9CK6", "9CKI"]


def chain_summary(chain):
    residues = [r for r in chain.get_residues() if is_aa(r, standard=True)]
    if not residues:
        return None
    nums = [r.id[1] for r in residues]
    first, last = min(nums), max(nums)
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
    return first, last, len(residues), gaps


def main():
    parser = PDBParser(QUIET=True)
    for pid in COMPANIONS:
        path = PROJECT / "structures" / f"{pid}.pdb"
        print(f"\n[step2b] {pid}  ({path})")
        s = parser.get_structure(pid, str(path))
        model = next(s.get_models())
        print(f"{'chain':<6}{'first':>6}{'last':>6}{'count':>7}  gaps")
        for chain in sorted(model, key=lambda c: c.id):
            info = chain_summary(chain)
            if info is None:
                continue
            first, last, count, gaps = info
            gap_str = ", ".join(f"{a}-{b}" if a != b else str(a)
                                for a, b in gaps) or "none"
            print(f"{chain.id:<6}{first:>6}{last:>6}{count:>7}  {gap_str}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
