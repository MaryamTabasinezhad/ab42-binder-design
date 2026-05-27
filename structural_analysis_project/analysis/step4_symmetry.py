"""Step 4: pairwise interfaces + helical face partition for 9CO4."""
import copy
import json
import math
import sys
import traceback
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from Bio.PDB import PDBParser
from Bio.PDB.Polypeptide import is_aa
from Bio.PDB.SASA import ShrakeRupley

PROJECT = Path.home() / "structural_analysis_project"
PID = "9CO4"
TARGETS = [10, 11, 13, 14, 15, 16, 19, 20, 22]


def load():
    p = PDBParser(QUIET=True)
    return p.get_structure(PID, str(PROJECT / "structures" / f"{PID}.pdb"))


def chain_total_sasa(structure, kept_chain_ids):
    """Sum SASA over all residues in kept_chain_ids; return per-chain totals."""
    s = copy.deepcopy(structure)
    model = next(s.get_models())
    for cid in [c.id for c in list(model)]:
        if cid not in kept_chain_ids:
            model.detach_child(cid)
    sr = ShrakeRupley(probe_radius=1.40, n_points=960)
    sr.compute(s, level="R")
    totals = {cid: 0.0 for cid in kept_chain_ids}
    for chain in model:
        for res in chain:
            if is_aa(res, standard=True):
                totals[chain.id] += res.sasa
    return totals


def cα_centroid(structure, chain_id):
    s = next(structure.get_models())
    coords = [a.coord for r in s[chain_id]
              if is_aa(r, standard=True) and "CA" in r
              for a in [r["CA"]]]
    return np.mean(coords, axis=0)


