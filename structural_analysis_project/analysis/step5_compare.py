"""Step 5 helper: cross-conformation target-residue comparison."""
import json
from pathlib import Path
import pandas as pd

PROJECT = Path.home() / "structural_analysis_project"
TARGETS = [10, 11, 13, 14, 15, 16, 19, 20, 22]
PDBS = ["9CO4", "9CK6", "9CKI"]


def main():
    df = pd.read_csv(PROJECT / "analysis" / "all_targets.csv")

    # Per-residue aggregate across chains for each PDB
    agg = (df.groupby(["pdb_id", "resi", "resname"])["sasa_assembly"]
             .agg(["mean", "min", "max", "median"])
             .round(2)
             .reset_index())
    print("[step5] mean SASA per (PDB, residue) across all chains:")
    pivot = agg.pivot_table(index=["resi", "resname"], columns="pdb_id",
                            values="mean").round(1)
    print(pivot)
    pivot.to_csv(PROJECT / "analysis" / "cross_conformation_mean.csv")

    # Per-residue, fraction of chains with SASA > 40 (exposed)
    exposed_frac = (df.assign(exposed=df["sasa_assembly"] > 40)
                      .groupby(["pdb_id", "resi", "resname"])["exposed"]
                      .mean()
                      .round(2)
                      .unstack("pdb_id"))
    print("\n[step5] fraction of chains classified EXPOSED (SASA > 40 Å²):")
    print(exposed_frac)
    exposed_frac.to_csv(PROJECT / "analysis" / "cross_conformation_exposed_frac.csv")

    # Identify reliably exposed (>=80% of chains exposed in all 3 PDBs)
    reliably_exposed = exposed_frac[(exposed_frac >= 0.8).all(axis=1)]
    print("\n[step5] residues exposed in >=80% of chains in ALL conformations:")
    print(reliably_exposed)

    # Reliably buried (<=20% in all)
    reliably_buried = exposed_frac[(exposed_frac <= 0.2).all(axis=1)]
    print("\n[step5] residues exposed in <=20% of chains in ALL conformations:")
    print(reliably_buried)


if __name__ == "__main__":
    main()
