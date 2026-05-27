#!/usr/bin/env python3
"""Prepare ColabFold input CSVs for Stage 7.3 TfR1 counter-screen.

3 targets × 310 designs:
  1. 6WRV (positive re-confirmation): binder + TfR1 chains A+B
  2. TfR2_apical (negative selectivity): binder + TfR2 apical domain
  3. 1SUV_Tf_competition (negative): binder + TfR1 + Tf (chains A+C+E)
"""

import csv
import json
from pathlib import Path
from Bio.PDB import PDBParser
from Bio.PDB.Polypeptide import protein_letters_3to1

BASE = Path("/home/ghaedi/projects/def-ghaedi/ghaedi/protein")
DESIGNS_CSV = BASE / "alzheimer/bindcraft/tfr1/designs/final_design_stats.csv"
STRUCTURES = BASE / "alzheimer/structures/tfr1"
OUTPUT_DIR = BASE / "alzheimer/bindcraft/tfr1/filtering/inputs"

TARGETS = {
    "6WRV_positive": {
        "pdb": STRUCTURES / "6WRV_target.pdb",
        "chains": ["A", "B"],
    },
    "TfR2_negative": {
        "pdb": STRUCTURES / "TfR2_apical.pdb",
        "chains": ["A"],
    },
    "1SUV_Tf_competition": {
        "pdb": STRUCTURES / "1SUV_TfR1_Tf_complex.pdb",
        "chains": ["A", "C", "E"],
    },
}


def extract_chain_sequences(pdb_path, chain_ids):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("target", str(pdb_path))
    model = structure[0]
    seqs = []
    for cid in chain_ids:
        chain = model[cid]
        seq = []
        for residue in chain:
            if residue.id[0] != " ":
                continue
            resname = residue.get_resname()
            if resname in protein_letters_3to1:
                seq.append(protein_letters_3to1[resname])
        seqs.append("".join(seq))
    return seqs


def main():
    designs = {}
    with open(DESIGNS_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            designs[row["Design"]] = row["Sequence"]
    print(f"Loaded {len(designs)} accepted designs")

    target_seqs = {}
    for name, info in TARGETS.items():
        seqs = extract_chain_sequences(info["pdb"], info["chains"])
        target_seqs[name] = seqs
        total_res = sum(len(s) for s in seqs)
        print(f"  {name}: {len(seqs)} chain(s), {total_res} residues")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for target_name in sorted(TARGETS):
        outfile = OUTPUT_DIR / f"colabfold_{target_name}.csv"
        count = 0
        with open(outfile, "w") as f:
            f.write("id,sequence\n")
            for design_id in sorted(designs):
                binder_seq = designs[design_id]
                full_seq = ":".join([binder_seq] + target_seqs[target_name])
                f.write(f"{design_id}_vs_{target_name},{full_seq}\n")
                count += 1
        print(f"  Wrote {outfile.name}: {count} complexes")

    print(f"\nDone. {len(TARGETS)} input CSVs in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
