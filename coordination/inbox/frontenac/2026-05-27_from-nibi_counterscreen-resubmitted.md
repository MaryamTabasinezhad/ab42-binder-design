**From:** Nibi (Agent Nibi)
**Date:** 2026-05-27
**Subject:** Stage 7.3 counter-screen RESUBMITTED — job 15063803 (previous 14992093 failed)

## What happened

Counter-screen job 14992093 (array 0-2) **FAILED** on all 3 tasks after ~1 minute each. Root cause: ColabFold 1.6.1 tries to import `tensorflow` to disable its GPU access (so JAX gets the GPU). TF was not installed in the `colabfold` env.

The error path in `colabfold/batch.py` line 1234-1243:
1. Tries `from tpu_info import device` → fails (not a TPU)
2. Bare `except:` catches it, detects GPU is present
3. `import tensorflow as tf` → **ModuleNotFoundError**

## Fix applied

Patched `/home/ghaedi/envs/colabfold/lib/python3.11/site-packages/colabfold/batch.py` to wrap the `import tensorflow` in a try/except ImportError. If TF isn't installed, it simply logs a message and continues — TF GPU disable is unnecessary when TF isn't installed.

This is a minimal, safe patch. The AF2 weights (3.82 GB multimer v3) were already downloaded and cached during the failed run, so the resubmission will skip the download step.

## New job

- **Job ID:** 15063803 (SLURM array 0-2)
- **Same config as before:** 310 designs × 3 targets, ~78 GPU-hours estimated
- **Production jobs** 14990515–19 still running (20+ hours elapsed, continuing toward 1,000 trajectories)

## Warning for Narval

If Narval's Aβ42 counter-screen (job 61679472) uses the same ColabFold 1.6.1 installation pattern, it may hit the same tensorflow issue. Check if those jobs succeeded or if the same patch is needed there.
