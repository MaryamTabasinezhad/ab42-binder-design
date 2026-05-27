"""Step 3: SASA analysis on 9CO4 (assembly + monomer reference) plus companions."""
import copy
import json
import sys
import traceback
from pathlib import Path

import pandas as pd
from Bio.PDB import PDBParser
from Bio.PDB.Polypeptide import is_aa
from Bio.PDB.SASA import ShrakeRupley

PROJECT = Path.home() / "structural_analysis_project"
TARGETS = [10, 11, 13, 14, 15, 16, 19, 20, 22]
PRIMARY = "9CO4"
COMPANIONS = ["9CK6", "9CKI"]


def classify(sasa):
    if sasa < 20:
        return "BURIED"
    if sasa <= 40:
        return "PARTIAL"
    return "EXPOSED"


def load_structure(pid):
    parser = PDBParser(QUIET=True)
    return parser.get_structure(pid, str(PROJECT / "structures" / f"{pid}.pdb"))


def per_residue_sasa(structure):
    """Run Shrake-Rupley at residue level on a structure copy.

    Returns dict (chain_id, resnum) -> (resname, sasa).
    """
    s = copy.deepcopy(structure)
    sr = ShrakeRupley(probe_radius=1.40, n_points=960)
    sr.compute(s, level="R")
    out = {}
    model = next(s.get_models())
    for chain in model:
        for res in chain:
            if not is_aa(res, standard=True):
                continue
            out[(chain.id, res.id[1])] = (res.get_resname(), res.sasa)
    return out


def isolated_chain_sasa(structure, chain_id):
    """SASA of a single chain extracted as a free monomer."""
    s = copy.deepcopy(structure)
    model = next(s.get_models())
    keep = chain_id
    detach = [c.id for c in list(model) if c.id != keep]
    for cid in detach:
        model.detach_child(cid)
    sr = ShrakeRupley(probe_radius=1.40, n_points=960)
    sr.compute(s, level="R")
    out = {}
    for res in model[keep]:
        if not is_aa(res, standard=True):
            continue
        out[(keep, res.id[1])] = (res.get_resname(), res.sasa)
    return out


def full_sasa_df(structure, pid):
    """All residues, all chains, in-assembly SASA."""
    sasa = per_residue_sasa(structure)
    rows = []
    for (cid, resi), (resn, val) in sasa.items():
        rows.append({"pdb_id": pid, "chain": cid, "resi": resi,
                     "resname": resn, "sasa_assembly": round(val, 2)})
    df = pd.DataFrame(rows).sort_values(["chain", "resi"]).reset_index(drop=True)
    return df, sasa


def target_table(sasa_assembly, sasa_alone, ref_chain, pid):
    """Target-residue table: one row per chain × target."""
    rows = []
    for (cid, resi), (resn, val) in sasa_assembly.items():
        if resi not in TARGETS:
            continue
        alone = sasa_alone.get((ref_chain, resi), (None, None))[1]
        ratio = (val / alone) if alone and alone > 0 else None
        rows.append({
            "pdb_id": pid,
            "chain": cid,
            "resi": resi,
            "resname": resn,
            "sasa_assembly": round(val, 2),
            "sasa_alone_refchain": round(alone, 2) if alone else None,
            "burial_ratio": round(ratio, 3) if ratio is not None else None,
            "classification": classify(val),
        })
    df = pd.DataFrame(rows).sort_values(["chain", "resi"]).reset_index(drop=True)
    return df


def run_one(pid):
    print(f"\n[step3] === {pid} ===")
    s = load_structure(pid)

    print(f"[step3] {pid}: assembly SASA")
    df_full, sasa_asm = full_sasa_df(s, pid)
    out_csv = PROJECT / "analysis" / f"{pid}_sasa.csv"
    df_full.to_csv(out_csv, index=False)
    print(f"[step3] {pid}: full per-residue table -> {out_csv}")

    # pick reference chain: A if present, else first
    model = next(s.get_models())
    chain_ids = sorted(c.id for c in model)
    ref = "A" if "A" in chain_ids else chain_ids[0]
    print(f"[step3] {pid}: monomer reference = chain {ref}")
    sasa_alone = isolated_chain_sasa(s, ref)

    df_targets = target_table(sasa_asm, sasa_alone, ref, pid)
    print(f"\n[step3] {pid}: target-residue SASA table "
          f"(burial_ratio = assembly / chain-{ref}-alone)")
    print(df_targets.to_string(index=False))
    return df_full, df_targets, sasa_asm, sasa_alone, ref


def main():
    all_targets = []
    primary_full, primary_targets, primary_asm, primary_alone, primary_ref = run_one(PRIMARY)
    all_targets.append(primary_targets)
    primary_targets.to_csv(PROJECT / "analysis" / "9CO4_targets.csv", index=False)

    for pid in COMPANIONS:
        _, df_targets, _, _, _ = run_one(pid)
        df_targets.to_csv(PROJECT / "analysis" / f"{pid}_targets.csv", index=False)
        all_targets.append(df_targets)

    combined = pd.concat(all_targets, ignore_index=True)
    combined.to_csv(PROJECT / "analysis" / "all_targets.csv", index=False)
    print(f"\n[step3] combined target-residue table -> "
          f"{(PROJECT / 'analysis' / 'all_targets.csv').name}")

    # also dump primary in-assembly SASA dict for downstream Step 4
    asm_dump = {f"{c}:{r}": [n, round(v, 4)]
                for (c, r), (n, v) in primary_asm.items()}
    alone_dump = {f"{c}:{r}": [n, round(v, 4)]
                  for (c, r), (n, v) in primary_alone.items()}
    (PROJECT / "analysis" / "9CO4_sasa_assembly.json").write_text(
        json.dumps(asm_dump, indent=2))
    (PROJECT / "analysis" / "9CO4_sasa_alone_chainA.json").write_text(
        json.dumps(alone_dump, indent=2))
    print(f"[step3] dumped JSON sasa maps for Step 4")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
