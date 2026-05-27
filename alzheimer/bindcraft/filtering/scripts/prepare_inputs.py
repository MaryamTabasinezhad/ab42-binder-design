#!/usr/bin/env python3
"""Prepare ColabFold input CSVs for Stage 3 counter-screen.

For each target, creates a CSV with columns: id,sequence
where sequence = binder_seq:target_chain1_seq:target_chain2_seq:...

Uses single_sequence MSA mode (no MSA server needed).
"""

import csv
import sys
from pathlib import Path
from Bio.PDB import PDBParser
from Bio.PDB.Polypeptide import protein_letters_3to1

REPO = Path("/lustre07/scratch/ghaedi/ab42-binder-design")
DESIGNS_CSV = REPO / "alzheimer/bindcraft/designs/final_design_stats.csv"
STRUCTURES = REPO / "alzheimer/structures"
OUTPUT_DIR = REPO / "alzheimer/bindcraft/filtering/inputs"
MANIFEST = REPO / "coordination/manifests/manifest_stage3_narval.tsv"

TARGETS = {
    "9CO4": STRUCTURES / "9CO4.pdb",
    "9CKI": STRUCTURES / "negative_targets/9CKI.pdb",
    "9CK6": STRUCTURES / "negative_targets/9CK6.pdb",
    "7Q4B": STRUCTURES / "negative_targets/7Q4B.pdb",
    "7Q4M": STRUCTURES / "negative_targets/7Q4M.pdb",
    "6SHS": STRUCTURES / "negative_targets/6SHS.pdb",
    "1IYT": STRUCTURES / "negative_targets/1IYT.pdb",
    "Ab40_monomer": STRUCTURES / "negative_targets/Ab40_monomer_af2.pdb",
}

# Use 3 interior chains per fibril, matching the 9CO4 C/E/G design target.
# For monomers (1IYT, Ab40_monomer), use all chains (just 1).
TARGET_CHAINS = {
    "9CO4": ["C", "E", "G"],
    "9CKI": ["C", "E", "G"],
    "9CK6": ["C", "E", "G"],
    "7Q4B": ["C", "E", "G"],
    "7Q4M": ["C", "E", "G"],
    "6SHS": ["C", "E", "G"],
}


def extract_chain_sequences(pdb_path, chain_ids=None):
    """Extract amino acid sequences from PDB chains."""
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("target", str(pdb_path))
    model = structure[0]

    seqs = []
    for chain in model:
        if chain_ids and chain.id not in chain_ids:
            continue
        seq = []
        for residue in chain:
            if residue.id[0] != " ":
                continue
            resname = residue.get_resname()
            if resname in protein_letters_3to1:
                seq.append(protein_letters_3to1[resname])
        if seq:
            seqs.append("".join(seq))
    return seqs


def main():
    designs = {}
    with open(DESIGNS_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            designs[row["Design"]] = row["Sequence"]

    manifest_designs = set()
    manifest_targets = set()
    with open(MANIFEST) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            manifest_designs.add(row["design_id"])
            manifest_targets.add(row["target_pdb"])

    print(f"Designs in manifest: {len(manifest_designs)}")
    print(f"Targets in manifest: {sorted(manifest_targets)}")

    target_seqs = {}
    for target_name, pdb_path in TARGETS.items():
        if target_name not in manifest_targets:
            continue
        chains = TARGET_CHAINS.get(target_name)
        chain_seqs = extract_chain_sequences(pdb_path, chains)
        target_seqs[target_name] = chain_seqs
        total_res = sum(len(s) for s in chain_seqs)
        print(f"  {target_name}: {len(chain_seqs)} chain(s), {total_res} residues total")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for target_name in sorted(manifest_targets):
        outfile = OUTPUT_DIR / f"colabfold_{target_name}.csv"
        count = 0
        with open(outfile, "w") as f:
            f.write("id,sequence\n")
            for design_id in sorted(manifest_designs):
                binder_seq = designs[design_id]
                full_seq = ":".join([binder_seq] + target_seqs[target_name])
                f.write(f"{design_id}_vs_{target_name},{full_seq}\n")
                count += 1
        print(f"  Wrote {outfile.name}: {count} complexes")

    print(f"\nDone. {len(manifest_targets)} input CSVs in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
