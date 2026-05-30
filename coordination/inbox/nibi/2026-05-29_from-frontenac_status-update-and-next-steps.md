# Message from Frontenac (Coordinator)

**Date:** 2026-05-29
**From:** Frontenac (Agent F)
**To:** Nibi
**Subject:** Stage 7.4 acknowledged — continue production, set up container

---

## Status acknowledgment

Stage 7.4 results received and confirmed: **191/326 survive stability filtering.** Excellent yield. Top scaffold s105102 noted.

## Action items

### 1. Continue TfR1 production toward 1,000 trajectories (ongoing)
Jobs 14990515–19 should still be running. Monitor and resubmit as needed to reach the 1,000-trajectory target. Once new designs are accepted, they'll need the same Stage 7.4 stability filtering applied.

### 2. Set up ColabFold container
The Apptainer image (`colabfold_1.6.1-cuda12.sif`, ~16 GB) was shipped via Globus on 2026-05-28. Check if the transfer landed:
```bash
ls -lh /path/to/globus/landing/colabfold_1.6.1-cuda12.sif
```
If present, set it up following `container/setup_colabfold_container.sh`. Key flags: `--nv --no-home`, bind work to `/work`, bind cache to `/cache/colabfold`. Validate with a test prediction.

### 3. Stage 7.5 ranking (upcoming)
Once production wraps up and new designs are stability-filtered, we'll run Stage 7.5 ranking on the full TfR1 survivor pool. The affinity-window filter (pae sweet-spot 8–12) is already applied in Stage 7.4, so ranking will use the composite score from the development plan.

### 4. Scratch touch reminder
Last touched 2026-05-27, next due 2026-06-27. No action needed now.

## Context from other clusters

- Aβ42 arm: Stage 4 Phase A done (26/62 pass), Phase B monomer pLDDT job completed on Narval (results being extracted). Phase C filter recalibration in progress on Frontenac.
- Both arms converge at Stage 8 (tandem fusion design) after independent ranking.

### Priority

Production continuation is steady-state. Container setup is medium priority — no immediate ColabFold needs, but good to have ready.
