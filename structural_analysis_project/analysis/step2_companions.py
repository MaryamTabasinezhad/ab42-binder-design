"""Step 2: Find sibling depositions by Butan & Strittmatter."""
import json
import re
import subprocess
import sys
import traceback
import urllib.request
from pathlib import Path

PROJECT = Path.home() / "structural_analysis_project"
STRUCT_DIR = PROJECT / "structures"
HEADER_URL = "https://files.rcsb.org/header/{}.cif"
PDB_URL = "https://files.rcsb.org/download/{}.pdb"
SEARCH_API = "https://search.rcsb.org/rcsbsearch/v2/query"


def fetch(url, timeout=30):
    """Return (status_code, body_text) — does not raise on 404."""
    req = urllib.request.Request(url, headers={"User-Agent": "structural-analysis/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error fetching {url}: {e}") from e


def parse_cif_header(text):
    """Crude mmCIF header parser — extracts a few specific items we need."""
    out = {
        "title": None,
        "authors": [],
        "release_date": None,
        "deposit_date": None,
        "resolution": None,
        "chains": [],
        "organism": None,
    }
    # _struct.title — may be quoted/multi-line
    m = re.search(r"_struct\.title\s+(['\"])(.+?)\1", text, re.DOTALL)
    if m:
        out["title"] = re.sub(r"\s+", " ", m.group(2)).strip()
    else:
        m = re.search(r"_struct\.title\s+;([^;]*?);", text, re.DOTALL)
        if m:
            out["title"] = re.sub(r"\s+", " ", m.group(1)).strip()

    # audit_author loop
    m = re.search(r"loop_\s*\n((?:_audit_author\.[^\n]*\n)+)((?:.*?\n)+?)#",
                  text, re.DOTALL)
    if m:
        cols = [c.strip() for c in m.group(1).strip().splitlines()]
        name_idx = next((i for i, c in enumerate(cols)
                         if c == "_audit_author.name"), None)
        if name_idx is not None:
            for line in m.group(2).strip().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("loop_"):
                    continue
                # tokens may be quoted strings with commas
                toks = re.findall(r"'([^']*)'|\"([^\"]*)\"|(\S+)", line)
                toks = [a or b or c for a, b, c in toks]
                if name_idx < len(toks):
                    out["authors"].append(toks[name_idx])

    # release / deposit dates
    m = re.search(r"_pdbx_audit_revision_history\.revision_date\s+([0-9-]+)", text)
    if m:
        out["release_date"] = m.group(1)
    m = re.search(r"_pdbx_database_status\.recvd_initial_deposition_date\s+([0-9-]+)", text)
    if m:
        out["deposit_date"] = m.group(1)

    # resolution (em or x-ray)
    for key in (r"_em_3d_reconstruction\.resolution",
                r"_reflns\.d_resolution_high",
                r"_refine\.ls_d_res_high"):
        m = re.search(key + r"\s+([0-9.]+)", text)
        if m:
            out["resolution"] = float(m.group(1))
            break

    # chains via entity_poly.pdbx_strand_id
    chains = set()
    for m in re.finditer(r"_entity_poly\.pdbx_strand_id\s+([^\n]+)", text):
        v = m.group(1).strip().strip("'\"")
        for c in v.split(","):
            chains.add(c.strip())
    if not chains:
        # loop form
        loop_match = re.search(
            r"loop_\s*\n((?:_entity_poly\.[^\n]*\n)+)((?:.*?\n)+?)#",
            text, re.DOTALL)
        if loop_match:
            cols = [c.strip() for c in loop_match.group(1).strip().splitlines()]
            sidx = next((i for i, c in enumerate(cols)
                         if c == "_entity_poly.pdbx_strand_id"), None)
            if sidx is not None:
                for line in loop_match.group(2).strip().splitlines():
                    toks = re.findall(r"'([^']*)'|\"([^\"]*)\"|(\S+)", line)
                    toks = [a or b or c for a, b, c in toks]
                    if sidx < len(toks):
                        for c in toks[sidx].split(","):
                            chains.add(c.strip())
    out["chains"] = sorted(chains)

    # source organism
    m = re.search(r"_entity_src_(?:gen|nat)\.pdbx_(?:gene_src_)?scientific_name\s+(['\"])(.+?)\1",
                  text)
    if m:
        out["organism"] = m.group(2).strip()
    else:
        m = re.search(r"_entity_src_(?:gen|nat)\.pdbx_(?:gene_src_)?scientific_name\s+(\S+)",
                      text)
        if m:
            out["organism"] = m.group(1).strip("'\"")
    return out


def has_both_authors(authors):
    a_str = " ".join(authors).lower()
    return "butan" in a_str and "strittmatter" in a_str


def scan_range():
    print("[step2] scanning 9CO0..9COZ headers")
    hits = []
    suffixes = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for s in suffixes:
        pdb_id = f"9CO{s}"
        if pdb_id == "9CO4":
            continue
        url = HEADER_URL.format(pdb_id)
        status, body = fetch(url)
        if status != 200 or not body.strip():
            continue
        info = parse_cif_header(body)
        info["pdb_id"] = pdb_id
        line = (f"  {pdb_id}  res={info['resolution']}  "
                f"chains={len(info['chains'])}  "
                f"released={info['release_date']}  "
                f"authors={','.join(info['authors'][:3])}"
                f"{'...' if len(info['authors']) > 3 else ''}  "
                f"title={info['title']}")
        print(line)
        hits.append(info)
    return hits


def search_api():
    print("\n[step2] querying RCSB search API for Butan AND Strittmatter")
    query = {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "audit_author.name",
                        "operator": "contains_phrase",
                        "value": "Butan",
                    },
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "audit_author.name",
                        "operator": "contains_phrase",
                        "value": "Strittmatter",
                    },
                },
            ],
        },
        "return_type": "entry",
        "request_options": {"paginate": {"start": 0, "rows": 100}},
    }
    data = json.dumps(query).encode("utf-8")
    req = urllib.request.Request(
        SEARCH_API, data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    parsed = json.loads(body)
    ids = [r["identifier"] for r in parsed.get("result_set", [])]
    print(f"  search API returned {len(ids)} entries: {ids}")
    return ids


def download_pdb(pdb_id):
    out_path = STRUCT_DIR / f"{pdb_id}.pdb"
    print(f"  downloading {pdb_id} -> {out_path.name}")
    subprocess.run(
        ["curl", "-fsSL", "--max-time", "60",
         "-o", str(out_path), PDB_URL.format(pdb_id)],
        check=True,
    )
    if out_path.stat().st_size < 1000:
        raise RuntimeError(f"{pdb_id}.pdb suspiciously small")
    head = out_path.read_text(errors="replace").splitlines()[0]
    if "<html" in head.lower() or not head.startswith("HEADER"):
        raise RuntimeError(f"{pdb_id}.pdb does not look like a PDB file")


def main():
    range_hits = scan_range()
    api_ids = search_api()

    candidates = {}
    for h in range_hits:
        if has_both_authors(h["authors"]):
            candidates[h["pdb_id"]] = h
    for pid in api_ids:
        if pid not in candidates and pid != "9CO4":
            # Fetch header to confirm and get metadata
            status, body = fetch(HEADER_URL.format(pid))
            if status == 200 and body.strip():
                info = parse_cif_header(body)
                info["pdb_id"] = pid
                if has_both_authors(info["authors"]):
                    candidates[pid] = info

    # Drop 9CO4 itself if it appeared
    candidates.pop("9CO4", None)

    print(f"\n[step2] {len(candidates)} companion entries identified:")
    for pid, info in sorted(candidates.items()):
        print(f"  {pid}: res={info['resolution']} Å, "
              f"chains={len(info['chains'])}, "
              f"released={info['release_date']}, "
              f"organism={info['organism']}")
        print(f"       title: {info['title']}")

    # Download companion PDBs
    print("\n[step2] downloading companion PDB files")
    for pid in sorted(candidates):
        download_pdb(pid)

    # Save manifest
    manifest = {pid: {k: v for k, v in info.items() if k != "raw"}
                for pid, info in candidates.items()}
    (PROJECT / "analysis" / "companions.json").write_text(
        json.dumps(manifest, indent=2))
    print(f"[step2] manifest written to analysis/companions.json")
    return manifest


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
