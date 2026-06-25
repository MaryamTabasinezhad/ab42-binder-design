#!/usr/bin/env python3
"""
Stage 9 — sequence-based synthesis prep (no PDBs required).

Steps 9.2 (liability scan + ProtParam), 9.3 (His6-SUMO construct assembly).
Run under an env with biopython (e.g. colabfold):
    eval "$(conda shell.bash hook)" && conda activate colabfold
    python3 stage9_sequence_prep.py \
        --manifest ../inputs/fusion_manifest.csv \
        --merged   ../stage8_results_merged.csv \
        --out      stage9_sequence_prep.csv

Outputs one row per panel design with developability metrics, liability motif
hits, and the assembled His6-SUMO expression construct (protein). Codon
optimization (9.4) is a separate DNAChisel step that consumes the
`construct_protein` column.
"""
import argparse, csv, re
from Bio.SeqUtils.ProtParam import ProteinAnalysis

# ---- His6-SUMO (Smt3) cassette -------------------------------------------
# N-term Met, His6, short GS linker, then S. cerevisiae Smt3 (SUMO) ending in
# the di-Gly that Ulp1/SUMO-protease cleaves after -> native fusion N-terminus.
HIS6_SUMO = (
    "MGHHHHHHGS"
    "SDSEVNQEAKPEVKPEVKPETHINLKVSDGSSEIFFKIKKTTPLRRLMEAFAKRQGKEMDSLRFLYDGIRIQADQTPEDLDMEDNDIIEAHREQIGG"
)
TAG_NAME = "His6-SUMO(Smt3), Ulp1-cleavable -> native N-term"

# ---- liability motifs (scan the FUSION sequence, not the tag) -------------
LIABILITY_PATTERNS = {
    "deamidation_NG": r"N[G]",          # fastest Asn deamidation
    "deamidation_NS": r"N[S]",
    "deamidation_NT": r"N[T]",
    "isomerization_DG": r"D[G]",        # Asp isomerization hotspots
    "isomerization_DP": r"D[P]",
    "nglyc_sequon": r"N[^P][ST]",       # N-X-S/T (irrelevant in E. coli; flagged)
    "free_cys": r"C",                   # should be zero across panel
    "met_NtermOx": r"^M",               # informational
}
# crude low-complexity: any single residue run >= 5 (linker GS runs excluded by
# scanning arms only is overkill; we report runs in the FULL fusion but ignore G/S)
def low_complexity_runs(seq, minrun=5):
    hits = []
    for m in re.finditer(r"(.)\1{%d,}" % (minrun - 1), seq):
        if m.group(1) not in "GS":      # GS linkers are intentional
            hits.append(f"{m.group(1)}x{len(m.group(0))}@{m.start()+1}")
    return hits


def scan_liabilities(fusion_seq):
    flags = {}
    for name, pat in LIABILITY_PATTERNS.items():
        n = len(re.findall(pat, fusion_seq))
        if n:
            flags[name] = n
    lc = low_complexity_runs(fusion_seq)
    if lc:
        flags["low_complexity"] = ";".join(lc)
    return flags


def protparam(seq):
    pa = ProteinAnalysis(seq)
    # ProtParam can't handle non-standard letters; fusion panel is standard AAs.
    return {
        "length": len(seq),
        "mw_kda": round(pa.molecular_weight() / 1000.0, 2),
        "pI": round(pa.isoelectric_point(), 2),
        "gravy": round(pa.gravy(), 3),
        "ext_coeff_red": int(pa.molar_extinction_coefficient()[0]),  # reduced Cys
        "aromaticity": round(pa.aromaticity(), 3),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--merged", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    manifest = {r["id"]: r for r in csv.DictReader(open(args.manifest))}
    panel = [r for r in csv.DictReader(open(args.merged))
             if r.get("panel_selected", "").lower() == "true"]
    panel.sort(key=lambda r: int(r["rank"]))

    rows = []
    for r in panel:
        m = manifest[r["id"]]
        fusion = m["sequence"]
        construct = HIS6_SUMO + fusion        # native N-term after Ulp1 cleavage
        liab = scan_liabilities(fusion)
        pp_fusion = protparam(fusion)
        pp_construct = protparam(construct)
        # severity heuristic: free Cys or low-complexity (non-GS) = hard flag
        severe = []
        if liab.get("free_cys"):
            severe.append("free_Cys")
        if liab.get("low_complexity"):
            severe.append("low_complexity")
        rows.append({
            "rank": r["rank"],
            "id": r["id"],
            "domain_order": m["domain_order"],
            "linker_name": m["linker_name"],
            "arm1_plddt": r["arm1_plddt"],
            "arm2_plddt": r["arm2_plddt"],
            "inter_domain_pae": r["inter_domain_pae"],
            "fusion_len": pp_fusion["length"],
            "fusion_mw_kda": pp_fusion["mw_kda"],
            "fusion_pI": pp_fusion["pI"],
            "fusion_gravy": pp_fusion["gravy"],
            "fusion_ext_coeff": pp_fusion["ext_coeff_red"],
            "construct_len": pp_construct["length"],
            "construct_mw_kda": pp_construct["mw_kda"],
            "construct_pI": pp_construct["pI"],
            "liabilities": ";".join(f"{k}={v}" for k, v in sorted(liab.items())) or "none",
            "severe_flags": ";".join(severe) or "none",
            "tag_architecture": TAG_NAME,
            "fusion_seq": fusion,
            "construct_protein": construct,
        })

    fields = list(rows[0].keys())
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    # summary
    n_severe = sum(1 for r in rows if r["severe_flags"] != "none")
    print(f"[stage9 seq-prep] {len(rows)} panel designs processed -> {args.out}")
    print(f"  construct length range: {min(r['construct_len'] for r in rows)}"
          f"-{max(r['construct_len'] for r in rows)} aa "
          f"(tag adds {len(HIS6_SUMO)} aa)")
    print(f"  fusion pI range: {min(r['fusion_pI'] for r in rows)}"
          f"-{max(r['fusion_pI'] for r in rows)}")
    print(f"  designs with severe flags: {n_severe}/{len(rows)}")
    print(f"\n{'rank':>4} {'id':40} {'pI':>5} {'MW':>6} {'gravy':>6} liabilities")
    for r in rows:
        print(f"{r['rank']:>4} {r['id']:40} {r['fusion_pI']:>5} "
              f"{r['fusion_mw_kda']:>6} {r['fusion_gravy']:>6} {r['liabilities']}")


if __name__ == "__main__":
    main()
