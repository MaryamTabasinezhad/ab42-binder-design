#!/usr/bin/env python3
"""
Generate 250 tandem fusion sequences from top Aβ42 × top TfR1 binders.
5 Aβ42 × 5 TfR1 × 10 linker variants = 250 fusions.

Usage:
  python generate_fusions.py \
    --ab42-csv <stage5_ranked.csv> \
    --tfr1-csv <stage7_5_ranked.csv> \
    --output-dir <fusion/inputs/>
"""

import argparse
import csv
from pathlib import Path

AB42_TOP_N = 5
TFR1_TOP_N = 5

AB42_SKIP_SCAFFOLDS = {}

LINKERS = [
    {"id": "v1",  "order": "ab-tfr1", "name": "GS3",    "seq": "GGGGS" * 3},
    {"id": "v2",  "order": "ab-tfr1", "name": "GS4",    "seq": "GGGGS" * 4},
    {"id": "v3",  "order": "ab-tfr1", "name": "GS5",    "seq": "GGGGS" * 5},
    {"id": "v4",  "order": "ab-tfr1", "name": "EAAAK",  "seq": "AEAAAKEAAAKEAAAKA"},
    {"id": "v5",  "order": "ab-tfr1", "name": "PAPAP",  "seq": "PAPAP"},
    {"id": "v6",  "order": "tfr1-ab", "name": "GS3",    "seq": "GGGGS" * 3},
    {"id": "v7",  "order": "tfr1-ab", "name": "GS4",    "seq": "GGGGS" * 4},
    {"id": "v8",  "order": "tfr1-ab", "name": "GS5",    "seq": "GGGGS" * 5},
    {"id": "v9",  "order": "tfr1-ab", "name": "EAAAK",  "seq": "AEAAAKEAAAKEAAAKA"},
    {"id": "v10", "order": "tfr1-ab", "name": "PAPAP",  "seq": "PAPAP"},
]


def short_name(design_name):
    parts = design_name.split('_')
    scaffold = parts[2] if len(parts) > 2 else parts[0]
    mpnn = parts[3] if len(parts) > 3 else ""
    mpnn_num = mpnn.replace("mpnn", "m") if mpnn else ""
    return f"{scaffold}{mpnn_num}"


def load_top_designs(csv_path, n, id_col, seq_col, scaffold_col=None):
    designs = []
    seen_scaffolds = set()
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            scaffold = row.get(scaffold_col, '') if scaffold_col else ''
            if scaffold in seen_scaffolds and scaffold_col:
                continue
            designs.append({
                'id': row[id_col],
                'sequence': row[seq_col],
                'scaffold': scaffold,
                'short': short_name(row[id_col]),
            })
            if scaffold:
                seen_scaffolds.add(scaffold)
            if len(designs) >= n:
                break
    return designs


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ab42-csv", required=True)
    p.add_argument("--tfr1-csv", required=True)
    p.add_argument("--output-dir", required=True)
    args = p.parse_args()

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    ab42_designs = load_top_designs(
        args.ab42_csv, AB42_TOP_N,
        id_col='design', seq_col='sequence', scaffold_col='scaffold'
    )
    tfr1_designs = load_top_designs(
        args.tfr1_csv, TFR1_TOP_N,
        id_col='Design', seq_col='Sequence', scaffold_col='scaffold'
    )

    print(f"Aβ42 designs ({len(ab42_designs)}):")
    for d in ab42_designs:
        print(f"  {d['id']} ({d['scaffold']}, {len(d['sequence'])} aa)")

    print(f"\nTfR1 designs ({len(tfr1_designs)}):")
    for d in tfr1_designs:
        print(f"  {d['id']} ({d['scaffold']}, {len(d['sequence'])} aa)")

    fusions = []
    for ab in ab42_designs:
        for tfr in tfr1_designs:
            for linker in LINKERS:
                if linker['order'] == 'ab-tfr1':
                    seq = ab['sequence'] + linker['seq'] + tfr['sequence']
                    arm1_id, arm2_id = ab['id'], tfr['id']
                    arm1_len, arm2_len = len(ab['sequence']), len(tfr['sequence'])
                else:
                    seq = tfr['sequence'] + linker['seq'] + ab['sequence']
                    arm1_id, arm2_id = tfr['id'], ab['id']
                    arm1_len, arm2_len = len(tfr['sequence']), len(ab['sequence'])

                fusion_id = f"fusion_{ab['short']}_{tfr['short']}_{linker['id']}"
                fusions.append({
                    'id': fusion_id,
                    'sequence': seq,
                    'ab42_design': ab['id'],
                    'tfr1_design': tfr['id'],
                    'linker_id': linker['id'],
                    'linker_name': linker['name'],
                    'domain_order': linker['order'],
                    'linker_seq': linker['seq'],
                    'linker_len': len(linker['seq']),
                    'arm1_id': arm1_id,
                    'arm2_id': arm2_id,
                    'arm1_len': arm1_len,
                    'arm2_len': arm2_len,
                    'total_len': len(seq),
                })

    # Write full manifest
    manifest_path = outdir / 'fusion_manifest.csv'
    manifest_fields = [
        'id', 'sequence', 'ab42_design', 'tfr1_design',
        'linker_id', 'linker_name', 'domain_order', 'linker_seq',
        'linker_len', 'arm1_id', 'arm2_id', 'arm1_len', 'arm2_len', 'total_len'
    ]
    with open(manifest_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=manifest_fields)
        writer.writeheader()
        writer.writerows(fusions)

    # Write ColabFold input (id,sequence)
    cf_all = outdir / 'fusion_input.csv'
    with open(cf_all, 'w') as f:
        f.write('id,sequence\n')
        for fu in fusions:
            f.write(f"{fu['id']},{fu['sequence']}\n")

    # Split for two clusters
    mid = len(fusions) // 2
    for label, subset, fname in [
        ('A (Frontenac)', fusions[:mid], 'fusion_input_A.csv'),
        ('B (Narval)', fusions[mid:], 'fusion_input_B.csv'),
    ]:
        path = outdir / fname
        with open(path, 'w') as f:
            f.write('id,sequence\n')
            for fu in subset:
                f.write(f"{fu['id']},{fu['sequence']}\n")

    print(f"\nGenerated {len(fusions)} fusion candidates")
    print(f"Length range: {min(f['total_len'] for f in fusions)}–{max(f['total_len'] for f in fusions)} aa")
    print(f"\nFiles written:")
    print(f"  Manifest: {manifest_path}")
    print(f"  ColabFold input (all): {cf_all}")
    print(f"  ColabFold input A (Frontenac, {mid}): {outdir / 'fusion_input_A.csv'}")
    print(f"  ColabFold input B (Narval, {len(fusions)-mid}): {outdir / 'fusion_input_B.csv'}")


if __name__ == "__main__":
    main()
