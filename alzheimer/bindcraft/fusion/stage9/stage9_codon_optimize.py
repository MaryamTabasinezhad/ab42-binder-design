#!/usr/bin/env python3
"""
Stage 9.4 — codon optimization of the His6-SUMO expression constructs for
E. coli, plus final synthesis sheet (9.5).

Run with the DNAChisel venv (CC env stripped so it uses the PyPI numpy):
    env -u PYTHONPATH -u PIP_CONFIG_FILE \
        .venv-dnachisel/bin/python stage9_codon_optimize.py \
        --in  stage9_sequence_prep.csv \
        --out synthesis_panel.csv

For each construct protein:
  * reverse-translate + optimize for E. coli (codon usage matching + GC control)
  * forbid internal NdeI (CATATG) and XhoI (CTCGAG) so the NdeI/XhoI cloning
    sites into pET-28a(+) stay unique
  * avoid hairpins and 8+ homopolymers
  * prepend NdeI (CATATG includes the start ATG) and append a double stop + XhoI
Emits the order-ready DNA and a merged synthesis sheet.
"""
import argparse, csv
from dnachisel import (
    DnaOptimizationProblem, reverse_translate,
    CodonOptimize, EnforceGCContent, AvoidPattern, EnforceTranslation,
    AvoidHairpins,
)

SPECIES = "e_coli"
NDEI = "CATATG"      # contains the ATG start
XHOI = "CTCGAG"
STOP2 = "TAATGA"     # tandem stop


def optimize_one(protein):
    """Return codon-optimized CDS (no cloning sites) for a protein sequence."""
    seq = reverse_translate(protein)
    problem = DnaOptimizationProblem(
        sequence=seq,
        constraints=[
            EnforceTranslation(),
            # global 40-60% with a more permissive 35-65% local window — the
            # tight 50bp/40-60% combo is infeasible against codon optimization
            # in acidic, low-GC regions and is stricter than vendors require.
            EnforceGCContent(mini=0.40, maxi=0.60),
            EnforceGCContent(mini=0.35, maxi=0.65, window=50),
            AvoidPattern(NDEI),
            AvoidPattern(XHOI),
            AvoidPattern("8xA"), AvoidPattern("8xT"),
            AvoidPattern("8xG"), AvoidPattern("8xC"),
            AvoidHairpins(stem_size=10, hairpin_window=80),
        ],
        objectives=[CodonOptimize(species=SPECIES)],
        logger=None,
    )
    problem.max_random_iters = 20000
    problem.resolve_constraints()
    problem.optimize()
    cds = problem.sequence
    assert len(cds) % 3 == 0 and len(cds) == 3 * len(protein)
    return cds, problem.constraints_text_summary()


def gc(s):
    return round(100.0 * (s.count("G") + s.count("C")) / len(s), 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.inp)))
    out = []
    for r in rows:
        protein = r["construct_protein"]
        cds, summary = optimize_one(protein)
        ok = "INFEASIBLE" not in summary and "FAIL" not in summary
        # order-ready insert: NdeI ... CDS ... double-stop ... XhoI.
        # NdeI = CATATG and its ATG IS the start codon. CDS starts with ATG, so
        # prepend "CAT" -> "CATATG..." (the 3 extra bases are the 5' NdeI part,
        # outside the reading frame). Append tandem stop + XhoI.
        insert = "CAT" + cds + STOP2 + XHOI
        out.append({
            "final_rank": r["rank"],
            "id": r["id"],
            "domain_order": r["domain_order"],
            "linker_name": r["linker_name"],
            "arm1_plddt": r["arm1_plddt"],
            "arm2_plddt": r["arm2_plddt"],
            "inter_domain_pae": r["inter_domain_pae"],
            "construct_len_aa": r["construct_len"],
            "construct_mw_kda": r["construct_mw_kda"],
            "construct_pI": r["construct_pI"],
            "fusion_pI": r["fusion_pI"],
            "fusion_gravy": r["fusion_gravy"],
            "fusion_ext_coeff": r["fusion_ext_coeff"],
            "liabilities": r["liabilities"],
            "severe_flags": r["severe_flags"],
            "tag_architecture": r["tag_architecture"],
            "vector": "pET-28a(+), NdeI/XhoI",
            "cds_gc_pct": gc(cds),
            "constraints_ok": ok,
            "construct_protein": protein,
            "order_dna_NdeI_XhoI": insert,
        })

    fields = list(out[0].keys())
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out)

    n_ok = sum(1 for r in out if r["constraints_ok"])
    print(f"[stage9 codon-opt] {len(out)} constructs optimized -> {args.out}")
    print(f"  constraints satisfied: {n_ok}/{len(out)}")
    print(f"  CDS GC% range: {min(r['cds_gc_pct'] for r in out)}"
          f"-{max(r['cds_gc_pct'] for r in out)}")
    print(f"  insert length range: "
          f"{min(len(r['order_dna_NdeI_XhoI']) for r in out)}"
          f"-{max(len(r['order_dna_NdeI_XhoI']) for r in out)} bp")


if __name__ == "__main__":
    main()
