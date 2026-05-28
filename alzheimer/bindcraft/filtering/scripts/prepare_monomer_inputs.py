#!/usr/bin/env python3
"""
Prepare ColabFold monomer input CSV for Stage 4 Phase B.

Extracts binder sequences from all 62 designs (not just Phase A survivors)
so we get monomer pLDDT for the full set. The final Stage 4 filter
combines Phase A + Phase B results.

Output: alzheimer/bindcraft/filtering/inputs/monomer_input.csv
Format: id,sequence (ColabFold batch format)
"""

import csv
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STATS_CSV = os.path.join(REPO_ROOT, "bindcraft", "designs", "final_design_stats.csv")
OUTPUT_DIR = os.path.join(REPO_ROOT, "bindcraft", "filtering", "inputs")
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "monomer_input.csv")


def main():
    with open(STATS_CSV) as f:
        rows = list(csv.DictReader(f))

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'sequence'])
        for row in rows:
            writer.writerow([row['Design'], row['Sequence']])

    print(f"Wrote {len(rows)} monomer sequences to {OUTPUT_CSV}")
    print(f"Lengths: {min(int(r['Length']) for r in rows)}–{max(int(r['Length']) for r in rows)} residues")
    print(f"\nNext: submit run_monomer_plddt.sh")


if __name__ == '__main__':
    main()
