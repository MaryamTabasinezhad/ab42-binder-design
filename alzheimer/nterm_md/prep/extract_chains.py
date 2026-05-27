"""Extract chains A, A+B, A+B+C from 9CO4 and report residue ranges."""
from pathlib import Path
from Bio.PDB import PDBParser, PDBIO, Select

INPUT = Path(__file__).parent.parent / "input" / "9CO4.pdb"
OUTDIR = Path(__file__).parent

parser = PDBParser(QUIET=True)
structure = parser.get_structure("9CO4", str(INPUT))


class ChainSelect(Select):
    def __init__(self, chains):
        self.chains = set(chains)

    def accept_chain(self, chain):
        return chain.id in self.chains

    def accept_residue(self, residue):
        # standard amino acids only (skip HETATM/water/ligands)
        return residue.id[0] == " "


def write_chains(chains, name):
    out = OUTDIR / f"{name}.pdb"
    io = PDBIO()
    io.set_structure(structure)
    io.save(str(out), ChainSelect(chains))
    return out


def report(pdbpath):
    s = parser.get_structure("x", str(pdbpath))
    by_chain = {}
    for chain in s.get_chains():
        resids = [r.id[1] for r in chain if r.id[0] == " "]
        by_chain[chain.id] = (len(resids), min(resids), max(resids))
    return by_chain


if __name__ == "__main__":
    print(f"Loaded 9CO4 from {INPUT}")
    print("Chains in source:", sorted([c.id for c in structure.get_chains()]))
    print()

    for name, chains in [("chainA_only", ["A"]),
                         ("chainA_B", ["A", "B"]),
                         ("chainA_B_C", ["A", "B", "C"])]:
        out = write_chains(chains, name)
        size = out.stat().st_size
        info = report(out)
        print(f"{name}.pdb  ({size} bytes)")
        for cid, (n, lo, hi) in info.items():
            print(f"   chain {cid}: {n} residues, range {lo}-{hi}")
        print()
