# BindCraft Multi-Agent Coordination Protocol

**Last updated:** 2026-05-20
**Owner:** Agent F (Frontenac) — Central Coordinator

---

## Campaign

De novo binder design targeting **Abeta-42** (PDB 9CO4, chains C/E/G) using BindCraft. Each cluster runs independent BindCraft trajectories; accepted designs are collected on Frontenac for final analysis.

## Agent Registry

| Agent | Cluster | Working Dir | GPU | Status |
|-------|---------|-------------|-----|--------|
| **F** (Frontenac) | CAC Queen's | `/global/project/hpcg6049/protein/alzheimer/bindcraft/` | A100 | ACTIVE — job 8415123 running (resumed), 50 accepted designs from 924 trajectories |
| **Nibi** | Alliance Canada (Waterloo) | `/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/` | H100 | NEW — setup pending |

## Design Parameters (identical across all agents)

- **Target PDB:** `9CO4_CEG.pdb` (chains C, E, G)
- **Hotspots:** C10,C11,C13,C14,C15,C16,E10,E11,E13,E14,E15,E16,G10,G11,G13,G14,G15,G16
- **Binder lengths:** 60–90 residues
- **Binder name prefix:** `ab42`
- **Design algorithm:** 4stage
- **MPNN:** soluble weights, 20 seqs, fix interface, temp 0.1
- **Filters:** default_filters.json (from repo)
- **Advanced settings:** advanced_ab42.json (identical copy on each agent)
- **Omit AAs:** C (cysteine)

These parameters MUST NOT be modified by any agent.

## SLURM Conventions

| | Frontenac | Nibi |
|---|---|---|
| Account | `def-hpcg6049_gpu` | `def-ghaedi` |
| GPU type | A100 | H100 |
| GPU request | `--gres=gpu:a100:1` | `--gres=gpu:h100:1` |
| Max walltime | 14 days | 7 days |
| Main job time | `13-23:00:00` | `6-23:00:00` |
| Main job memory | `64G` | `64G` |
| Parallel job time | `05:59:00` | `05:59:00` |
| Parallel job memory | `48G` | `48G` |
| Partition | (do not specify) | (do not specify) |

### Memory note

The original 42G allocation OOM-killed the Frontenac main job after 11 days (JAX/Python memory fragmentation over long runs). All scripts now use 64G for main jobs and 48G for parallel jobs.

## Communication

Agents communicate via sync directories and Globus transfers. Each agent writes status to their own `sync/to_frontenac/` directory.

### Nibi → Frontenac (Globus)
- Nibi writes to: `<nibi_workdir>/sync/to_frontenac/status_nibi.md`
- Transfer via Globus CLI:
  ```bash
  globus transfer \
    <nibi_endpoint_id>:/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft/sync/to_frontenac/ \
    <frontenac_endpoint_id>:/global/project/hpcg6049/protein/alzheimer/bindcraft/sync/from_nibi/ \
    --recursive --sync-level checksum
  ```
- Nibi is an Alliance institutional endpoint — direct transfer to Frontenac works (no two-hop needed if Frontenac has a managed endpoint; otherwise relay via Fir).

### Convergence data transfer (end of campaign)
Transfer accepted designs and stats from Nibi to Frontenac:
```bash
# Accepted PDBs
globus transfer <nibi>:<nibi_workdir>/designs/Accepted/ \
  <frontenac>:<frontenac_workdir>/sync/from_nibi/designs_accepted/ \
  --recursive --sync-level checksum

# Stats CSV
globus transfer <nibi>:<nibi_workdir>/designs/final_design_stats.csv \
  <frontenac>:<frontenac_workdir>/sync/from_nibi/final_design_stats_nibi.csv

# Parallel job accepted PDBs (if any)
for i in 1 2 3 4; do
  globus transfer <nibi>:<nibi_workdir>/designs_p${i}/Accepted/ \
    <frontenac>:<frontenac_workdir>/sync/from_nibi/designs_p${i}_accepted/ \
    --recursive --sync-level checksum
done
```

### Merging results on Frontenac

After Globus transfer completes:

1. **PDBs:** Copy Nibi's accepted PDBs into a separate directory (do NOT mix into Frontenac's `designs/Accepted/`):
   ```
   sync/from_nibi/designs_accepted/ → combined_analysis/nibi_accepted/
   ```

2. **Stats CSV:** Concatenate (skip Nibi's header row):
   ```bash
   head -1 designs/final_design_stats.csv > combined_analysis/combined_stats.csv
   tail -n +2 designs/final_design_stats.csv >> combined_analysis/combined_stats.csv
   tail -n +2 sync/from_nibi/final_design_stats_nibi.csv >> combined_analysis/combined_stats.csv
   ```

3. **Name collisions:** Seeds are random, so collisions are astronomically unlikely. Verify with:
   ```bash
   cut -d, -f2 combined_analysis/combined_stats.csv | sort | uniq -d
   ```

## Design Naming

All designs use the `ab42` prefix. BindCraft appends length, seed, MPNN sequence number, and model number automatically. Since seeds are random, there is zero risk of name collision between agents.

## Convergence

When the campaign ends (jobs complete or wall time expires), all accepted PDBs and `final_design_stats.csv` from each agent are collected on Frontenac for combined ranking and analysis.

## Rules for All Agents

1. Use ONLY the provided settings, filters, and advanced config — no modifications
2. Report status after: install complete, job submission, job failure, periodically during runs
3. Do NOT delete accepted designs
4. Log all SLURM job IDs
5. Ask Frontenac (via sync or conversation) before changing anything