def main():
    s = load()
    chain_ids = sorted(c.id for c in next(s.get_models()))
    print(f"[step4] chains: {chain_ids}")

    print("[step4] computing per-chain alone SASA totals (10 runs)...")
    alone_totals = {}
    for cid in chain_ids:
        t = chain_total_sasa(s, {cid})[cid]
        alone_totals[cid] = t
        print(f"  chain {cid} alone total = {t:.1f} Å²")

    print("\n[step4] computing pairwise interface areas (45 pair runs)...")
    pair_rows = []
    for a, b in combinations(chain_ids, 2):
        pair_totals = chain_total_sasa(s, {a, b})
        buried_a = alone_totals[a] - pair_totals[a]
        buried_b = alone_totals[b] - pair_totals[b]
        bsa = buried_a + buried_b  # total buried surface area on interface
        pair_rows.append({
            "chain_i": a, "chain_j": b,
            "buried_i": round(buried_a, 1),
            "buried_j": round(buried_b, 1),
            "interface_BSA": round(bsa, 1),
        })
    df = pd.DataFrame(pair_rows).sort_values("interface_BSA", ascending=False)
    df.to_csv(PROJECT / "analysis" / "9CO4_pairwise_interfaces.csv", index=False)
    print("\n[step4] pairwise interfaces (sorted by BSA, top 15):")
    print(df.head(15).to_string(index=False))

    # Direct neighbours: pairs with BSA > some fraction of max
    max_bsa = df["interface_BSA"].max()
    threshold = 0.30 * max_bsa
    neighbours = df[df["interface_BSA"] >= threshold]
    print(f"\n[step4] direct neighbour pairs (BSA >= 30% of max = "
          f"{threshold:.0f} Å²):")
    for _, r in neighbours.iterrows():
        print(f"  {r['chain_i']}-{r['chain_j']}: {r['interface_BSA']:.1f} Å²")

    # ---- helical axis + angular partition ----
    print("\n[step4] computing chain Cα centroids and helical axis")
    centroids = {cid: cα_centroid(s, cid) for cid in chain_ids}
    M = np.array([centroids[c] for c in chain_ids])
    com = M.mean(axis=0)
    Mc = M - com
    # principal axis = top eigenvector of covariance
    cov = Mc.T @ Mc
    w, v = np.linalg.eigh(cov)
    axis = v[:, -1]  # largest eigenvalue
    axis = axis / np.linalg.norm(axis)
    print(f"  helical axis vector: {axis}")

    # Project off-axis component, build angular reference
    proj = Mc - np.outer(Mc @ axis, axis)
    # pick reference perpendicular vector from chain A
    ref = proj[0] / np.linalg.norm(proj[0])
    # second basis = axis × ref
    e2 = np.cross(axis, ref)
    e2 = e2 / np.linalg.norm(e2)

    angles = {}
    z_proj = {}
    for cid, p in zip(chain_ids, proj):
        x = float(p @ ref)
        y = float(p @ e2)
        ang = math.degrees(math.atan2(y, x))
        angles[cid] = ang
        z_proj[cid] = float((centroids[cid] - com) @ axis)

    print("\n  chain  angle(°)  z(Å)")
    for cid in chain_ids:
        print(f"  {cid:^6} {angles[cid]:8.2f}  {z_proj[cid]:7.2f}")

    # Wrap angle differences relative to chain A; consecutive subunits
    # in helical lattice should differ by ~178° (the ΔΦ).
    # Sort chains by z (axial position) and report angle delta along axis.
    by_z = sorted(chain_ids, key=lambda c: z_proj[c])
    print(f"\n  chains by axial position (z): {by_z}")
    deltas = []
    for c1, c2 in zip(by_z, by_z[1:]):
        d = (angles[c2] - angles[c1] + 540) % 360 - 180  # signed delta
        deltas.append((c1, c2, d, z_proj[c2] - z_proj[c1]))
    print("  step    Δφ(°)   Δz(Å)")
    for c1, c2, d, dz in deltas:
        print(f"  {c1}->{c2}  {d:7.2f}  {dz:6.2f}")

    # ---- Face partition: angular analysis ----
    a_ang = angles["A"]
    angular_face_A = []
    angular_face_B = []
    for cid in chain_ids:
        d = (angles[cid] - a_ang + 540) % 360 - 180
        if abs(d) < 90:
            angular_face_A.append(cid)
        else:
            angular_face_B.append(cid)
    print(f"\n[step4] angular partition (within ±90° of chain A's azimuth):")
    print(f"  angular_face_A = {angular_face_A}")
    print(f"  angular_face_B = {angular_face_B}")

    # ---- Face partition: connected-component on strong interfaces ----
    # Treat pairs with BSA >= 1000 Å² as protofilament edges.
    edges = [(r['chain_i'], r['chain_j']) for _, r in df.iterrows()
             if r['interface_BSA'] >= 1000]
    parent = {c: c for c in chain_ids}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        parent[find(a)] = find(b)
    for a, b in edges:
        union(a, b)
    components = {}
    for c in chain_ids:
        components.setdefault(find(c), []).append(c)
    comp_groups = sorted(components.values(), key=lambda g: -len(g))
    print(f"\n[step4] interface-based protofilament partition "
          f"(connected components, BSA >= 1000 Å²):")
    for i, g in enumerate(comp_groups):
        print(f"  group_{i} = {sorted(g)}")
    if len(comp_groups) >= 2:
        face_A = sorted(comp_groups[0])
        face_B = sorted(comp_groups[1])
    else:
        face_A = angular_face_A
        face_B = angular_face_B

    expected_A = list("ACEGI")
    expected_B = list("BDFHJ")
    matches_angular = (sorted(angular_face_A) == expected_A
                       and sorted(angular_face_B) == expected_B) \
                      or (sorted(angular_face_B) == expected_A
                          and sorted(angular_face_A) == expected_B)
    matches_interface = (face_A == expected_A and face_B == expected_B) \
                        or (face_B == expected_A and face_A == expected_B)
    print(f"\n[step4] hypothesis check:")
    print(f"  expected partition: {{A,C,E,G,I}} vs {{B,D,F,H,J}}")
    print(f"  angular partition matches: {matches_angular}")
    print(f"  interface partition matches: {matches_interface}")
    print(f"\n[step4] using interface-based partition as canonical 'face' "
          f"definition for patch analysis (these are the two protofilaments).")

    # ---- Patch residues: target residues per face with SASA_assembly > 40 ----
    asm = json.loads((PROJECT / "analysis" / "9CO4_sasa_assembly.json").read_text())
    asm_lookup = {tuple(k.split(":", 1)): (v[0], v[1])
                  for k, v in asm.items()}

    def patch_for(face):
        # set of (chain, resi, resname, sasa) where resi in targets and sasa > 40
        items = []
        for cid in face:
            for resi in TARGETS:
                key = (cid, str(resi))
                if key in asm_lookup:
                    resn, val = asm_lookup[key]
                    if val > 40:
                        items.append((cid, resi, resn, round(val, 2)))
        return items

    patches_A = patch_for(face_A)
    patches_B = patch_for(face_B)
    print(f"\n[step4] face_A candidate patch residues (SASA_assembly > 40 Å²): "
          f"{len(patches_A)} entries")
    for c, r, n, v in patches_A:
        print(f"  {c} {n}{r}  {v}")
    print(f"\n[step4] face_B candidate patch residues (SASA_assembly > 40 Å²): "
          f"{len(patches_B)} entries")
    for c, r, n, v in patches_B:
        print(f"  {c} {n}{r}  {v}")

    # save
    (PROJECT / "analysis" / "9CO4_faces.json").write_text(json.dumps({
        "face_A_interface_based": face_A,
        "face_B_interface_based": face_B,
        "angular_face_A": angular_face_A,
        "angular_face_B": angular_face_B,
        "interface_matches_expected": matches_interface,
        "angular_matches_expected": matches_angular,
        "principal_axis": axis.tolist(),
        "angles_deg": angles,
        "z_proj": z_proj,
        "patches_face_A": [{"chain": c, "resi": r, "resname": n, "sasa": v}
                           for c, r, n, v in patches_A],
        "patches_face_B": [{"chain": c, "resi": r, "resname": n, "sasa": v}
                           for c, r, n, v in patches_B],
    }, indent=2))
    print(f"\n[step4] face/patch analysis saved -> analysis/9CO4_faces.json")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
