# Nibi GPU-hours report

**From:** Nibi (Worker)
**To:** Frontenac (Coordinator)
**Date:** 2026-06-09
**Re:** GPU-hours pull for NVIDIA Inception pitch deck

## Numbers

| Metric | Value |
|---|---|
| **GPU-hours** | **1103.0** |
| **GPU jobs** | **30** |
| **GPU type** | H100 80GB (all 30 jobs) |

## Verification notes

- Ran your one-liner verbatim. The strict regex `gres/gpu=[0-9]+` is correct on Nibi — every GPU job's `AllocTRES` carries a plain `gres/gpu=1` key alongside `gres/gpu:h100=1`, e.g.:
  `billing=12200,cpu=4,gres/gpu:h100=1,gres/gpu=1,mem=42G,node=1`
- Cross-checked: 30 jobs mention GPU in `AllocTRES`, and all 30 match the strict regex — **no undercounting**.
- All 30 jobs are H100 (1 GPU each). No A100 usage on Nibi.

## Caveat (for an honest deck figure)

The 1103.0 GPU-hours is **total GPU wall-time consumed**, which includes failed runs. State breakdown of the 30 jobs:
- COMPLETED: 9
- FAILED: 16
- OUT_OF_MEMORY: 5

All burned real allocation, so 1103.0 is the defensible "GPU-hours consumed" number. If the deck wants *productive* hours only, that subset would be lower — flag which framing you want and I can recompute.

The 30 jobs are the long multi-hour H100 batch runs that produced the 2,051 TfR1 trajectories (each sbatch job ran many trajectories).

## 3-cluster running total

- Frontenac: 1,891 GPU-hours / 921 jobs (your verified figure)
- Nibi: 1,103.0 GPU-hours / 30 jobs (this report) — all H100
- Narval: (pending)
