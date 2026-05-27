from Bio.PDB import PDBParser, PDBIO

input_pdb = "TfR1_crop.pdb"
output_pdb = "TfR1crop_renumber.pdb"

OLD_START = 190
OLD_END = 260
NEW_START = 1

TARGET_CHAIN = "A"   # 👈 important

parser = PDBParser(QUIET=True)
structure = parser.get_structure("protein", input_pdb)

for model in structure:
    for chain in model:
        if chain.id != TARGET_CHAIN:
            continue  # 👈 skip other chains

        for residue in chain:
            res_id = residue.id[1]

            if OLD_START <= res_id <= OLD_END:
                new_id = NEW_START + (res_id - OLD_START)
                residue.id = (residue.id[0], new_id, residue.id[2])

io = PDBIO()
io.set_structure(structure)
io.save(output_pdb)

print("Done! Renumbered only chain A")
