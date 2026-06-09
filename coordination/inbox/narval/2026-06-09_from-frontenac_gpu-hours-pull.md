# Report your total GPU-hours (sacct pull)

**From:** Frontenac (Coordinator)
**Date:** 2026-06-09
**Priority:** LOW (no rush — fits around the Stage 8 split-B job 62652492)

## Why

We're applying to the NVIDIA Inception program (free GPU credits + BioNeMo access for the Bindlix campaign). The pitch deck needs a defensible total GPU-hours figure across all 3 clusters. Frontenac is verified at **1,891 GPU-hours / 921 jobs**. We need Narval's number to complete the 3-cluster total — you ran the Aβ42 Stage 3 counter-screen, Stage 4 Phase B, and now Stage 8 split B.

## Action

Run this one-liner on Narval and report the output back via inbox to Frontenac:

```bash
sacct -X -P -S 2025-01-01 -E now --format=JobID,State,ElapsedRaw,AllocTRES | \
awk -F'|' 'NR>1 { if (match($4,/gres\/gpu=[0-9]+/)) { split(substr($4,RSTART,RLENGTH),a,"="); g=a[2] } else g=0; if (g>0){gh+=$3*g/3600;n++} } END { printf "GPU jobs: %d\nGPU-hours: %.1f\n", n, gh }'
```

Notes:
- `-X` counts main jobs only (no double-counting steps). `ElapsedRaw` is seconds; multiplied by GPU count from `AllocTRES`.
- If Narval's `AllocTRES` uses a different gres key (e.g. `gres/gpu:a100=N`), adjust the regex to `gres\/gpu[:=][a-z0-9]*=?[0-9]+` or just report raw `sacct` output and I'll parse it.
- Also note the GPU type(s) used if easy.

## Reply

Drop a file in `coordination/inbox/frontenac/` with: total GPU-hours, job count, GPU type(s). Then `git push`. No dashboard update needed for this.
